#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_trend_change_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-history.json"
FIXTURE = ROOT / "reports" / "canonical-trend-change-history-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH TRANSITION TREND CHANGE HISTORY: FAIL - {message}")


def receipt(receipt_id: str, generated_at: str, prior: str, resulting: str) -> dict:
    return {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_trend_change_receipt.v0.1",
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "change_state": "CHANGED" if prior != resulting else "UNCHANGED",
        "prior_trend_class": prior,
        "resulting_trend_class": resulting,
        "manual_tasks_required": [],
        "user_action_required": False,
        "predictive_claim": False,
    }


def main() -> int:
    if not RECONCILER.exists():
        fail("reconciler is missing")

    current = receipt("trend-change.current", "2026-07-14T08:00:00+00:00", "RECOVERY_OBSERVED", "STABLE_HEALTHY")
    previous = receipt("trend-change.previous", "2026-07-14T07:00:00+00:00", "REPEATED_FAIL_CLOSED", "RECOVERY_OBSERVED")
    duplicate = dict(current)
    duplicate["generated_at"] = "2026-07-14T06:30:00+00:00"

    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    FIXTURE.write_text(json.dumps({"changes": [previous, duplicate]}, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)

    env = os.environ.copy()
    env["CANONICAL_HEALTH_TRANSITION_TREND_CHANGE_HISTORY_SOURCE"] = str(FIXTURE)
    try:
        completed = subprocess.run(
            [sys.executable, str(RECONCILER)], cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "reconciler exited non-zero")
        if not HISTORY.exists():
            fail("history was not generated")

        payload = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = payload.get("changes", [])
        if len(changes) != 2:
            fail("deduplicated history must contain exactly two entries")
        if [item.get("receipt_id") for item in changes] != ["trend-change.previous", "trend-change.current"]:
            fail("history ordering or deduplication mismatch")
        policy = payload.get("retention_policy", {})
        if policy.get("maximum_entries") != 24:
            fail("maximum_entries must be 24")
        if policy.get("deduplication_key") != "receipt_id":
            fail("deduplication key mismatch")
        if policy.get("ordering") != "generated_at ascending":
            fail("ordering mismatch")
        if payload.get("manual_tasks_required") != [] or payload.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if payload.get("predictive_claim") is not False:
            fail("predictive_claim must be false")
        if payload.get("reconciliation_owner") != "canonical build-pages job":
            fail("reconciliation owner mismatch")
        if payload.get("public_endpoint") != "/status/canonical-workflow-health-transition-trend-change-history.json":
            fail("public endpoint mismatch")

        print("CANONICAL WORKFLOW HEALTH TRANSITION TREND CHANGE HISTORY: PASS - entries=2 deduplicated=true manual_tasks=0")
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        HISTORY.unlink(missing_ok=True)
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
