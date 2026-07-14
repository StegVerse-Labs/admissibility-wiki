#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_health_summary.py"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-observation-history.json"
SUMMARY = ROOT / "static" / "status" / "canonical-workflow-health-summary.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH SUMMARY: FAIL - {message}")


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    fixture = {
        "schema": "admissibility_wiki.canonical_workflow_observation_history.v0.1",
        "observations": [
            {
                "receipt_id": "cancelled.1",
                "created_at": "2026-07-14T05:00:00+00:00",
                "job_status_observed": "cancelled",
                "full_validation_status": None,
                "reconstruction_status": None,
                "reconstruction_evaluation_result": None,
                "observation_state": "FAIL_CLOSED_OBSERVED",
            },
            {
                "receipt_id": "deferred.1",
                "created_at": "2026-07-14T06:00:00+00:00",
                "job_status_observed": "success",
                "full_validation_status": "PASS",
                "reconstruction_status": "PASS",
                "reconstruction_evaluation_result": "DEFER_NO_SUPERSESSION",
                "observation_state": "INCOMPLETE_OBSERVATION",
            },
        ],
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    SUMMARY.unlink(missing_ok=True)

    try:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "generator exited non-zero")
        if not SUMMARY.exists():
            fail("summary was not generated")

        summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        if summary.get("current_health") != "EXTERNAL_EVIDENCE_DEFERRED":
            fail("latest health classification mismatch")
        counts = summary.get("health_class_counts", {})
        if counts.get("TRANSIENT_CANCELLATION") != 1:
            fail("cancellation count mismatch")
        if counts.get("EXTERNAL_EVIDENCE_DEFERRED") != 1:
            fail("external evidence count mismatch")
        if summary.get("manual_tasks_required") != []:
            fail("summary assigns manual tasks")
        if summary.get("user_action_required") is not False:
            fail("summary requires user action")
        if summary.get("public_endpoint") != "/status/canonical-workflow-health-summary.json":
            fail("public endpoint mismatch")
        if "next repository-owned trigger" not in summary.get("automation_response", {}).get("TRANSIENT_CANCELLATION", ""):
            fail("cancellation response is not automation-owned")

        print("CANONICAL WORKFLOW HEALTH SUMMARY: PASS - classifications=2 manual_tasks=0")
        return 0
    finally:
        HISTORY.unlink(missing_ok=True)
        SUMMARY.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
