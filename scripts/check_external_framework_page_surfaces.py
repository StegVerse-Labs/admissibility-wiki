#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "external-frameworks" / "generated-page-surfaces.json"
SUMMARY_CHECK = ROOT / "scripts" / "check_generated_page_validation_summary.py"

REQUIRED_ACTIVE = {
    "metadata": (
        "scripts/generate_external_framework_page_metadata.py",
        "scripts/check_external_framework_page_metadata.py",
    ),
    "mapping": (
        "scripts/generate_external_framework_page_mapping.py",
        "scripts/check_external_framework_page_mapping.py",
    ),
    "page_status": (
        "scripts/generate_external_framework_page_status.py",
        "scripts/check_external_framework_page_status.py",
    ),
    "analysis_boundary": (
        "scripts/generate_external_framework_page_analysis_boundary.py",
        "scripts/check_external_framework_page_analysis_boundary.py",
    ),
    "closeout_state": (
        "scripts/generate_generated_page_closeout_state.py",
        "scripts/check_generated_page_closeout_state_generation.py",
    ),
    "workflow_entrypoint_migration": (
        "docs/external-frameworks/generated-page-workflow-entrypoint-migration.json",
        "scripts/check_generated_page_workflow_entrypoint_migration.py",
    ),
    "entrypoint_closeout_propagation": (
        "docs/external-frameworks/generated-page-entrypoint-closeout-propagation.json",
        "scripts/check_generated_page_entrypoint_closeout_propagation.py",
    ),
    "release_evidence_bundle": (
        "docs/external-frameworks/generated-page-release-evidence-bundle.json",
        "scripts/check_generated_page_release_evidence_bundle.py",
    ),
}


def main() -> int:
    failures: list[str] = []
    if not STATE.exists():
        print("EXTERNAL FRAMEWORK PAGE SURFACES: FAIL")
        print("- generated-page-surfaces.json missing")
        return 1

    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_surfaces":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")

    active = {item.get("surface_id"): item for item in data.get("active_surfaces", [])}
    for surface_id, paths in REQUIRED_ACTIVE.items():
        item = active.get(surface_id)
        if not item:
            failures.append(f"missing active surface: {surface_id}")
            continue
        generator, validator = paths
        if item.get("generator") != generator:
            failures.append(f"generator mismatch: {surface_id}")
        if item.get("validator") != validator:
            failures.append(f"validator mismatch: {surface_id}")
        if item.get("manual_task_required") is not False:
            failures.append(f"manual task boundary mismatch: {surface_id}")
        for path in paths:
            if not (ROOT / path).exists():
                failures.append(f"referenced file missing: {path}")

    boundary = data.get("boundary", {})
    if boundary.get("generated_surfaces_are_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_page_surface_wiring_required") is not False:
        failures.append("manual wiring boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

    if SUMMARY_CHECK.exists():
        result = subprocess.run(["python", str(SUMMARY_CHECK)], check=False)
        if result.returncode != 0:
            failures.append("validation summary check failed")

    print("EXTERNAL FRAMEWORK PAGE SURFACES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
