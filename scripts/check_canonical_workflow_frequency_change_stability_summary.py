#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_frequency_change_stability_summary.py"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-summary.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY: FAIL - {message}")


def item(receipt_id: str, generated_at: str, changed_fields: list[str]) -> dict:
    return {
        "receipt_id": receipt_id,
        "generated_at": generated_at,
        "change_state": "CHANGED" if changed_fields else "UNCHANGED",
        "changed_fields": changed_fields,
    }


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    fixture = {
        "changes": [
            item("frequency-change.1", "2026-07-14T07:00:00+00:00", []),
            item("frequency-change.2", "2026-07-14T08:00:00+00:00", ["frequency_class"]),
            item("frequency-change.3", "2026-07-14T09:00:00+00:00", ["recency_class"]),
            item("frequency-change.4", "2026-07-14T10:00:00+00:00", []),
        ]
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)

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

        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("stability_class") != "MIXED_FREQUENCY_RECENCY_MOVEMENT":
            fail("stability class mismatch")
        evidence = data.get("evidence", {})
        if evidence.get("maximum_recent_entries") != 12:
            fail("maximum_recent_entries must be 12")
        if evidence.get("evaluated_entries") != 4:
            fail("evaluated_entries mismatch")
        if evidence.get("changed_count") != 2 or evidence.get("unchanged_count") != 2:
            fail("change counts mismatch")
        if evidence.get("frequency_class_change_count") != 1:
            fail("frequency class count mismatch")
        if evidence.get("recency_class_change_count") != 1:
            fail("recency class count mismatch")
        if evidence.get("both_fields_change_count") != 0:
            fail("both-fields count mismatch")
        if evidence.get("runs_since_last_class_change") != 1:
            fail("runs_since_last_class_change mismatch")

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
        if data.get("public_endpoint") != "/status/canonical-workflow-frequency-change-stability-summary.json":
            fail("public endpoint mismatch")

        print(
            "CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY: PASS - "
            "class=MIXED_FREQUENCY_RECENCY_MOVEMENT manual_tasks=0"
        )
        return 0
    finally:
        HISTORY.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
