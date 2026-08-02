#!/usr/bin/env python3
"""Execute the bounded AGCP Registry review queue and persist continuation state."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "static/external-frameworks/agcp-registry-assessment.v0.1.json"
VALIDATOR = ROOT / "scripts/check_agcp_registry_assessment.py"
REPORT = ROOT / "reports/agcp-registry-task-execution.json"


def main() -> int:
    failures: list[str] = []
    if not ASSESSMENT.exists():
        failures.append(str(ASSESSMENT.relative_to(ROOT)))
        data: dict[str, object] = {}
    else:
        try:
            data = json.loads(ASSESSMENT.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid assessment: {exc}")
            data = {}

    validator_result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    ) if VALIDATOR.exists() else None

    if validator_result is None:
        failures.append(str(VALIDATOR.relative_to(ROOT)))
        validator_exit = 127
        validator_output = "validator missing"
    else:
        validator_exit = validator_result.returncode
        validator_output = validator_result.stdout.rstrip()
        if validator_exit != 0:
            failures.append("assessment validator failed")

    capture = data.get("source_capture", {}) if isinstance(data, dict) else {}
    verified = isinstance(capture, dict) and capture.get("independently_verified") is True
    planned_release_observed = isinstance(capture, dict) and capture.get("planned_release_observed") is True

    if failures:
        lifecycle_state = "FAILED"
        next_task = "repair the exact failed repository path recorded in failures"
    elif verified and planned_release_observed:
        lifecycle_state = "COMPLETE"
        next_task = "preserve canonical workflow, deployment, and public-route evidence"
    elif planned_release_observed and not verified:
        lifecycle_state = "REVIEW_REQUIRED"
        next_task = "run repository-owned independent source verification against the observed release evidence"
    else:
        lifecycle_state = "BLOCKED"
        next_task = "re-observe canonical AGCP source and release evidence on the next scheduled repository cycle"

    payload = {
        "schema_version": "agcp-registry-task-execution.v1",
        "task_id": "ADMISSIBILITY-AGCP-001",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "owner_repository": "StegVerse-Labs/admissibility-wiki",
        "trigger": "wiki-public-anchor task mesh or canonical validation workflow",
        "inputs": [
            str(ASSESSMENT.relative_to(ROOT)),
            str(VALIDATOR.relative_to(ROOT)),
            "docs/external-frameworks/agcp-registry.md",
            "docs/external-frameworks/AGCP_REGISTRY_MIRROR_HANDOFF.md"
        ],
        "state": lifecycle_state,
        "validator_exit_code": validator_exit,
        "validator_output": validator_output,
        "failures": failures,
        "release_condition": {
            "planned_release_observed": planned_release_observed,
            "independently_verified": verified,
            "machine_observable": True
        },
        "next_executable_task": {
            "description": next_task,
            "owner": "repository_canonical_workflow",
            "location": "scripts/run_agcp_registry_tasks.py"
        },
        "duplicate_execution_control": {
            "canonical_task_id": "ADMISSIBILITY-AGCP-001",
            "single_report_path": str(REPORT.relative_to(ROOT)),
            "append_only_parallel_queue_forbidden": True
        },
        "manual_user_tasks_required": [],
        "external_tasks_exist": False,
        "development_halted": False,
        "authority_boundary": {
            "review_is_certification": False,
            "review_is_admissibility": False,
            "review_grants_execution_authority": False,
            "review_grants_publication_or_release_authority": False
        }
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"AGCP REGISTRY TASK: {lifecycle_state}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
