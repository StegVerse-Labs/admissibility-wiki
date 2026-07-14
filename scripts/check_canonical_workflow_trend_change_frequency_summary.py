#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_trend_change_frequency_summary.py"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-history.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-trend-change-frequency-summary.json"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW TREND CHANGE FREQUENCY: FAIL - {message}")


def main() -> int:
    fixture = {
        "changes": [
            {"receipt_id": "c1", "generated_at": "2026-07-14T01:00:00+00:00", "change_state": "UNCHANGED"},
            {"receipt_id": "c2", "generated_at": "2026-07-14T02:00:00+00:00", "change_state": "CHANGED"},
            {"receipt_id": "c3", "generated_at": "2026-07-14T03:00:00+00:00", "change_state": "UNCHANGED"},
            {"receipt_id": "c4", "generated_at": "2026-07-14T04:00:00+00:00", "change_state": "CHANGED"},
        ]
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    OUT.unlink(missing_ok=True)
    try:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "generator exited non-zero")
        if not OUT.exists():
            fail("summary was not generated")
        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("frequency_class") != "FREQUENT_CHANGE_OBSERVED":
            fail("frequency class mismatch")
        if data.get("recency_class") != "CURRENT_RECEIPT_CHANGED":
            fail("recency class mismatch")
        evidence = data.get("evidence", {})
        if evidence.get("evaluated_entries") != 4 or evidence.get("changed_count") != 2:
            fail("evidence counts mismatch")
        if evidence.get("observed_change_ratio") != 0.5:
            fail("observed ratio mismatch")
        scope = data.get("evaluation_scope", {})
        if scope.get("descriptive_only") is not True:
            fail("descriptive_only must be true")
        if scope.get("predictive_claim") is not False or scope.get("causal_claim_beyond_receipt_fields") is not False:
            fail("claim boundaries mismatch")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("evaluation_owner") != "canonical build-pages job":
            fail("evaluation owner mismatch")
        if data.get("public_endpoint") != "/status/canonical-workflow-trend-change-frequency-summary.json":
            fail("public endpoint mismatch")
        print("CANONICAL WORKFLOW TREND CHANGE FREQUENCY: PASS - entries=4 ratio=0.5 manual_tasks=0")
        return 0
    finally:
        HISTORY.unlink(missing_ok=True)
        OUT.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
