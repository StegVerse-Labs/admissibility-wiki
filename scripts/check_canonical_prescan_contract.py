#!/usr/bin/env python3
"""Validate the single-workflow canonical pre-scan diagnostic contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
RUNNER = ROOT / "scripts" / "run_canonical_prescan.py"
TEST = ROOT / "tests" / "test_canonical_prescan.py"
RECEIPT = ROOT / "receipts" / "canonical-prescan-diagnostic-repair-2026-07-25.json"

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


def require_receipt() -> None:
    text = require_file(RECEIPT)
    try:
        receipt = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"repair receipt is not valid JSON: {exc}") from exc

    expected = {
        "schema": "admissibility_wiki.canonical_prescan_diagnostic_repair_receipt.v1",
        "issue": 38,
        "state": "IMPLEMENTED_PENDING_RUN_BOUND_ARTIFACT_OBSERVATION",
        "canonical_workflow": ".github/workflows/validate-chain-continuation.yml",
        "runner": "scripts/run_canonical_prescan.py",
        "contract_validator": "scripts/check_canonical_prescan_contract.py",
        "regression_test": "tests/test_canonical_prescan.py",
        "full_chain_validator": "scripts/check_full_validation_chain.py",
        "manual_task_required": False,
        "user_manual_action_required": False,
    }
    mismatches = [
        f"{key}: expected {value!r}, found {receipt.get(key)!r}"
        for key, value in expected.items()
        if receipt.get(key) != value
    ]
    enforcement = receipt.get("enforcement")
    if not isinstance(enforcement, dict) or not all(enforcement.get(key) is True for key in (
        "prescan_continues_after_individual_failure",
        "full_scan_runs_after_prescan_failure",
        "final_result_fails_when_prescan_fails",
        "final_result_fails_when_full_scan_fails",
        "single_active_workflow_required",
    )):
        mismatches.append("enforcement contract is incomplete or not fail-closed")
    if mismatches:
        raise AssertionError("repair receipt contract mismatch:\n" + "\n".join(f"- {item}" for item in mismatches))


def main() -> int:
    try:
        workflow = require_file(WORKFLOW)
        runner = require_file(RUNNER)
        test = require_file(TEST)
        require_fragments("canonical workflow", workflow, REQUIRED_WORKFLOW_FRAGMENTS)
        require_fragments("canonical pre-scan runner", runner, REQUIRED_RUNNER_FRAGMENTS)
        require_fragments("canonical pre-scan regression test", test, REQUIRED_TEST_FRAGMENTS)
        require_receipt()

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
    print("Diagnostic continuation and its durable repair receipt remain bound to the single canonical workflow; final enforcement remains fail-closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
