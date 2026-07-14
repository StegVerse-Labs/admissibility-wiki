#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_observation_rollup.py"
OUT = ROOT / "static" / "status" / "canonical-workflow-observation-rollup.json"
STATUS_DIR = ROOT / "static" / "status"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION ROLLUP: FAIL - {message}")


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    created: list[Path] = []
    required_names = [
        "canonical-workflow-observation-receipt.json",
        "canonical-workflow-observation-history.json",
        "canonical-workflow-health-summary.json",
        "canonical-workflow-health-transition-receipt.json",
        "canonical-workflow-health-transition-history.json",
        "canonical-workflow-health-transition-trend.json",
        "canonical-workflow-health-transition-trend-change-receipt.json",
        "canonical-workflow-health-transition-trend-change-history.json",
        "canonical-workflow-trend-change-frequency-summary.json",
        "canonical-workflow-trend-change-frequency-change-receipt.json",
        "canonical-workflow-trend-change-frequency-change-history.json",
        "canonical-workflow-frequency-change-stability-summary.json",
        "canonical-workflow-frequency-change-stability-change-receipt.json",
        "canonical-workflow-frequency-change-stability-change-history.json",
        "canonical-workflow-stability-change-frequency-summary.json",
        "canonical-workflow-stability-change-frequency-change-receipt.json",
        "canonical-workflow-stability-change-frequency-change-history.json",
    ]
    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    for name in required_names:
        path = STATUS_DIR / name
        if not path.exists():
            path.write_text("{}\n", encoding="utf-8")
            created.append(path)
    OUT.unlink(missing_ok=True)

    try:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stdout or "generator exited non-zero")
        if not OUT.exists():
            fail("rollup was not generated")

        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("terminal_envelope") is not True:
            fail("terminal_envelope must be true")
        if data.get("recursive_derivative_expansion_allowed") is not False:
            fail("recursive derivative expansion must be disabled")
        if data.get("completeness_state") != "COMPLETE_LOCAL_CHAIN":
            fail("complete fixture chain must produce COMPLETE_LOCAL_CHAIN")
        if data.get("artifact_count") != 17:
            fail("artifact_count must be 17")
        if data.get("present_count") != 17 or data.get("missing_count") != 0:
            fail("presence counts mismatch")
        if data.get("missing_artifact_ids") != []:
            fail("missing_artifact_ids must be empty")
        artifacts = data.get("artifacts", [])
        if len(artifacts) != 17:
            fail("artifact pointer count mismatch")
        if any(item.get("local_presence") != "PRESENT" for item in artifacts):
            fail("all fixture artifacts must be PRESENT")
        if any(item.get("public_reachability") != "NOT_OBSERVED_UNTIL_POST_DEPLOY_VERIFICATION" for item in artifacts):
            fail("public reachability boundary mismatch")
        if any(item.get("semantic_reclassification_performed") is not False for item in artifacts):
            fail("rollup must not semantically reclassify artifacts")
        if data.get("generation_owner") != "canonical build-pages job":
            fail("generation owner mismatch")
        if data.get("next_evaluation") != "next repository-owned canonical workflow trigger":
            fail("next evaluation is not automation-owned")
        if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
            fail("no-manual boundary violated")
        if data.get("public_endpoint") != "/status/canonical-workflow-observation-rollup.json":
            fail("public endpoint mismatch")
        for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
            if data.get(key) is not False:
                fail(f"{key} must be false")

        print("CANONICAL WORKFLOW OBSERVATION ROLLUP: PASS - terminal=true artifacts=17 manual_tasks=0")
        return 0
    finally:
        OUT.unlink(missing_ok=True)
        for path in created:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
