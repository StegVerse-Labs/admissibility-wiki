#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-summary.json"
WINDOW = 12


def main() -> int:
    changes: list[dict] = []
    history_state = "NOT_YET_PUBLISHED"
    if HISTORY.exists():
        history = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = list(history.get("changes", []))
        history_state = "AVAILABLE"

    recent = changes[-WINDOW:]
    changed_count = sum(1 for item in recent if item.get("change_state") == "CHANGED")
    unchanged_count = sum(1 for item in recent if item.get("change_state") == "UNCHANGED")
    total = len(recent)
    observed_frequency = (changed_count / total) if total else None
    latest = recent[-1] if recent else None
    last_changed_index = next(
        (index for index, item in enumerate(reversed(recent)) if item.get("change_state") == "CHANGED"),
        None,
    )
    runs_since_change = last_changed_index if last_changed_index is not None else None

    if not recent:
        frequency_class = "AWAITING_AUTOMATED_TREND_CHANGE_HISTORY"
    elif changed_count == 0:
        frequency_class = "NO_CHANGE_OBSERVED"
    elif changed_count == 1:
        frequency_class = "ISOLATED_CHANGE_OBSERVED"
    elif observed_frequency is not None and observed_frequency >= 0.5:
        frequency_class = "FREQUENT_CHANGE_OBSERVED"
    else:
        frequency_class = "OCCASIONAL_CHANGE_OBSERVED"

    recency_class = (
        "AWAITING_AUTOMATED_TREND_CHANGE_HISTORY"
        if not recent
        else "CURRENT_RECEIPT_CHANGED"
        if latest and latest.get("change_state") == "CHANGED"
        else "CHANGE_NOT_IN_WINDOW"
        if runs_since_change is None
        else "RECENT_CHANGE"
        if runs_since_change <= 2
        else "OLDER_CHANGE_IN_WINDOW"
    )

    payload = {
        "schema": "admissibility_wiki.canonical_workflow_trend_change_frequency_summary.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-trend-change-frequency-summary.json",
        "history_state": history_state,
        "frequency_class": frequency_class,
        "recency_class": recency_class,
        "evidence": {
            "maximum_recent_entries": WINDOW,
            "evaluated_entries": total,
            "changed_count": changed_count,
            "unchanged_count": unchanged_count,
            "observed_change_ratio": observed_frequency,
            "runs_since_last_changed_receipt": runs_since_change,
            "latest_change_receipt_id": (latest or {}).get("receipt_id"),
            "latest_change_state": (latest or {}).get("change_state"),
        },
        "evaluation_scope": {
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
            "frequency_denominator": "bounded retained trend-change receipts",
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
            "Observed frequency and recency do not predict future changes.",
            "The summary does not identify causes beyond fields already preserved in receipts.",
            "A low change frequency does not grant release, deployment, execution, or mutation authority.",
            "No frequency or recency class assigns a manual task to the user."
        ]
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW TREND CHANGE FREQUENCY: PASS - "
        f"frequency={frequency_class} recency={recency_class} entries={total} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
