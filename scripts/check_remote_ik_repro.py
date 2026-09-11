from __future__ import annotations

import argparse
import json
import pickle
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.ik_contract import extract_request_archive, read_request_manifest
from server.ik_execution import run_python_ik
from server.remote_ik_client import build_request_archive


def _motion_arrays(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as values:
        return {
            key: np.asarray(values[key])
            for key in ("root_pos", "root_rot", "dof_pos")
        }


def _pickle_arrays(path: Path) -> dict[str, np.ndarray]:
    with path.open("rb") as stream:
        value = pickle.load(stream)  # trusted artifact generated in this temporary check
    return {key: np.asarray(value[key]) for key in ("root_pos", "root_rot", "dof_pos")}


def _assert_arrays_equal(
    local_arrays: dict[str, np.ndarray], remote_arrays: dict[str, np.ndarray], label: str,
) -> None:
    for key in local_arrays:
        if local_arrays[key].shape != remote_arrays[key].shape:
            raise AssertionError(
                f"{label} {key} shape differs: "
                f"{local_arrays[key].shape} != {remote_arrays[key].shape}"
            )
        np.testing.assert_allclose(local_arrays[key], remote_arrays[key], rtol=0.0, atol=0.0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare the existing Primary CLI with the Remote Python execution boundary."
    )
    parser.add_argument("config", type=Path, help="Existing Primary config snapshot")
    parser.add_argument("--main-config", type=Path, help="Also compare Main using this config snapshot")
    parser.add_argument("--frames", type=int, default=2, help="Source frames used for the quick check")
    args = parser.parse_args()
    if args.frames < 1:
        raise ValueError("--frames must be at least 1")

    original = json.loads(args.config.resolve().read_text(encoding="utf-8"))
    start = int(original.get("frame_range", {}).get("start", 0))
    original["frame_range"] = {"start": start, "stop": start + args.frames, "step": 1}
    original.setdefault("output", {})["run_id"] = "9900000001"
    original["output"]["overwrite_existing"] = False

    transfer_root = ROOT / "workspace" / ".ik_repro_check"
    transfer_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=transfer_root) as temporary_name:
        temporary = Path(temporary_name)
        local_root = temporary / "local"
        local_root.mkdir()
        local_config = local_root / "config.json"
        local_config.write_text(json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8")
        local_process = subprocess.run(
            [sys.executable, "-u", str(ROOT / "server/retarget/primary_retarget.py"), str(local_config)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if local_process.returncode != 0:
            raise RuntimeError(f"Local Primary failed:\n{local_process.stdout[-12000:]}")

        request_archive = temporary / "request.zip"
        build_request_archive(
            destination=request_archive,
            repository_root=ROOT,
            stage="primary",
            client_job_id="repro-check",
            config_path=local_config,
        )
        request = read_request_manifest(request_archive)
        package = temporary / "package"
        extract_request_archive(
            request_archive, package, request, max_uncompressed_bytes=4 * 1024**3,
        )
        remote = run_python_ik(
            request, package, temporary / "remote", ROOT,
        )

        filename = "9900000001_primary.npz"
        local_arrays = _motion_arrays(local_root / "9900000001" / filename)
        remote_arrays = _motion_arrays(remote.output_directory / filename)
        _assert_arrays_equal(local_arrays, remote_arrays, "Primary NPZ")
        frame_count = len(local_arrays["root_pos"])
        print(
            "Remote Python reproducibility: OK; "
            f"frames={frame_count}, root_pos/root_rot/dof_pos are exactly equal"
        )

        if args.main_config is not None:
            main_config = json.loads(args.main_config.resolve().read_text(encoding="utf-8"))
            main_id = "9900000001-01"
            main_config["primary_run_id"] = "9900000001"
            main_config["main_id"] = main_id
            main_config["artifact_generation_id"] = "repro-check"
            local_main_dir = local_root / "9900000001" / ".main-local"
            local_main_dir.mkdir()
            local_main_config = local_main_dir / f"{main_id}_main_config.json"
            local_main_config.write_text(
                json.dumps(main_config, ensure_ascii=False, indent=2), encoding="utf-8",
            )
            local_main_process = subprocess.run(
                [sys.executable, "-u", str(ROOT / "server/retarget/main_retarget.py"), str(local_main_config)],
                cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            if local_main_process.returncode != 0:
                raise RuntimeError(f"Local Main failed:\n{local_main_process.stdout[-12000:]}")

            main_archive = temporary / "main-request.zip"
            build_request_archive(
                destination=main_archive,
                repository_root=ROOT,
                stage="main",
                client_job_id="main-repro-check",
                config_path=local_main_config,
                primary_directory=remote.output_directory,
            )
            main_request = read_request_manifest(main_archive)
            main_package = temporary / "main-package"
            extract_request_archive(
                main_archive, main_package, main_request, max_uncompressed_bytes=4 * 1024**3,
            )
            remote_main = run_python_ik(
                main_request, main_package, temporary / "remote-main", ROOT,
            )
            main_npz = f"{main_id}_main.npz"
            _assert_arrays_equal(
                _motion_arrays(local_main_dir / main_npz),
                _motion_arrays(remote_main.output_directory / main_npz),
                "Main NPZ",
            )
            main_pkl = f"{main_id}_main.pkl"
            _assert_arrays_equal(
                _pickle_arrays(local_main_dir / main_pkl),
                _pickle_arrays(remote_main.output_directory / main_pkl),
                "Main PKL",
            )
            print("Remote Python Main reproducibility: OK; NPZ and PKL motion arrays are exactly equal")


if __name__ == "__main__":
    main()
