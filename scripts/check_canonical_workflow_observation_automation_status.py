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
    if data.get("state") != "AUTOMATED_FREQUENCY_CHANGE_STABILITY_CHANGE_HISTORY_BOUND":
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
    }
    for key, value in expected_endpoints.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    chain = data.get("publication_chain", [])
    for phrase in (
        "build-pages derives a bounded descriptive frequency and recency summary from trend-change history",
        "build-pages emits a frequency-class change receipt by comparing the current summary with the prior public summary",
        "build-pages reconciles the frequency-class change receipt into bounded deduplicated frequency-change history",
        "build-pages derives a bounded descriptive stability summary from frequency-change history",
        "build-pages emits a stability-class change receipt by comparing the current stability summary with the prior public summary",
        "build-pages reconciles the stability-class change receipt into bounded deduplicated stability-change history",
        "verify-public-pages checks observation, health, transition, trend, frequency, frequency-change-history, stability-summary, stability-change, and stability-change-history endpoints",
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
    if stability.get("owner") != "canonical build-pages job":
        fail("stability owner mismatch")
    if stability.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("stability evaluation must remain automation-owned")

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
    if stability_change.get("owner") != "canonical build-pages job":
        fail("stability-change owner mismatch")
    if stability_change.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("stability-change evaluation must remain automation-owned")

    stability_history = data.get("frequency_change_stability_change_history_policy", {})
    if stability_history.get("maximum_entries") != 24:
        fail("stability-change history maximum_entries must be 24")
    if stability_history.get("deduplication_key") != "receipt_id":
        fail("stability-change history deduplication key mismatch")
    if stability_history.get("ordering") != "generated_at ascending":
        fail("stability-change history ordering mismatch")
    if stability_history.get("descriptive_only") is not True:
        fail("stability-change history must remain descriptive")
    if stability_history.get("predictive_claim") is not False:
        fail("stability-change history predictive_claim must be false")
    if stability_history.get("causal_claim_beyond_receipt_fields") is not False:
        fail("stability-change history causal claim boundary mismatch")
    if stability_history.get("owner") != "canonical build-pages job":
        fail("stability-change history owner mismatch")
    if "without assigning a manual task" not in stability_history.get("prior_history_unavailable_result", ""):
        fail("stability-change history unavailable policy must remain no-manual")
    if stability_history.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
        fail("stability-change history reconciliation must remain automation-owned")

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
        "manual_tasks=0 stability_change_history=bounded_nonpredictive"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
