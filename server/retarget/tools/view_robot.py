"""Command-line entry point for the standalone MuJoCo Robot Viewer."""
from __future__ import annotations

import argparse
from pathlib import Path

from server.robot_registry import load_registry, repository_root
from server.retarget.robot_motion_viewer import (
    RobotViewerModel,
    load_viewer_motion,
    run_native_viewer,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Open a registered Robot in MuJoCo. Without a motion file the "
            "registered initial pose is shown; with a trusted PKL/NPZ the "
            "motion is played."
        )
    )
    parser.add_argument(
        "motion",
        nargs="?",
        type=Path,
        help="Trusted GMR-compatible .pkl or canonical MEVA Cloud .npz",
    )
    parser.add_argument("--variant", help="Registered global Variant ID")
    parser.add_argument("--manufacturer", help="Optional manufacturer ID")
    parser.add_argument("--robot", help="Optional robot ID")
    parser.add_argument(
        "--root-rot-order",
        choices=("xyzw", "wxyz"),
        help="Override motion quaternion order (GMR-compatible PKL default: xyzw)",
    )
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--no-loop", action="store_true")
    parser.add_argument("--start-paused", action="store_true")
    parser.add_argument(
        "--axes",
        choices=("off", "selected", "all"),
        default="off",
        help=(
            "Initial axis display; selecting a Link switches to selected "
            "and No select switches to off (default: off)"
        ),
    )
    parser.add_argument("--axis-length", type=float, metavar="METERS")
    parser.add_argument(
        "--show-link-list",
        "--show-labels",
        dest="show_link_list",
        action="store_true",
        help="Show the keyboard-selectable Link list in the 3D view",
    )
    parser.add_argument(
        "--list-robots",
        action="store_true",
        help="List enabled registered Robot Variants and exit",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    repo = repository_root()
    if args.list_robots:
        records = [record for record in load_registry(repo) if record.enabled]
        for record in records:
            print(
                f"{record.variant_id:20}  {record.manufacturer_name} / "
                f"{record.robot_name} / {record.variant['name']}"
            )
        return
    if not args.variant:
        parser.error("--variant is required unless --list-robots is used")
    if args.motion is not None and args.motion.suffix.lower() == ".pkl":
        print(
            "SECURITY: PKL can execute code while loading. Open only a file "
            "from a trusted source."
        )
    try:
        robot = RobotViewerModel.from_variant(
            args.variant,
            manufacturer_id=args.manufacturer,
            robot_id=args.robot,
            root=repo,
        )
        motion = (
            load_viewer_motion(
                args.motion,
                root_rot_order=args.root_rot_order,
            )
            if args.motion is not None
            else None
        )
        run_native_viewer(
            robot,
            motion,
            speed=args.speed,
            loop=not args.no_loop,
            axes=args.axes,
            axis_length_m=args.axis_length,
            show_labels=args.show_link_list,
            start_paused=args.start_paused,
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
