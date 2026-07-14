#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_change.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-summary.json"
PREVIOUS = ROOT / "reports" / "stability-change-frequency-previous.fixture.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE: FAIL - {message}")


def main() -> int:
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    PREVIOUS.parent.mkdir(parents=True, exist_ok=True)
    previous = {
        "frequency_class": "ISOLATED_STABILITY_CHANGE_OBSERVED",
        "recency_class": "RECENT_STABILITY_CHANGE",
    }
    current = {
        "frequency_class": "FREQUENT_STABILITY_CHANGE_OBSERVED",
        "recency_class": "CURRENT_RECEIPT_CHANGED",
        "evidence": {"latest_change_receipt_id": "stability-change.4", "evaluated_entries": 4},
        "evaluation_scope": {
            "descriptive_only": True,
            "predictive_claim": False,
            "causal_claim_beyond_receipt_fields": False,
        },
        "manual_tasks_required": [],
        "user_action_required": False,
    }
    PREVIOUS.write_text(json.dumps(previous, indent=2) + "\n", encoding="utf-8")
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)
    env = dict(os.environ)
    env["CANONICAL_STABILITY_CHANGE_FREQUENCY_SOURCE"] = str(PREVIOUS)

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
        if set(data.get("changed_fields", [])) != {"frequency_class", "recency_class"}:
            fail("changed_fields mismatch")
        if data.get("prior_frequency_class") != "ISOLATED_STABILITY_CHANGE_OBSERVED":
            fail("prior frequency mismatch")
        if data.get("resulting_frequency_class") != "FREQUENT_STABILITY_CHANGE_OBSERVED":
            fail("resulting frequency mismatch")
        if data.get("prior_recency_class") != "RECENT_STABILITY_CHANGE":
            fail("prior recency mismatch")
        if data.get("resulting_recency_class") != "CURRENT_RECEIPT_CHANGED":
            fail("resulting recency mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if data.get("predictive_claim") is not False or data.get("causal_claim_beyond_receipt_fields") is not False:
            fail("claim boundaries mismatch")
        if data.get("change_owner") != "canonical build-pages job":
            fail("change owner mismatch")
        if data.get("public_endpoint") != "/status/canonical-workflow-stability-change-frequency-change-receipt.json":
            fail("public endpoint mismatch")
        print("CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE: PASS - changed_fields=2 manual_tasks=0")
        return 0
    finally:
        PREVIOUS.unlink(missing_ok=True)
        CURRENT.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
