from __future__ import annotations

import json
import pickle
import tempfile
import unittest
from pathlib import Path

import numpy as np

from server.api.retarget_artifact_api import (
    _main_artifact_frame_counts,
    _publish_main_failure_artifacts,
    _publish_main_artifact_set,
    _publish_primary_failure_artifacts,
)
from server.retarget.viewer_data import write_viewer_bin


class MainArtifactPublishTests(unittest.TestCase):
    MAIN_ID = "2608250002-01"

    def write_set(self, path: Path, frames: int, generation: str) -> None:
        path.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path / f"{self.MAIN_ID}_main_target.npz",
            frame=np.arange(frames, dtype=np.int32),
        )
        np.savez_compressed(
            path / f"{self.MAIN_ID}_main.npz",
            frame=np.arange(frames, dtype=np.int32),
        )
        (path / f"{self.MAIN_ID}_main_config.json").write_text(
            json.dumps({
                "main_id": self.MAIN_ID,
                "artifact_generation_id": generation,
                "main_runtime_context": {"frame_count": frames},
            }),
            encoding="utf-8",
        )
        with (path / f"{self.MAIN_ID}_main.pkl").open("wb") as stream:
            pickle.dump({"root_pos": np.zeros((frames, 3))}, stream)
        write_viewer_bin(
            path / f"{self.MAIN_ID}_main_viewer.bin",
            {
                "stage": "main",
                "frames": frames,
                "frame_count": frames,
                "artifact_generation_id": generation,
            },
            {"frame": np.arange(frames, dtype=np.int32)},
        )

    def test_retry_replaces_501_frame_set_with_one_500_frame_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / self.MAIN_ID
            staging = root / ".retry.staging"
            self.write_set(destination, 501, "old-generation")
            self.write_set(staging, 500, "new-generation")

            published_path, files = _publish_main_artifact_set(
                staging,
                destination,
                self.MAIN_ID,
                expected_frames=500,
                generation_id="new-generation",
            )

            self.assertEqual(published_path, destination)
            self.assertEqual(len(files), 5)
            self.assertEqual(
                _main_artifact_frame_counts(destination, self.MAIN_ID),
                {
                    "target": 500,
                    "motion": 500,
                    "config": 500,
                    "viewer": 500,
                    "pkl": 500,
                },
            )
            config = json.loads(
                (destination / f"{self.MAIN_ID}_main_config.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(config["artifact_generation_id"], "new-generation")

    def test_failure_replaces_old_set_with_config_viewer_and_error_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / self.MAIN_ID
            staging = root / ".failed.staging"
            self.write_set(destination, 501, "old-generation")
            staging.mkdir()
            stale_runtime = staging / ".remote-result"
            stale_runtime.mkdir()
            (stale_runtime / "partial.bin").write_bytes(b"partial")
            (staging / f"{self.MAIN_ID}_main_config.json").write_text(
                json.dumps({"main_id": self.MAIN_ID, "run_status": "partial"}),
                encoding="utf-8",
            )
            write_viewer_bin(
                staging / f"{self.MAIN_ID}_main_viewer.bin",
                {"stage": "main", "run_status": "partial", "frame_count": 500},
                {"frame": np.arange(500, dtype=np.int32)},
            )

            _, files = _publish_main_failure_artifacts(
                staging, destination, self.MAIN_ID, ["solver failed"],
            )

            self.assertEqual(files, [
                f"{self.MAIN_ID}_main_config.json",
                f"{self.MAIN_ID}_main_viewer.bin",
                f"{self.MAIN_ID}_error.log",
            ])
            self.assertEqual(
                sorted(path.name for path in destination.iterdir()), sorted(files)
            )
            self.assertIn(
                "solver failed",
                (destination / f"{self.MAIN_ID}_error.log").read_text(encoding="utf-8"),
            )

    def test_primary_failure_keeps_no_motion_export(self) -> None:
        run_id = "2608260001"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run = root / run_id
            run.mkdir()
            np.savez_compressed(run / f"{run_id}_primary.npz", frame=np.arange(3))
            request = root / f".{run_id}_request_config.json"
            request.write_text(
                json.dumps({"capsule_id": "2606050003", "config_name": "Primary Standard"}),
                encoding="utf-8",
            )

            _, files = _publish_primary_failure_artifacts(
                root, run_id, request, ["primary solver failed"],
            )

            self.assertEqual(files, [
                f"{run_id}_primary_config.json", f"{run_id}_error.log",
            ])
            self.assertFalse((run / f"{run_id}_primary.npz").exists())
            self.assertEqual(
                json.loads((run / f"{run_id}_primary_config.json").read_text(encoding="utf-8"))["run_status"],
                "failed",
            )


if __name__ == "__main__":
    unittest.main()
