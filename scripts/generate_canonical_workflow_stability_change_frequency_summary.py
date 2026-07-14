#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-summary.json"
WINDOW = 12


def main() -> int:
    changes: list[dict] = []
    history_state = "NOT_YET_PUBLISHED"
    if HISTORY.exists():
        payload = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = list(payload.get("changes", []))
        history_state = "AVAILABLE"

    recent = changes[-WINDOW:]
    total = len(recent)
    changed_count = sum(1 for item in recent if item.get("change_state") == "CHANGED")
    unchanged_count = sum(1 for item in recent if item.get("change_state") == "UNCHANGED")
    ratio = changed_count / total if total else None
    latest = recent[-1] if recent else None
    runs_since_change = next(
        (index for index, item in enumerate(reversed(recent)) if item.get("change_state") == "CHANGED"),
        None,
    )

    if not recent:
        frequency_class = "AWAITING_AUTOMATED_STABILITY_CHANGE_HISTORY"
    elif changed_count == 0:
        frequency_class = "NO_STABILITY_CHANGE_OBSERVED"
    elif changed_count == 1:
        frequency_class = "ISOLATED_STABILITY_CHANGE_OBSERVED"
    elif ratio is not None and ratio >= 0.5:
        frequency_class = "FREQUENT_STABILITY_CHANGE_OBSERVED"
    else:
        frequency_class = "OCCASIONAL_STABILITY_CHANGE_OBSERVED"

    recency_class = (
        "AWAITING_AUTOMATED_STABILITY_CHANGE_HISTORY"
        if not recent
        else "CURRENT_RECEIPT_CHANGED"
        if latest and latest.get("change_state") == "CHANGED"
        else "CHANGE_NOT_IN_WINDOW"
        if runs_since_change is None
        else "RECENT_STABILITY_CHANGE"
        if runs_since_change <= 2
        else "OLDER_STABILITY_CHANGE_IN_WINDOW"
    )

    payload = {
        "schema": "admissibility_wiki.canonical_workflow_stability_change_frequency_summary.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-stability-change-frequency-summary.json",
        "history_state": history_state,
        "frequency_class": frequency_class,
        "recency_class": recency_class,
        "evidence": {
            "maximum_recent_entries": WINDOW,
            "evaluated_entries": total,
            "changed_count": changed_count,
            "unchanged_count": unchanged_count,
            "observed_change_ratio": ratio,
            "runs_since_last_changed_receipt": runs_since_change,
            "latest_change_receipt_id": (latest or {}).get("receipt_id"),
            "latest_change_state": (latest or {}).get("change_state"),
            "latest_resulting_stability_class": (latest or {}).get("resulting_stability_class"),
        },
        "evaluation_scope": {
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
            "frequency_denominator": "bounded retained stability-change receipts",
        },
        "automation_response": "continue repository-owned bounded observation and regenerate on the next canonical trigger",
        "manual_tasks_required": [],
        "user_action_required": False,
        "evaluation_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "Observed stability-change frequency and recency do not predict future behavior.",
            "The summary does not establish causes beyond fields preserved in receipts.",
            "No class grants release, deployment, execution, or downstream mutation authority.",
            "No class assigns a manual task to the user.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY: PASS - "
        f"frequency={frequency_class} recency={recency_class} entries={total} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
