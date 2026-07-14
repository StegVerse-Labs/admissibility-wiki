#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHER = ROOT / "scripts" / "publish_canonical_workflow_observation_receipt.py"
UPSTREAM_DIR = ROOT / "reports" / "upstream-full-validation"
UPSTREAM = UPSTREAM_DIR / "full_validation_chain_report.json"
PUBLIC = ROOT / "static" / "status" / "canonical-workflow-observation-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION PUBLICATION: FAIL - {message}")


def main() -> int:
    if not PUBLISHER.exists():
        fail("publisher is missing")

    fixture = {
        "schema": "admissibility_wiki.full_validation_chain_report.v1",
        "overall_status": "PASS",
        "canonical_workflow_observation": {
            "schema": "admissibility_wiki.canonical_workflow_observation_receipt.v0.1",
            "receipt_id": "canonical-workflow-observation.validator.1",
            "repository": "StegVerse-Labs/admissibility-wiki",
            "commit": "validator-sha",
            "run_id": "validator-run",
            "run_attempt": "1",
            "job_status_observed": "success",
            "full_validation_status": "PASS",
            "reconstruction_status": "PASS",
            "reconstruction_evaluation_result": "DEFER_NO_SUPERSESSION",
            "observation_state": "PASS_OBSERVED",
            "manual_tasks_required": [],
            "user_action_required": False,
            "non_claims": ["This fixture does not grant authority."],
        },
    }

    UPSTREAM_DIR.mkdir(parents=True, exist_ok=True)
    UPSTREAM.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    PUBLIC.unlink(missing_ok=True)

    env = os.environ.copy()
    env.update({"GITHUB_RUN_ID": "validator-build-run", "GITHUB_RUN_ATTEMPT": "1"})
    try:
        completed = subprocess.run(
            [sys.executable, str(PUBLISHER)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "publisher exited non-zero")
        if not PUBLIC.exists():
            fail("public receipt was not generated")

        receipt = json.loads(PUBLIC.read_text(encoding="utf-8"))
        if receipt.get("observation_state") != "PASS_OBSERVED":
            fail("observation state mismatch")
        if receipt.get("manual_tasks_required") != []:
            fail("receipt assigns manual tasks")
        if receipt.get("user_action_required") is not False:
            fail("receipt requires user action")
        publication = receipt.get("publication", {})
        if publication.get("public_endpoint") != "/status/canonical-workflow-observation-receipt.json":
            fail("public endpoint mismatch")
        if publication.get("manual_tasks_required") != []:
            fail("publication assigns manual tasks")
        if publication.get("user_action_required") is not False:
            fail("publication requires user action")

        print("CANONICAL WORKFLOW OBSERVATION PUBLICATION: PASS - manual_tasks=0")
        return 0
    finally:
        UPSTREAM.unlink(missing_ok=True)
        try:
            UPSTREAM_DIR.rmdir()
        except OSError:
            pass
        PUBLIC.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
