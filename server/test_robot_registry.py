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
        self.assertEqual(
            runtime["robot"]["ui"]["symmetry"]["group_pairs"],
            [["left_arm", "right_arm"], ["left_leg", "right_leg"]],
        )
        self.assertNotIn("initial_keyframe", runtime["robot"])

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
        self.assertEqual(len(contacts["left"]["support_points"]), 4)
        self.assertEqual(len(contacts["right"]["support_points"]), 4)
        self.assertEqual(len(runtime["robot"]["ui"]["groups"]), 5)

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
