#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "workflow_manifest.json"
LOCAL_ENTRYPOINT = "python scripts/run_canonical_validation.py"

REQUIRED_COMMANDS = [
    "python scripts/check_workflow_sprawl.py",
    "python scripts/generate_external_framework_reports.py",
    "python scripts/generate_external_framework_results.py",
    "python scripts/generate_external_framework_page_metadata.py",
    "python scripts/generate_external_framework_page_mapping.py",
    "python scripts/generate_external_framework_page_status.py",
    "python scripts/check_chain_status_continuation.py",
    "python scripts/check_continuation_bundle.py",
    "python scripts/check_chain_snapshot.py",
    "python scripts/check_chain_snapshot_receipt.py",
    "python scripts/check_chain_auto.py",
    "python scripts/check_blocked_destination_record.py",
    "python scripts/check_goal_state.py",
    "python scripts/check_workflow_manifest.py",
    "python scripts/check_external_frameworks_index.py",
    "python scripts/check_external_framework_manifests.py",
    "python scripts/check_external_framework_terminology.py",
    "python scripts/check_external_framework_reports.py",
    "python scripts/check_external_framework_report_coverage.py",
    "python scripts/check_external_framework_report_generation.py",
    "python scripts/check_external_framework_results_page.py",
    "python scripts/check_external_framework_page_metadata.py",
    "python scripts/check_external_framework_page_mapping.py",
    "python scripts/check_external_framework_page_status.py",
    "python scripts/check_external_framework_expansion_policy.py",
    "python scripts/check_ci_evidence.py",
    "python scripts/check_guardian_destination.py",
]

EXPECTED = {
    "workflow_manifest": "WORKFLOW MANIFEST: PASS",
    "external_framework_report_coverage": "EXTERNAL FRAMEWORK REPORT COVERAGE: PASS",
    "external_framework_report_generation": "EXTERNAL FRAMEWORK REPORT GENERATION: PASS",
    "external_framework_results_page": "EXTERNAL FRAMEWORK RESULTS PAGE: PASS",
    "external_framework_page_metadata": "EXTERNAL FRAMEWORK PAGE METADATA: PASS",
    "external_framework_page_mapping": "EXTERNAL FRAMEWORK PAGE MAPPING: PASS",
    "external_framework_page_status": "EXTERNAL FRAMEWORK PAGE STATUS: PASS",
    "external_framework_expansion_policy": "EXTERNAL FRAMEWORK EXPANSION POLICY: PASS",
    "ci_evidence": "CI EVIDENCE: PASS",
}


def main() -> int:
    failures: list[str] = []
    if not MANIFEST.exists():
        print("WORKFLOW MANIFEST: FAIL")
        print("- workflow_manifest.json unavailable")
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("manifest_id") != "ADMISSIBILITY-WIKI-WORKFLOW-001":
        failures.append("manifest id mismatch")
    if manifest.get("schema_version") != "1.3":
        failures.append("schema version mismatch")

    workflows = manifest.get("canonical_workflows", [])
    if len(workflows) != 1:
        failures.append("canonical workflow count mismatch")
    elif workflows[0].get("path") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("canonical workflow path mismatch")

    if manifest.get("local_validation_entrypoint") != LOCAL_ENTRYPOINT:
        failures.append("local validation entrypoint mismatch")
    if LOCAL_ENTRYPOINT in manifest.get("verification_commands", []):
        failures.append("local validation entrypoint must not recurse through verification_commands")
    if not (ROOT / "scripts" / "run_canonical_validation.py").exists():
        failures.append("local validation entrypoint script missing")

    commands = manifest.get("verification_commands", [])
    for command in REQUIRED_COMMANDS:
        if command not in commands:
            failures.append(f"command unavailable: {command}")

    expected = manifest.get("expected_results", {})
    for key, value in EXPECTED.items():
        if expected.get(key) != value:
            failures.append(f"expected result mismatch: {key}")

    boundary = manifest.get("boundary", {})
    if boundary.get("active_workflow_count") != 1:
        failures.append("active workflow count mismatch")
    if boundary.get("canonical_workflow_installed") is not True:
        failures.append("canonical workflow boundary mismatch")
    if boundary.get("manual_workflow_install_required") is not False:
        failures.append("manual workflow boundary mismatch")
    if boundary.get("local_validation_entrypoint_is_authority") is not False:
        failures.append("local validation entrypoint authority boundary mismatch")
    if boundary.get("external_framework_outputs_are_authority") is not False:
        failures.append("external output boundary mismatch")
    if boundary.get("generated_framework_results_are_authority") is not False:
        failures.append("generated results authority boundary mismatch")
    if boundary.get("generated_framework_page_metadata_is_authority") is not False:
        failures.append("generated metadata authority boundary mismatch")
    if boundary.get("generated_framework_page_mapping_is_authority") is not False:
        failures.append("generated mapping authority boundary mismatch")
    if boundary.get("generated_framework_page_status_is_authority") is not False:
        failures.append("generated page status authority boundary mismatch")

    print("WORKFLOW MANIFEST:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
