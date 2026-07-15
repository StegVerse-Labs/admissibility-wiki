#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"

STATUS_FIELDS = [
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

ENRICHED_RESULTS = {
    "COMPATIBILITY_EVIDENCE_ONLY_PARAMETERIZED_BOUNDARY_CASE_PARTIAL",
}

EVIDENCE_CLASSES = {
    "MENTION_ONLY",
    "AUTHOR_COMMENTARY",
    "SOURCE_REVIEWED",
    "ARTIFACT_REVIEWED",
    "PARAMETERIZED_OBSERVATION",
    "REPRODUCIBLE_COMPARATIVE_TEST",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def status_for_complete(manifest: dict[str, Any]) -> dict[str, str]:
    mapping = manifest.get("transition_table_mapping", {})
    status: dict[str, str] = {}
    for field in STATUS_FIELDS:
        value = mapping.get(field)
        if field == "execution_authority_claim" and value is False:
            status[field] = "DENIED_BY_BOUNDARY"
        elif value in (None, ""):
            status[field] = "MISSING"
        else:
            status[field] = "PRESENT"
    return status


def status_for_source_blocked(manifest: dict[str, Any]) -> dict[str, str]:
    mapping = manifest.get("transition_table_mapping", {})
    source_required = {
        "source_reference",
        "source_version",
        "actor_or_authority_model",
        "evidence_model",
        "delegation_model",
        "SPE_overlap",
        "StegVerse_ecosystem_overlap",
    }
    provisional = {
        "allowed_use_boundary",
        "claims",
        "input_artifact_type",
    }
    status: dict[str, str] = {}
    for field in STATUS_FIELDS:
        value = mapping.get(field)
        if field == "execution_authority_claim" and value is False:
            status[field] = "DENIED_BY_BOUNDARY"
        elif field in source_required:
            status[field] = "SOURCE_REQUIRED"
        elif field in provisional:
            status[field] = "PROVISIONAL"
        elif value in (None, ""):
            status[field] = "MISSING"
        else:
            status[field] = "PRESENT"
    return status


def evidence_gate(report: dict[str, Any]) -> dict[str, Any]:
    observations = report.get("runtime_governance_benchmark_observations", [])
    parameterized_cases = report.get("parameterized_boundary_cases", [])
    all_cases = [*observations, *parameterized_cases]

    has_official_source = bool(report.get("sources")) or report.get("transition_table_mapping_status", {}).get("source_reference") == "PRESENT"
    has_artifact = any(
        bool(case.get(field))
        for case in all_cases
        for field in ("raw_audit_payload_attached", "screenshot_attached", "observed_output_attached")
    )
    has_parameterized_case = bool(all_cases)
    has_raw_output = bool(all_cases) and all(bool(case.get("raw_audit_payload_attached") or case.get("observed_output_attached")) for case in all_cases)
    has_timestamp = bool(all_cases) and all(bool(case.get("timestamp_attached")) for case in all_cases)
    has_runtime_config = bool(all_cases) and all(bool(case.get("runtime_configuration_attached")) for case in all_cases)
    has_source_hash = bool(all_cases) and all(bool(case.get("source_hash_attached")) for case in all_cases)
    has_replay_command = bool(report.get("replay_commands"))
    has_expected_outcome = bool(all_cases) and all(bool(case.get("stegverse_expected_posture") or case.get("expected_outcome")) for case in all_cases)
    independently_reproduced = bool(report.get("independent_reproduction", {}).get("completed"))

    reproducible = all([
        has_parameterized_case,
        has_raw_output,
        has_timestamp,
        has_runtime_config,
        has_source_hash,
        has_replay_command,
        has_expected_outcome,
        independently_reproduced,
    ])

    if reproducible:
        evidence_class = "REPRODUCIBLE_COMPARATIVE_TEST"
    elif has_parameterized_case:
        evidence_class = "PARAMETERIZED_OBSERVATION"
    elif has_artifact:
        evidence_class = "ARTIFACT_REVIEWED"
    elif has_official_source:
        evidence_class = "SOURCE_REVIEWED"
    elif report.get("author_commentary"):
        evidence_class = "AUTHOR_COMMENTARY"
    else:
        evidence_class = "MENTION_ONLY"

    missing = []
    required = {
        "shared_test_vector": has_parameterized_case,
        "raw_output": has_raw_output,
        "timestamp": has_timestamp,
        "runtime_configuration": has_runtime_config,
        "source_version_or_hash": has_source_hash,
        "replay_commands": has_replay_command,
        "declared_expected_outcome": has_expected_outcome,
        "independent_reproduction": independently_reproduced,
    }
    for field, present in required.items():
        if not present:
            missing.append(field)

    return {
        "evidence_class": evidence_class,
        "independently_reproducible": reproducible,
        "comparative_testing_claim_allowed": reproducible,
        "required_fields": required,
        "missing_fields": missing,
    }


def build_base_report(entry: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    source_blocked = entry.get("testbench_state") == "SOURCE_BLOCKED_FAIL_CLOSED"
    result = "SOURCE_BLOCKED_FAIL_CLOSED" if source_blocked else "COMPATIBILITY_EVIDENCE_ONLY"
    cycle_status = "SOURCE_BLOCKED_CYCLE_RECORDED" if source_blocked else "FIRST_FRAMEWORK_CYCLE_COMPLETE"
    status = status_for_source_blocked(manifest) if source_blocked else status_for_complete(manifest)

    boundary = {
        "certification_claim": False,
        "endorsement_claim": False,
        "execution_authority_claim": False,
        "commit_time_authority_claim": False,
        "compatibility_report_is_authority": False,
        "missing_or_partial_fields_fail_closed": True,
    }
    if source_blocked:
        boundary["official_source_required_for_completion"] = True

    action = (
        "Add an official public source reference before upgrading this report from SOURCE_BLOCKED_FAIL_CLOSED."
        if source_blocked
        else "Add executable observations, raw outputs, pinned versions, replay commands, and independent reproduction before making comparative-testing claims."
    )

    report = {
        "artifact_type": "external_framework_compatibility_report",
        "schema_version": "0.7",
        "framework_id": entry["framework_id"],
        "framework_manifest": entry["manifest_path"],
        "registry": "docs/external-frameworks/index.json",
        "testbench_basis": "transition_table_elements",
        "result": result,
        "cycle_status": cycle_status,
        "transition_table_mapping_status": status,
        "SPE_overlap_result": manifest.get("SPE_overlap", {}),
        "StegVerse_ecosystem_overlap_result": manifest.get("StegVerse_ecosystem_overlap", {}),
        "boundary": boundary,
        "next_required_action": action,
    }
    report["evidence_gate"] = evidence_gate(report)
    return report


def build_report(entry: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    return build_base_report(entry, manifest)


def preserve_enriched_report(base: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    if not existing or existing.get("result") not in ENRICHED_RESULTS:
        return base

    report = dict(existing)
    for key in [
        "artifact_type",
        "framework_id",
        "framework_manifest",
        "registry",
        "testbench_basis",
    ]:
        report[key] = base[key]

    report["schema_version"] = "0.7"
    boundary = dict(report.get("boundary", {}))
    boundary.update(base["boundary"])
    report["boundary"] = boundary
    report["evidence_gate"] = evidence_gate(report)
    report["next_required_action"] = (
        "Attach every missing reproducibility field listed in evidence_gate.missing_fields, then complete an independent rerun before claiming comparative testing."
    )
    return report


def main() -> int:
    registry = read_json(REGISTRY)
    for entry in registry.get("entries", []):
        manifest_path = entry.get("manifest_path")
        if not isinstance(manifest_path, str):
            continue
        manifest = read_json(ROOT / manifest_path)
        out = REPORT_DIR / f"{entry['framework_id']}.compatibility.json"
        existing = read_json(out) if out.exists() else None
        report = preserve_enriched_report(build_base_report(entry, manifest), existing)
        if report.get("evidence_gate", {}).get("evidence_class") not in EVIDENCE_CLASSES:
            raise ValueError(f"invalid evidence class for {entry['framework_id']}")
        write_json(out, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
