from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.remote_ik_client import (  # noqa: E402
    RemoteIKClient,
    build_request_archive,
    extract_result_archive,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit a short Primary job to a Remote IK worker")
    parser.add_argument("config", type=Path)
    parser.add_argument("--url", required=True)
    parser.add_argument("--token", default="")
    parser.add_argument("--frames", type=int, default=1)
    args = parser.parse_args()
    if args.frames < 1:
        raise ValueError("--frames must be at least 1")

    config = json.loads(args.config.resolve().read_text(encoding="utf-8"))
    start = int(config.get("frame_range", {}).get("start", 0))
    config["frame_range"] = {"start": start, "stop": start + args.frames, "step": 1}
    config.setdefault("output", {})["run_id"] = "9900000002"
    config["output"]["overwrite_existing"] = False
    transfer_root = ROOT / "workspace" / ".ik_http_check"
    transfer_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=transfer_root) as name:
        directory = Path(name)
        config_path = directory / "config.json"
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        archive = directory / "request.zip"
        build_request_archive(
            destination=archive, repository_root=ROOT, stage="primary",
            client_job_id="http-check", config_path=config_path,
        )
        client = RemoteIKClient(args.url, args.token)
        status = client.submit(archive)
        job_id = status["job_id"]
        while status["status"] in {"queued", "running"}:
            time.sleep(0.2)
            status = client.status(job_id)
        if status["status"] != "completed":
            raise RuntimeError(f"Remote IK failed: {status.get('error')}")
        result_zip = directory / "result.zip"
        client.download_result(job_id, result_zip)
        result = directory / "result"
        files = extract_result_archive(result_zip, result)
        npz_path = result / "9900000002_primary.npz"
        pkl_path = result / "9900000002_primary.pkl"
        with np.load(npz_path, allow_pickle=False) as motion:
            frames = len(motion["root_pos"])
            dof_shape = tuple(motion["dof_pos"].shape)
        print(
            "Remote IK HTTP: OK; "
            f"job_id={job_id}, frames={frames}, dof_shape={dof_shape}, "
            f"files={len(files)}, legacy_pkl_present={pkl_path.is_file()}"
        )


if __name__ == "__main__":
    main()
