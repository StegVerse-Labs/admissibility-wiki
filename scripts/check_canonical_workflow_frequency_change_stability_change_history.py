#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILER = ROOT / "scripts" / "reconcile_canonical_workflow_frequency_change_stability_change_history.py"
CURRENT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-history.json"
FIXTURE = ROOT / "reports" / "stability-change-history-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY CHANGE HISTORY: FAIL - {message}")


def receipt(receipt_id: str, generated_at: str, state: str, prior: str, resulting: str) -> dict:
    return {
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "change_state": state,
        "prior_stability_class": prior,
        "resulting_stability_class": resulting,
        "manual_tasks_required": [],
        "user_action_required": False,
        "descriptive_only": True,
        "predictive_claim": False,
        "causal_claim_beyond_receipt_fields": False,
    }


def main() -> int:
    if not RECONCILER.exists():
        fail("reconciler is missing")

    prior = [
        receipt("s1", "2026-07-14T01:00:00+00:00", "UNCHANGED", "NO_CLASS_CHANGE_OBSERVED", "NO_CLASS_CHANGE_OBSERVED"),
        receipt("s2", "2026-07-14T02:00:00+00:00", "CHANGED", "NO_CLASS_CHANGE_OBSERVED", "ISOLATED_CLASS_CHANGE_OBSERVED"),
        receipt("s2", "2026-07-14T02:30:00+00:00", "CHANGED", "NO_CLASS_CHANGE_OBSERVED", "ISOLATED_CLASS_CHANGE_OBSERVED"),
    ]
    current = receipt("s3", "2026-07-14T03:00:00+00:00", "CHANGED", "ISOLATED_CLASS_CHANGE_OBSERVED", "REPEATED_CLASS_CHANGE_OBSERVED")
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps({"changes": prior}, indent=2) + "\n", encoding="utf-8")
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    HISTORY.unlink(missing_ok=True)

    env = dict(os.environ)
    env["CANONICAL_FREQUENCY_CHANGE_STABILITY_CHANGE_HISTORY_SOURCE"] = str(FIXTURE)
    try:
        completed = subprocess.run(
            [sys.executable, str(RECONCILER)], cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "reconciler exited non-zero")
        if not HISTORY.exists():
            fail("history was not generated")
        data = json.loads(HISTORY.read_text(encoding="utf-8"))
        changes = data.get("changes", [])
        if len(changes) != 3:
            fail("deduplicated history must contain three entries")
        if [item.get("receipt_id") for item in changes] != ["s1", "s2", "s3"]:
            fail("history ordering or deduplication mismatch")
        policy = data.get("retention_policy", {})
        if policy.get("maximum_entries") != 24 or policy.get("deduplication_key") != "receipt_id":
            fail("retention policy mismatch")
        if policy.get("ordering") != "generated_at ascending":
            fail("ordering policy mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if data.get("predictive_claim") is not False or data.get("causal_claim_beyond_receipt_fields") is not False:
            fail("claim boundaries mismatch")
        if data.get("reconciliation_owner") != "canonical build-pages job":
            fail("reconciliation owner mismatch")
        if data.get("public_endpoint") != "/status/canonical-workflow-frequency-change-stability-change-history.json":
            fail("public endpoint mismatch")
        print("CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY CHANGE HISTORY: PASS - entries=3 manual_tasks=0")
        return 0
    finally:
        FIXTURE.unlink(missing_ok=True)
        CURRENT.unlink(missing_ok=True)
        HISTORY.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
