#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend.json"
RECENT_WINDOW = 6


def is_healthy(value: object) -> bool:
    return value == "HEALTHY"


def classify(transitions: list[dict]) -> tuple[str, dict]:
    if not transitions:
        return "AWAITING_AUTOMATED_TRANSITION_HISTORY", {
            "reason": "no transition history is available yet",
            "evaluated_entries": 0,
        }

    recent = transitions[-RECENT_WINDOW:]
    latest = recent[-1]
    latest_result = latest.get("resulting_health")
    resulting = [item.get("resulting_health") for item in recent]
    changed = [item for item in recent if item.get("transition_state") == "CHANGED"]
    healthy_boundary_crossings = sum(
        1
        for item in recent
        if is_healthy(item.get("prior_health")) != is_healthy(item.get("resulting_health"))
    )

    latest_streak = 0
    for value in reversed(resulting):
        if value == latest_result:
            latest_streak += 1
        else:
            break

    evidence = {
        "evaluated_entries": len(recent),
        "recent_window_limit": RECENT_WINDOW,
        "latest_resulting_health": latest_result,
        "latest_resulting_health_streak": latest_streak,
        "changed_transition_count": len(changed),
        "healthy_boundary_crossings": healthy_boundary_crossings,
        "recent_resulting_health": resulting,
    }

    if healthy_boundary_crossings >= 3:
        evidence["reason"] = "three or more healthy/non-healthy boundary crossings occurred in the bounded recent window"
        return "UNSTABLE_OSCILLATION", evidence

    if latest_result == "HEALTHY":
        if latest.get("prior_health") != "HEALTHY" and latest.get("transition_state") == "CHANGED":
            evidence["reason"] = "the latest bounded transition changed from a non-healthy class to HEALTHY"
            return "RECOVERY_OBSERVED", evidence
        if latest_streak >= 2:
            evidence["reason"] = "HEALTHY is the resulting class for at least two consecutive bounded transitions"
            return "STABLE_HEALTHY", evidence
        evidence["reason"] = "the latest resulting class is HEALTHY without enough history for a stability claim"
        return "HEALTHY_OBSERVED", evidence

    if latest_result == "EXTERNAL_EVIDENCE_DEFERRED":
        evidence["reason"] = "the latest resulting class preserves unresolved external-evidence deferral"
        return "UNRESOLVED_DEFERRAL", evidence

    if latest_streak >= 2:
        evidence["reason"] = "the same non-healthy resulting class appears in at least two consecutive bounded transitions"
        return "REPEATED_FAIL_CLOSED", evidence

    if latest.get("transition_state") == "UNCHANGED":
        evidence["reason"] = "the latest non-healthy class was preserved without change"
        return "STABLE_FAIL_CLOSED", evidence

    evidence["reason"] = "bounded transition evidence is mixed and does not satisfy a stronger descriptive class"
    return "MIXED_BOUNDED_HISTORY", evidence


def response_for(trend: str) -> str:
    responses = {
        "AWAITING_AUTOMATED_TRANSITION_HISTORY": "allow the canonical workflow to create and reconcile the first transition receipt",
        "RECOVERY_OBSERVED": "continue repository-owned scheduled observation; make no prediction of persistence",
        "STABLE_HEALTHY": "continue repository-owned scheduled observation",
        "HEALTHY_OBSERVED": "continue observation until bounded evidence supports stability or another class",
        "UNRESOLVED_DEFERRAL": "preserve fail-closed deferral until declared external evidence conditions change",
        "REPEATED_FAIL_CLOSED": "remain fail-closed and re-evaluate on repository mutation or scheduled trigger",
        "STABLE_FAIL_CLOSED": "remain fail-closed and re-evaluate automatically",
        "UNSTABLE_OSCILLATION": "preserve fail-closed posture and continue bounded observation without predictive claims",
        "MIXED_BOUNDED_HISTORY": "continue repository-owned bounded observation",
    }
    return responses[trend]


def main() -> int:
    transitions: list[dict] = []
    history_binding: dict[str, object] = {
        "history_endpoint": "/status/canonical-workflow-health-transition-history.json",
        "history_available": False,
    }
    if HISTORY.exists():
        history = json.loads(HISTORY.read_text(encoding="utf-8"))
        transitions = list(history.get("transitions", []))
        history_binding.update({
            "history_available": True,
            "history_generated_at": history.get("generated_at"),
            "history_entry_count": len(transitions),
            "latest_transition_receipt_id": history.get("latest_transition", {}).get("receipt_id"),
        })

    trend_class, evidence = classify(transitions)
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_trend.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-transition-trend.json",
        "trend_class": trend_class,
        "evidence": evidence,
        "history_binding": history_binding,
        "automation_response": response_for(trend_class),
        "evaluation_scope": {
            "maximum_recent_entries": RECENT_WINDOW,
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
        },
        "manual_tasks_required": [],
        "user_action_required": False,
        "evaluation_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This trend summary is descriptive and bounded; it does not predict future workflow behavior.",
            "A recovery observation does not prove durable recovery.",
            "A stable classification does not grant release, deployment, execution, or downstream mutation authority.",
            "No trend class assigns a manual task to the user."
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW HEALTH TRANSITION TREND: PASS - "
        f"trend={trend_class} entries={evidence['evaluated_entries']} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
