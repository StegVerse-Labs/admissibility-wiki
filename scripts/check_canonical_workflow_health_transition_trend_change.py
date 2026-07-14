#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_health_transition_trend_change.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-receipt.json"
FIXTURE = ROOT / "reports" / "canonical-workflow-prior-trend-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH TRANSITION TREND CHANGE: FAIL - {message}")


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    prior = {
        "trend_class": "REPEATED_FAIL_CLOSED",
        "generated_at": "2026-07-14T07:00:00+00:00",
    }
    current = {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_trend.v0.1",
        "trend_class": "RECOVERY_OBSERVED",
        "evidence": {"evaluated_entries": 2, "reason": "bounded recovery fixture"},
        "history_binding": {"latest_transition_receipt_id": "recovery.1"},
        "automation_response": "continue repository-owned scheduled observation; make no prediction of persistence",
        "evaluation_scope": {"predictive_claim": False},
        "manual_tasks_required": [],
        "user_action_required": False,
    }

    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(prior, indent=2) + "\n", encoding="utf-8")
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)

    env = os.environ.copy()
    env["CANONICAL_HEALTH_TRANSITION_TREND_SOURCE"] = str(FIXTURE)
    try:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)], cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "generator exited non-zero")
        if not OUT.exists():
            fail("trend-change receipt was not generated")

        payload = json.loads(OUT.read_text(encoding="utf-8"))
        if payload.get("change_state") != "CHANGED":
            fail("change_state mismatch")
        if payload.get("prior_trend_class") != "REPEATED_FAIL_CLOSED":
            fail("prior trend mismatch")
        if payload.get("resulting_trend_class") != "RECOVERY_OBSERVED":
            fail("resulting trend mismatch")
        if payload.get("manual_tasks_required") != [] or payload.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if payload.get("predictive_claim") is not False:
            fail("predictive_claim must be false")
        if payload.get("change_owner") != "canonical build-pages job":
            fail("change owner mismatch")
        if payload.get("public_endpoint") != "/status/canonical-workflow-health-transition-trend-change-receipt.json":
            fail("public endpoint mismatch")
        if payload.get("authority_granted") is not False:
            fail("authority_granted must be false")

        print("CANONICAL WORKFLOW HEALTH TRANSITION TREND CHANGE: PASS - changed=1 manual_tasks=0 predictive_claim=false")
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())