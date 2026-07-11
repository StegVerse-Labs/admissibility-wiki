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
        "Add an official public source reference before upgrading this report from SOURCE_BLOCKED_FAIL_CLOSED to COMPATIBILITY_EVIDENCE_ONLY."
        if source_blocked
        else "Expand the same manifest-and-report cycle to every registry entry with an official source reference."
    )

    return {
        "artifact_type": "external_framework_compatibility_report",
        "schema_version": "0.2",
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


def build_report(entry: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    """Backward-compatible report builder used by validators and older callers.

    `build_base_report` is the canonical implementation. This alias preserves the
    established public module API so report-generation checks do not fail when
    older integrations still call `build_report`.
    """
    return build_base_report(entry, manifest)


def preserve_enriched_report(
    base: dict[str, Any], existing: dict[str, Any] | None
) -> dict[str, Any]:
    """Preserve verified framework-specific evidence while refreshing canonical references.

    Generated reports are baseline artifacts. Once a report has been explicitly enriched
    with bounded benchmark observations, generation must not erase that evidence. The
    existing enriched report remains authoritative for its extension fields, while core
    identity/reference fields and mandatory fail-closed boundaries are refreshed.
    """
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

    boundary = dict(report.get("boundary", {}))
    boundary.update(base["boundary"])
    report["boundary"] = boundary
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
        write_json(out, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
