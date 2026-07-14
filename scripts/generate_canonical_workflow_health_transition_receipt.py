#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-observation-history.json"
HEALTH = ROOT / "static" / "status" / "canonical-workflow-health-summary.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-health-transition-receipt.json"


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


def cause_for(current: dict, previous: dict | None) -> dict:
    if previous is None:
        return {
            "cause_class": "INITIAL_AUTOMATED_OBSERVATION",
            "cause_field": "history_length",
            "prior_value": 0,
            "resulting_value": 1,
        }

    comparisons = [
        ("job_status_observed", previous.get("job_status_observed"), current.get("job_status_observed")),
        ("full_validation_status", previous.get("full_validation_status"), current.get("full_validation_status")),
        ("reconstruction_status", previous.get("reconstruction_status"), current.get("reconstruction_status")),
        (
            "reconstruction_evaluation_result",
            previous.get("reconstruction_evaluation_result"),
            current.get("reconstruction_evaluation_result"),
        ),
        ("observation_state", previous.get("observation_state"), current.get("observation_state")),
    ]
    changed = [
        {"field": field, "prior": prior, "resulting": resulting}
        for field, prior, resulting in comparisons
        if prior != resulting
    ]
    if not changed:
        return {
            "cause_class": "NO_HEALTH_RELEVANT_CHANGE",
            "cause_field": None,
            "prior_value": None,
            "resulting_value": None,
            "changed_fields": [],
        }

    primary = changed[0]
    return {
        "cause_class": "OBSERVED_EVIDENCE_CHANGE",
        "cause_field": primary["field"],
        "prior_value": primary["prior"],
        "resulting_value": primary["resulting"],
        "changed_fields": changed,
    }


def consequence_for(resulting_health: str) -> str:
    consequences = {
        "HEALTHY": "continue scheduled observation without granting authority",
        "TRANSIENT_CANCELLATION": "remain fail-closed until the next repository-owned trigger",
        "VALIDATION_FAILURE": "block promotion and re-evaluate after repository mutation or scheduled trigger",
        "RECONSTRUCTION_FAILURE": "block promotion and regenerate on the next repository-owned trigger",
        "EXTERNAL_EVIDENCE_DEFERRED": "preserve DEFER_NO_SUPERSESSION until declared evidence conditions change",
        "INCOMPLETE_OBSERVATION": "make no pass claim and re-evaluate on the next repository-owned trigger",
        "FAIL_CLOSED_OTHER": "remain fail-closed and re-evaluate automatically",
        "AWAITING_AUTOMATED_OBSERVATION": "await the first repository-owned observation",
    }
    return consequences[resulting_health]


def compact(observation: dict | None) -> dict | None:
    if observation is None:
        return None
    return {
        "receipt_id": observation.get("receipt_id"),
        "created_at": observation.get("created_at"),
        "commit": observation.get("commit"),
        "run_id": observation.get("run_id"),
        "job_status_observed": observation.get("job_status_observed"),
        "full_validation_status": observation.get("full_validation_status"),
        "reconstruction_status": observation.get("reconstruction_status"),
        "reconstruction_evaluation_result": observation.get("reconstruction_evaluation_result"),
        "observation_state": observation.get("observation_state"),
    }


def main() -> int:
    if not HEALTH.exists():
        raise SystemExit("workflow health summary is missing")

    health = json.loads(HEALTH.read_text(encoding="utf-8"))
    observations: list[dict] = []
    if HISTORY.exists():
        history = json.loads(HISTORY.read_text(encoding="utf-8"))
        observations = list(history.get("observations", []))

    current = observations[-1] if observations else None
    previous = observations[-2] if len(observations) >= 2 else None
    prior_health = classify(previous) if previous is not None else "AWAITING_AUTOMATED_OBSERVATION"
    resulting_health = classify(current) if current is not None else "AWAITING_AUTOMATED_OBSERVATION"
    cause = cause_for(current or {}, previous) if current is not None else {
        "cause_class": "NO_OBSERVATION_AVAILABLE",
        "cause_field": None,
        "prior_value": None,
        "resulting_value": None,
    }

    transition_changed = prior_health != resulting_health
    receipt = {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_receipt.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-transition-receipt.json",
        "transition_id": f"workflow-health-transition.{(current or {}).get('receipt_id', 'awaiting')}",
        "transition_changed": transition_changed,
        "prior_health": prior_health,
        "resulting_health": resulting_health,
        "cause": cause,
        "prior_observation": compact(previous),
        "resulting_observation": compact(current),
        "fail_closed_consequence": consequence_for(resulting_health),
        "health_summary_binding": {
            "summary_endpoint": health.get("public_endpoint"),
            "summary_current_health": health.get("current_health"),
            "matches_resulting_health": health.get("current_health") == resulting_health,
        },
        "continuation": {
            "owner": "canonical workflow and declared source/review owners",
            "next_event": "next repository-owned canonical workflow trigger or declared evidence-state change",
            "manual_tasks_required": [],
            "user_action_required": False,
        },
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This receipt explains one bounded workflow-health transition only.",
            "A changed health class does not grant mutation, release, deployment, or execution authority.",
            "A deferred external-evidence class is not acceptance or rejection of the external source.",
            "No health transition assigns a manual task to the user."
        ],
    }

    if receipt["health_summary_binding"]["matches_resulting_health"] is not True:
        raise SystemExit("health transition does not match the generated health summary")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW HEALTH TRANSITION: PASS - "
        f"{prior_health}->{resulting_health} changed={str(transition_changed).lower()} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
