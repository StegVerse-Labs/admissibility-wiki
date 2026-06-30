#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "docs" / "external-frameworks" / "generated-page-validation-summary.json"
PROGRESS_CHECK = ROOT / "scripts" / "check_generated_page_progress.py"

REQUIRED_VALIDATORS = [
    "scripts/check_external_framework_page_analysis_boundary.py",
    "scripts/check_external_framework_page_candidates.py",
    "scripts/check_external_framework_page_surfaces.py",
    "scripts/check_generated_page_surfaces_handoff.py",
    "scripts/check_generated_page_surfaces_root_addendum.py",
]


def main() -> int:
    failures: list[str] = []
    if not SUMMARY.exists():
        print("GENERATED PAGE VALIDATION SUMMARY: FAIL")
        print("- summary missing")
        return 1

    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_validation_summary":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("validated_through") != "scripts/check_external_framework_page_status.py":
        failures.append("validated-through mismatch")

    for key in ["surface_inventory", "surface_handoff", "root_addendum"]:
        path = data.get(key)
        if not isinstance(path, str) or not (ROOT / path).exists():
            failures.append(f"missing referenced path: {key}")

    validators = data.get("validators_called_by_page_status", [])
    for validator in REQUIRED_VALIDATORS:
        if validator not in validators:
            failures.append(f"missing validator: {validator}")
        elif not (ROOT / validator).exists():
            failures.append(f"validator file missing: {validator}")

    removed = data.get("manual_tasks_removed", [])
    for task in ["generated_surface_discovery", "generated_surface_handoff_discovery", "generated_surface_root_handoff_discovery"]:
        if task not in removed:
            failures.append(f"manual task not removed: {task}")

    boundary = data.get("boundary", {})
    if boundary.get("validation_summary_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")
    if boundary.get("manual_generated_surface_discovery_required") is not False:
        failures.append("manual discovery boundary mismatch")

    if PROGRESS_CHECK.exists():
        result = subprocess.run(["python", str(PROGRESS_CHECK)], check=False)
        if result.returncode != 0:
            failures.append("generated page progress check failed")

    print("GENERATED PAGE VALIDATION SUMMARY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
