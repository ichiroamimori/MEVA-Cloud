"""Launch the existing install/setup viewer in its own native process."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from server.robot_registry import RobotVariant


def launch_robot_viewer(record: RobotVariant, motion: Path) -> int:
    resolved_motion = motion.resolve()
    if not resolved_motion.is_file():
        raise FileNotFoundError(f"Viewer motion not found: {resolved_motion}")
    command = [
        sys.executable, "-m", "server.retarget.tools.view_robot",
        str(resolved_motion),
        "--manufacturer", record.manufacturer_id,
        "--robot", record.robot_id,
        "--variant", record.variant_id,
        "--maximized",
    ]
    # A file avoids filling a pipe during a long interactive session.
    output = tempfile.TemporaryFile()
    try:
        process = subprocess.Popen(
            command, cwd=str(record.repository_root_path),
            stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        try:
            code = process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            def reap() -> None:
                try:
                    process.wait()
                finally:
                    output.close()

            threading.Thread(target=reap, daemon=True).start()
            return process.pid
        output.seek(0)
        detail = output.read().decode("utf-8", errors="replace")[-4000:]
        raise RuntimeError(f"Robot Viewer exited during startup ({code}): {detail}")
    except Exception:
        output.close()
        raise
