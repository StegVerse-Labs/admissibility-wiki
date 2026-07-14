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
]
REQUIRED = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_trend_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_summary.py",
    ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_change.py",
    ROOT / "scripts" / "reconcile_canonical_workflow_trend_change_frequency_change_history.py",
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
    if data.get("state") != "AUTOMATED_TREND_CHANGE_FREQUENCY_CHANGE_HISTORY_BOUND":
        fail("state mismatch")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("no-manual boundary violated")
    for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
        if data.get(key) is not False:
            fail(f"{key} must be false")

    expected_endpoints = {
        "trend_change_frequency_endpoint": "/status/canonical-workflow-trend-change-frequency-summary.json",
        "trend_change_frequency_change_endpoint": "/status/canonical-workflow-trend-change-frequency-change-receipt.json",
        "trend_change_frequency_change_history_endpoint": "/status/canonical-workflow-trend-change-frequency-change-history.json",
    }
    for key, value in expected_endpoints.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    chain = data.get("publication_chain", [])
    for phrase in (
        "build-pages derives a bounded descriptive frequency and recency summary from trend-change history",
        "build-pages emits a frequency-class change receipt by comparing the current summary with the prior public summary",
        "build-pages reconciles the frequency-class change receipt into bounded deduplicated frequency-change history",
        "verify-public-pages checks observation, health, transition, trend, change-history, frequency-summary, frequency-change, and frequency-change-history endpoints",
    ):
        if phrase not in chain:
            fail(f"publication chain missing: {phrase}")

    history = data.get("trend_change_history_policy", {})
    if history.get("maximum_entries") != 24 or history.get("deduplication_key") != "receipt_id" or history.get("ordering") != "generated_at ascending":
        fail("trend-change history policy mismatch")

    frequency = data.get("trend_change_frequency_policy", {})
    if frequency.get("maximum_recent_entries") != 12:
        fail("frequency window must be 12")
    if frequency.get("descriptive_only") is not True:
        fail("frequency summary must be descriptive")
    if frequency.get("predictive_claim") is not False or frequency.get("causal_claim_beyond_receipt_fields") is not False:
        fail("frequency claim boundary mismatch")
    if frequency.get("owner") != "canonical build-pages job":
        fail("frequency owner mismatch")
    if frequency.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("frequency evaluation must remain automation-owned")

    change = data.get("trend_change_frequency_change_policy", {})
    if change.get("comparison") != "current generated frequency and recency classes against prior public summary":
        fail("frequency-change comparison mismatch")
    if set(change.get("states", [])) != {"CHANGED", "UNCHANGED"}:
        fail("frequency-change states mismatch")
    if set(change.get("changed_fields", [])) != {"frequency_class", "recency_class"}:
        fail("frequency-change fields mismatch")
    if change.get("descriptive_only") is not True:
        fail("frequency-change must remain descriptive")
    if change.get("predictive_claim") is not False or change.get("causal_claim_beyond_receipt_fields") is not False:
        fail("frequency-change claim boundary mismatch")
    if "without assigning a manual task" not in change.get("prior_summary_unavailable_result", ""):
        fail("frequency-change unavailable policy must remain no-manual")
    if change.get("owner") != "canonical build-pages job":
        fail("frequency-change owner mismatch")
    if change.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("frequency-change evaluation must remain automation-owned")

    change_history = data.get("trend_change_frequency_change_history_policy", {})
    if change_history.get("maximum_entries") != 24:
        fail("frequency-change history maximum_entries must be 24")
    if change_history.get("deduplication_key") != "receipt_id":
        fail("frequency-change history deduplication key mismatch")
    if change_history.get("ordering") != "generated_at ascending":
        fail("frequency-change history ordering mismatch")
    if change_history.get("descriptive_only") is not True:
        fail("frequency-change history must remain descriptive")
    if change_history.get("predictive_claim") is not False:
        fail("frequency-change history predictive_claim must be false")
    if change_history.get("causal_claim_beyond_receipt_fields") is not False:
        fail("frequency-change history causal claim boundary mismatch")
    if change_history.get("owner") != "canonical build-pages job":
        fail("frequency-change history owner mismatch")
    if "without assigning a manual task" not in change_history.get("prior_history_unavailable_result", ""):
        fail("frequency-change history unavailable policy must remain no-manual")
    if change_history.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
        fail("frequency-change history reconciliation must remain automation-owned")

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
        "manual_tasks=0 frequency_change_history=bounded_nonpredictive"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
