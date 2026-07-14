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
]
REQUIRED = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_trend_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_summary.py",
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
    if data.get("state") != "AUTOMATED_TREND_CHANGE_FREQUENCY_BOUND":
        fail("state mismatch")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("no-manual boundary violated")
    for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
        if data.get(key) is not False:
            fail(f"{key} must be false")

    if data.get("trend_change_frequency_endpoint") != "/status/canonical-workflow-trend-change-frequency-summary.json":
        fail("frequency endpoint mismatch")
    chain = data.get("publication_chain", [])
    if "build-pages derives a bounded descriptive frequency and recency summary from trend-change history" not in chain:
        fail("frequency generation missing from publication chain")
    if "verify-public-pages checks observation, health, transition, trend, change-history, and frequency-summary endpoints" not in chain:
        fail("frequency endpoint verification missing from publication chain")

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

    print("CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - manual_tasks=0 frequency=bounded_nonpredictive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
