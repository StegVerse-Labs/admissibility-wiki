#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-summary.json"
CHANGE_GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_frequency_change_stability_change.py"
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
    changed = [item for item in recent if item.get("change_state") == "CHANGED"]
    changed_count = len(changed)
    unchanged_count = sum(1 for item in recent if item.get("change_state") == "UNCHANGED")
    frequency_field_count = sum(1 for item in recent if "frequency_class" in item.get("changed_fields", []))
    recency_field_count = sum(1 for item in recent if "recency_class" in item.get("changed_fields", []))
    both_fields_count = sum(
        1 for item in recent
        if {"frequency_class", "recency_class"}.issubset(set(item.get("changed_fields", [])))
    )
    latest = recent[-1] if recent else None
    runs_since_change = next(
        (index for index, item in enumerate(reversed(recent)) if item.get("change_state") == "CHANGED"),
        None,
    )

    mixed_movement = (
        changed_count > 0
        and frequency_field_count > 0
        and recency_field_count > 0
        and (frequency_field_count != recency_field_count or both_fields_count < changed_count)
    )

    if not recent:
        stability_class = "AWAITING_AUTOMATED_FREQUENCY_CHANGE_HISTORY"
    elif changed_count == 0:
        stability_class = "NO_CLASS_CHANGE_OBSERVED"
    elif mixed_movement:
        stability_class = "MIXED_FREQUENCY_RECENCY_MOVEMENT"
    elif changed_count == 1:
        stability_class = "ISOLATED_CLASS_CHANGE_OBSERVED"
    else:
        stability_class = "REPEATED_CLASS_CHANGE_OBSERVED"

    payload = {
        "schema": "admissibility_wiki.canonical_workflow_frequency_change_stability_summary.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-frequency-change-stability-summary.json",
        "history_state": history_state,
        "stability_class": stability_class,
        "evidence": {
            "maximum_recent_entries": WINDOW,
            "evaluated_entries": total,
            "changed_count": changed_count,
            "unchanged_count": unchanged_count,
            "frequency_class_change_count": frequency_field_count,
            "recency_class_change_count": recency_field_count,
            "both_fields_change_count": both_fields_count,
            "runs_since_last_class_change": runs_since_change,
            "latest_change_receipt_id": (latest or {}).get("receipt_id"),
            "latest_change_state": (latest or {}).get("change_state"),
        },
        "evaluation_scope": {
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
            "stability_claim": "bounded retained frequency-change receipts only",
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
            "Observed bounded stability does not predict future stability or instability.",
            "Mixed movement records field-level receipt differences and does not establish an independent cause.",
            "No class grants release, deployment, execution, or downstream mutation authority.",
            "No stability class assigns a manual task to the user.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY: PASS - "
        f"class={stability_class} entries={total} manual_tasks=0"
    )

    if not CHANGE_GENERATOR.exists():
        raise SystemExit("workflow frequency-change stability-change generator is missing")
    completed = subprocess.run(
        [sys.executable, str(CHANGE_GENERATOR)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit("workflow frequency-change stability-change generation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
