from __future__ import annotations

import json
import pickle
import struct
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import numpy as np

from server.retarget.check_offsets import (
    BVH_DISTAL_JOINT,
    normalize,
    offset_fingerprint,
    parse_bvh_offsets,
    source_long_axis_canonical,
)
from meva_canonical_geometry import CANONICAL_GEOMETRY_VERSION
from server.retarget.mapping_tasks import axis_angle_rad, quat_rotate_vec
from server.retarget.motion_io import save_gmr_pickle, save_motion_npz, trajectory_derivatives
from server.retarget.viewer_data import MAGIC, write_viewer_bin


class CanonicalOffsetTests(unittest.TestCase):
    def test_axis_error_ignores_twist_and_detects_axis_tilt(self) -> None:
        axis = np.asarray([1.0, 0.0, 0.0])
        identity = np.asarray([1.0, 0.0, 0.0, 0.0])
        twist_x_90 = np.asarray([
            np.cos(np.pi / 4.0), np.sin(np.pi / 4.0), 0.0, 0.0,
        ])
        tilt_z_90 = np.asarray([
            np.cos(np.pi / 4.0), 0.0, 0.0, np.sin(np.pi / 4.0),
        ])
        target = quat_rotate_vec(identity, axis)
        self.assertAlmostEqual(
            axis_angle_rad(target, quat_rotate_vec(twist_x_90, axis)), 0.0,
            places=7,
        )
        self.assertAlmostEqual(
            axis_angle_rad(target, quat_rotate_vec(tilt_z_90, axis)),
            np.pi / 2.0,
            places=7,
        )

    def test_supported_reference_bvhs_match_canonical_directions(self) -> None:
        root = Path(__file__).resolve().parents[2]
        paths = list((
            root / "workspace" / "users" / "local_user" / "capsules"
        ).glob("*/meva/*.bvh"))
        if len(paths) < 2:
            self.skipTest("Two MEVA reference BVHs are not available")
        for path in paths[:2]:
            offsets, _ = parse_bvh_offsets(path)
            for segment in (
                "Pelvis", "Thoracic2", "Thoracic2+LumberSpine",
                "LeftUpperArm", "LeftForearm", "RightUpperArm", "RightForearm",
                "LeftUpperLeg", "LeftLowerLeg", "RightUpperLeg", "RightLowerLeg",
            ):
                np.testing.assert_allclose(
                    source_long_axis_canonical(segment),
                    normalize(offsets[BVH_DISTAL_JOINT[segment]]),
                    atol=1e-8,
                )

    def test_fingerprint_excludes_capsule_bvh_and_tracks_geometric_inputs(self) -> None:
        cfg = {
            "source": {"bvh": "capsule_a.bvh"},
            "mappings": [{"source_segment": "Pelvis", "target_link": "pelvis"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            robot = Path(directory) / "robot.xml"
            robot.write_text("<mujoco/>", encoding="utf-8")
            first = offset_fingerprint(cfg, robot)
            other_capsule = deepcopy(cfg)
            other_capsule["source"]["bvh"] = "different_subject.bvh"
            self.assertEqual(first, offset_fingerprint(other_capsule, robot))
            self.assertNotIn("bvh_sha256", first)

            changed_mapping = deepcopy(cfg)
            changed_mapping["mappings"][0]["target_link"] = "torso_link"
            self.assertNotEqual(first, offset_fingerprint(changed_mapping, robot))

            robot.write_text("<mujoco model='changed'/>", encoding="utf-8")
            self.assertNotEqual(first, offset_fingerprint(cfg, robot))
            robot.write_text("<mujoco/>", encoding="utf-8")
            self.assertNotEqual(
                first,
                offset_fingerprint(
                    cfg, robot,
                    geometry_version=CANONICAL_GEOMETRY_VERSION + "-changed",
                ),
            )
            self.assertNotEqual(
                first,
                offset_fingerprint(cfg, robot, geometry_hash="changed"),
            )


class MotionArtifactTests(unittest.TestCase):
    def test_offline_derivatives_and_motion_npz(self) -> None:
        fps = 2.0
        time = np.arange(5, dtype=np.float64) / fps
        values = (time * time)[:, None]
        velocity, acceleration = trajectory_derivatives(values, fps)
        np.testing.assert_allclose(velocity[:, 0], 2.0 * time)
        np.testing.assert_allclose(acceleration[:, 0], 2.0)

        motion = {
            "fps": fps,
            "root_pos": np.column_stack((time * time, time * 0.0, time * 0.0)),
            "root_rot": np.tile([0.0, 0.0, 0.0, 1.0], (5, 1)),
            "dof_pos": values,
            "source_frame_float": time * 100.0,
            "source_frame_indices": np.rint(time * 100.0).astype(np.int32),
            "time_s": time,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "primary.npz"
            arrays = save_motion_npz(
                path, motion, joint_names=["joint"], root_rot_order="xyzw"
            )
            required = {
                "schema_version", "fps", "frame", "time_s",
                "source_frame_float", "source_frame_nearest", "root_pos",
                "root_rot", "root_rot_order", "joint_names", "dof_pos",
                "dof_vel", "dof_acc", "root_lin_vel", "root_ang_vel",
            }
            self.assertEqual(set(arrays), required)
            self.assertTrue(path.exists())
            self.assertFalse(any("diagnostic" in key for key in arrays))

    def test_gmr_pickle_has_exact_consumer_contract_and_xyzw_rotation(self) -> None:
        motion = {
            "fps": 30.0,
            "root_pos": np.zeros((2, 3)),
            "root_rot": np.tile([1.0, 0.0, 0.0, 0.0], (2, 1)),
            "dof_pos": np.zeros((2, 1)),
            "metadata": {"root_rot_order": "wxyz"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.pkl"
            saved = save_gmr_pickle(path, motion)
            with path.open("rb") as stream:
                loaded = pickle.load(stream)
            self.assertEqual(set(loaded), {
                "fps", "root_pos", "root_rot", "dof_pos",
                "local_body_pos", "link_body_list",
            })
            np.testing.assert_allclose(saved["root_rot"], [[0, 0, 0, 1]] * 2)

    def test_viewer_bin_fixed_header_embeds_metadata_and_uint8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "primary_viewer.bin"
            write_viewer_bin(path, {
                "schema_version": "1.0",
                "array_metadata": {
                    "severity": {"unit": "1", "semantic_description": "test severity"}
                },
            }, {"severity": np.asarray([0, 191, 255], dtype=np.uint8)})
            raw = path.read_bytes()
            self.assertEqual(raw[:8], MAGIC)
            binary_version, header_length = struct.unpack("<II", raw[8:16])
            header = json.loads(raw[16:16 + header_length].decode("utf-8"))
            self.assertEqual(binary_version, header["format_version"])
            block = header["blocks"][0]
            self.assertEqual(block["dtype"], "uint8")
            self.assertEqual(block["shape"], [3])
            self.assertEqual(block["offset"], 0)
            self.assertEqual(block["unit"], "1")
            self.assertEqual(raw[16 + header_length:], bytes([0, 191, 255]))

    def test_short_primary_run_writes_four_standard_files_and_no_pickle(self) -> None:
        root = Path(__file__).resolve().parents[2]
        source = next((
            root / "workspace" / "users" / "local_user" / "capsules"
        ).glob("*/meva/sequence_*.csv"), None)
        standard = (
            root / "server" / "retarget_assets" / "configs" / "meva"
            / "unitree" / "g1_29dof" / "primary_standard.json"
        )
        robot = root / "server" / "robots" / "unitree" / "g1" / "g1_29dof.xml"
        if source is None or not standard.exists() or not robot.exists():
            self.skipTest("Primary integration fixtures are unavailable")
        from server.retarget.primary_retarget import main as run_primary

        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            (temporary_root / "server").mkdir()
            (temporary_root / "workspace").mkdir()
            cfg = json.loads(standard.read_text(encoding="utf-8"))
            run_id = "2608259999"
            cfg.update({
                "capsule_id": "2606050001",
                "source": {
                    "type": "meva_csv", "file": str(source),
                    "header_row_1based": 8, "sampling_rate_hz": 100,
                    "quaternion_order": "wxyz",
                    "quaternion_columns": "{segment}_q_gs_{component}",
                },
                "frame_range": {"start": 0, "stop": 10, "step": 1},
                "sampling": {"rate_fps": 30.0},
            })
            cfg["robot"]["mjcf"] = str(robot)
            cfg.setdefault("output", {}).update({
                "run_id": run_id, "overwrite_existing": False,
                "root_rot_order": "xyzw", "save_diagnostics_csv": False,
                "save_debug_artifacts": False,
            })
            cfg["output"].pop("pkl_name", None)
            config_path = temporary_root / "request.json"
            config_path.write_text(json.dumps(cfg), encoding="utf-8")
            run_path, _ = run_primary(config_path)
            expected = {
                f"{run_id}_primary_target.npz",
                f"{run_id}_primary.npz",
                f"{run_id}_primary_config.json",
                f"{run_id}_primary_viewer.bin",
            }
            self.assertEqual({path.name for path in run_path.iterdir()}, expected)
            self.assertFalse(list(run_path.glob("*.pkl")))
            self.assertFalse(list(run_path.glob("*offsets.json")))
            snapshot = json.loads((
                run_path / f"{run_id}_primary_config.json"
            ).read_text(encoding="utf-8"))
            self.assertEqual(snapshot["schema_version"], "1.0")
            self.assertTrue(snapshot["name"])
            self.assertIn("source", snapshot)
            self.assertIn("mappings", snapshot)

            with np.load(run_path / f"{run_id}_primary_target.npz", allow_pickle=False) as archive:
                self.assertTrue({
                    "schema_version", "source_fps", "target_fps", "start_frame",
                    "end_frame", "frame", "time_s", "source_frame_float",
                    "source_frame_nearest", "segment_names", "segment_quat",
                    "quaternion_order", "pelvis_z_m", "left_foot_z_m",
                    "right_foot_z_m", "gcp_left_ff", "gcp_left_ca",
                    "gcp_right_ff", "gcp_right_ca",
                    "meva_foot_to_ground_offset_m",
                    "robot_foot_to_ground_offset_m",
                }.issubset(archive.files))
                self.assertEqual(archive["frame"].shape, (3,))
                self.assertEqual(archive["segment_quat"].shape[0], 3)
                self.assertAlmostEqual(float(archive["target_fps"]), 30.0)
            with np.load(run_path / f"{run_id}_primary.npz", allow_pickle=False) as archive:
                primary_dof = archive["dof_pos"].copy()
                self.assertEqual(archive["root_pos"].shape[1:], (3,))
                self.assertEqual(archive["root_rot"].shape[1:], (4,))
                self.assertEqual(archive["dof_pos"].shape, archive["dof_vel"].shape)
                self.assertEqual(archive["dof_pos"].shape, archive["dof_acc"].shape)
            raw = (run_path / f"{run_id}_primary_viewer.bin").read_bytes()
            _, header_length = struct.unpack("<II", raw[8:16])
            header = json.loads(raw[16:16 + header_length].decode("utf-8"))
            blocks = {item["name"]: item for item in header["blocks"]}
            for name in (
                "ik_iterations", "ik_converged", "ik_final_joint_delta_rad",
                "orientation_residual_rotvec_rad", "orientation_residual_angle_rad",
                "orientation_target_direction", "orientation_result_direction",
                "orientation_axis_error_rad",
                "analytic_joint_target_rad", "analytic_joint_target_enabled",
                "analytic_joint_target_branch", "analytic_joint_target_singularity",
                "joint_velocity_rad_s", "joint_acceleration_rad_s2",
                "joint_limit_severity", "self_collision_signed_distance_m",
                "link_pos", "link_quat", "geom_pos", "foot_support_point_pos",
            ):
                self.assertIn(name, blocks)
            self.assertEqual(blocks["foot_support_point_pos"]["shape"], [3, 8, 3])
            self.assertEqual(len(header["foot_support_points"]), 8)
            self.assertEqual(header["array_offset_basis"], "payload_start")
            self.assertEqual(header["endianness"], "little")
            self.assertEqual(header["frames"], 3)
            self.assertEqual(
                blocks["orientation_residual_rotvec_rad"]["shape"], [3, 14, 3]
            )
            self.assertEqual(
                blocks["orientation_target_direction"]["shape"], [3, 14, 3]
            )
            self.assertEqual(
                blocks["orientation_axis_error_rad"]["shape"], [3, 14]
            )
            self.assertEqual(
                blocks["position_residual_xyz_m"]["shape"], [3, 1, 3]
            )
            self.assertEqual(blocks["ik_converged"]["dtype"], "uint8")
            self.assertEqual(blocks["analytic_joint_target_rad"]["shape"], [3, 29])
            self.assertEqual(blocks["analytic_joint_target_enabled"]["dtype"], "uint8")
            self.assertIn("analytic_joint_target", header)
            payload_start = 16 + header_length

            def viewer_array(name: str) -> np.ndarray:
                block = blocks[name]
                dtype = {
                    "float32": "<f4", "int32": "<i4", "uint8": "u1"
                }[block["dtype"]]
                return np.frombuffer(
                    raw,
                    dtype=dtype,
                    count=int(np.prod(block["shape"])),
                    offset=payload_start + int(block["offset"]),
                ).reshape(block["shape"])

            orientation_xyz = viewer_array("orientation_residual_rotvec_rad")
            np.testing.assert_allclose(
                viewer_array("orientation_residual_angle_rad"),
                np.linalg.norm(orientation_xyz, axis=2),
                rtol=1e-6, atol=1e-7,
            )
            target_direction = viewer_array("orientation_target_direction")
            result_direction = viewer_array("orientation_result_direction")
            axis_error = viewer_array("orientation_axis_error_rad")
            axis_mask = np.asarray([
                str(mapping.get("orientation_mode", "full")) == "axis"
                for mapping in header["orientation_mappings"]
            ])
            self.assertTrue(np.all(np.isfinite(axis_error[:, axis_mask])))
            self.assertTrue(np.all(np.isnan(axis_error[:, ~axis_mask])))
            np.testing.assert_allclose(
                np.linalg.norm(target_direction[:, axis_mask], axis=2), 1.0,
                rtol=1e-6, atol=1e-6,
            )
            np.testing.assert_allclose(
                np.linalg.norm(result_direction[:, axis_mask], axis=2), 1.0,
                rtol=1e-6, atol=1e-6,
            )
            expected_axis_error = np.arccos(np.clip(np.sum(
                target_direction[:, axis_mask] * result_direction[:, axis_mask],
                axis=2,
            ), -1.0, 1.0))
            np.testing.assert_allclose(
                axis_error[:, axis_mask], expected_axis_error,
                rtol=1e-5, atol=2e-4,
            )
            position_xyz = viewer_array("position_residual_xyz_m")
            np.testing.assert_allclose(
                viewer_array("position_residual_norm_m"),
                np.linalg.norm(position_xyz, axis=2),
                rtol=1e-6, atol=1e-7,
            )

            # Main must consume the canonical Primary NPZ and create the only
            # new GMR-compatible pickle in the pipeline.
            from server.retarget.main_retarget import run_main

            main_standard = (
                root / "server" / "retarget_assets" / "configs" / "meva"
                / "unitree" / "g1_29dof" / "main_standard.json"
            )
            main_id = f"{run_id}-01"
            main_dir = run_path / main_id
            main_dir.mkdir()
            main_cfg = json.loads(main_standard.read_text(encoding="utf-8"))
            main_cfg["primary_run_id"] = run_id
            main_cfg["source"] = deepcopy(cfg["source"])
            main_cfg["robot"]["mjcf"] = str(robot)
            main_config_path = main_dir / f"{main_id}_main_config.json"
            main_config_path.write_text(json.dumps(main_cfg), encoding="utf-8")
            run_main(main_config_path)

            expected_main = {
                f"{main_id}_main_target.npz", f"{main_id}_main.npz",
                f"{main_id}_main_config.json", f"{main_id}_main_viewer.bin",
                f"{main_id}_main.pkl",
            }
            self.assertEqual({path.name for path in main_dir.iterdir()}, expected_main)
            main_target_path = main_dir / f"{main_id}_main_target.npz"
            with np.load(main_target_path, allow_pickle=False) as archive:
                self.assertTrue({
                    "schema_version", "target_fps", "frame", "time_s",
                    "source_frame_float", "source_frame_nearest",
                    "pelvis_target_xyz", "pelvis_target_quat", "quaternion_order",
                    "link_names", "link_orientation_mode", "link_axis_local",
                    "link_target_quat", "left_pelvis_to_foot_direction",
                    "right_pelvis_to_foot_direction", "left_gcp_corrected",
                    "right_gcp_corrected", "left_min_geom_index",
                    "right_min_geom_index", "left_geom_target_z",
                    "right_geom_target_z", "left_geom_names", "right_geom_names",
                }.issubset(archive.files))
            main_npz = main_dir / f"{main_id}_main.npz"
            self.assertTrue(main_npz.exists())
            main_pickle = main_dir / f"{main_id}_main.pkl"
            self.assertTrue(main_pickle.exists())
            generated_pickles = list(temporary_root.rglob("*.pkl"))
            self.assertEqual(len(generated_pickles), 1)
            self.assertEqual(generated_pickles[0].name, main_pickle.name)
            with main_pickle.open("rb") as stream:
                gmr = pickle.load(stream)
            self.assertEqual(set(gmr), {
                "fps", "root_pos", "root_rot", "dof_pos",
                "local_body_pos", "link_body_list",
            })
            self.assertEqual(gmr["root_pos"].shape[1:], (3,))
            self.assertEqual(gmr["root_rot"].shape[1:], (4,))
            self.assertEqual(gmr["dof_pos"].ndim, 2)
            with np.load(main_npz, allow_pickle=False) as archive:
                self.assertEqual(set(archive.files), {
                    "schema_version", "fps", "frame", "time_s",
                    "source_frame_float", "source_frame_nearest", "root_pos",
                    "root_rot", "root_rot_order", "joint_names", "dof_pos",
                    "dof_vel", "dof_acc", "root_lin_vel", "root_ang_vel",
                })
                main_dof = archive["dof_pos"].copy()
                order = str(archive["root_rot_order"])
                expected_gmr_rotation = archive["root_rot"] if order == "xyzw" else archive["root_rot"][:, [1, 2, 3, 0]]
                np.testing.assert_allclose(gmr["root_rot"], expected_gmr_rotation)
            self.assertGreater(float(np.max(np.abs(main_dof - primary_dof))), 1e-10)

            main_snapshot = json.loads(main_config_path.read_text(encoding="utf-8"))
            self.assertEqual(main_snapshot["schema_version"], "1.0")
            self.assertEqual(main_snapshot["main_runtime_context"]["primary_run_id"], run_id)
            self.assertEqual(
                main_snapshot["main_runtime_context"]["main_target_file"],
                main_target_path.name,
            )

            main_raw = (main_dir / f"{main_id}_main_viewer.bin").read_bytes()
            self.assertEqual(main_raw[:8], raw[:8])
            _, main_header_length = struct.unpack("<II", main_raw[8:16])
            main_header = json.loads(
                main_raw[16:16 + main_header_length].decode("utf-8")
            )
            self.assertEqual(main_header["stage"], "main")
            main_blocks = {item["name"]: item for item in main_header["blocks"]}
            common_fields = {
                "frame", "time_s", "source_frame_float", "source_frame_nearest",
                "joint_angle_rad", "joint_velocity_rad_s",
                "joint_acceleration_rad_s2", "joint_limit_actual_rad",
                "joint_limit_margin_rad", "joint_limit_severity",
                "joint_velocity_severity", "joint_acceleration_severity",
                "ik_iterations", "ik_converged", "ik_final_joint_delta_rad",
                "link_pos", "link_quat", "geom_pos",
                "self_collision_signed_distance_m", "self_collision_severity",
                "orientation_residual_rotvec_rad", "position_residual_xyz_m",
            }
            self.assertTrue(common_fields.issubset(main_blocks))
            for name in common_fields & set(blocks):
                self.assertEqual(main_blocks[name]["dtype"], blocks[name]["dtype"])
                self.assertEqual(main_blocks[name]["shape"], blocks[name]["shape"])
            for name in (
                "foot_geom_target_z_m", "foot_geom_result_z_m",
                "foot_geom_residual_z_m", "gcp_left_corrected",
                "gcp_right_corrected", "pelvis_to_foot_residual_angle_rad",
                "foot_support_point_pos", "foot_support_target_z_m",
                "foot_support_result_z_m", "foot_support_residual_z_m",
                "gcp_left_raw", "gcp_right_raw", "gcp_left_smoothed",
                "gcp_right_smoothed", "gcp_left_used", "gcp_right_used",
                "support_state", "foot_support_min_point_index",
                "pelvis_to_foot_meva_direction",
            ):
                self.assertIn(name, main_blocks)
            self.assertEqual(len(main_header["foot_support_points"]), 8)
            main_payload_start = 16 + main_header_length

            def main_viewer_array(name: str) -> np.ndarray:
                block = main_blocks[name]
                dtype = {"float32": "<f4", "int32": "<i4", "uint8": "u1"}[block["dtype"]]
                return np.frombuffer(
                    main_raw, dtype=dtype, count=int(np.prod(block["shape"])),
                    offset=main_payload_start + int(block["offset"]),
                ).reshape(block["shape"])

            np.testing.assert_allclose(main_viewer_array("joint_angle_rad"), main_dof)
            np.testing.assert_allclose(
                main_viewer_array("foot_geom_residual_z_m"),
                main_viewer_array("foot_geom_target_z_m")
                - main_viewer_array("foot_geom_result_z_m"),
                rtol=1e-6, atol=1e-7,
            )
            np.testing.assert_allclose(
                main_viewer_array("foot_support_residual_z_m"),
                main_viewer_array("foot_support_target_z_m")
                - main_viewer_array("foot_support_result_z_m"),
                rtol=1e-6, atol=1e-7,
            )
            main_orientation_xyz = main_viewer_array("orientation_residual_rotvec_rad")
            np.testing.assert_allclose(
                main_viewer_array("orientation_residual_angle_rad"),
                np.linalg.norm(main_orientation_xyz, axis=2),
                rtol=1e-6, atol=1e-7,
            )


if __name__ == "__main__":
    unittest.main()
