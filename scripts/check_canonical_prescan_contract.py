#!/usr/bin/env python3
"""Validate the single-workflow canonical pre-scan diagnostic contract."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
RUNNER = ROOT / "scripts" / "run_canonical_prescan.py"
TEST = ROOT / "tests" / "test_canonical_prescan.py"

REQUIRED_WORKFLOW_FRAGMENTS = [
    "- name: Run canonical pre-scan",
    "id: canonical-prescan",
    "continue-on-error: true",
    "run: python scripts/run_canonical_prescan.py",
    "- name: Upload canonical pre-scan report",
    "name: canonical-prescan-report",
    "path: reports/canonical-prescan-report.json",
    "- name: Scan complete validation chain",
    "if: always()",
    "prescan_path = Path('reports/canonical-prescan-report.json')",
    "if prescan['overall_status'] != 'PASS' or report['overall_status'] != 'PASS':",
]

REQUIRED_RUNNER_FRAGMENTS = [
    'REPORT = ROOT / "reports" / "canonical-prescan-report.json"',
    '"schema": "admissibility_wiki.canonical_prescan_report.v1"',
    '"overall_status": "FAIL" if failed else "PASS"',
    'return 1 if failed else 0',
]

REQUIRED_TEST_FRAGMENTS = [
    "def test_failure_does_not_stop_later_commands",
    "self.assertEqual(run_mock.call_count, 3)",
    'self.assertEqual(report["overall_status"], "FAIL")',
    "def test_success_returns_zero",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_fragments(label: str, text: str, fragments: list[str]) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        formatted = "\n".join(f"- {fragment}" for fragment in missing)
        raise AssertionError(f"{label} is missing required contract fragments:\n{formatted}")


def main() -> int:
    try:
        workflow = require_file(WORKFLOW)
        runner = require_file(RUNNER)
        test = require_file(TEST)
        require_fragments("canonical workflow", workflow, REQUIRED_WORKFLOW_FRAGMENTS)
        require_fragments("canonical pre-scan runner", runner, REQUIRED_RUNNER_FRAGMENTS)
        require_fragments("canonical pre-scan regression test", test, REQUIRED_TEST_FRAGMENTS)

        workflow_files = list((ROOT / ".github" / "workflows").glob("*.yml")) + list(
            (ROOT / ".github" / "workflows").glob("*.yaml")
        )
        active = [path for path in workflow_files if path.name != "README.md"]
        if len(active) != 1 or active[0].name != "validate-chain-continuation.yml":
            names = ", ".join(sorted(path.name for path in active)) or "none"
            raise AssertionError(f"single canonical workflow contract violated: {names}")
    except AssertionError as exc:
        print(f"CANONICAL PRE-SCAN CONTRACT: FAIL\n{exc}")
        return 1

    print("CANONICAL PRE-SCAN CONTRACT: PASS")
    print("Diagnostic continuation is bound to the single canonical workflow; final enforcement remains fail-closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
