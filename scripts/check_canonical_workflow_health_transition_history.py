#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_health_transition_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-health-transition-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-history.json"
TREND = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend.json"
FIXTURE = ROOT / "reports" / "canonical-health-transition-history-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH TRANSITION HISTORY: FAIL - {message}")


def snapshot(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def restore(path: Path, prior: bytes | None) -> None:
    if prior is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(prior)


def transition(receipt_id: str, generated_at: str, prior: str, resulting: str) -> dict:
    return {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_receipt.v0.1",
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-transition-receipt.json",
        "transition_state": "CHANGED" if prior != resulting else "UNCHANGED",
        "prior_health": prior,
        "resulting_health": resulting,
        "prior_cause": {"health_class": prior},
        "resulting_cause": {"health_class": resulting},
        "fail_closed_consequence": "continue scheduled observation",
        "manual_tasks_required": [],
        "user_action_required": False,
        "transition_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": ["fixture"],
    }


def main() -> int:
    if not RECONCILER.exists():
        fail("reconciler is missing")

    previous = transition(
        "workflow-health-transition.previous",
        "2026-07-14T05:00:00+00:00",
        "AWAITING_AUTOMATED_OBSERVATION",
        "TRANSIENT_CANCELLATION",
    )
    duplicate_old = transition(
        "workflow-health-transition.current",
        "2026-07-14T05:30:00+00:00",
        "TRANSIENT_CANCELLATION",
        "VALIDATION_FAILURE",
    )
    current = transition(
        "workflow-health-transition.current",
        "2026-07-14T06:00:00+00:00",
        "TRANSIENT_CANCELLATION",
        "HEALTHY",
    )
    prior = {path: snapshot(path) for path in (CURRENT, HISTORY, TREND, FIXTURE)}
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(
        json.dumps({"transitions": [previous, duplicate_old]}, indent=2) + "\n",
        encoding="utf-8",
    )
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)
    TREND.unlink(missing_ok=True)

    env = os.environ.copy()
    env["CANONICAL_HEALTH_TRANSITION_HISTORY_SOURCE"] = str(FIXTURE)
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
        if not TREND.exists():
            fail("trend summary was not generated")

        history = json.loads(HISTORY.read_text(encoding="utf-8"))
        transitions = history.get("transitions", [])
        if len(transitions) != 2:
            fail("deduplicated transition count mismatch")
        if [item.get("receipt_id") for item in transitions] != [
            "workflow-health-transition.previous",
            "workflow-health-transition.current",
        ]:
            fail("transition order or deduplication mismatch")
        if transitions[-1].get("resulting_health") != "HEALTHY":
            fail("current receipt did not replace duplicate prior copy")
        if history.get("transition_state_counts") != {"CHANGED": 2, "UNCHANGED": 0}:
            fail("transition state counts mismatch")
        policy = history.get("retention_policy", {})
        if policy.get("maximum_entries") != 24:
            fail("bounded retention mismatch")
        if policy.get("deduplication_key") != "receipt_id":
            fail("deduplication key mismatch")
        if policy.get("ordering") != "generated_at ascending":
            fail("ordering mismatch")
        if history.get("manual_tasks_required") != [] or history.get("user_action_required") is not False:
            fail("history violates no-manual boundary")
        if history.get("reconciliation_owner") != "canonical build-pages job":
            fail("reconciliation owner mismatch")
        if history.get("public_endpoint") != "/status/canonical-workflow-health-transition-history.json":
            fail("public endpoint mismatch")

        trend = json.loads(TREND.read_text(encoding="utf-8"))
        if trend.get("trend_class") != "RECOVERY_OBSERVED":
            fail("reconciled history did not produce recovery trend")
        if trend.get("manual_tasks_required") != [] or trend.get("user_action_required") is not False:
            fail("trend violates no-manual boundary")
        if trend.get("evaluation_scope", {}).get("predictive_claim") is not False:
            fail("trend must remain non-predictive")

        print("CANONICAL WORKFLOW HEALTH TRANSITION HISTORY: PASS - entries=2 deduplicated=1 trend=RECOVERY_OBSERVED manual_tasks=0 preserved_run_bound_artifacts=true")
        return 0
    finally:
        for path, content in prior.items():
            restore(path, content)


if __name__ == "__main__":
    raise SystemExit(main())
