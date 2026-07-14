#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_trend_change_frequency_change_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-change-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-change-history.json"
FIXTURE = ROOT / "reports" / "canonical-frequency-change-history-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW TREND CHANGE FREQUENCY CHANGE HISTORY: FAIL - {message}")


def receipt(
    receipt_id: str,
    generated_at: str,
    prior_frequency: str,
    resulting_frequency: str,
    prior_recency: str,
    resulting_recency: str,
) -> dict:
    changed_fields: list[str] = []
    if prior_frequency != resulting_frequency:
        changed_fields.append("frequency_class")
    if prior_recency != resulting_recency:
        changed_fields.append("recency_class")
    return {
        "schema": "admissibility_wiki.canonical_workflow_trend_change_frequency_change_receipt.v0.1",
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "change_state": "CHANGED" if changed_fields else "UNCHANGED",
        "changed_fields": changed_fields,
        "prior_frequency_class": prior_frequency,
        "resulting_frequency_class": resulting_frequency,
        "prior_recency_class": prior_recency,
        "resulting_recency_class": resulting_recency,
        "manual_tasks_required": [],
        "user_action_required": False,
        "descriptive_only": True,
        "predictive_claim": False,
        "causal_claim_beyond_receipt_fields": False,
    }


def main() -> int:
    if not RECONCILER.exists():
        fail("reconciler is missing")

    current = receipt(
        "frequency-change.current",
        "2026-07-14T10:00:00+00:00",
        "OCCASIONAL_CHANGE_OBSERVED",
        "FREQUENT_CHANGE_OBSERVED",
        "RECENT_CHANGE",
        "CURRENT_RECEIPT_CHANGED",
    )
    previous = receipt(
        "frequency-change.previous",
        "2026-07-14T09:00:00+00:00",
        "ISOLATED_CHANGE_OBSERVED",
        "OCCASIONAL_CHANGE_OBSERVED",
        "OLDER_CHANGE_IN_WINDOW",
        "RECENT_CHANGE",
    )
    duplicate = dict(current)
    duplicate["generated_at"] = "2026-07-14T08:30:00+00:00"

    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    FIXTURE.write_text(json.dumps({"changes": [previous, duplicate]}, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)

    env = os.environ.copy()
    env["CANONICAL_TREND_CHANGE_FREQUENCY_CHANGE_HISTORY_SOURCE"] = str(FIXTURE)
    try:
        completed = subprocess.run(
            [sys.executable, str(RECONCILER)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "reconciler exited non-zero")
        if not HISTORY.exists():
            fail("history was not generated")

        payload = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = payload.get("changes", [])
        if len(changes) != 2:
            fail("deduplicated history must contain exactly two entries")
        if [item.get("receipt_id") for item in changes] != [
            "frequency-change.previous",
            "frequency-change.current",
        ]:
            fail("history ordering or deduplication mismatch")

        policy = payload.get("retention_policy", {})
        if policy.get("maximum_entries") != 24:
            fail("maximum_entries must be 24")
        if policy.get("deduplication_key") != "receipt_id":
            fail("deduplication key mismatch")
        if policy.get("ordering") != "generated_at ascending":
            fail("ordering mismatch")

        if payload.get("change_state_counts", {}).get("CHANGED") != 2:
            fail("CHANGED count mismatch")
        field_counts = payload.get("changed_field_counts", {})
        if field_counts.get("frequency_class") != 2:
            fail("frequency_class count mismatch")
        if field_counts.get("recency_class") != 2:
            fail("recency_class count mismatch")

        if payload.get("manual_tasks_required") != [] or payload.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if payload.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if payload.get("predictive_claim") is not False:
            fail("predictive_claim must be false")
        if payload.get("causal_claim_beyond_receipt_fields") is not False:
            fail("causal claim boundary mismatch")
        if payload.get("reconciliation_owner") != "canonical build-pages job":
            fail("reconciliation owner mismatch")
        if payload.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
            fail("next reconciliation is not automation-owned")
        if payload.get("public_endpoint") != "/status/canonical-workflow-trend-change-frequency-change-history.json":
            fail("public endpoint mismatch")

        print(
            "CANONICAL WORKFLOW TREND CHANGE FREQUENCY CHANGE HISTORY: PASS - "
            "entries=2 deduplicated=true manual_tasks=0"
        )
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        HISTORY.unlink(missing_ok=True)
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
