from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

import mujoco
import numpy as np

from server.robot_registry import resolve_variant
from server.retarget.foot_support import (
    load_foot_support_definition,
    support_point_world_positions,
)
from server.retarget.robot_runtime_definition import (
    RobotRuntimeDefinitionError,
    load_robot_runtime_definition,
)


ROOT = Path(__file__).resolve().parents[2]


class RobotRuntimeDefinitionTests(unittest.TestCase):
    def runtime(self, variant_id: str):
        record = resolve_variant(variant_id, root=ROOT)
        return load_robot_runtime_definition(ROOT, record.runtime_robot(ROOT))

    def test_g1_and_k1_compile_to_valid_common_definition(self) -> None:
        for variant_id, expected_dof, expected_pelvis_body in (
            ("g1_29dof", 29, "pelvis"),
            ("k1_22dof", 22, "Trunk"),
        ):
            runtime = self.runtime(variant_id)
            self.assertEqual(len(runtime.output_joint_names), expected_dof)
            self.assertIn(runtime.root_body, runtime.body_names)
            self.assertEqual(runtime.initial_qpos.shape, (runtime.model.nq,))
            self.assertEqual(runtime.pelvis_reference.body_name, expected_pelvis_body)
            self.assertEqual(
                runtime.pelvis_reference.local_position, (0.0, 0.0, 0.0)
            )

            data = mujoco.MjData(runtime.model)
            data.qpos[:] = runtime.initial_qpos
            mujoco.mj_forward(runtime.model, data)
            body_id = mujoco.mj_name2id(
                runtime.model,
                mujoco.mjtObj.mjOBJ_BODY,
                expected_pelvis_body,
            )
            np.testing.assert_allclose(
                runtime.pelvis_reference.world_position(runtime.model, data),
                data.xpos[body_id],
            )

    def test_k1_primary_axes_are_resolved_in_link_local_coordinates(self) -> None:
        runtime = self.runtime("k1_22dof")
        expected = {
            "Left_Arm_3": [0.0, 1.0, 0.0],
            "Right_Arm_3": [0.0, -1.0, 0.0],
            "left_hand_link": [0.0, 1.0, 0.0],
            "right_hand_link": [0.0, -1.0, 0.0],
            "Left_Hip_Yaw": [-0.014, 0.0, -0.117],
            "Right_Hip_Yaw": [-0.014, 0.0, -0.117],
            "left_foot_link": [1.0, 0.0, 0.0],
            "right_foot_link": [1.0, 0.0, 0.0],
        }
        for body_name, axis in expected.items():
            orientation = runtime.orientation(body_name)
            self.assertTrue(orientation.axis_alignment_supported, body_name)
            np.testing.assert_allclose(
                orientation.primary_axis,
                np.asarray(axis) / np.linalg.norm(axis),
                atol=1e-6,
            )
        for body_name in ("Left_Shank", "Right_Shank"):
            orientation = runtime.orientation(body_name)
            self.assertTrue(orientation.axis_alignment_supported)
            self.assertGreater(
                float(np.dot(orientation.primary_axis, [0.0, 0.0, -1.0])),
                0.99999,
            )
        self.assertIsNone(runtime.orientation("left_hand_link").secondary_axis)
        np.testing.assert_allclose(
            runtime.orientation("left_foot_link").secondary_axis,
            [0.0, 0.0, -1.0],
        )

    def test_k1_support_points_resolve_against_compiled_model(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        runtime_robot = record.runtime_robot(ROOT)
        runtime = load_robot_runtime_definition(ROOT, runtime_robot)
        definition = load_foot_support_definition(
            runtime.model, {"robot": runtime_robot}
        )
        self.assertIsNotNone(definition)
        data = mujoco.MjData(runtime.model)
        data.qpos[:] = runtime.initial_qpos
        mujoco.mj_forward(runtime.model, data)
        for side in ("left", "right"):
            points = support_point_world_positions(data, definition.sides[side])
            self.assertEqual(points.shape, (4, 3))
            self.assertTrue(np.all(np.isfinite(points)))

    def test_axis_mapping_without_primary_axis_is_rejected(self) -> None:
        runtime = self.runtime("g1_29dof")
        config = {
            "mappings": [{
                "source_segment": "LeftForearm",
                "target_link": "left_wrist_roll_link",
                "orientation_mode": "axis",
            }]
        }
        with self.assertRaisesRegex(
            RobotRuntimeDefinitionError, "requires a Primary axis"
        ):
            runtime.validate_config(config)

    def test_manifest_body_reference_is_checked_after_mujoco_compile(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        robot = record.runtime_robot(ROOT)
        robot = deepcopy(robot)
        robot["retargeting"]["target_geometry"]["Left_Arm_3"] = {
            "type": "body_to_body",
            "distal_body": "missing_body",
        }
        with self.assertRaisesRegex(
            RobotRuntimeDefinitionError, "Invalid distal body"
        ):
            load_robot_runtime_definition(ROOT, robot)

    def test_missing_pelvis_reference_body_is_rejected(self) -> None:
        record = resolve_variant("k1_22dof", root=ROOT)
        robot = deepcopy(record.runtime_robot(ROOT))
        robot["retargeting"]["landmarks"]["pelvis_reference"]["body"] = (
            "missing_body"
        )
        with self.assertRaisesRegex(
            RobotRuntimeDefinitionError, "Pelvis reference body not found"
        ):
            load_robot_runtime_definition(ROOT, robot)


if __name__ == "__main__":
    unittest.main()
