#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_health_transition_trend.py"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH TRANSITION TREND: FAIL - {message}")


def transition(receipt_id: str, generated_at: str, prior: str, resulting: str) -> dict:
    return {
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "transition_state": "CHANGED" if prior != resulting else "UNCHANGED",
        "prior_health": prior,
        "resulting_health": resulting,
    }


def run_case(name: str, transitions: list[dict], expected: str) -> None:
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps({
        "schema": "admissibility_wiki.canonical_workflow_health_transition_history.v0.1",
        "generated_at": "2026-07-14T07:00:00+00:00",
        "latest_transition": {"receipt_id": transitions[-1]["receipt_id"] if transitions else None},
        "transitions": transitions,
    }, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)

    completed = subprocess.run(
        [sys.executable, str(GENERATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"{name}: {completed.stdout or 'generator exited non-zero'}")
    if not OUT.exists():
        fail(f"{name}: trend summary was not generated")
    payload = json.loads(OUT.read_text(encoding="utf-8"))
    if payload.get("trend_class") != expected:
        fail(f"{name}: expected {expected}, got {payload.get('trend_class')}")
    if payload.get("manual_tasks_required") != [] or payload.get("user_action_required") is not False:
        fail(f"{name}: no-manual boundary violated")
    if payload.get("evaluation_scope", {}).get("predictive_claim") is not False:
        fail(f"{name}: predictive_claim must be false")
    if payload.get("authority_granted") is not False:
        fail(f"{name}: authority_granted must be false")
    if payload.get("public_endpoint") != "/status/canonical-workflow-health-transition-trend.json":
        fail(f"{name}: public endpoint mismatch")


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")
    try:
        run_case(
            "recovery",
            [transition("failure.1", "2026-07-14T05:00:00+00:00", "HEALTHY", "VALIDATION_FAILURE"),
             transition("recovery.1", "2026-07-14T06:00:00+00:00", "VALIDATION_FAILURE", "HEALTHY")],
            "RECOVERY_OBSERVED",
        )
        run_case(
            "repeated-failure",
            [transition("failure.1", "2026-07-14T05:00:00+00:00", "HEALTHY", "VALIDATION_FAILURE"),
             transition("failure.2", "2026-07-14T06:00:00+00:00", "VALIDATION_FAILURE", "VALIDATION_FAILURE")],
            "REPEATED_FAIL_CLOSED",
        )
        run_case(
            "deferral",
            [transition("defer.1", "2026-07-14T06:00:00+00:00", "AWAITING_AUTOMATED_OBSERVATION", "EXTERNAL_EVIDENCE_DEFERRED")],
            "UNRESOLVED_DEFERRAL",
        )
        print("CANONICAL WORKFLOW HEALTH TRANSITION TREND: PASS - cases=3 manual_tasks=0 predictive_claim=false")
        return 0
    finally:
        HISTORY.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
