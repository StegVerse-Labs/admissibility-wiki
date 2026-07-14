#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-observation-history.json"
SUMMARY = ROOT / "static" / "status" / "canonical-workflow-health-summary.json"
TRANSITION = ROOT / "static" / "status" / "canonical-workflow-health-transition-receipt.json"
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


def cause_for(observation: dict | None, health_class: str) -> dict:
    observation = observation or {}
    return {
        "health_class": health_class,
        "observation_state": observation.get("observation_state"),
        "job_status_observed": observation.get("job_status_observed"),
        "full_validation_status": observation.get("full_validation_status"),
        "reconstruction_status": observation.get("reconstruction_status"),
        "reconstruction_evaluation_result": observation.get("reconstruction_evaluation_result"),
        "receipt_id": observation.get("receipt_id"),
    }


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
    generated_at = datetime.now(timezone.utc).isoformat()
    response = {
        "HEALTHY": "continue scheduled observation",
        "TRANSIENT_CANCELLATION": "re-evaluate on next repository-owned trigger",
        "VALIDATION_FAILURE": "remain fail-closed and re-evaluate after repository mutation or scheduled trigger",
        "RECONSTRUCTION_FAILURE": "remain fail-closed and regenerate on next repository-owned trigger",
        "EXTERNAL_EVIDENCE_DEFERRED": "preserve DEFER_NO_SUPERSESSION until declared evidence conditions change",
        "INCOMPLETE_OBSERVATION": "re-evaluate on next repository-owned trigger",
        "FAIL_CLOSED_OTHER": "remain fail-closed and re-evaluate automatically",
        "AWAITING_AUTOMATED_OBSERVATION": "allow canonical workflow to create the first observation",
    }
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_health_summary.v0.1",
        "generated_at": generated_at,
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-summary.json",
        "history_state": history_state,
        "current_health": current_health,
        "latest_observation": latest,
        "health_class_counts": counts,
        "classification_order": list(response),
        "automation_response": response,
        "manual_tasks_required": [],
        "user_action_required": False,
        "remediation_owner": "canonical workflow and declared source/review owners",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This summary classifies workflow evidence; it does not grant authority.",
            "A failure classification does not create a manual remediation task for the user.",
            "External-evidence deferral is not source rejection or acceptance.",
        ],
    }

    previous_observation = observations[-2] if len(observations) >= 2 else None
    current_observation = observations[-1] if observations else None
    previous_health = classify(previous_observation) if previous_observation else "AWAITING_AUTOMATED_OBSERVATION"
    transition_state = "CHANGED" if previous_health != current_health else "UNCHANGED"
    transition = {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_receipt.v0.1",
        "receipt_id": f"workflow-health-transition.{(current_observation or {}).get('receipt_id') or 'awaiting'}",
        "generated_at": generated_at,
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-transition-receipt.json",
        "transition_state": transition_state,
        "prior_health": previous_health,
        "resulting_health": current_health,
        "prior_cause": cause_for(previous_observation, previous_health),
        "resulting_cause": cause_for(current_observation, current_health),
        "fail_closed_consequence": response[current_health],
        "manual_tasks_required": [],
        "user_action_required": False,
        "transition_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This receipt explains an observed health-class transition; it does not grant authority.",
            "An unchanged class is still recorded to preserve continuity.",
            "The receipt does not convert external-evidence deferral into acceptance or rejection.",
        ],
    }

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    TRANSITION.write_text(json.dumps(transition, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW HEALTH SUMMARY: PASS - "
        f"health={current_health} transition={transition_state} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
