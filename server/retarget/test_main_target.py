from __future__ import annotations

import tempfile
import unittest
import json
import pickle
from pathlib import Path

import numpy as np
import mujoco

from main_calibration import _free_joint_qpos_addr, _hinge_joints, _qpos_from_primary_frame
from foot_support import load_foot_support_definition, support_point_world_positions
from main_prepare import GeomZTask, prepare_main_ik_from_target
from main_target import _target_z, build_main_target, load_main_target


class MainTargetTest(unittest.TestCase):
    def test_common_delta_preserves_foot_shape(self):
        base = np.asarray([[0.03, 0.05, 0.04, 0.06], [-0.01, 0.01, 0.00, 0.02]])
        target = _target_z(base, np.asarray([0.6, 0.2]))
        np.testing.assert_allclose(target[0] - base[0], -0.018)
        np.testing.assert_allclose(target[1] - base[1], 0.01)
        np.testing.assert_allclose(np.diff(target, axis=1), np.diff(base, axis=1))

    def test_schema_loader(self):
        n = 3
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample_main_target.npz"
            np.savez_compressed(
                path,
                schema_version=np.asarray("1.1"), target_fps=np.asarray(30.0),
                frame=np.arange(n), time_s=np.arange(n) / 30.0,
                source_frame_float=np.arange(n, dtype=np.float64),
                source_frame_nearest=np.arange(n, dtype=np.int64),
                pelvis_target_xyz=np.zeros((n, 3)),
                pelvis_target_quat=np.tile([1.0, 0.0, 0.0, 0.0], (n, 1)),
                quaternion_order=np.asarray("wxyz"),
                link_names=np.asarray(["pelvis"]),
                link_orientation_mode=np.asarray(["full"]),
                link_axis_local=np.zeros((1, 3)),
                link_target_quat=np.tile([[[1.0, 0.0, 0.0, 0.0]]], (n, 1, 1)),
                left_pelvis_to_foot_direction=np.tile([0.0, 0.0, -1.0], (n, 1)),
                right_pelvis_to_foot_direction=np.tile([0.0, 0.0, -1.0], (n, 1)),
                left_gcp_corrected=np.asarray([0.0, 0.5, 1.0]),
                right_gcp_corrected=np.asarray([1.0, 0.5, 0.0]),
                left_min_geom_index=np.asarray([0, 1, 2]),
                right_min_geom_index=np.asarray([3, 2, 1]),
                left_geom_target_z=np.zeros((n, 4)),
                right_geom_target_z=np.zeros((n, 4)),
                left_geom_names=np.asarray(["l0", "l1", "l2", "l3"]),
                right_geom_names=np.asarray(["r0", "r1", "r2", "r3"]),
            )
            loaded = load_main_target(path, expected_frames=n, expected_fps=30.0)
            self.assertEqual(set(loaded), {
                "schema_version", "target_fps", "frame", "time_s",
                "source_frame_float", "source_frame_nearest",
                "pelvis_target_xyz", "pelvis_target_quat", "quaternion_order",
                "link_names", "link_orientation_mode", "link_axis_local",
                "link_target_quat", "left_pelvis_to_foot_direction",
                "right_pelvis_to_foot_direction",
                "left_gcp_corrected", "right_gcp_corrected",
                "left_min_geom_index", "right_min_geom_index",
                "left_geom_target_z", "right_geom_target_z",
                "left_geom_names", "right_geom_names",
            })

    def test_representative_primary_build(self):
        root = Path(__file__).resolve().parents[2]
        primary_dir = root / (
            "workspace/users/local_user/capsules/2606050001/retarget/"
            "g1_29dof/2608230006"
        )
        config_path = primary_dir / "2608230006-01/2608230006-01_main_config.json"
        if not config_path.exists():
            self.skipTest("Representative Capsule is not available")
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        with (primary_dir / "2608230006_primary.pkl").open("rb") as stream:
            primary = pickle.load(stream)
        model = mujoco.MjModel.from_xml_path(str(root / cfg["robot"]["mjcf"]))
        support = load_foot_support_definition(model, cfg)
        data = mujoco.MjData(model)
        free_qadr = _free_joint_qpos_addr(model)
        hinges = _hinge_joints(model)
        contact = {}
        positions = {"left": [], "right": []}
        for frame_index in range(len(primary["root_pos"])):
            data.qpos[:] = _qpos_from_primary_frame(
                model, primary, frame_index, free_qadr, hinges
            )
            mujoco.mj_forward(model, data)
            for side in ("left", "right"):
                positions[side].append(
                    support_point_world_positions(data, support.sides[side])
                )
        for side in ("left", "right"):
            definition = support.sides[side]
            contact[side] = {
                "labels": list(definition.names),
                "display_names": definition.display_names,
                "body_name": definition.body_name,
                "body_id": definition.body_id,
                "local_positions": definition.local_positions,
                "xyz": np.asarray(positions[side]),
            }
        main_cfg = cfg["main"]
        offsets = cfg["foot_to_ground_offset"]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "representative_main_target.npz"
            build_main_target(
                output_path=output,
                primary=primary,
                primary_target_path=primary_dir / "2608230006_primary_target.npz",
                model=model,
                cfg=cfg,
                contact_geometry=contact,
                mapping_offset_path=config_path.parent / cfg["offsets"]["file"],
                fallback_common_scale=1.0,
                meva_foot_to_ground_offset_m=float(offsets["meva_m"]),
                robot_foot_to_ground_offset_m=float(offsets["robot_m"]),
                gcp_smoothing_ms=float(main_cfg["gcp_smoothing_ms"]),
                gcp_min_offset=float(main_cfg["gcp_min_offset"]),
                gcp_max_offset=float(main_cfg["gcp_max_offset"]),
                gcp_power_number=float(main_cfg["gcp_power_number"]),
            )
            target = load_main_target(
                output,
                expected_frames=len(primary["root_pos"]),
                expected_fps=float(primary["fps"]),
            )
            self.assertEqual(target["left_geom_target_z"].shape[1], 4)
            self.assertTrue(np.all(np.isfinite(target["right_geom_target_z"])))
            ik = prepare_main_ik_from_target(
                primary_pkl=primary_dir / "2608230006_primary.pkl",
                main_target_npz=output,
                robot_xml=root / cfg["robot"]["mjcf"],
                cfg=cfg,
                sole_position_weights=main_cfg[
                    "ground_contact_height_correction"
                ]["sole_position_weights"],
            )
            expected_q = _qpos_from_primary_frame(
                ik.model, primary, 0, _free_joint_qpos_addr(ik.model),
                _hinge_joints(ik.model),
            )
            np.testing.assert_allclose(ik.solver_frame_specs[0].initial_q, expected_q)
            prepared = ik.solver_frame_specs[0].prepare(ik.initial_configuration)
            z_tasks = [task for task in prepared.tasks if isinstance(task, GeomZTask)]
            self.assertEqual(len(z_tasks), 8)
            self.assertTrue(all(task.k == 1 for task in z_tasks))
            expected_spatial = 2 if cfg["spatial_constraints"][
                "pelvis_foot_direction"
            ]["enabled"] else 0
            self.assertEqual(
                len(prepared.tasks), len(cfg["mappings"]) + 8 + expected_spatial
            )
            self.assertEqual(
                [str(value) for value in target["link_names"]],
                [str(mapping["target_link"]) for mapping in cfg["mappings"]],
            )


if __name__ == "__main__":
    unittest.main()
