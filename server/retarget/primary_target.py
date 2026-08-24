from __future__ import annotations

from pathlib import Path
import csv

import numpy as np

try:
    from .mapping_tasks import source_segments_for_columns
    from .meva_schema import MEVA_GCP_COLUMN_INDICES, MEVA_POSITION_COLUMN_INDICES
    from .tools.cubic_spline import cubic_spline_resample
    from .tools.quaternion_slerp import quaternion_slerp_resample
    from .tools.sampling import target_timeline
except ImportError:
    from mapping_tasks import source_segments_for_columns
    from meva_schema import MEVA_GCP_COLUMN_INDICES, MEVA_POSITION_COLUMN_INDICES
    from tools.cubic_spline import cubic_spline_resample
    from tools.quaternion_slerp import quaternion_slerp_resample
    from tools.sampling import target_timeline


SCHEMA_VERSION = "1.0"


def build_primary_target(*, cfg: dict, repo_root: Path, output_path: Path) -> Path:
    source_cfg = cfg["source"]
    source_fps = float(source_cfg.get("sampling_rate_hz", 100.0))
    target_fps = float(cfg.get("sampling", {}).get("rate_fps", 30.0))
    csv_path = (repo_root / source_cfg["file"]).resolve()
    header_row = int(source_cfg.get("header_row_1based", 8))
    physical_segments: list[str] = []
    for mapping in cfg.get("mappings", []):
        for segment in source_segments_for_columns(str(mapping["source_segment"])):
            if segment not in physical_segments:
                physical_segments.append(segment)
    pattern = str(source_cfg["quaternion_columns"])
    quaternion_order = str(source_cfg.get("quaternion_order", "wxyz"))
    components = list(quaternion_order)
    if sorted(components) != sorted("wxyz"):
        raise ValueError(f"Unsupported quaternion order: {quaternion_order}")
    quaternion_keys = [
        [pattern.format(segment=segment, component=component) for component in components]
        for segment in physical_segments
    ]
    frame_cfg = cfg.get("frame_range", {})
    start = int(frame_cfg.get("start", 0))
    raw_stop = frame_cfg.get("stop")
    requested_stop = None if raw_stop is None else int(raw_stop)
    if start < 0 or (requested_stop is not None and requested_stop <= start):
        raise ValueError("Primary frame range is empty")

    # The MEVA CSV is large. Extract only target-builder columns in a single
    # streaming pass instead of materializing every string field twice.
    source_quaternions: list[list[list[float]]] = []
    source_indices: list[int] = []
    source_xyz = {name: [] for name in MEVA_POSITION_COLUMN_INDICES}
    source_gcp = {name: [] for name in MEVA_GCP_COLUMN_INDICES}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        for _ in range(header_row - 1):
            next(reader, None)
        fields = [value.strip() for value in (next(reader, None) or [])]
        field_index = {name: index for index, name in enumerate(fields)}
        missing = [key for keys in quaternion_keys for key in keys if key not in field_index]
        if missing:
            raise KeyError(f"Missing MEVA quaternion columns: {missing}")
        quaternion_indices = [[field_index[key] for key in keys] for keys in quaternion_keys]
        max_fixed_index = max(
            [index for indices in MEVA_POSITION_COLUMN_INDICES.values() for index in indices]
            + list(MEVA_GCP_COLUMN_INDICES.values())
        )
        interpolation_start = max(0, start - 1)
        interpolation_stop = None if requested_stop is None else requested_stop + 1
        for source_frame, row in enumerate(reader):
            if source_frame < interpolation_start:
                continue
            if interpolation_stop is not None and source_frame >= interpolation_stop:
                break
            if len(row) <= max_fixed_index:
                raise ValueError(f"MEVA frame {source_frame} is shorter than required schema")
            source_quaternions.append([
                [float(row[index]) for index in indices]
                for indices in quaternion_indices
            ])
            source_indices.append(source_frame)
            for name, indices in MEVA_POSITION_COLUMN_INDICES.items():
                source_xyz[name].append([float(row[index]) for index in indices])
            for name, index in MEVA_GCP_COLUMN_INDICES.items():
                source_gcp[name].append(float(row[index]))

    source_quaternions_array = np.asarray(source_quaternions, dtype=np.float64)
    xyz_arrays = {name: np.asarray(values, dtype=np.float64) for name, values in source_xyz.items()}
    gcp_arrays = {name: np.asarray(values, dtype=np.float64) for name, values in source_gcp.items()}
    selected_source_count = len(source_quaternions_array)
    if selected_source_count == 0:
        raise ValueError("MEVA source has no data rows")
    if not all(np.all(np.isfinite(values)) for values in [source_quaternions_array, *xyz_arrays.values(), *gcp_arrays.values()]):
        raise ValueError("MEVA target columns contain NaN/Inf")

    available_last = source_indices[-1]
    end = available_last if requested_stop is None else min(requested_stop - 1, available_last)
    frame, time_s, source_float, source_nearest = target_timeline(
        start_frame=start, end_frame=end, source_fps=source_fps, target_fps=target_fps
    )
    # A selected range normally has the following source sample available for
    # interpolation.  At the physical end of the source file it does not, so
    # discard only target samples that fall beyond the final recorded frame.
    in_recorded_range = source_float <= available_last + 1e-12
    frame = frame[in_recorded_range]
    time_s = time_s[in_recorded_range]
    source_float = source_float[in_recorded_range]
    source_nearest = source_nearest[in_recorded_range]
    source_time = np.asarray(source_indices, dtype=np.float64) / source_fps
    target_time_absolute = source_float / source_fps

    segment_quat = np.empty((len(frame), len(physical_segments), 4), dtype=np.float64)
    for segment_index, segment in enumerate(physical_segments):
        segment_quat[:, segment_index] = quaternion_slerp_resample(
            source_time,
            source_quaternions_array[:, segment_index, :],
            target_time_absolute,
        )

    xyz = {
        name: cubic_spline_resample(
            source_time,
            xyz_arrays[name],
            target_time_absolute,
        )
        for name, indices in MEVA_POSITION_COLUMN_INDICES.items()
    }
    gcp = {}
    for name, column_index in MEVA_GCP_COLUMN_INDICES.items():
        gcp[name] = np.clip(
            cubic_spline_resample(source_time, gcp_arrays[name], target_time_absolute),
            0.0,
            1.0,
        )

    offsets = cfg.get("foot_to_ground_offset", {})
    meva_offset = float(offsets.get("meva_m", 0.030))
    robot_offset = float(offsets.get(
        "robot_m",
        cfg.get("ground_contact_estimation", {}).get("robot_foot_ground_height_m", 0.035),
    ))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        schema_version=np.asarray(SCHEMA_VERSION),
        source_fps=np.asarray(source_fps, dtype=np.float64),
        target_fps=np.asarray(target_fps, dtype=np.float64),
        start_frame=np.asarray(start, dtype=np.int32),
        end_frame=np.asarray(end, dtype=np.int32),
        frame=frame,
        time_s=time_s,
        source_frame_float=source_float,
        source_frame_nearest=source_nearest,
        segment_names=np.asarray(physical_segments, dtype=np.str_),
        segment_quat=segment_quat,
        quaternion_order=np.asarray(quaternion_order),
        pelvis_xyz_m=xyz["Pelvis"],
        left_foot_xyz_m=xyz["LeftFoot"],
        right_foot_xyz_m=xyz["RightFoot"],
        pelvis_z_m=xyz["Pelvis"][:, 2],
        left_foot_z_m=xyz["LeftFoot"][:, 2],
        right_foot_z_m=xyz["RightFoot"][:, 2],
        gcp_left_ff=gcp["left_ff"],
        gcp_left_ca=gcp["left_ca"],
        gcp_right_ff=gcp["right_ff"],
        gcp_right_ca=gcp["right_ca"],
        meva_foot_to_ground_offset_m=np.asarray(meva_offset, dtype=np.float64),
        robot_foot_to_ground_offset_m=np.asarray(robot_offset, dtype=np.float64),
        source_file=np.asarray(str(source_cfg["file"])),
    )
    return output_path


def load_primary_target(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as archive:
        return {key: archive[key] for key in archive.files}
