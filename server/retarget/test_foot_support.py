from __future__ import annotations

import unittest
from pathlib import Path

import mujoco
import numpy as np

from foot_support import (
    load_foot_support_definition,
    support_point_jacobian,
    support_point_world_positions,
)
from server.robot_registry import apply_variant_to_runtime_config, resolve_variant
from robot_model_info import (
    bodies_are_directly_adjacent, collision_pair_descriptors,
)


class FootSupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]

    def load(self, variant_id: str):
        record = resolve_variant(variant_id, root=self.root)
        cfg = apply_variant_to_runtime_config({"robot": {}}, record, root=self.root)
        model = mujoco.MjModel.from_xml_path(str(record.model_path))
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        return model, data, cfg, load_foot_support_definition(model, cfg)

    def test_g1_keeps_existing_sphere_centers(self) -> None:
        model, data, _, definition = self.load("g1_29dof")
        expected = np.asarray([
            [-0.05, 0.025, -0.03], [-0.05, -0.025, -0.03],
            [0.12, 0.03, -0.03], [0.12, -0.03, -0.03],
        ])
        self.assertAlmostEqual(definition.robot_foot_to_ground_offset_m, 0.035)
        np.testing.assert_allclose(definition.sides["left"].local_positions, expected)
        support_world = support_point_world_positions(data, definition.sides["left"])
        body_id = definition.sides["left"].body_id
        sphere_ids = [
            geom_id for geom_id in range(model.ngeom)
            if int(model.geom_bodyid[geom_id]) == body_id
            and int(model.geom_type[geom_id]) == int(mujoco.mjtGeom.mjGEOM_SPHERE)
        ]
        np.testing.assert_allclose(support_world, data.geom_xpos[sphere_ids])

    def test_k1_uses_box_bottom_corners(self) -> None:
        model, data, _, definition = self.load("k1_22dof")
        expected = np.asarray([
            [-0.064, 0.035, -0.038], [-0.064, -0.035, -0.038],
            [0.116, 0.035, -0.038], [0.116, -0.035, -0.038],
        ])
        self.assertEqual(model.nv, 28)
        self.assertAlmostEqual(definition.robot_foot_to_ground_offset_m, 0.038)
        np.testing.assert_allclose(definition.sides["left"].local_positions, expected)
        jacobian = support_point_jacobian(
            model, data, definition.sides["left"], 0
        )
        self.assertEqual(jacobian.shape, (3, model.nv))
        self.assertTrue(np.all(np.isfinite(jacobian)))
        record = resolve_variant("k1_22dof", root=self.root)
        self.assertEqual(len(collision_pair_descriptors(model, record.model_path)), 174)

    def test_g1_and_k1_collision_candidates_exclude_direct_neighbors(self) -> None:
        for variant_id in ("g1_29dof", "k1_22dof"):
            with self.subTest(variant_id=variant_id):
                record = resolve_variant(variant_id, root=self.root)
                model = mujoco.MjModel.from_xml_path(str(record.model_path))
                for pair in collision_pair_descriptors(model, record.model_path):
                    body_a = int(model.geom_bodyid[int(pair["geom_a_id"])])
                    body_b = int(model.geom_bodyid[int(pair["geom_b_id"])])
                    self.assertFalse(
                        bodies_are_directly_adjacent(model, body_a, body_b),
                        pair["key"],
                    )


if __name__ == "__main__":
    unittest.main()
