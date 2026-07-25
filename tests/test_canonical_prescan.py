#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "run_canonical_prescan.py"
SPEC = importlib.util.spec_from_file_location("run_canonical_prescan", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Completed:
    def __init__(self, returncode: int, stdout: str) -> None:
        self.returncode = returncode
        self.stdout = stdout


class CanonicalPrescanTests(unittest.TestCase):
    def test_failure_does_not_stop_later_commands(self) -> None:
        commands = [
            ("first", ["python", "first.py"]),
            ("second", ["python", "second.py"]),
            ("third", ["python", "third.py"]),
        ]
        completions = [
            Completed(1, "first failed"),
            Completed(0, "second passed"),
            Completed(0, "third passed"),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "canonical-prescan-report.json"
            with (
                mock.patch.object(MODULE, "COMMANDS", commands),
                mock.patch.object(MODULE, "REPORT", report_path),
                mock.patch.object(MODULE.subprocess, "run", side_effect=completions) as run_mock,
                mock.patch.dict(MODULE.os.environ, {}, clear=True),
            ):
                result = MODULE.main()

            self.assertEqual(result, 1)
            self.assertEqual(run_mock.call_count, 3)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["overall_status"], "FAIL")
            self.assertEqual(report["total_commands"], 3)
            self.assertEqual(report["passed_commands"], 2)
            self.assertEqual(report["failed_commands"], 1)
            self.assertEqual([item["status"] for item in report["results"]], ["FAIL", "PASS", "PASS"])
            self.assertFalse(report.get("authority", {}).get("deployment_authorized", False))

    def test_success_returns_zero(self) -> None:
        commands = [("only", ["python", "only.py"])]
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "canonical-prescan-report.json"
            with (
                mock.patch.object(MODULE, "COMMANDS", commands),
                mock.patch.object(MODULE, "REPORT", report_path),
                mock.patch.object(MODULE.subprocess, "run", return_value=Completed(0, "ok")),
                mock.patch.dict(MODULE.os.environ, {}, clear=True),
            ):
                result = MODULE.main()

            self.assertEqual(result, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["overall_status"], "PASS")
            self.assertEqual(report["failed_commands"], 0)


if __name__ == "__main__":
    unittest.main()
