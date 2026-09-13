from __future__ import annotations

import sys
import threading
import time
import unittest
from pathlib import Path

from server.managed_process import (
    ManagedProcessCancelled,
    ManagedProcessTimeout,
    run_managed_process,
)


class ManagedProcessTests(unittest.TestCase):
    def test_cancellation_stops_a_silent_process(self) -> None:
        cancel = threading.Event()
        timer = threading.Timer(0.2, cancel.set)
        timer.start()
        started = time.monotonic()
        try:
            with self.assertRaises(ManagedProcessCancelled):
                run_managed_process(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    cwd=Path.cwd(), cancel_event=cancel, timeout_sec=10,
                )
        finally:
            timer.cancel()
        self.assertLess(time.monotonic() - started, 8)

    def test_timeout_stops_a_silent_process(self) -> None:
        started = time.monotonic()
        with self.assertRaises(ManagedProcessTimeout):
            run_managed_process(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                cwd=Path.cwd(), timeout_sec=0.2,
            )
        self.assertLess(time.monotonic() - started, 8)

    def test_output_is_streamed(self) -> None:
        lines: list[str] = []
        returncode, logs = run_managed_process(
            [sys.executable, "-c", "print('ready', flush=True)"],
            cwd=Path.cwd(), timeout_sec=5, line_callback=lines.append,
        )
        self.assertEqual(0, returncode)
        self.assertEqual(["ready"], logs)
        self.assertEqual(logs, lines)


if __name__ == "__main__":
    unittest.main()
