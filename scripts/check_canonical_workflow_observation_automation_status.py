#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "canonical-workflow-observation-automation.json"
PUBLICATION_VALIDATOR = ROOT / "scripts" / "check_canonical_workflow_observation_publication.py"
HISTORY_VALIDATOR = ROOT / "scripts" / "check_canonical_workflow_observation_history.py"
REQUIRED_FILES = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "write_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "publish_canonical_workflow_observation_receipt.py",
    PUBLICATION_VALIDATOR,
    ROOT / "scripts" / "reconcile_canonical_workflow_observation_history.py",
    HISTORY_VALIDATOR,
    ROOT / "scripts" / "check_full_validation_chain.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION AUTOMATION: FAIL - {message}")


def run_validator(path: Path, label: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        fail(f"{label} failed")


def main() -> int:
    if not STATUS.exists():
        fail("public status artifact is missing")
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"required automation file is missing: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("state") != "AUTOMATED_PUBLICATION_AND_HISTORY_BOUND":
        fail("state must be AUTOMATED_PUBLICATION_AND_HISTORY_BOUND")
    if data.get("manual_tasks_required") != []:
        fail("manual_tasks_required must be empty")
    if data.get("user_action_required") is not False:
        fail("user_action_required must be false")
    if data.get("authority_granted") is not False:
        fail("authority_granted must be false")
    if data.get("release_authority_granted") is not False:
        fail("release_authority_granted must be false")
    if data.get("downstream_mutation_authority_granted") is not False:
        fail("downstream_mutation_authority_granted must be false")

    expected_endpoints = {
        "automation_contract_endpoint": "/status/canonical-workflow-observation-automation.json",
        "run_bound_receipt_endpoint": "/status/canonical-workflow-observation-receipt.json",
        "history_endpoint": "/status/canonical-workflow-observation-history.json",
    }
    for key, value in expected_endpoints.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    chain = data.get("publication_chain", [])
    required_phrases = [
        "full-validation-chain-report artifact transfers it to build-pages",
        "build-pages publishes the embedded receipt into static/status",
        "build-pages reconciles the current receipt with the prior public bounded history",
        "verify-public-pages checks the automation, run-bound receipt, and history endpoints",
    ]
    for phrase in required_phrases:
        if phrase not in chain:
            fail(f"publication chain missing: {phrase}")

    history_policy = data.get("history_policy", {})
    if history_policy.get("maximum_entries") != 24:
        fail("history maximum_entries must be 24")
    if history_policy.get("deduplication_key") != "receipt_id":
        fail("history deduplication_key must be receipt_id")
    if history_policy.get("ordering") != "created_at ascending":
        fail("history ordering must be created_at ascending")
    if "without assigning a manual task" not in history_policy.get("prior_history_unavailable_result", ""):
        fail("prior-history-unavailable policy must remain no-manual")
    if history_policy.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
        fail("history reconciliation must remain automation-owned")

    states = set(data.get("observation_states", []))
    required_states = {"PASS_OBSERVED", "FAIL_CLOSED_OBSERVED", "INCOMPLETE_OBSERVATION"}
    if states != required_states:
        fail("observation states do not match the governed set")

    triggers = data.get("trigger_ownership", {})
    for trigger in ("push", "pull_request", "workflow_dispatch", "hourly_schedule"):
        if triggers.get(trigger) != "repository automation":
            fail(f"trigger {trigger} is not automation-owned")

    if "next repository-owned trigger" not in data.get("cancelled_run_policy", ""):
        fail("cancelled-run policy must assign automatic re-evaluation")
    if "do not become user tasks" not in data.get("external_evidence_policy", ""):
        fail("external-evidence policy must prohibit user task assignment")

    non_claims = data.get("non_claims", [])
    if not any("does not grant" in claim for claim in non_claims):
        fail("authority non-claim is missing")

    run_validator(PUBLICATION_VALIDATOR, "run-bound publication validator")
    run_validator(HISTORY_VALIDATOR, "observation history validator")

    print(
        "CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - "
        "manual_tasks=0 user_action=false publication=bound history=reconciled"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
