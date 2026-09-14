from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from server.retarget.check_offsets import load_approved_offsets


class ApprovedOffsetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]

    def _config(self, robot: dict, mappings: list[dict]) -> Path:
        directory = tempfile.TemporaryDirectory(dir=self.root / "workspace")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "config.json"
        path.write_text(
            json.dumps({"robot": robot, "mappings": mappings}), encoding="utf-8"
        )
        return path

    def test_k1_uses_approved_asset_for_mapping_subset(self) -> None:
        path = self._config(
            {"manufacturer": "booster", "model": "k1", "variant": "k1_22dof"},
            [{
                "source_segment": "LeftUpperArm",
                "target_link": "Left_Arm_3",
                "orientation_mode": "axis",
            }],
        )
        with patch(
            "server.retarget.check_offsets.compute_offsets",
            side_effect=AssertionError("production must not inspect/generate runtime cache"),
        ):
            offsets, asset, generated = load_approved_offsets(path)
        self.assertFalse(generated)
        self.assertIn("server/robots/booster/k1/retarget_assets", asset.as_posix())
        np.testing.assert_allclose(
            offsets["Left_Arm_3"],
            [0.016747046953130732, 0.9995968834948491,
             0.02292290196749781, -0.0003840457307244864],
        )

    def test_g1_uses_same_generic_approved_asset_mechanism(self) -> None:
        path = self._config(
            {"manufacturer": "unitree", "model": "g1", "variant": "g1_29dof"},
            [{
                "source_segment": "Pelvis", "target_link": "pelvis",
                "orientation_mode": "full",
            }],
        )
        offsets, asset, _ = load_approved_offsets(path)
        self.assertIn("server/robots/unitree/g1/retarget_assets", asset.as_posix())
        self.assertEqual({"pelvis"}, set(offsets))

    def test_g1_approved_alternate_mapping_mode_remains_available(self) -> None:
        path = self._config(
            {"manufacturer": "unitree", "model": "g1", "variant": "g1_29dof"},
            [{
                "source_segment": "LeftUpperLeg",
                "target_link": "left_hip_yaw_link",
                "orientation_mode": "full",
            }],
        )
        offsets, _, _ = load_approved_offsets(path)
        np.testing.assert_allclose(
            offsets["left_hip_yaw_link"],
            [0.6866093903881503, -0.6998824894357001,
             -0.13873248896925264, 0.13958990836194468],
        )

    def test_unapproved_mapping_requires_robot_setup_approval(self) -> None:
        path = self._config(
            {"manufacturer": "booster", "model": "k1", "variant": "k1_22dof"},
            [{
                "source_segment": "LeftUpperArm",
                "target_link": "Left_Arm_1",
                "orientation_mode": "full",
            }],
        )
        with self.assertRaisesRegex(ValueError, "not covered by the approved"):
            load_approved_offsets(path)

    def test_missing_approved_policy_fails_clearly(self) -> None:
        path = self._config(
            {"manufacturer": "future", "model": "robot", "variant": "future_v1"}, []
        )
        record = SimpleNamespace(
            meva_offset_policy="missing", manufacturer_id="future",
            robot_id="robot", variant_id="future_v1",
        )
        with patch("server.robot_registry.resolve_variant", return_value=record):
            with self.assertRaisesRegex(ValueError, "no approved MEVA Offset policy"):
                load_approved_offsets(path)

    def test_hash_mismatch_fails_before_ik(self) -> None:
        path = self._config(
            {"manufacturer": "future", "model": "robot", "variant": "future_v1"}, []
        )
        asset = path.parent / "approved.json"
        asset.write_text("{}", encoding="utf-8")
        record = SimpleNamespace(
            meva_offset_policy="approved", approved_meva_offset_path=asset,
            approved_meva_offset_sha256="0" * 64,
            manufacturer_id="future", robot_id="robot", variant_id="future_v1",
        )
        with patch("server.robot_registry.resolve_variant", return_value=record):
            with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                load_approved_offsets(path)

    def test_explicit_no_offset_policy_uses_identity_offsets(self) -> None:
        path = self._config(
            {"manufacturer": "future", "model": "robot", "variant": "future_v1"},
            [{
                "source_segment": "Pelvis", "target_link": "base",
                "orientation_mode": "full",
            }],
        )
        record = SimpleNamespace(
            meva_offset_policy="none", manifest_path=path,
            manufacturer_id="future", robot_id="robot", variant_id="future_v1",
        )
        with patch("server.robot_registry.resolve_variant", return_value=record):
            offsets, _, generated = load_approved_offsets(path)
        self.assertFalse(generated)
        np.testing.assert_array_equal(offsets["base"], [1.0, 0.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
