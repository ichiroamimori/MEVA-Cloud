from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RETARGET = ROOT / "server" / "retarget"
if str(RETARGET) not in sys.path:
    sys.path.insert(0, str(RETARGET))

from analytic_joint_target import (
    _rotation,
    _three_axis_candidates,
    build_analytic_joint_target_profile,
    detect_analytic_joint_clusters,
)
from server.retarget.robot_runtime_definition import (
    load_robot_runtime_definition_for_config,
)


def k1_config() -> dict:
    return {
        "robot": {"manufacturer": "booster", "model": "k1", "variant": "k1_22dof"},
        "mappings": [
            {"source_segment": "Thoracic2", "target_link": "Trunk", "orientation_mode": "full"},
            {"source_segment": "LeftUpperArm", "target_link": "Left_Arm_3", "orientation_mode": "axis"},
            {"source_segment": "RightUpperArm", "target_link": "Right_Arm_3", "orientation_mode": "axis"},
            {"source_segment": "LeftUpperLeg", "target_link": "Left_Hip_Yaw", "orientation_mode": "axis"},
            {"source_segment": "RightUpperLeg", "target_link": "Right_Hip_Yaw", "orientation_mode": "axis"},
        ],
    }


class AnalyticJointTargetTests(unittest.TestCase):
    def test_g1_detects_generic_clusters_and_distal_axial_joint(self) -> None:
        path = (
            ROOT / "server" / "retarget_assets" / "configs" / "meva"
            / "unitree" / "g1_29dof" / "primary_standard.json"
        )
        config = json.loads(path.read_text(encoding="utf-8"))
        runtime = load_robot_runtime_definition_for_config(ROOT, config)
        clusters = detect_analytic_joint_clusters(runtime, config)
        by_id = {cluster.cluster_id: cluster for cluster in clusters}
        shoulder = by_id["torso_link->left_shoulder_yaw_link"]
        self.assertTrue(shoulder.supported)
        self.assertEqual(shoulder.axial_joint_index, 2)
        self.assertLess(shoulder.axial_alignment_deg, 30.0)
        self.assertEqual(len(clusters), 7)
        self.assertNotIn("floating_base_joint", {
            name for cluster in clusters for name in cluster.joint_names
        })
        wrist = by_id["left_elbow_link->left_wrist_yaw_link"]
        self.assertFalse(wrist.supported)
        self.assertEqual(
            wrist.detection_reason,
            "proximal_mapping_does_not_define_full_orientation",
        )

    def test_k1_canonical_singular_arm_is_structurally_supported(self) -> None:
        config = k1_config()
        runtime = load_robot_runtime_definition_for_config(
            ROOT, config, validate_config=False
        )
        clusters = detect_analytic_joint_clusters(runtime, config)
        by_id = {cluster.cluster_id: cluster for cluster in clusters}
        arm = by_id["Trunk->Left_Arm_3"]
        self.assertTrue(arm.supported)
        self.assertEqual(arm.axial_joint_index, 2)
        self.assertLess(arm.axial_sensitivity, 1e-7)
        self.assertGreater(arm.rank_ratio_max, 0.1)
        hip = by_id["Trunk->Left_Hip_Yaw"]
        self.assertTrue(hip.supported)
        self.assertEqual(hip.axial_joint_index, 2)

    def test_general_three_axis_inverse_uses_actual_axes(self) -> None:
        axes = np.asarray([
            [0.0, 0.961246, 0.275692],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ])
        expected = np.asarray([0.45, -0.35, 0.62])
        target = (
            _rotation(axes[0], expected[0])
            @ _rotation(axes[1], expected[1])
            @ _rotation(axes[2], expected[2])
        )
        candidates = _three_axis_candidates(
            target, axes, expected + np.asarray([0.01, -0.01, 0.01]),
            (False, False, False), ((0.0, 0.0),) * 3,
        )
        self.assertTrue(candidates)
        actual = min(candidates, key=lambda item: np.linalg.norm(item[0] - expected))[0]
        np.testing.assert_allclose(actual, expected, atol=1e-7)

    def test_axis_only_profile_uses_direction_and_excludes_distal_twist(self) -> None:
        config = {
            "robot": {
                "manufacturer": "unitree", "model": "g1",
                "variant": "g1_29dof",
            },
            "mappings": [
                {
                    "source_segment": "Thoracic2", "target_link": "torso_link",
                    "orientation_mode": "full",
                },
                {
                    "source_segment": "LeftUpperArm",
                    "target_link": "left_shoulder_yaw_link",
                    "orientation_mode": "axis",
                },
            ],
        }
        runtime = load_robot_runtime_definition_for_config(
            ROOT, config, validate_config=False
        )
        data = mujoco.MjData(runtime.model)
        data.qpos[:] = runtime.initial_qpos
        mujoco.mj_forward(runtime.model, data)
        torso_id = mujoco.mj_name2id(
            runtime.model, mujoco.mjtObj.mjOBJ_BODY, "torso_link"
        )
        shoulder_id = mujoco.mj_name2id(
            runtime.model, mujoco.mjtObj.mjOBJ_BODY, "left_shoulder_yaw_link"
        )
        torso_quat = np.asarray(data.xquat[torso_id], dtype=float)
        shoulder_quat = np.asarray(data.xquat[shoulder_id], dtype=float)
        primary_axis = np.asarray(
            runtime.orientation("left_shoulder_yaw_link").primary_axis,
            dtype=float,
        )
        target_direction = (
            np.asarray(data.xmat[shoulder_id], dtype=float).reshape(3, 3)
            @ primary_axis
        )
        common_directions = {
            "left_shoulder_yaw_link": np.repeat(target_direction[None, :], 2, axis=0)
        }
        profile_a = build_analytic_joint_target_profile(
            runtime,
            config,
            {
                "torso_link": np.repeat(torso_quat[None, :], 2, axis=0),
                "left_shoulder_yaw_link": np.repeat(shoulder_quat[None, :], 2, axis=0),
            },
            common_directions,
        )
        profile_b = build_analytic_joint_target_profile(
            runtime,
            config,
            {
                "torso_link": np.repeat(torso_quat[None, :], 2, axis=0),
                # Deliberately unrelated distal orientations: Axis-only generation
                # must consume only the already-resolved Primary Axis direction.
                "left_shoulder_yaw_link": np.asarray([
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                ]),
            },
            common_directions,
        )
        np.testing.assert_array_equal(profile_a.target_enabled, profile_b.target_enabled)
        np.testing.assert_allclose(
            profile_a.target_rad[profile_a.target_enabled],
            profile_b.target_rad[profile_b.target_enabled],
            atol=1e-12,
        )
        shoulder = profile_a.clusters[0]
        self.assertEqual(shoulder.axial_joint_index, 2)
        columns = {name: index for index, name in enumerate(profile_a.joint_names)}
        self.assertFalse(
            profile_a.target_enabled[:, columns[shoulder.joint_names[2]]].any()
        )


if __name__ == "__main__":
    unittest.main()
