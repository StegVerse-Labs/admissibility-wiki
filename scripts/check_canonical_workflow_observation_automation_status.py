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
HEALTH_VALIDATOR = ROOT / "scripts" / "check_canonical_workflow_health_summary.py"
TRANSITION_VALIDATOR = ROOT / "scripts" / "check_canonical_workflow_health_transition_receipt.py"
TRANSITION_HISTORY_VALIDATOR = ROOT / "scripts" / "check_canonical_workflow_health_transition_history.py"
REQUIRED_FILES = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "write_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "publish_canonical_workflow_observation_receipt.py",
    PUBLICATION_VALIDATOR,
    ROOT / "scripts" / "reconcile_canonical_workflow_observation_history.py",
    HISTORY_VALIDATOR,
    ROOT / "scripts" / "generate_canonical_workflow_health_summary.py",
    HEALTH_VALIDATOR,
    TRANSITION_VALIDATOR,
    ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_history.py",
    TRANSITION_HISTORY_VALIDATOR,
    ROOT / "scripts" / "check_full_validation_chain.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION AUTOMATION: FAIL - {message}")


def run_validator(path: Path, label: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(path)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        fail(f"{label} failed")


def main() -> int:
    if not STATUS.exists(): fail("public status artifact is missing")
    for path in REQUIRED_FILES:
        if not path.exists(): fail(f"required automation file is missing: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("state") != "AUTOMATED_HEALTH_TRANSITION_HISTORY_BOUND":
        fail("state must be AUTOMATED_HEALTH_TRANSITION_HISTORY_BOUND")
    for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
        if data.get(key) is not False: fail(f"{key} must be false")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("no-manual boundary violated")

    expected_endpoints = {
        "automation_contract_endpoint": "/status/canonical-workflow-observation-automation.json",
        "run_bound_receipt_endpoint": "/status/canonical-workflow-observation-receipt.json",
        "history_endpoint": "/status/canonical-workflow-observation-history.json",
        "health_summary_endpoint": "/status/canonical-workflow-health-summary.json",
        "health_transition_endpoint": "/status/canonical-workflow-health-transition-receipt.json",
        "health_transition_history_endpoint": "/status/canonical-workflow-health-transition-history.json",
    }
    for key, value in expected_endpoints.items():
        if data.get(key) != value: fail(f"{key} mismatch")

    chain = data.get("publication_chain", [])
    for phrase in (
        "build-pages reconciles the current receipt with the prior public bounded history",
        "build-pages classifies the reconciled history into a compact workflow health summary",
        "build-pages emits a health-transition receipt from consecutive classified observations",
        "build-pages reconciles the transition receipt into bounded deduplicated transition history",
        "verify-public-pages checks observation, health, transition receipt, and transition-history endpoints",
    ):
        if phrase not in chain: fail(f"publication chain missing: {phrase}")

    history_policy = data.get("history_policy", {})
    if history_policy.get("maximum_entries") != 24 or history_policy.get("deduplication_key") != "receipt_id" or history_policy.get("ordering") != "created_at ascending":
        fail("observation history policy mismatch")

    transition_history = data.get("health_transition_history_policy", {})
    if transition_history.get("maximum_entries") != 24: fail("transition history maximum_entries must be 24")
    if transition_history.get("deduplication_key") != "receipt_id": fail("transition history deduplication key mismatch")
    if transition_history.get("ordering") != "generated_at ascending": fail("transition history ordering mismatch")
    if transition_history.get("owner") != "canonical build-pages job": fail("transition history owner mismatch")
    if "without assigning a manual task" not in transition_history.get("prior_history_unavailable_result", ""):
        fail("transition history unavailable policy must remain no-manual")
    if transition_history.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
        fail("transition history reconciliation must remain automation-owned")

    for trigger in ("push", "pull_request", "workflow_dispatch", "hourly_schedule"):
        if data.get("trigger_ownership", {}).get(trigger) != "repository automation":
            fail(f"trigger {trigger} is not automation-owned")
    if "next repository-owned trigger" not in data.get("cancelled_run_policy", ""):
        fail("cancelled-run policy must assign automatic re-evaluation")
    if "do not become user tasks" not in data.get("external_evidence_policy", ""):
        fail("external-evidence policy must prohibit user task assignment")

    run_validator(PUBLICATION_VALIDATOR, "run-bound publication validator")
    run_validator(HISTORY_VALIDATOR, "observation history validator")
    run_validator(HEALTH_VALIDATOR, "workflow health validator")
    run_validator(TRANSITION_VALIDATOR, "workflow health transition validator")
    run_validator(TRANSITION_HISTORY_VALIDATOR, "workflow health transition history validator")

    print("CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - manual_tasks=0 transition_history=bounded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
