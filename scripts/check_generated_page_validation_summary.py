#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "docs" / "external-frameworks" / "generated-page-validation-summary.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
PROGRESS_CHECK = ROOT / "scripts" / "check_generated_page_progress.py"
SUMMARY_GENERATION_CHECK = ROOT / "scripts" / "check_generated_page_validation_summary_generation.py"

REQUIRED_VALIDATORS = [
    "scripts/check_external_framework_page_analysis_boundary.py",
    "scripts/check_external_framework_page_candidates.py",
    "scripts/check_external_framework_page_surfaces.py",
    "scripts/check_generated_page_surfaces_handoff.py",
    "scripts/check_generated_page_surfaces_root_addendum.py",
    "scripts/check_generated_page_workflow_entrypoint_migration.py",
    "scripts/check_generated_page_entrypoint_closeout_propagation.py",
    "scripts/check_generated_page_closeout_state_generation.py",
]


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if path.exists():
        result = subprocess.run(["python", str(path)], check=False)
        if result.returncode != 0:
            failures.append(f"{label} failed")


def main() -> int:
    failures: list[str] = []
    if not SUMMARY.exists():
        print("GENERATED PAGE VALIDATION SUMMARY: FAIL")
        print("- summary missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE VALIDATION SUMMARY: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_validation_summary":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
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
    for task in ["generated_surface_discovery", "generated_surface_handoff_discovery", "generated_surface_root_handoff_discovery", "generated_closeout_state_reconstruction"]:
        if task not in removed:
            failures.append(f"manual task not removed: {task}")

    boundary = data.get("boundary", {})
    if boundary.get("validation_summary_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")
    if boundary.get("manual_generated_surface_discovery_required") is not False:
        failures.append("manual discovery boundary mismatch")
    if model.get("boundary", {}).get("manual_state_reconstruction_required") is not False:
        failures.append("state model manual reconstruction boundary mismatch")

    run_check(SUMMARY_GENERATION_CHECK, "validation summary generation check", failures)
    run_check(PROGRESS_CHECK, "generated page progress check", failures)

    print("GENERATED PAGE VALIDATION SUMMARY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
