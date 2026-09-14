from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from server.robot_registry import (
    RobotRegistryError,
    apply_variant_to_runtime_config,
    load_registry,
    public_catalog,
    resolve_variant,
    validate_retarget_config,
)


class RobotRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_g1_registry_and_runtime_resolution(self) -> None:
        records = load_registry(self.root)
        self.assertEqual(
            [item.variant_id for item in records],
            ["g1_29dof", "g1_23dof", "g1_23dof_rev_1_0", "k1_22dof"],
        )
        enabled = [item.variant_id for item in records if item.enabled]
        self.assertEqual(enabled, ["g1_29dof", "k1_22dof"])

        record = resolve_variant("g1_29dof", root=self.root)
        runtime = apply_variant_to_runtime_config(
            {"robot": {
                "manufacturer": "unitree", "model": "g1", "variant": "g1_29dof",
            }},
            record,
            root=self.root,
        )
        self.assertEqual(runtime["robot"]["model_format"], "mjcf")
        self.assertEqual(
            runtime["robot"]["mjcf"],
            "server/robots/unitree/g1/g1_29dof.xml",
        )
        self.assertEqual(runtime["robot"]["initial_pose"], {"type": "model_default"})
        self.assertEqual(runtime["robot"]["root_body"], "pelvis")
        self.assertTrue(runtime["robot"]["floating_base"])
        self.assertEqual(runtime["robot"]["output_joint_order"], "model_hinge_order")
        self.assertEqual(len(runtime["robot"]["ui"]["groups"]), 5)
        skeleton = runtime["robot"]["ui"]["skeleton"]
        self.assertEqual(
            [part["pattern"] for part in skeleton["parts"]],
            ["surface", "surface", "triangle", "triangle", "support", "support"],
        )
        self.assertEqual(
            runtime["robot"]["retargeting"]["landmarks"]["pelvis_reference"],
            {"body": "pelvis", "local_position": [0.0, 0.0, 0.0]},
        )
        self.assertEqual(
            runtime["robot"]["ui"]["symmetry"]["group_pairs"],
            [["left_arm", "right_arm"], ["left_leg", "right_leg"]],
        )
        self.assertNotIn("initial_keyframe", runtime["robot"])
        self.assertEqual(
            runtime["robot"]["retarget_assets"]["meva_offsets"]["policy"],
            "approved",
        )
        self.assertTrue(record.approved_meva_offset_path.is_file())

    def test_catalog_keeps_disabled_variants_for_management(self) -> None:
        catalog = public_catalog(self.root)
        self.assertEqual(len(catalog["robots"]), 2)
        variants = next(
            robot["variants"] for robot in catalog["robots"]
            if robot["robot_id"] == "g1"
        )
        self.assertEqual(sum(bool(item["enabled"]) for item in variants), 1)

    def test_k1_registry_and_fixed_foot_metadata(self) -> None:
        record = resolve_variant("k1_22dof", root=self.root)
        runtime = apply_variant_to_runtime_config({"robot": {}}, record, root=self.root)
        contacts = runtime["robot"]["foot_contacts"]
        self.assertEqual(contacts["robot_foot_to_ground_offset_m"], 0.038)
        self.assertEqual(record.meva_offset_policy, "approved")
        self.assertTrue(record.approved_meva_offset_path.is_file())
        self.assertEqual(len(contacts["left"]["support_points"]), 4)
        self.assertEqual(len(contacts["right"]["support_points"]), 4)
        self.assertEqual(len(runtime["robot"]["ui"]["groups"]), 5)
        skeleton = runtime["robot"]["ui"]["skeleton"]
        self.assertEqual(skeleton["parts"][2]["role"], "head")
        self.assertEqual(
            [part["pattern"] for part in skeleton["parts"]],
            [
                "surface", "surface", "circle", "semantic_axis", "semantic_axis",
                "support", "support",
            ],
        )
        self.assertNotIn("left_hand_link", skeleton["hide_parent_edges"])
        self.assertNotIn("right_hand_link", skeleton["hide_parent_edges"])
        self.assertFalse(any(part["pattern"] == "triangle" for part in skeleton["parts"]))
        self.assertEqual(
            skeleton["parts"][3],
            {
                "role": "left_hand", "pattern": "semantic_axis",
                "body": "left_hand_link", "length_m": 0.2,
            },
        )
        self.assertEqual(
            runtime["robot"]["retargeting"]["landmarks"]["pelvis_reference"],
            {"body": "Trunk", "local_position": [0.0, 0.0, 0.0]},
        )
        semantics = runtime["robot"]["retargeting"]["terminal_semantics"]
        self.assertEqual(semantics["left_foot_link"]["secondary"], [0.0, 0.0, -1.0])

        g1 = apply_variant_to_runtime_config(
            {"robot": {}}, resolve_variant("g1_29dof", root=self.root), root=self.root
        )
        self.assertTrue(any(
            part["pattern"] == "triangle"
            for part in g1["robot"]["ui"]["skeleton"]["parts"]
        ))

    def test_k1_full_body_mapping_does_not_require_target_geometry(self) -> None:
        record = resolve_variant("k1_22dof", root=self.root)
        config = {
            "robot": {"manufacturer": "booster", "model": "k1", "variant": "k1_22dof"},
            "mappings": [{
                "source_segment": "LeftUpperArm",
                "target_link": "Left_Arm_1",
                "orientation_mode": "full",
            }],
        }
        summary = validate_retarget_config(record, config)
        self.assertEqual(summary["mapping_count"], 1)

    def test_k1_axis_mapping_requires_manifest_primary_axis(self) -> None:
        record = resolve_variant("k1_22dof", root=self.root)
        config = {
            "robot": {"manufacturer": "booster", "model": "k1", "variant": "k1_22dof"},
            "mappings": [{
                "source_segment": "LeftUpperArm",
                "target_link": "Left_Arm_1",
                "orientation_mode": "axis",
            }],
        }
        with self.assertRaisesRegex(RobotRegistryError, "requires a Primary axis"):
            validate_retarget_config(record, config)

    def test_standard_configs_match_registered_model(self) -> None:
        record = resolve_variant("g1_29dof", root=self.root)
        directory = (
            self.root / "server" / "retarget_assets" / "configs" / "meva"
            / "unitree" / "g1_29dof"
        )
        for filename in ("primary_standard.json", "main_standard.json"):
            config = json.loads((directory / filename).read_text(encoding="utf-8"))
            summary = validate_retarget_config(record, config)
            self.assertEqual(summary["dof"], 29)
            self.assertEqual(summary["mapping_count"], 14)
            self.assertNotIn("mjcf", config["robot"])

    def test_missing_manifest_reports_expected_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            robots = root / "server" / "robots"
            robots.mkdir(parents=True)
            (robots / "robots.json").write_text(json.dumps({
                "schema_version": "1.0",
                "robots": [{
                    "manufacturer_id": "test",
                    "manufacturer_name": "Test",
                    "robot_id": "robot",
                    "robot_name": "Test Robot",
                    "manifest": "test/robot/manifest.json",
                    "enabled": True,
                }],
            }), encoding="utf-8")
            with self.assertRaisesRegex(RobotRegistryError, "manifest.json not found"):
                load_registry(root)


if __name__ == "__main__":
    unittest.main()
