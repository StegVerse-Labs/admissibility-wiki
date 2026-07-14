#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "canonical-workflow-observation-automation.json"
VALIDATORS = [
    ROOT / "scripts" / "check_canonical_workflow_observation_publication.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_history.py",
    ROOT / "scripts" / "check_canonical_workflow_health_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_receipt.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_history.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend_change.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_change.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_change.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_change.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_change_history.py",
]
REQUIRED = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_summary.py",
    ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_change.py",
    ROOT / "scripts" / "reconcile_canonical_workflow_stability_change_frequency_change_history.py",
    ROOT / "scripts" / "check_full_validation_chain.py",
] + VALIDATORS


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION AUTOMATION: FAIL - {message}")


def main() -> int:
    if not STATUS.exists():
        fail("status artifact missing")
    for path in REQUIRED:
        if not path.exists():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("state") != "AUTOMATED_STABILITY_CHANGE_FREQUENCY_CHANGE_HISTORY_BOUND":
        fail("state mismatch")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("no-manual boundary violated")
    for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
        if data.get(key) is not False:
            fail(f"{key} must be false")

    expected = {
        "stability_change_frequency_endpoint": "/status/canonical-workflow-stability-change-frequency-summary.json",
        "stability_change_frequency_change_endpoint": "/status/canonical-workflow-stability-change-frequency-change-receipt.json",
        "stability_change_frequency_change_history_endpoint": "/status/canonical-workflow-stability-change-frequency-change-history.json",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    frequency = data.get("stability_change_frequency_policy", {})
    if frequency.get("maximum_recent_entries") != 12:
        fail("frequency window must be 12")
    if frequency.get("descriptive_only") is not True or frequency.get("predictive_claim") is not False:
        fail("frequency claim boundary mismatch")
    if frequency.get("causal_claim_beyond_receipt_fields") is not False:
        fail("frequency causal claim boundary mismatch")

    change = data.get("stability_change_frequency_change_policy", {})
    if set(change.get("states", [])) != {"CHANGED", "UNCHANGED"}:
        fail("comparison states mismatch")
    if set(change.get("changed_fields", [])) != {"frequency_class", "recency_class"}:
        fail("comparison changed_fields mismatch")
    if change.get("descriptive_only") is not True or change.get("predictive_claim") is not False:
        fail("comparison claim boundary mismatch")
    if change.get("causal_claim_beyond_receipt_fields") is not False:
        fail("comparison causal claim boundary mismatch")
    if "without assigning a manual task" not in change.get("prior_summary_unavailable_result", ""):
        fail("comparison unavailable policy must remain no-manual")

    history = data.get("stability_change_frequency_change_history_policy", {})
    if history.get("maximum_entries") != 24:
        fail("history maximum_entries must be 24")
    if history.get("deduplication_key") != "receipt_id":
        fail("history deduplication key mismatch")
    if history.get("ordering") != "generated_at ascending":
        fail("history ordering mismatch")
    if history.get("descriptive_only") is not True or history.get("predictive_claim") is not False:
        fail("history claim boundary mismatch")
    if history.get("causal_claim_beyond_receipt_fields") is not False:
        fail("history causal claim boundary mismatch")
    if "without assigning a manual task" not in history.get("prior_history_unavailable_result", ""):
        fail("history unavailable policy must remain no-manual")
    if history.get("owner") != "canonical build-pages job":
        fail("history owner mismatch")
    if history.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
        fail("history reconciliation must remain automation-owned")

    for trigger in ("push", "pull_request", "workflow_dispatch", "hourly_schedule"):
        if data.get("trigger_ownership", {}).get(trigger) != "repository automation":
            fail(f"trigger {trigger} is not automation-owned")

    for validator in VALIDATORS:
        completed = subprocess.run(
            [sys.executable, str(validator)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.returncode != 0:
            fail(f"validator failed: {validator.name}")

    print(
        "CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - "
        "manual_tasks=0 stability_change_frequency_change_history=bounded_nonpredictive"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
