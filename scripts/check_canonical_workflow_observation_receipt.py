#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_canonical_workflow_observation_receipt.py"
OUT = ROOT / "reports" / "canonical-workflow-observation-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION RECEIPT: FAIL - {message}")


def main() -> int:
    if not WRITER.exists():
        fail("writer is missing")

    env = os.environ.copy()
    env.update({
        "CANONICAL_JOB_STATUS": "success",
        "GITHUB_EVENT_NAME": "validator",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_SHA": "validator-sha",
        "GITHUB_RUN_ID": "validator-run",
        "GITHUB_RUN_ATTEMPT": "1",
    })
    completed = subprocess.run(
        [sys.executable, str(WRITER)],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stdout or "writer exited non-zero")
    if not OUT.exists():
        fail("writer did not create receipt")

    receipt = json.loads(OUT.read_text(encoding="utf-8"))
    if receipt.get("schema") != "admissibility_wiki.canonical_workflow_observation_receipt.v0.1":
        fail("schema mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if receipt.get("commit") != "validator-sha":
        fail("commit binding mismatch")
    if receipt.get("run_id") != "validator-run":
        fail("run binding mismatch")
    if receipt.get("manual_tasks_required") != []:
        fail("manual_tasks_required must be empty")
    if receipt.get("user_action_required") is not False:
        fail("user_action_required must be false")
    if receipt.get("observation_state") not in {
        "PASS_OBSERVED",
        "FAIL_CLOSED_OBSERVED",
        "INCOMPLETE_OBSERVATION",
    }:
        fail("invalid observation state")
    non_claims = receipt.get("non_claims", [])
    if not any("does not grant" in claim for claim in non_claims):
        fail("authority non-claim is missing")
    if not any("does not assign a manual task" in claim for claim in non_claims):
        fail("no-manual-task non-claim is missing")

    print(
        "CANONICAL WORKFLOW OBSERVATION RECEIPT: PASS - "
        f"state={receipt['observation_state']} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
