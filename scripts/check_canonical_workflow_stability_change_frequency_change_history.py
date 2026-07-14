#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_stability_change_frequency_change_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-history.json"
FIXTURE = ROOT / "reports" / "stability-change-frequency-change-history.fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE HISTORY: FAIL - {message}")


def receipt(receipt_id: str, generated_at: str, changed_fields: list[str]) -> dict:
    return {
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "change_state": "CHANGED" if changed_fields else "UNCHANGED",
        "changed_fields": changed_fields,
        "prior_frequency_class": "ISOLATED_STABILITY_CHANGE_OBSERVED",
        "resulting_frequency_class": "FREQUENT_STABILITY_CHANGE_OBSERVED",
        "prior_recency_class": "RECENT_STABILITY_CHANGE",
        "resulting_recency_class": "CURRENT_RECEIPT_CHANGED",
        "manual_tasks_required": [],
        "user_action_required": False,
        "descriptive_only": True,
        "predictive_claim": False,
        "causal_claim_beyond_receipt_fields": False,
    }


def main() -> int:
    current = receipt("comparison.current", "2026-07-14T12:00:00+00:00", ["frequency_class", "recency_class"])
    previous = receipt("comparison.previous", "2026-07-14T11:00:00+00:00", ["frequency_class"])
    duplicate = dict(current)
    duplicate["generated_at"] = "2026-07-14T10:30:00+00:00"

    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    FIXTURE.write_text(json.dumps({"changes": [previous, duplicate]}, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)
    env = dict(os.environ)
    env["CANONICAL_STABILITY_CHANGE_FREQUENCY_CHANGE_HISTORY_SOURCE"] = str(FIXTURE)

    try:
        completed = subprocess.run(
            [sys.executable, str(RECONCILER)], cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "reconciler exited non-zero")
        if not HISTORY.exists():
            fail("history was not generated")
        data = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = data.get("changes", [])
        if len(changes) != 2:
            fail("deduplicated history must contain two entries")
        if [item.get("receipt_id") for item in changes] != ["comparison.previous", "comparison.current"]:
            fail("history ordering or deduplication mismatch")
        policy = data.get("retention_policy", {})
        if policy.get("maximum_entries") != 24:
            fail("maximum_entries must be 24")
        if policy.get("deduplication_key") != "receipt_id":
            fail("deduplication key mismatch")
        if policy.get("ordering") != "generated_at ascending":
            fail("ordering mismatch")
        if data.get("change_state_counts", {}).get("CHANGED") != 2:
            fail("CHANGED count mismatch")
        fields = data.get("changed_field_counts", {})
        if fields.get("frequency_class") != 2 or fields.get("recency_class") != 1:
            fail("changed field counts mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if data.get("predictive_claim") is not False or data.get("causal_claim_beyond_receipt_fields") is not False:
            fail("claim boundaries mismatch")
        if data.get("reconciliation_owner") != "canonical build-pages job":
            fail("reconciliation owner mismatch")
        if data.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
            fail("next reconciliation is not automation-owned")
        if data.get("public_endpoint") != "/status/canonical-workflow-stability-change-frequency-change-history.json":
            fail("public endpoint mismatch")
        print("CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE HISTORY: PASS - entries=2 manual_tasks=0")
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        HISTORY.unlink(missing_ok=True)
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
