from __future__ import annotations

import unittest
from pathlib import Path
import sys

import mujoco

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.retarget.robot_model_info import (
    body_descriptors,
    joint_descriptors,
    robot_model_metadata,
    ui_metadata,
)


class RobotModelInfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = ROOT

    def metadata(self, relative_model: str, ui: dict) -> dict:
        return robot_model_metadata(self.root, {
            "robot": {"mjcf": relative_model, "ui": ui},
        })

    def test_registered_g1_and_k1_dof_and_groups(self) -> None:
        from server.robot_registry import resolve_variant

        expected = {"g1_29dof": (29, 30), "k1_22dof": (22, 23)}
        for variant_id, (dof, bodies) in expected.items():
            record = resolve_variant(variant_id, root=self.root)
            metadata = robot_model_metadata(
                self.root, {"robot": record.runtime_robot(self.root)}
            )
            self.assertEqual(metadata["actuated_dof_count"], dof)
            self.assertEqual(len(metadata["bodies"]), bodies)
            self.assertEqual(len({body["name"] for body in metadata["bodies"]}), bodies)
            assigned = [
                name for group in metadata["groups"] for name in group["body_names"]
            ]
            self.assertEqual(len(assigned), bodies)
            self.assertEqual(len(set(assigned)), bodies)
            self.assertEqual(metadata["groups"][0]["id"], "root")
            self.assertTrue(metadata["groups"][0]["root_group"])

            mapping_targets = set(metadata["mapping_target_links"])
            self.assertEqual(len(mapping_targets), bodies)
            self.assertEqual(
                mapping_targets,
                {
                    body["name"]
                    for body in metadata["bodies"]
                    if body["mapping_target"]
                },
            )

    def test_g1_mapping_metadata_exposes_analytic_joint_rows(self) -> None:
        import json

        config = json.loads((
            self.root / "server" / "retarget_assets" / "configs" / "meva"
            / "unitree" / "g1_29dof" / "primary_standard.json"
        ).read_text(encoding="utf-8"))
        metadata = robot_model_metadata(self.root, config)
        targets = set(metadata["analytic_joint_target_joints"])
        axial = set(metadata["analytic_joint_axial_joints"])
        self.assertIn("left_shoulder_pitch_joint", targets)
        self.assertIn("left_shoulder_roll_joint", targets)
        self.assertNotIn("left_shoulder_yaw_joint", targets)
        self.assertIn("left_shoulder_yaw_joint", axial)

    def test_k1_has_only_its_runtime_joint_structure(self) -> None:
        from server.robot_registry import resolve_variant

        record = resolve_variant("k1_22dof", root=self.root)
        metadata = robot_model_metadata(
            self.root, {"robot": record.runtime_robot(self.root)}
        )
        names = {joint["name"] for joint in metadata["joints"]}
        self.assertIn("Left_Elbow_Pitch", names)
        self.assertIn("Left_Elbow_Yaw", names)
        self.assertNotIn("left_wrist_pitch_joint", names)
        self.assertNotIn("waist_yaw_joint", names)
        self.assertFalse(next(j for j in metadata["joints"] if j["type_name"] == "free")["controllable"])

    def test_full_mapping_and_axis_capability_are_separate(self) -> None:
        from server.robot_registry import resolve_variant

        record = resolve_variant("g1_29dof", root=self.root)
        metadata = robot_model_metadata(
            self.root, {"robot": record.runtime_robot(self.root)}
        )
        by_name = {body["name"]: body for body in metadata["bodies"]}
        self.assertTrue(by_name["left_elbow_link"]["mapping_target"])
        self.assertTrue(by_name["left_wrist_roll_link"]["mapping_target"])
        self.assertTrue(by_name["left_wrist_roll_link"]["full_orientation_supported"])
        self.assertFalse(by_name["left_wrist_roll_link"]["axis_alignment_supported"])
        self.assertTrue(by_name["left_elbow_link"]["axis_alignment_supported"])

    def test_missing_ui_groups_fall_back_to_root_subtree_without_symmetry_control(self) -> None:
        model = mujoco.MjModel.from_xml_path(
            str(self.root / "server/robots/booster/k1/K1_22dof.xml")
        )
        joints = joint_descriptors(model)
        bodies = body_descriptors(model, joints)
        presentation = ui_metadata(model, bodies, joints, {})
        self.assertEqual(len(presentation["groups"]), 1)
        self.assertEqual(presentation["groups"][0]["id"], "Trunk")
        self.assertNotIn("symmetry_partner", presentation["groups"][0])
        self.assertEqual(len(presentation["groups"][0]["body_names"]), 23)

    def test_group_rejects_unknown_body(self) -> None:
        model = mujoco.MjModel.from_xml_path(
            str(self.root / "server/robots/booster/k1/K1_22dof.xml")
        )
        joints = joint_descriptors(model)
        bodies = body_descriptors(model, joints)
        with self.assertRaisesRegex(ValueError, "unknown bodies"):
            ui_metadata(model, bodies, joints, {
                "groups": [{"id": "bad", "name": "BAD", "bodies": ["missing"]}]
            })


if __name__ == "__main__":
    unittest.main()
