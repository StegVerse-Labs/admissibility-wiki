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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
        if report.get("artifact_type") != "external_framework_compatibility_report":
            failures.append(f"artifact type mismatch: {report_path.relative_to(ROOT)}")
        if report.get("schema_version") != "0.2":
            failures.append(f"schema version mismatch: {report_path.relative_to(ROOT)}")
        framework_id = report.get("framework_id")
        if framework_id not in known_ids:
            failures.append(f"unknown framework id: {framework_id}")
        if report.get("testbench_basis") != "transition_table_elements":
            failures.append(f"basis mismatch: {framework_id}")
        if report.get("result") != "COMPATIBILITY_EVIDENCE_ONLY":
            failures.append(f"result mismatch: {framework_id}")
        if report.get("cycle_status") != "FIRST_FRAMEWORK_CYCLE_COMPLETE":
            failures.append(f"cycle status mismatch: {framework_id}")

        manifest = report.get("framework_manifest")
        if not isinstance(manifest, str) or not (ROOT / manifest).exists():
            failures.append(f"missing manifest reference: {framework_id}")
        status = report.get("transition_table_mapping_status", {})
        for key in REQUIRED_STATUS_KEYS:
            if key not in status:
                failures.append(f"missing transition table status {key}: {framework_id}")
            elif status[key] == "PARTIAL":
                failures.append(f"partial transition table status {key}: {framework_id}")

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
