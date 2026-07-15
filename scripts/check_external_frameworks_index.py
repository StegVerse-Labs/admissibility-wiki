#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_MD = ROOT / "docs" / "external-frameworks" / "index.md"
INDEX_JSON = ROOT / "docs" / "external-frameworks" / "index.json"
MANIFEST_SCHEMA = ROOT / "docs" / "external-frameworks" / "framework-manifest.schema.json"
SIDEBAR_ASSOCIATIONS = ROOT / "static" / "external-frameworks" / "sidebar-page-associations.v1.json"
CANONICAL_UNION = ROOT / "static" / "external-frameworks" / "canonical-union-inventory.v1.json"

REQUIRED_ENTRY_FIELDS = [
    "framework_id",
    "name",
    "status",
    "path",
    "manifest_path",
    "source",
    "testbench_state",
    "claims_certification",
    "claims_endorsement",
    "claims_execution_authority",
]

MINIMUM_TRANSITION_TABLE_ELEMENTS = [
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

ALLOWED_SCHEMA_VERSIONS = {"0.3", "0.4"}
ALLOWED_GOAL_IDS = {
    "external-framework-compatibility-testbench",
    "external-framework-expansion-cycle",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [INDEX_MD, INDEX_JSON, MANIFEST_SCHEMA, SIDEBAR_ASSOCIATIONS, CANONICAL_UNION]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORKS INDEX: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    data = load_json(INDEX_JSON)
    md = INDEX_MD.read_text(encoding="utf-8")
    associations = load_json(SIDEBAR_ASSOCIATIONS)
    canonical_union = load_json(CANONICAL_UNION)

    if data.get("artifact_type") != "external_framework_registry":
        failures.append("artifact type mismatch")
    if data.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
        failures.append("schema version mismatch")
    if data.get("goal_id") not in ALLOWED_GOAL_IDS:
        failures.append("goal id mismatch")

    model = data.get("testbench_model", {})
    if model.get("basis") != "transition_table_elements":
        failures.append("testbench basis mismatch")
    elements = model.get("minimum_transition_table_elements", [])
    for element in MINIMUM_TRANSITION_TABLE_ELEMENTS:
        if element not in elements:
            failures.append(f"missing transition table element: {element}")

    required = data.get("required_entry_fields", [])
    for field in REQUIRED_ENTRY_FIELDS:
        if field not in required:
            failures.append(f"missing required entry field: {field}")

    entries = data.get("entries", [])
    if not entries:
        failures.append("no framework entries")
    ids: set[str] = set()
    for entry in entries:
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"entry {entry.get('framework_id')} missing field: {field}")
        framework_id = entry.get("framework_id")
        if not isinstance(framework_id, str) or framework_id in ids:
            failures.append(f"invalid or duplicate framework id: {framework_id}")
        else:
            ids.add(framework_id)
        path = entry.get("path")
        if isinstance(path, str) and not (ROOT / path).exists():
            failures.append(f"entry path missing: {path}")
        manifest_path = entry.get("manifest_path")
        if not isinstance(manifest_path, str) or not (ROOT / manifest_path).exists():
            failures.append(f"manifest path missing: {manifest_path}")
        for claim_field in ["claims_certification", "claims_endorsement", "claims_execution_authority"]:
            if entry.get(claim_field) is not False:
                failures.append(f"entry {entry.get('framework_id')} boundary mismatch: {claim_field}")

    sidebar_ids = {
        entry.get("framework_id")
        for entry in associations.get("entries", [])
        if entry.get("page_type") == "framework"
    }
    union_ids = {
        entry.get("record_id")
        for entry in canonical_union.get("records", [])
        if entry.get("external_framework") is True
    }
    if not sidebar_ids:
        failures.append("sidebar framework coverage is empty")
    if not sidebar_ids.issubset(ids):
        failures.append("sidebar framework IDs are not fully represented in the canonical registry")
    if not ids.issubset(union_ids):
        failures.append("registry framework IDs are not fully represented in the canonical union")

    required_index_references = [
        "External Framework Evaluation Standard",
        "External Framework Evaluation Results",
        "Expanded External Framework Intake",
        "External Framework Family Coverage",
        "External Framework Intake Promotion Criteria",
        "External Framework Page Template",
        "Evidence Provenance Rollout",
    ]
    for reference in required_index_references:
        if reference not in md:
            failures.append(f"index markdown missing canonical navigation reference: {reference}")

    boundary = data.get("boundary", {})
    false_keys = [
        "index_inclusion_is_certification",
        "index_inclusion_is_endorsement",
        "index_inclusion_is_execution_authority",
    ]
    true_keys = [
        "testbench_outputs_are_compatibility_evidence_only",
        "missing_source_fails_closed",
        "missing_transition_table_mapping_fails_closed",
        "undefined_overlap_fails_closed",
    ]
    for key in false_keys:
        if boundary.get(key) is not False:
            failures.append(f"boundary false mismatch: {key}")
    for key in true_keys:
        if boundary.get(key) is not True:
            failures.append(f"boundary true mismatch: {key}")

    print("EXTERNAL FRAMEWORKS INDEX:", "FAIL" if failures else "PASS")
    print(f"registry_entries={len(ids)}")
    print(f"sidebar_frameworks={len(sidebar_ids)}")
    print(f"canonical_union_external_records={len(union_ids)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
