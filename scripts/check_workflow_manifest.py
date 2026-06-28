#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "workflow_manifest.json"

REQUIRED_COMMANDS = [
    "python scripts/check_chain_status_continuation.py",
    "python scripts/check_continuation_bundle.py",
    "python scripts/check_chain_snapshot.py",
    "python scripts/check_chain_snapshot_receipt.py",
    "python scripts/check_chain_auto.py",
    "python scripts/check_workflow_manifest.py",
    "python scripts/check_guardian_destination.py",
]

EXPECTED_RESULTS = {
    "chain_continuation": "CHAIN CONTINUATION: PASS",
    "continuation_bundle": "CONTINUATION BUNDLE: PASS",
    "chain_snapshot": "CHAIN SNAPSHOT: PASS",
    "chain_snapshot_receipt": "CHAIN SNAPSHOT RECEIPT: PASS",
    "chain_auto": "CHAIN AUTO: PASS",
    "workflow_manifest": "WORKFLOW MANIFEST: PASS",
    "destination_state": "GUARDIAN DESTINATION: BLOCKED",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not MANIFEST.exists():
        print("WORKFLOW MANIFEST: FAIL")
        print("- missing workflow_manifest.json")
        return 1

    manifest = load_json(MANIFEST)

    if manifest.get("manifest_id") != "ADMISSIBILITY-WIKI-WORKFLOW-001":
        failures.append("manifest id mismatch")
    if manifest.get("schema_version") != "0.5":
        failures.append("schema version mismatch")

    workflows = manifest.get("canonical_workflows", [])
    if not workflows:
        failures.append("missing canonical workflow record")
    else:
        workflow = workflows[0]
        if workflow.get("path") != ".github/workflows/validate-chain-continuation.yml":
            failures.append("canonical workflow path mismatch")
        if workflow.get("installed") is not True:
            failures.append("canonical workflow not marked installed")
        if workflow.get("scheduled") is not True:
            failures.append("canonical workflow not marked scheduled")
        if workflow.get("cron") != "17 9 * * *":
            failures.append("cron mismatch")
        path = workflow.get("path")
        if isinstance(path, str) and not (ROOT / path).exists():
            failures.append("canonical workflow file missing")

    commands = manifest.get("verification_commands", [])
    for command in REQUIRED_COMMANDS:
        if command not in commands:
            failures.append(f"missing command: {command}")

    expected = manifest.get("expected_results", {})
    for key, value in EXPECTED_RESULTS.items():
        if expected.get(key) != value:
            failures.append(f"expected result mismatch: {key}")

    reports = manifest.get("generated_reports", [])
    if "reports/guardian_destination_status.json" not in reports:
        failures.append("missing generated report path")

    boundary = manifest.get("boundary", {})
    for key in [
        "canonical_workflow_installed",
        "scheduled_check_installed",
        "manual_workflow_install_required",
        "manual_destination_search_required",
    ]:
        if key not in boundary:
            failures.append(f"missing boundary key: {key}")
    if boundary.get("canonical_workflow_installed") is not True:
        failures.append("canonical workflow boundary mismatch")
    if boundary.get("scheduled_check_installed") is not True:
        failures.append("scheduled check boundary mismatch")
    if boundary.get("manual_workflow_install_required") is not False:
        failures.append("manual workflow boundary mismatch")
    if boundary.get("manual_destination_search_required") is not False:
        failures.append("manual search boundary mismatch")

    print("WORKFLOW MANIFEST:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
