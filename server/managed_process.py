from __future__ import annotations

import os
import queue
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Sequence


class ManagedProcessCancelled(RuntimeError):
    pass


class ManagedProcessTimeout(RuntimeError):
    pass


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    """Best-effort termination of the fixed IK subprocess and its children."""
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_managed_process(
    command: Sequence[str],
    *,
    cwd: Path,
    cancel_event: threading.Event | None = None,
    timeout_sec: float | None = None,
    line_callback: Callable[[str], None] | None = None,
    log_limit: int = 1000,
) -> tuple[int, list[str]]:
    creationflags = (
        subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    )
    process = subprocess.Popen(
        list(command),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        creationflags=creationflags,
        start_new_session=os.name != "nt",
    )
    assert process.stdout is not None

    output: queue.Queue[str | None] = queue.Queue()

    def read_output() -> None:
        try:
            for raw_line in process.stdout:
                output.put(raw_line)
        finally:
            output.put(None)

    reader = threading.Thread(
        target=read_output,
        daemon=True,
        name=f"ik-output-{process.pid}",
    )
    reader.start()
    started = time.monotonic()
    logs: list[str] = []
    stream_finished = False
    try:
        while not stream_finished or process.poll() is None:
            if cancel_event is not None and cancel_event.is_set():
                terminate_process_tree(process)
                raise ManagedProcessCancelled("IK execution was cancelled")
            if timeout_sec is not None and time.monotonic() - started >= timeout_sec:
                terminate_process_tree(process)
                raise ManagedProcessTimeout(
                    f"IK execution exceeded {timeout_sec:g} seconds"
                )
            try:
                raw_line = output.get(timeout=0.2)
            except queue.Empty:
                continue
            if raw_line is None:
                stream_finished = True
                continue
            line = raw_line.rstrip()
            if line:
                logs.append(line)
                if len(logs) > log_limit:
                    logs = logs[-log_limit:]
                if line_callback is not None:
                    line_callback(line)
        return process.wait(), logs
    finally:
        if process.poll() is None:
            terminate_process_tree(process)
        process.stdout.close()
        reader.join(timeout=1)
