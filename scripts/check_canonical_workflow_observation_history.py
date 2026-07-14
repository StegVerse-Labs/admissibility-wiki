#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_observation_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-observation-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-observation-history.json"
FIXTURE = ROOT / "reports" / "canonical-observation-history-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION HISTORY: FAIL - {message}")


def main() -> int:
    if not RECONCILER.exists():
        fail("reconciler is missing")

    current_payload = {
        "schema": "admissibility_wiki.canonical_workflow_observation_receipt.v0.1",
        "receipt_id": "canonical-workflow-observation.current.1",
        "created_at": "2026-07-14T06:00:00+00:00",
        "commit": "current-sha",
        "run_id": "current-run",
        "observation_state": "PASS_OBSERVED",
        "manual_tasks_required": [],
        "user_action_required": False,
    }
    previous_payload = {
        "schema": "admissibility_wiki.canonical_workflow_observation_history.v0.1",
        "observations": [
            {
                "receipt_id": "canonical-workflow-observation.previous.1",
                "created_at": "2026-07-14T05:00:00+00:00",
                "commit": "previous-sha",
                "run_id": "previous-run",
                "observation_state": "FAIL_CLOSED_OBSERVED",
                "manual_tasks_required": [],
                "user_action_required": False,
            }
        ],
    }

    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current_payload, indent=2) + "\n", encoding="utf-8")
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(previous_payload, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)

    env = os.environ.copy()
    env["CANONICAL_OBSERVATION_HISTORY_SOURCE"] = str(FIXTURE)
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

        history = json.loads(HISTORY.read_text(encoding="utf-8"))
        observations = history.get("observations", [])
        if len(observations) != 2:
            fail("expected two reconciled observations")
        if history.get("latest_observation", {}).get("receipt_id") != "canonical-workflow-observation.current.1":
            fail("latest observation mismatch")
        if history.get("state_counts", {}).get("PASS_OBSERVED") != 1:
            fail("PASS count mismatch")
        if history.get("state_counts", {}).get("FAIL_CLOSED_OBSERVED") != 1:
            fail("FAIL_CLOSED count mismatch")
        if history.get("manual_tasks_required") != []:
            fail("history assigns manual tasks")
        if history.get("user_action_required") is not False:
            fail("history requires user action")
        if history.get("next_reconciliation") != "next repository-owned canonical workflow trigger":
            fail("next reconciliation is not automation-owned")
        if history.get("public_endpoint") != "/status/canonical-workflow-observation-history.json":
            fail("public endpoint mismatch")

        print("CANONICAL WORKFLOW OBSERVATION HISTORY: PASS - entries=2 manual_tasks=0")
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        HISTORY.unlink(missing_ok=True)
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
