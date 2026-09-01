from __future__ import annotations

import unittest
from pathlib import Path
import sys

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.retarget.check_offsets import (
    build_mapping_offset,
    build_terminal_semantic_offset,
    _mapping_signature,
)
from server.retarget.robot_runtime_definition import load_robot_runtime_definition
from server.robot_registry import resolve_variant, variant_retargeting_metadata


class OrientationOffsetTests(unittest.TestCase):
    def test_head_uses_shared_semantic_frame_for_k1(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        model = mujoco.MjModel.from_xml_path(str(record.model_path))
        metadata = variant_retargeting_metadata(record)
        quat, detail = build_mapping_offset(
            model,
            "Head",
            "Head_2",
            metadata.get("target_geometry") or {},
            metadata["terminal_semantics"],
            orientation_mode="full",
        )
        self.assertTrue(np.isfinite(quat).all())
        self.assertEqual(detail["source_geometry_mode"], "semantic_frame")
        self.assertEqual(detail["secondary_axis_semantics"], "face_forward")
        np.testing.assert_allclose(
            detail["source_primary_axis_local"], [0.0, 1.0, 0.0]
        )
        np.testing.assert_allclose(
            detail["robot_long_axis_link_local"], [0.0, 0.0, 1.0]
        )

    def test_g1_foot_outward_normal_preserves_legacy_physical_offset(self) -> None:
        legacy = {
            "left_ankle_roll_link": {
                "primary": [1.0, 0.0, 0.0],
                "secondary": [0.0, 0.0, 1.0],
                "secondary_name": "sole_up_normal",
            }
        }
        current = {
            "left_ankle_roll_link": {
                "primary": [1.0, 0.0, 0.0],
                "secondary": [0.0, 0.0, -1.0],
                "secondary_name": "sole_outward_normal",
            }
        }
        old_quat, _ = build_terminal_semantic_offset(
            "LeftFoot", "left_ankle_roll_link", legacy
        )
        new_quat, _ = build_terminal_semantic_offset(
            "LeftFoot", "left_ankle_roll_link", current
        )
        self.assertAlmostEqual(abs(float(np.dot(old_quat, new_quat))), 1.0, places=12)

    def test_k1_body_without_axis_definition_still_supports_full_mapping(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        model = mujoco.MjModel.from_xml_path(str(record.model_path))
        quat, detail = build_mapping_offset(
            model, "LeftUpperArm", "Left_Arm_1", {}, {}, orientation_mode="full"
        )
        self.assertTrue(np.isfinite(quat).all())
        self.assertEqual(detail["source_geometry_mode"], "body_local_frame")
        with self.assertRaisesRegex(KeyError, "No Primary axis"):
            build_mapping_offset(
                model, "LeftUpperArm", "Left_Arm_1", {}, {}, orientation_mode="axis"
            )

    def test_k1_foot_primary_axis_supports_axis_mode(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        model = mujoco.MjModel.from_xml_path(str(record.model_path))
        metadata = variant_retargeting_metadata(record)
        quat, detail = build_mapping_offset(
            model,
            "LeftFoot",
            "left_foot_link",
            metadata.get("target_geometry") or {},
            metadata["terminal_semantics"],
            orientation_mode="axis",
        )
        self.assertTrue(np.isfinite(quat).all())
        self.assertEqual(detail["source_geometry_mode"], "primary_axis:terminal_semantics")

    def test_k1_trunk_full_mapping_uses_explicit_primary_and_secondary(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        runtime = load_robot_runtime_definition(ROOT, record.runtime_robot(ROOT))
        metadata = variant_retargeting_metadata(record)
        quat, detail = build_mapping_offset(
            runtime.model,
            "Thoracic2",
            "Trunk",
            metadata.get("target_geometry") or {},
            metadata["terminal_semantics"],
            orientation_mode="full",
            robot_orientation=runtime.orientation("Trunk"),
        )
        self.assertTrue(np.isfinite(quat).all())
        self.assertEqual(
            detail["source_geometry_mode"], "semantic_frame:runtime_definition"
        )
        self.assertEqual(detail["secondary_axis_semantics"], "face_forward")
        np.testing.assert_allclose(
            detail["robot_long_axis_link_local"], [0.0, 0.0, 1.0]
        )
        np.testing.assert_allclose(
            detail["robot_secondary_axis_link_local"], [1.0, 0.0, 0.0]
        )

    def test_g1_torso_offset_is_unchanged_without_explicit_secondary(self) -> None:
        record = resolve_variant("g1_29dof", root=ROOT)
        runtime = load_robot_runtime_definition(ROOT, record.runtime_robot(ROOT))
        metadata = variant_retargeting_metadata(record)
        quat, detail = build_mapping_offset(
            runtime.model,
            "Thoracic2",
            "torso_link",
            metadata["target_geometry"],
            metadata["terminal_semantics"],
            orientation_mode="full",
            robot_orientation=runtime.orientation("torso_link"),
        )
        self.assertEqual(detail["source_geometry_mode"], "meva_canonical_direction")
        expected = np.asarray([
            0.689075862343592,
            -0.689079564753991,
            0.158656135836124,
            -0.158656988296875,
        ])
        self.assertAlmostEqual(abs(float(np.dot(quat, expected))), 1.0, places=12)

    def test_offset_fingerprint_mapping_signature_includes_mode(self) -> None:
        common = {"source_segment": "LeftUpperArm", "target_link": "Left_Arm_1"}
        full = _mapping_signature([{**common, "orientation_mode": "full"}])
        axis = _mapping_signature([{**common, "orientation_mode": "axis"}])
        self.assertNotEqual(full, axis)


if __name__ == "__main__":
    unittest.main()
