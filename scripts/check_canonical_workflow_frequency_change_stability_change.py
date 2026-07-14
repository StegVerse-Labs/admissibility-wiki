#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_frequency_change_stability_change.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-summary.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-receipt.json"
PRIOR = ROOT / "reports" / "frequency-change-stability-prior.fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY CHANGE: FAIL - {message}")


def main() -> int:
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    PRIOR.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps({
        "stability_class": "REPEATED_CLASS_CHANGE_OBSERVED",
        "evidence": {"latest_change_receipt_id": "frequency-change.4"},
        "evaluation_scope": {
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
        },
        "automation_response": "continue repository-owned bounded observation",
        "manual_tasks_required": [],
        "user_action_required": False,
    }, indent=2) + "\n", encoding="utf-8")
    PRIOR.write_text(json.dumps({"stability_class": "ISOLATED_CLASS_CHANGE_OBSERVED"}, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)
    env = dict(os.environ)
    env["CANONICAL_FREQUENCY_CHANGE_STABILITY_SOURCE"] = str(PRIOR)
    try:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)], cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "generator exited non-zero")
        if not OUT.exists():
            fail("change receipt was not generated")
        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("change_state") != "CHANGED":
            fail("change_state mismatch")
        if data.get("prior_stability_class") != "ISOLATED_CLASS_CHANGE_OBSERVED":
            fail("prior stability class mismatch")
        if data.get("resulting_stability_class") != "REPEATED_CLASS_CHANGE_OBSERVED":
            fail("resulting stability class mismatch")
        if data.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if data.get("predictive_claim") is not False or data.get("causal_claim_beyond_receipt_fields") is not False:
            fail("claim boundary mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("change_owner") != "canonical build-pages job":
            fail("change owner mismatch")
        if data.get("public_endpoint") != "/status/canonical-workflow-frequency-change-stability-change-receipt.json":
            fail("public endpoint mismatch")
        print("CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY CHANGE: PASS - changed manual_tasks=0")
        return 0
    finally:
        CURRENT.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)
        PRIOR.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
