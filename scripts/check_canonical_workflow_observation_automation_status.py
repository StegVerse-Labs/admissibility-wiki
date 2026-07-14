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
]
REQUIRED = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_trend_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_summary.py",
    ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_change.py",
    ROOT / "scripts" / "reconcile_canonical_workflow_trend_change_frequency_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_frequency_change_stability_summary.py",
    ROOT / "scripts" / "generate_canonical_workflow_frequency_change_stability_change.py",
    ROOT / "scripts" / "reconcile_canonical_workflow_frequency_change_stability_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_summary.py",
    ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_change.py",
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
    if data.get("state") != "AUTOMATED_STABILITY_CHANGE_FREQUENCY_CHANGE_BOUND":
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
        "frequency_change_stability_endpoint": "/status/canonical-workflow-frequency-change-stability-summary.json",
        "frequency_change_stability_change_endpoint": "/status/canonical-workflow-frequency-change-stability-change-receipt.json",
        "frequency_change_stability_change_history_endpoint": "/status/canonical-workflow-frequency-change-stability-change-history.json",
        "stability_change_frequency_endpoint": "/status/canonical-workflow-stability-change-frequency-summary.json",
        "stability_change_frequency_change_endpoint": "/status/canonical-workflow-stability-change-frequency-change-receipt.json",
    }
    for key, value in expected_endpoints.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    chain = data.get("publication_chain", [])
    for phrase in (
        "build-pages derives a bounded descriptive stability summary from frequency-change history",
        "build-pages emits a stability-class change receipt by comparing the current stability summary with the prior public summary",
        "build-pages reconciles the stability-class change receipt into bounded deduplicated stability-change history",
        "build-pages derives a bounded descriptive frequency and recency summary from stability-change history",
        "build-pages emits a stability-change frequency-class receipt by comparing current frequency and recency classes with prior public values",
        "verify-public-pages checks observation, health, transition, trend, frequency, stability, bounded-history, stability-change-frequency, and stability-change-frequency-change endpoints",
    ):
        if phrase not in chain:
            fail(f"publication chain missing: {phrase}")

    stability = data.get("frequency_change_stability_policy", {})
    if stability.get("maximum_recent_entries") != 12:
        fail("stability window must be 12")
    if stability.get("descriptive_only") is not True:
        fail("stability summary must remain descriptive")
    if stability.get("predictive_claim") is not False or stability.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability claim boundary mismatch")
    required_stability_classes = {
        "AWAITING_AUTOMATED_FREQUENCY_CHANGE_HISTORY",
        "NO_CLASS_CHANGE_OBSERVED",
        "ISOLATED_CLASS_CHANGE_OBSERVED",
        "REPEATED_CLASS_CHANGE_OBSERVED",
        "MIXED_FREQUENCY_RECENCY_MOVEMENT",
    }
    if set(stability.get("classes", [])) != required_stability_classes:
        fail("stability classes mismatch")

    stability_change = data.get("frequency_change_stability_change_policy", {})
    if stability_change.get("comparison") != "current generated stability class against prior public stability summary":
        fail("stability-change comparison mismatch")
    if set(stability_change.get("states", [])) != {"CHANGED", "UNCHANGED"}:
        fail("stability-change states mismatch")
    if stability_change.get("descriptive_only") is not True:
        fail("stability-change must remain descriptive")
    if stability_change.get("predictive_claim") is not False or stability_change.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability-change claim boundary mismatch")
    if "without assigning a manual task" not in stability_change.get("prior_summary_unavailable_result", ""):
        fail("stability-change unavailable policy must remain no-manual")

    stability_history = data.get("frequency_change_stability_change_history_policy", {})
    if stability_history.get("maximum_entries") != 24:
        fail("stability-change history maximum_entries must be 24")
    if stability_history.get("deduplication_key") != "receipt_id":
        fail("stability-change history deduplication key mismatch")
    if stability_history.get("ordering") != "generated_at ascending":
        fail("stability-change history ordering mismatch")
    if stability_history.get("descriptive_only") is not True:
        fail("stability-change history must remain descriptive")
    if stability_history.get("predictive_claim") is not False or stability_history.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability-change history claim boundary mismatch")
    if "without assigning a manual task" not in stability_history.get("prior_history_unavailable_result", ""):
        fail("stability-change history unavailable policy must remain no-manual")

    frequency = data.get("stability_change_frequency_policy", {})
    if frequency.get("maximum_recent_entries") != 12:
        fail("stability-change frequency window must be 12")
    if frequency.get("descriptive_only") is not True:
        fail("stability-change frequency must remain descriptive")
    if frequency.get("predictive_claim") is not False or frequency.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability-change frequency claim boundary mismatch")
    required_frequency_classes = {
        "AWAITING_AUTOMATED_STABILITY_CHANGE_HISTORY",
        "NO_STABILITY_CHANGE_OBSERVED",
        "ISOLATED_STABILITY_CHANGE_OBSERVED",
        "OCCASIONAL_STABILITY_CHANGE_OBSERVED",
        "FREQUENT_STABILITY_CHANGE_OBSERVED",
    }
    required_recency_classes = {
        "AWAITING_AUTOMATED_STABILITY_CHANGE_HISTORY",
        "CURRENT_RECEIPT_CHANGED",
        "RECENT_STABILITY_CHANGE",
        "OLDER_STABILITY_CHANGE_IN_WINDOW",
        "CHANGE_NOT_IN_WINDOW",
    }
    if set(frequency.get("frequency_classes", [])) != required_frequency_classes:
        fail("stability-change frequency classes mismatch")
    if set(frequency.get("recency_classes", [])) != required_recency_classes:
        fail("stability-change recency classes mismatch")
    if frequency.get("owner") != "canonical build-pages job":
        fail("stability-change frequency owner mismatch")
    if frequency.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("stability-change frequency evaluation must remain automation-owned")

    frequency_change = data.get("stability_change_frequency_change_policy", {})
    if frequency_change.get("comparison") != "current generated stability-change frequency and recency classes against prior public summary":
        fail("stability-change frequency comparison mismatch")
    if set(frequency_change.get("states", [])) != {"CHANGED", "UNCHANGED"}:
        fail("stability-change frequency states mismatch")
    if set(frequency_change.get("changed_fields", [])) != {"frequency_class", "recency_class"}:
        fail("stability-change frequency changed_fields mismatch")
    if frequency_change.get("descriptive_only") is not True:
        fail("stability-change frequency comparison must remain descriptive")
    if frequency_change.get("predictive_claim") is not False or frequency_change.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability-change frequency comparison claim boundary mismatch")
    if "without assigning a manual task" not in frequency_change.get("prior_summary_unavailable_result", ""):
        fail("stability-change frequency comparison unavailable policy must remain no-manual")
    if frequency_change.get("owner") != "canonical build-pages job":
        fail("stability-change frequency comparison owner mismatch")
    if frequency_change.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("stability-change frequency comparison evaluation must remain automation-owned")

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
        "manual_tasks=0 stability_change_frequency_change=bounded_nonpredictive"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
