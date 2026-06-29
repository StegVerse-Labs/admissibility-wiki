#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
SCHEMA = ROOT / "docs" / "external-frameworks" / "framework-manifest.schema.json"

REQUIRED_TOP_LEVEL = [
    "artifact_type",
    "schema_version",
    "framework_id",
    "name",
    "source_reference",
    "source_version",
    "allowed_use_boundary",
    "claims",
    "non_claims",
    "transition_table_mapping",
    "SPE_overlap",
    "StegVerse_ecosystem_overlap",
    "fail_closed_conditions",
    "boundary",
]

REQUIRED_TRANSITION_FIELDS = [
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

    for path in [REGISTRY, SCHEMA]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK MANIFESTS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = load_json(REGISTRY)
    entries = registry.get("entries", [])
    manifest_entries = [entry for entry in entries if isinstance(entry.get("manifest_path"), str)]
    if not manifest_entries:
        failures.append("no manifest-backed framework entries")

    for entry in manifest_entries:
        manifest_path = ROOT / entry["manifest_path"]
        if not manifest_path.exists():
            failures.append(f"missing manifest: {entry['manifest_path']}")
            continue

        manifest = load_json(manifest_path)
        for field in REQUIRED_TOP_LEVEL:
            if field not in manifest:
                failures.append(f"{entry['framework_id']} missing top-level field: {field}")

        if manifest.get("artifact_type") != "external_framework_manifest":
            failures.append(f"{entry['framework_id']} artifact type mismatch")
        if manifest.get("framework_id") != entry.get("framework_id"):
            failures.append(f"{entry['framework_id']} framework id mismatch")
        if manifest.get("name") != entry.get("name"):
            failures.append(f"{entry['framework_id']} name mismatch")

        for list_field in ["allowed_use_boundary", "claims", "non_claims", "fail_closed_conditions"]:
            value = manifest.get(list_field)
            if not isinstance(value, list) or not value:
                failures.append(f"{entry['framework_id']} missing non-empty list: {list_field}")

        mapping = manifest.get("transition_table_mapping", {})
        if not isinstance(mapping, dict):
            failures.append(f"{entry['framework_id']} transition mapping not object")
        else:
            for field in REQUIRED_TRANSITION_FIELDS:
                if field not in mapping:
                    failures.append(f"{entry['framework_id']} missing transition-table field: {field}")
            if mapping.get("execution_authority_claim") is not False:
                failures.append(f"{entry['framework_id']} execution authority mapping must be false")

        for overlap_field in ["SPE_overlap", "StegVerse_ecosystem_overlap"]:
            value = manifest.get(overlap_field)
            if not isinstance(value, dict) or not value:
                failures.append(f"{entry['framework_id']} missing overlap object: {overlap_field}")

        boundary = manifest.get("boundary", {})
        for key in [
            "certification_claim",
            "endorsement_claim",
            "execution_authority_claim",
            "commit_time_authority_claim",
            "compatibility_manifest_is_authority",
        ]:
            if boundary.get(key) is not False:
                failures.append(f"{entry['framework_id']} boundary false mismatch: {key}")
        if boundary.get("missing_or_partial_fields_fail_closed") is not True:
            failures.append(f"{entry['framework_id']} fail-closed boundary missing")

    print("EXTERNAL FRAMEWORK MANIFESTS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
