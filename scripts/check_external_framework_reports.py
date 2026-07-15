#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"

REQUIRED_STATUS_KEYS = [
    "framework_identity",
    "source_reference",
    "source_version",
    "allowed_use_boundary",
    "claims",
    "non_claims",
    "input_artifact_type",
    "output_artifact_type",
    "actor_or_authority_model",
    "evidence_model",
    "policy_or_rule_model",
    "delegation_model",
    "decision_or_result_model",
    "execution_authority_claim",
    "receipt_or_trace_model",
    "reconstruction_model",
    "SPE_overlap",
    "StegVerse_ecosystem_overlap",
    "fail_closed_conditions",
]

ALLOWED_SCHEMA_VERSIONS = {"0.2", "0.3", "0.4", "0.5", "0.6", "0.7"}
ALLOWED_RESULTS = {
    "COMPATIBILITY_EVIDENCE_ONLY",
    "COMPATIBILITY_EVIDENCE_ONLY_PARAMETERIZED_BOUNDARY_CASE_PARTIAL",
    "SOURCE_BLOCKED_FAIL_CLOSED",
}
ALLOWED_EVIDENCE_CLASSES = {
    "MENTION_ONLY",
    "AUTHOR_COMMENTARY",
    "SOURCE_REVIEWED",
    "ARTIFACT_REVIEWED",
    "PARAMETERIZED_OBSERVATION",
    "REPRODUCIBLE_COMPARATIVE_TEST",
}
REPRODUCIBILITY_FIELDS = {
    "shared_test_vector",
    "raw_output",
    "timestamp",
    "runtime_configuration",
    "source_version_or_hash",
    "replay_commands",
    "declared_expected_outcome",
    "independent_reproduction",
}
ALLOWED_STATUS_VALUES = {
    "PRESENT",
    "PRESENT_AS_EXTERNAL_CLAIMS",
    "PRESENT_REPOSITORY_REFERENCE",
    "PUBLIC_SITE_CURRENT_AS_OF_2026_07_06",
    "PUBLIC_SITE_CURRENT_AS_OF_2026_07_06_PLUS_LIVE_DEMO_CAPTURE_2026_07_07",
    "DENIED_BY_BOUNDARY",
    "ADJACENT",
    "PARTIAL",
}
SOURCE_BLOCKED_STATUS_VALUES = {
    "SOURCE_REQUIRED",
    "PROVISIONAL",
    "MISSING",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def allowed_status_values_for_result(result: str | None) -> set[str]:
    values = set(ALLOWED_STATUS_VALUES)
    if result == "SOURCE_BLOCKED_FAIL_CLOSED":
        values.update(SOURCE_BLOCKED_STATUS_VALUES)
    return values


def check_evidence_gate(report: dict[str, Any], framework_id: str, failures: list[str]) -> None:
    gate = report.get("evidence_gate")
    if not isinstance(gate, dict):
        failures.append(f"missing evidence gate: {framework_id}")
        return

    evidence_class = gate.get("evidence_class")
    if evidence_class not in ALLOWED_EVIDENCE_CLASSES:
        failures.append(f"invalid evidence class {evidence_class}: {framework_id}")

    required_fields = gate.get("required_fields")
    if not isinstance(required_fields, dict):
        failures.append(f"missing evidence required-fields map: {framework_id}")
        return

    missing_required_keys = sorted(REPRODUCIBILITY_FIELDS - set(required_fields))
    if missing_required_keys:
        failures.append(f"missing reproducibility keys for {framework_id}: {', '.join(missing_required_keys)}")

    missing_fields = gate.get("missing_fields")
    if not isinstance(missing_fields, list):
        failures.append(f"missing evidence missing-fields list: {framework_id}")
        missing_fields = []

    expected_missing = sorted(key for key in REPRODUCIBILITY_FIELDS if required_fields.get(key) is not True)
    if sorted(missing_fields) != expected_missing:
        failures.append(f"evidence missing-fields mismatch: {framework_id}")

    reproducible = gate.get("independently_reproducible") is True
    comparative_claim = gate.get("comparative_testing_claim_allowed") is True
    all_fields_present = all(required_fields.get(key) is True for key in REPRODUCIBILITY_FIELDS)

    if reproducible != all_fields_present:
        failures.append(f"reproducibility boolean mismatch: {framework_id}")
    if comparative_claim != reproducible:
        failures.append(f"comparative claim mismatch: {framework_id}")
    if evidence_class == "REPRODUCIBLE_COMPARATIVE_TEST" and not reproducible:
        failures.append(f"reproducible class without complete gate: {framework_id}")
    if reproducible and evidence_class != "REPRODUCIBLE_COMPARATIVE_TEST":
        failures.append(f"complete gate not promoted to reproducible class: {framework_id}")


def main() -> int:
    failures: list[str] = []

    if not REGISTRY.exists():
        failures.append("missing registry")
    if not REPORT_DIR.exists():
        failures.append("missing reports directory")

    if failures:
        print("EXTERNAL FRAMEWORK REPORTS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = load_json(REGISTRY)
    known_ids = {entry.get("framework_id") for entry in registry.get("entries", [])}
    reports = sorted(REPORT_DIR.glob("*.compatibility.json"))
    if not reports:
        failures.append("no compatibility reports")

    for report_path in reports:
        report = load_json(report_path)
        framework_id = report.get("framework_id")
        result = report.get("result")
        allowed_status_values = allowed_status_values_for_result(result)

        if report.get("artifact_type") != "external_framework_compatibility_report":
            failures.append(f"artifact type mismatch: {report_path.relative_to(ROOT)}")
        if report.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
            failures.append(f"schema version mismatch: {report_path.relative_to(ROOT)}")
        if framework_id not in known_ids:
            failures.append(f"unknown framework id: {framework_id}")
        if report.get("testbench_basis") != "transition_table_elements":
            failures.append(f"basis mismatch: {framework_id}")
        if result not in ALLOWED_RESULTS:
            failures.append(f"result mismatch: {framework_id}")
        if not report.get("cycle_status"):
            failures.append(f"missing cycle status: {framework_id}")

        manifest = report.get("framework_manifest")
        if not isinstance(manifest, str) or not (ROOT / manifest).exists():
            failures.append(f"missing manifest reference: {framework_id}")
        status = report.get("transition_table_mapping_status", {})
        for key in REQUIRED_STATUS_KEYS:
            if key not in status:
                failures.append(f"missing transition table status {key}: {framework_id}")
            elif status[key] not in allowed_status_values:
                failures.append(f"unexpected transition table status {key}={status[key]}: {framework_id}")

        if result != "SOURCE_BLOCKED_FAIL_CLOSED":
            source_blocked_values = sorted({value for value in status.values() if value in SOURCE_BLOCKED_STATUS_VALUES})
            if source_blocked_values:
                failures.append(
                    f"source-blocked status outside SOURCE_BLOCKED_FAIL_CLOSED result: {framework_id}: "
                    + ", ".join(source_blocked_values)
                )

        check_evidence_gate(report, str(framework_id), failures)

        if framework_id == "morrison-runtime":
            observations = report.get("runtime_governance_benchmark_observations", [])
            observed_ids = {item.get("id") for item in observations if isinstance(item, dict)}
            for required_id in ["MRG-BENCH-RG-003-PREPARE-001", "MRG-BENCH-RG-002-EXECUTE-001"]:
                if required_id not in observed_ids:
                    failures.append(f"missing Morrison benchmark observation: {required_id}")
            if report.get("benchmark_suite") != "static/external-frameworks/runtime-governance-benchmark-suite.v0.1.json":
                failures.append("Morrison report missing benchmark suite reference")
            if report.get("evidence_gate", {}).get("evidence_class") != "PARAMETERIZED_OBSERVATION":
                failures.append("Morrison evidence must remain PARAMETERIZED_OBSERVATION until full reproducibility gate passes")

        for overlap_key in ["SPE_overlap_result", "StegVerse_ecosystem_overlap_result"]:
            value = report.get(overlap_key)
            if not isinstance(value, dict) or not value:
                failures.append(f"missing overlap result {overlap_key}: {framework_id}")

        boundary = report.get("boundary", {})
        for key in [
            "certification_claim",
            "endorsement_claim",
            "execution_authority_claim",
            "commit_time_authority_claim",
            "compatibility_report_is_authority",
        ]:
            if boundary.get(key) is not False:
                failures.append(f"boundary false mismatch {key}: {framework_id}")
        if boundary.get("missing_or_partial_fields_fail_closed") is not True:
            failures.append(f"missing fail-closed boundary: {framework_id}")

    print("EXTERNAL FRAMEWORK REPORTS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
