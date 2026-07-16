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
TRANSITION = ROOT / "static" / "status" / "canonical-workflow-health-transition-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW HEALTH TRANSITION: FAIL - {message}")


def snapshot(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def restore(path: Path, prior: bytes | None) -> None:
    if prior is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(prior)


def main() -> int:
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
                "receipt_id": "healthy.1",
                "created_at": "2026-07-14T06:00:00+00:00",
                "job_status_observed": "success",
                "full_validation_status": "PASS",
                "reconstruction_status": "PASS",
                "reconstruction_evaluation_result": "ALLOW_SUPERSESSION",
                "observation_state": "PASS_OBSERVED",
            },
        ],
    }
    prior = {path: snapshot(path) for path in (HISTORY, SUMMARY, TRANSITION)}
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    SUMMARY.unlink(missing_ok=True)
    TRANSITION.unlink(missing_ok=True)

    try:
        result = subprocess.run(
            [sys.executable, str(GENERATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            fail(result.stdout or "generator exited non-zero")
        if not TRANSITION.exists():
            fail("transition receipt was not generated")

        receipt = json.loads(TRANSITION.read_text(encoding="utf-8"))
        if receipt.get("schema") != "admissibility_wiki.canonical_workflow_health_transition_receipt.v0.1":
            fail("unexpected schema")
        if receipt.get("transition_state") != "CHANGED":
            fail("changed transition was not detected")
        if receipt.get("prior_health") != "TRANSIENT_CANCELLATION":
            fail("prior health mismatch")
        if receipt.get("resulting_health") != "HEALTHY":
            fail("resulting health mismatch")
        if receipt.get("manual_tasks_required") != []:
            fail("manual task was assigned")
        if receipt.get("user_action_required") is not False:
            fail("user action was assigned")
        if receipt.get("transition_owner") != "canonical build-pages job":
            fail("transition owner mismatch")
        if receipt.get("authority_granted") is not False:
            fail("receipt grants authority")
        if receipt.get("public_endpoint") != "/status/canonical-workflow-health-transition-receipt.json":
            fail("public endpoint mismatch")

        print("CANONICAL WORKFLOW HEALTH TRANSITION: PASS - changed=true manual_tasks=0 preserved_run_bound_artifacts=true")
        return 0
    finally:
        for path, content in prior.items():
            restore(path, content)


if __name__ == "__main__":
    raise SystemExit(main())
