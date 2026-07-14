#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-observation-history.json"
SUMMARY = ROOT / "static" / "status" / "canonical-workflow-health-summary.json"
AUTOMATION = ROOT / "static" / "status" / "canonical-workflow-observation-automation.json"


def classify(observation: dict) -> str:
    state = observation.get("observation_state")
    job = observation.get("job_status_observed")
    full = observation.get("full_validation_status")
    reconstruction = observation.get("reconstruction_status")
    supersession = observation.get("reconstruction_evaluation_result")

    if state == "PASS_OBSERVED":
        return "HEALTHY"
    if job == "cancelled":
        return "TRANSIENT_CANCELLATION"
    if full == "FAIL":
        return "VALIDATION_FAILURE"
    if reconstruction == "FAIL":
        return "RECONSTRUCTION_FAILURE"
    if supersession == "DEFER_NO_SUPERSESSION":
        return "EXTERNAL_EVIDENCE_DEFERRED"
    if state == "INCOMPLETE_OBSERVATION":
        return "INCOMPLETE_OBSERVATION"
    return "FAIL_CLOSED_OTHER"


def main() -> int:
    if not AUTOMATION.exists():
        raise SystemExit("workflow observation automation contract is missing")

    observations: list[dict] = []
    history_state = "NOT_YET_PUBLISHED"
    if HISTORY.exists():
        payload = json.loads(HISTORY.read_text(encoding="utf-8"))
        observations = list(payload.get("observations", []))
        history_state = "AVAILABLE"

    classified = [
        {
            "receipt_id": item.get("receipt_id"),
            "created_at": item.get("created_at"),
            "commit": item.get("commit"),
            "run_id": item.get("run_id"),
            "observation_state": item.get("observation_state"),
            "health_class": classify(item),
        }
        for item in observations
    ]
    latest = classified[-1] if classified else None
    counts: dict[str, int] = {}
    for item in classified:
        health_class = str(item["health_class"])
        counts[health_class] = counts.get(health_class, 0) + 1

    current_health = latest["health_class"] if latest else "AWAITING_AUTOMATED_OBSERVATION"
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_health_summary.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-summary.json",
        "history_state": history_state,
        "current_health": current_health,
        "latest_observation": latest,
        "health_class_counts": counts,
        "classification_order": [
            "HEALTHY",
            "TRANSIENT_CANCELLATION",
            "VALIDATION_FAILURE",
            "RECONSTRUCTION_FAILURE",
            "EXTERNAL_EVIDENCE_DEFERRED",
            "INCOMPLETE_OBSERVATION",
            "FAIL_CLOSED_OTHER",
            "AWAITING_AUTOMATED_OBSERVATION"
        ],
        "automation_response": {
            "HEALTHY": "continue scheduled observation",
            "TRANSIENT_CANCELLATION": "re-evaluate on next repository-owned trigger",
            "VALIDATION_FAILURE": "remain fail-closed and re-evaluate after repository mutation or scheduled trigger",
            "RECONSTRUCTION_FAILURE": "remain fail-closed and regenerate on next repository-owned trigger",
            "EXTERNAL_EVIDENCE_DEFERRED": "preserve DEFER_NO_SUPERSESSION until declared evidence conditions change",
            "INCOMPLETE_OBSERVATION": "re-evaluate on next repository-owned trigger",
            "FAIL_CLOSED_OTHER": "remain fail-closed and re-evaluate automatically",
            "AWAITING_AUTOMATED_OBSERVATION": "allow canonical workflow to create the first observation"
        },
        "manual_tasks_required": [],
        "user_action_required": False,
        "remediation_owner": "canonical workflow and declared source/review owners",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This summary classifies workflow evidence; it does not grant authority.",
            "A failure classification does not create a manual remediation task for the user.",
            "External-evidence deferral is not source rejection or acceptance."
        ]
    }

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"CANONICAL WORKFLOW HEALTH SUMMARY: PASS - health={current_health} manual_tasks=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
