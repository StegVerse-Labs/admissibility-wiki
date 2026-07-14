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

REQUIRED_NAMES = [
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


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION ROLLUP: FAIL - {message}")


def run_generator() -> dict:
    OUT.unlink(missing_ok=True)
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
        fail("rollup was not generated")
    return json.loads(OUT.read_text(encoding="utf-8"))


def check_common(data: dict) -> None:
    if data.get("terminal_envelope") is not True:
        fail("terminal_envelope must be true")
    if data.get("recursive_derivative_expansion_allowed") is not False:
        fail("recursive derivative expansion must be disabled")
    if data.get("artifact_count") != 17:
        fail("artifact_count must be 17")
    artifacts = data.get("artifacts", [])
    if len(artifacts) != 17:
        fail("artifact pointer count mismatch")
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


def main() -> int:
    if not GENERATOR.exists():
        fail("generator is missing")

    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    backups: dict[Path, bytes | None] = {}
    paths = [STATUS_DIR / name for name in REQUIRED_NAMES]
    for path in paths:
        backups[path] = path.read_bytes() if path.exists() else None
        path.write_text("{}\n", encoding="utf-8")

    missing_path = STATUS_DIR / REQUIRED_NAMES[-1]
    try:
        complete = run_generator()
        check_common(complete)
        if complete.get("completeness_state") != "COMPLETE_LOCAL_CHAIN":
            fail("complete fixture chain must produce COMPLETE_LOCAL_CHAIN")
        if complete.get("present_count") != 17 or complete.get("missing_count") != 0:
            fail("complete presence counts mismatch")
        if complete.get("missing_artifact_ids") != []:
            fail("complete missing_artifact_ids must be empty")
        if any(item.get("local_presence") != "PRESENT" for item in complete.get("artifacts", [])):
            fail("all complete fixture artifacts must be PRESENT")

        missing_path.unlink()
        incomplete = run_generator()
        check_common(incomplete)
        if incomplete.get("completeness_state") != "FAIL_CLOSED_INCOMPLETE_LOCAL_CHAIN":
            fail("missing artifact must produce FAIL_CLOSED_INCOMPLETE_LOCAL_CHAIN")
        if incomplete.get("present_count") != 16 or incomplete.get("missing_count") != 1:
            fail("incomplete presence counts mismatch")
        if incomplete.get("missing_artifact_ids") != ["stability_change_frequency_change_history"]:
            fail("incomplete missing_artifact_ids mismatch")
        missing_records = [
            item for item in incomplete.get("artifacts", [])
            if item.get("artifact_id") == "stability_change_frequency_change_history"
        ]
        if len(missing_records) != 1 or missing_records[0].get("local_presence") != "MISSING":
            fail("missing artifact pointer must remain explicit")

        print(
            "CANONICAL WORKFLOW OBSERVATION ROLLUP: PASS - "
            "terminal=true complete_path=PASS incomplete_path=FAIL_CLOSED artifacts=17 manual_tasks=0"
        )
        return 0
    finally:
        OUT.unlink(missing_ok=True)
        for path, content in backups.items():
            if content is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(content)


if __name__ == "__main__":
    raise SystemExit(main())
