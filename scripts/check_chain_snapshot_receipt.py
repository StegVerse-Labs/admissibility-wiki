#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json"

REQUIRED_FILE_FIELDS = [
    "snapshot",
    "continuation_manifest",
    "continuation_schema",
    "automation_state",
    "goal_state",
    "canonical_workflow",
    "workflow_mirror",
    "workflow_manifest",
    "blocked_destination_manifest",
]

REQUIRED_VALIDATORS = [
    "scripts/check_chain_status_continuation.py",
    "scripts/check_continuation_bundle.py",
    "scripts/check_chain_snapshot.py",
    "scripts/check_chain_snapshot_receipt.py",
    "scripts/check_chain_auto.py",
    "scripts/check_blocked_destination_record.py",
    "scripts/check_goal_state.py",
    "scripts/check_workflow_manifest.py",
    "scripts/check_external_frameworks_index.py",
    "scripts/check_guardian_destination.py",
]

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
    "destination_state": "GUARDIAN DESTINATION: BLOCKED",
}

TRUE_BOUNDARIES = [
    "canonical_workflow_installed",
    "scheduled_check_installed",
    "no_activation_claim",
    "no_closure_claim",
    "no_adoption_claim",
    "no_endorsement_claim",
    "no_external_framework_validation_claim",
    "no_consequence_binding_standing_claim",
]

FALSE_BOUNDARIES = [
    "snapshot_is_release_tag",
    "snapshot_is_activation_evidence",
    "workflow_mirror_is_ci_activation",
    "manual_workflow_install_required",
    "manual_destination_search_required",
    "queued_external_framework_testbench_is_active",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not RECEIPT.exists():
        print("CHAIN SNAPSHOT RECEIPT: FAIL")
        print("- missing receipt")
        return 1

    receipt = load_json(RECEIPT)

    if receipt.get("artifact_type") != "chain_snapshot_receipt":
        failures.append("artifact type mismatch")
    if receipt.get("schema_version") != "0.6":
        failures.append("schema version mismatch")
    if receipt.get("status") != "BLOCKED_ON_DESTINATION_REPOSITORY":
        failures.append("status mismatch")

    for key in REQUIRED_FILE_FIELDS:
        value = receipt.get(key)
        if not isinstance(value, str):
            failures.append(f"missing file reference: {key}")
        elif not (ROOT / value).exists():
            failures.append(f"referenced file missing: {value}")

    validators = receipt.get("validators", [])
    for validator in REQUIRED_VALIDATORS:
        if validator not in validators:
            failures.append(f"missing validator: {validator}")
        elif not (ROOT / validator).exists():
            failures.append(f"validator file missing: {validator}")

    commands = receipt.get("validation_commands", [])
    for command in REQUIRED_COMMANDS:
        if command not in commands:
            failures.append(f"missing validation command: {command}")

    expected = receipt.get("expected_validation_results", {})
    for key, value in EXPECTED_RESULTS.items():
        if expected.get(key) != value:
            failures.append(f"expected result mismatch: {key}")

    if receipt.get("generated_report") != "reports/guardian_destination_status.json":
        failures.append("generated report mismatch")

    boundary = receipt.get("boundary", {})
    for key in TRUE_BOUNDARIES:
        if boundary.get(key) is not True:
            failures.append(f"true boundary mismatch: {key}")
    for key in FALSE_BOUNDARIES:
        if boundary.get(key) is not False:
            failures.append(f"false boundary mismatch: {key}")

    print("CHAIN SNAPSHOT RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
