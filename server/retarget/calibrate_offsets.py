# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

import mujoco
import mink
import numpy as np


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_repo_root(config_path: Path) -> Path:
    for p in [config_path.parent, *config_path.parents]:
        if (p / "server").exists() and (p / "workspace").exists():
            return p
    raise FileNotFoundError(
        "Repository root was not found. "
        "Expected a parent containing both 'server' and 'workspace'."
    )


def resolve_repo_path(repo_root: Path, value: str) -> Path:
    p = Path(value)
    if p.is_absolute():
        return p
    return (repo_root / p).resolve()


def normalize_quat_wxyz(q) -> np.ndarray:
    q = np.asarray(q, dtype=np.float64).reshape(4)
    n = float(np.linalg.norm(q))
    if not np.isfinite(n) or n <= 1e-12:
        raise ValueError(f"Invalid quaternion: {q}")
    return q / n


def quat_mul_wxyz(a, b) -> np.ndarray:
    out = np.empty(4, dtype=np.float64)
    mujoco.mju_mulQuat(
        out,
        normalize_quat_wxyz(a),
        normalize_quat_wxyz(b),
    )
    return normalize_quat_wxyz(out)


def quat_inv_wxyz(q) -> np.ndarray:
    q = normalize_quat_wxyz(q)
    return np.array([q[0], -q[1], -q[2], -q[3]], dtype=np.float64)


def read_meva_reference_row(
    csv_path: Path,
    header_row_1based: int,
    reference_frame: int,
) -> tuple[list[str], dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        for _ in range(header_row_1based - 1):
            next(f, None)

        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV header was not found.")

        for i, row in enumerate(reader):
            if i == reference_frame:
                return list(reader.fieldnames), row

    raise IndexError(
        f"Reference frame {reference_frame} is outside the CSV data range."
    )


def segment_quat(
    row: dict[str, str],
    pattern: str,
    segment: str,
) -> np.ndarray:
    keys = [
        pattern.format(segment=segment, component=c)
        for c in "wxyz"
    ]
    try:
        values = [float(row[k]) for k in keys]
    except KeyError as exc:
        raise KeyError(
            f"Missing MEVA quaternion column for {segment}: {exc}\n"
            f"Expected: {keys}"
        ) from exc

    return normalize_quat_wxyz(values)


def body_exists(model: mujoco.MjModel, name: str) -> bool:
    return (
        mujoco.mj_name2id(
            model,
            mujoco.mjtObj.mjOBJ_BODY,
            name,
        )
        >= 0
    )


def main(config_path: Path) -> None:
    config_path = config_path.resolve()
    cfg = load_json(config_path)
    repo_root = find_repo_root(config_path)

    csv_path = resolve_repo_path(repo_root, cfg["source"]["file"])
    xml_path = resolve_repo_path(repo_root, cfg["robot"]["mjcf"])

    if not csv_path.exists():
        raise FileNotFoundError(f"MEVA CSV not found: {csv_path}")
    if not xml_path.exists():
        raise FileNotFoundError(f"Robot MJCF not found: {xml_path}")

    reference_frame = int(cfg["frame_range"].get("start", 0))

    print("Config          :", config_path)
    print("MEVA CSV        :", csv_path)
    print("Robot MJCF      :", xml_path)
    print("Reference frame :", reference_frame)
    print()

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    configuration = mink.Configuration(model)

    keyframe_name = cfg["robot"].get("initial_keyframe")
    if keyframe_name:
        try:
            configuration.update_from_keyframe(keyframe_name)
        except Exception:
            print(
                f"WARNING: keyframe '{keyframe_name}' was not found. "
                "Using model default qpos."
            )
            configuration.update()
    else:
        configuration.update()

    _, reference_row = read_meva_reference_row(
        csv_path=csv_path,
        header_row_1based=int(cfg["source"]["header_row_1based"]),
        reference_frame=reference_frame,
    )

    pattern = cfg["source"]["quaternion_columns"]

    world_offset = normalize_quat_wxyz(
        cfg.get("world_alignment", {}).get(
            "offset_quaternion_wxyz",
            [1.0, 0.0, 0.0, 0.0],
        )
    )

    # primary_retarget.py currently uses:
    #
    #   q_target = q_world_offset * (q_meva * q_mapping_offset)
    #
    # Therefore, to make the reference frame exactly equal to the
    # robot's initial link orientation:
    #
    #   q_mapping_offset =
    #       inv(q_meva) * inv(q_world_offset) * q_robot_initial
    #
    # This script writes that right-side mapping offset into config.json.
    for mapping in cfg["mappings"]:
        source_segment = mapping["source_segment"]
        target_link = mapping["target_link"]

        if not body_exists(model, target_link):
            raise KeyError(
                f"Robot body/link not found in MJCF: {target_link}"
            )

        q_meva = segment_quat(
            row=reference_row,
            pattern=pattern,
            segment=source_segment,
        )

        robot_tf = configuration.get_transform_frame_to_world(
            target_link,
            "body",
        )
        q_robot = normalize_quat_wxyz(
            robot_tf.rotation().wxyz
        )

        q_mapping_offset = quat_mul_wxyz(
            quat_inv_wxyz(q_meva),
            quat_mul_wxyz(
                quat_inv_wxyz(world_offset),
                q_robot,
            ),
        )

        mapping["offset_quaternion_wxyz"] = [
            float(x) for x in q_mapping_offset
        ]

        print(
            f"{source_segment:16s} -> {target_link:28s} "
            f"{mapping['offset_quaternion_wxyz']}"
        )

    cfg["offset_calibration"] = {
        "method": "reference_frame_to_robot_initial_pose",
        "reference_frame": reference_frame,
        "calibrated_at": datetime.now().isoformat(timespec="seconds"),
        "note": (
            "Offsets are calibrated for primary_retarget.py convention: "
            "q_target = world_offset * (q_meva * mapping_offset)."
        ),
    }

    backup_path = config_path.with_name(
        "config.before_offset_calibration.json"
    )

    if not backup_path.exists():
        shutil.copy2(config_path, backup_path)
        print()
        print("Backup created  :", backup_path)
    else:
        print()
        print("Backup exists   :", backup_path)

    save_json(config_path, cfg)

    print("Config updated  :", config_path)
    print()
    print("Done. Re-run primary_retarget.py with this config.json.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Calibrate MEVA segment -> robot link orientation offsets "
            "and write them into config.json."
        )
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to retarget config.json",
    )
    args = parser.parse_args()
    main(args.config)
