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
    "python scripts/check_blocked_destination_record.py",
    "python scripts/check_goal_state.py",
    "python scripts/check_workflow_manifest.py",
    "python scripts/check_external_frameworks_index.py",
    "python scripts/check_external_framework_manifests.py",
    "python scripts/check_external_framework_reports.py",
    "python scripts/check_guardian_destination.py",
]

EXPECTED_RESULTS = {
    "chain_continuation": "CHAIN CONTINUATION: PASS",
    "continuation_bundle": "CONTINUATION BUNDLE: PASS",
    "chain_snapshot": "CHAIN SNAPSHOT: PASS",
    "chain_snapshot_receipt": "CHAIN SNAPSHOT RECEIPT: PASS",
    "chain_auto": "CHAIN AUTO: PASS",
    "blocked_destination_record": "BLOCKED DESTINATION RECORD: PASS",
    "goal_state": "GOAL STATE: PASS",
    "workflow_manifest": "WORKFLOW MANIFEST: PASS",
    "external_frameworks_index": "EXTERNAL FRAMEWORKS INDEX: PASS",
    "external_framework_manifests": "EXTERNAL FRAMEWORK MANIFESTS: PASS",
    "external_framework_reports": "EXTERNAL FRAMEWORK REPORTS: PASS",
    "destination_state": "GUARDIAN DESTINATION: BLOCKED",
}

REQUIRED_REPORTS = [
    "reports/guardian_destination_status.json",
    "docs/external-frameworks/reports/admissible-existence-seed-cycle.compatibility.json",
    "docs/external-frameworks/reports/care-runtime.compatibility.json",
]


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
    if manifest.get("schema_version") != "0.8":
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
    for report in REQUIRED_REPORTS:
        if report not in reports:
            failures.append(f"missing generated report path: {report}")
        elif not (ROOT / report).exists() and report != "reports/guardian_destination_status.json":
            failures.append(f"generated report file missing: {report}")

    boundary = manifest.get("boundary", {})
    for key in [
        "canonical_workflow_installed",
        "scheduled_check_installed",
        "manual_workflow_install_required",
        "manual_destination_search_required",
        "external_framework_outputs_are_authority",
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
    if boundary.get("external_framework_outputs_are_authority") is not False:
        failures.append("external framework authority boundary mismatch")

    print("WORKFLOW MANIFEST:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
