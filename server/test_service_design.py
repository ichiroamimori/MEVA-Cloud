from __future__ import annotations

import json
import csv
import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np
from pydantic import ValidationError

from server.capsule_identity import is_public_capsule, is_valid_capsule_id
from server.service_context import (
    DEVELOPMENT_USER,
    DEVELOPMENT_WORKSPACE,
    Plan,
    Role,
    User,
    Workspace,
    can_replace_standard,
    public_service_context,
)
from server.retarget.viewer_data import (
    FORMAT_VERSION,
    LEGACY_MAGIC,
    _serialize_bin,
    read_viewer_bin,
)
from server.retarget.meva_schema import (
    MEVA_GCP_COLUMN_INDICES,
    MEVA_POSITION_COLUMN_INDICES,
)
from server.retarget.primary_target import build_primary_target, load_primary_target


class ServiceDesignTests(unittest.TestCase):
    def test_development_identity_and_names_are_stable(self) -> None:
        self.assertEqual(DEVELOPMENT_USER.user_id, "Xenoma_Admin_01")
        self.assertEqual(DEVELOPMENT_USER.display_name, "Zenosuke Miyamoto")
        self.assertEqual(DEVELOPMENT_USER.role, "system_admin")
        self.assertIsNone(DEVELOPMENT_USER.email)
        self.assertIsNone(DEVELOPMENT_WORKSPACE.plan)
        context = public_service_context()
        self.assertEqual(context["user"]["role_label"], "System Admin")
        self.assertNotIn("plan_label", context["workspace"])
        self.assertEqual({item.value for item in Role}, {
            "admin", "user", "worker", "supervisor", "system_admin",
        })
        self.assertEqual({item.value for item in Plan}, {
            "free", "trial", "standard", "enterprise",
        })
        self.assertTrue(can_replace_standard(Role.SUPERVISOR))
        self.assertTrue(can_replace_standard(Role.SYSTEM_ADMIN))
        self.assertFalse(can_replace_standard(Role.ADMIN))
        self.assertFalse(can_replace_standard(Role.USER))
        self.assertFalse(can_replace_standard(Role.WORKER))

    def test_user_and_workspace_identifiers_are_validated(self) -> None:
        User(user_id="User_01-a", display_name="Same Name", role=Role.USER)
        Workspace(workspace_id="Workspace_01-a", display_name="日本語も可")
        with self.assertRaises(ValidationError):
            User(user_id="bad/user", display_name="Bad", role=Role.USER)
        with self.assertRaises(ValidationError):
            Workspace(workspace_id="bad workspace", display_name="Bad")

    def test_public_capsule_rule_is_centralized_and_strict(self) -> None:
        self.assertTrue(is_public_capsule("0000000001"))
        self.assertTrue(is_public_capsule("0000000123"))
        self.assertFalse(is_public_capsule("2609130042"))
        self.assertFalse(is_public_capsule("000000123"))
        self.assertFalse(is_public_capsule("000000ABCD"))
        self.assertTrue(is_valid_capsule_id("2609130042"))

    def test_current_bin_round_trip_preserves_capsule_and_auxiliary_bvh(self) -> None:
        payload = _serialize_bin(
            {
                "kind": "meva",
                "capsule_id": "2609130042",
                "gcp_names": ["left_ff"],
            },
            {
                "source_frame": np.array([0, 1], dtype=np.int32),
                "gcp": np.array([[0.1], [0.2]], dtype=np.float32),
                "bvh_bytes": np.frombuffer(b"HIERARCHY\r\n", dtype=np.uint8),
            },
        )
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "motion.bin"
            path.write_bytes(payload)
            header, arrays = read_viewer_bin(path)
        self.assertEqual(header["format_version"], FORMAT_VERSION)
        self.assertEqual(header["capsule_id"], "2609130042")
        self.assertEqual(bytes(arrays["bvh_bytes"]), b"HIERARCHY\r\n")

    def test_legacy_bin_remains_readable(self) -> None:
        header = {"format_version": 1, "kind": "meva", "blocks": []}
        encoded = json.dumps(header).encode("utf-8")
        payload = LEGACY_MAGIC + struct.pack("<I", len(encoded)) + encoded
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "legacy.bin"
            path.write_bytes(payload)
            loaded, arrays = read_viewer_bin(path)
        self.assertEqual(loaded["format_version"], 1)
        self.assertEqual(arrays, {})

    def test_primary_target_is_equal_for_csv_and_versioned_bin(self) -> None:
        segments = ["Pelvis", "LeftFoot", "RightFoot"]
        frame_count = 4
        positions = np.zeros((frame_count, len(segments), 3), dtype=np.float32)
        quaternions = np.zeros((frame_count, len(segments), 4), dtype=np.float32)
        quaternions[..., 0] = 1.0
        gcp = np.zeros((frame_count, len(MEVA_GCP_COLUMN_INDICES)), dtype=np.float32)
        for frame in range(frame_count):
            for segment_index in range(len(segments)):
                positions[frame, segment_index] = [frame * 0.01, segment_index, 0.1 + frame * 0.02]
            gcp[frame] = [0.1 * frame, 0.2 * frame, 0.3 * frame, 0.4 * frame]

        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            csv_path = root / "source.csv"
            width = max(MEVA_GCP_COLUMN_INDICES.values()) + 1
            header = [f"unused_{index}" for index in range(width)]
            quaternion_columns: dict[tuple[str, str], int] = {}
            next_column = 0
            for segment in segments:
                for component in "wxyz":
                    header[next_column] = f"{segment}_q_gs_{component}"
                    quaternion_columns[(segment, component)] = next_column
                    next_column += 1
            rows = []
            for frame in range(frame_count):
                row = ["0"] * width
                for segment_index, segment in enumerate(segments):
                    for component_index, component in enumerate("wxyz"):
                        row[quaternion_columns[(segment, component)]] = str(
                            quaternions[frame, segment_index, component_index]
                        )
                    for axis_index, column in enumerate(MEVA_POSITION_COLUMN_INDICES[segment]):
                        row[column] = str(positions[frame, segment_index, axis_index])
                for gcp_index, column in enumerate(MEVA_GCP_COLUMN_INDICES.values()):
                    row[column] = str(gcp[frame, gcp_index])
                rows.append(row)
            with csv_path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream)
                writer.writerow(header)
                writer.writerows(rows)

            bin_path = root / "source.bin"
            bin_path.write_bytes(_serialize_bin(
                {
                    "kind": "meva", "capsule_id": "2609130042", "fps": 100.0,
                    "segment_names": segments, "joint_names": ["dummy"],
                    "quaternion_order": "wxyz",
                    "gcp_names": list(MEVA_GCP_COLUMN_INDICES),
                },
                {
                    "source_frame": np.arange(frame_count, dtype=np.int32),
                    "segment_pos": positions, "segment_quat": quaternions,
                    "joint_pos": np.zeros((frame_count, 1, 3), dtype=np.float32),
                    "gcp": gcp,
                    "bvh_bytes": np.frombuffer(b"HIERARCHY\n", dtype=np.uint8),
                },
            ))
            base = {
                "capsule_id": "2609130042",
                "source": {
                    "sampling_rate_hz": 100.0, "header_row_1based": 1,
                    "quaternion_columns": "{segment}_q_gs_{component}",
                    "quaternion_order": "wxyz",
                },
                "sampling": {"rate_fps": 50.0},
                "frame_range": {"start": 0, "stop": frame_count, "step": 1},
                "mappings": [
                    {"source_segment": segment, "target_link": segment}
                    for segment in segments
                ],
                "robot": {"foot_contacts": {"robot_foot_to_ground_offset_m": 0.035}},
            }
            csv_config = json.loads(json.dumps(base))
            csv_config["source"]["file"] = csv_path.name
            bin_config = json.loads(json.dumps(base))
            bin_config["source"]["file"] = bin_path.name
            csv_output = load_primary_target(build_primary_target(
                cfg=csv_config, repo_root=root, output_path=root / "csv.npz",
            ))
            bin_output = load_primary_target(build_primary_target(
                cfg=bin_config, repo_root=root, output_path=root / "bin.npz",
            ))
        for key in csv_output:
            if key == "source_file":
                continue
            if np.issubdtype(csv_output[key].dtype, np.number):
                np.testing.assert_allclose(csv_output[key], bin_output[key])
            else:
                np.testing.assert_array_equal(csv_output[key], bin_output[key])

    def test_config_switch_preserves_primary_frame_range(self) -> None:
        html = (
            Path(__file__).resolve().parents[1] / "app" / "retarget" / "index.html"
        ).read_text(encoding="utf-8")
        self.assertIn("const preservedStart = startFrame?.value", html)
        self.assertIn("const preservedEnd = endFrame?.value", html)
        self.assertNotIn("if(startFrame) startFrame.value = 0;\n    if(endFrame) endFrame.value = sourceMaxFrame", html)


if __name__ == "__main__":
    unittest.main()
