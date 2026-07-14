#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_stability_change_frequency_summary.py"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-summary.json"
CHANGE = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY: FAIL - {message}")


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    fixture = {
        "changes": [
            {"receipt_id": "s1", "change_state": "UNCHANGED", "resulting_stability_class": "NO_CLASS_CHANGE_OBSERVED"},
            {"receipt_id": "s2", "change_state": "CHANGED", "resulting_stability_class": "ISOLATED_CLASS_CHANGE_OBSERVED"},
            {"receipt_id": "s3", "change_state": "UNCHANGED", "resulting_stability_class": "ISOLATED_CLASS_CHANGE_OBSERVED"},
            {"receipt_id": "s4", "change_state": "CHANGED", "resulting_stability_class": "REPEATED_CLASS_CHANGE_OBSERVED"},
        ]
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)
    CHANGE.unlink(missing_ok=True)

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
        if not OUT.exists():
            fail("summary was not generated")
        if not CHANGE.exists():
            fail("comparison receipt was not generated")

        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("frequency_class") != "FREQUENT_STABILITY_CHANGE_OBSERVED":
            fail("frequency class mismatch")
        if data.get("recency_class") != "CURRENT_RECEIPT_CHANGED":
            fail("recency class mismatch")
        evidence = data.get("evidence", {})
        if evidence.get("maximum_recent_entries") != 12:
            fail("maximum_recent_entries must be 12")
        if evidence.get("evaluated_entries") != 4:
            fail("evaluated_entries mismatch")
        if evidence.get("changed_count") != 2 or evidence.get("unchanged_count") != 2:
            fail("change counts mismatch")
        if evidence.get("observed_change_ratio") != 0.5:
            fail("observed_change_ratio mismatch")
        if evidence.get("runs_since_last_changed_receipt") != 0:
            fail("runs_since_last_changed_receipt mismatch")

        scope = data.get("evaluation_scope", {})
        if scope.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if scope.get("predictive_claim") is not False:
            fail("predictive_claim must be false")
        if scope.get("causal_claim_beyond_receipt_fields") is not False:
            fail("causal claim boundary mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("evaluation_owner") != "canonical build-pages job":
            fail("evaluation owner mismatch")
        if data.get("next_evaluation") != "next repository-owned canonical workflow trigger":
            fail("next evaluation is not automation-owned")
        if data.get("public_endpoint") != "/status/canonical-workflow-stability-change-frequency-summary.json":
            fail("public endpoint mismatch")

        comparison = json.loads(CHANGE.read_text(encoding="utf-8"))
        if comparison.get("resulting_frequency_class") != "FREQUENT_STABILITY_CHANGE_OBSERVED":
            fail("comparison resulting frequency mismatch")
        if comparison.get("resulting_recency_class") != "CURRENT_RECEIPT_CHANGED":
            fail("comparison resulting recency mismatch")
        if comparison.get("manual_tasks_required") != [] or comparison.get("user_action_required") is not False:
            fail("comparison no-manual boundary violated")

        print(
            "CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY: PASS - "
            "frequency=FREQUENT_STABILITY_CHANGE_OBSERVED comparison=generated manual_tasks=0"
        )
        return 0
    finally:
        HISTORY.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)
        CHANGE.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
