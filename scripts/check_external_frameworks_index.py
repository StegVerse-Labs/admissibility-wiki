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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [INDEX_MD, INDEX_JSON, MANIFEST_SCHEMA]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORKS INDEX: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    data = load_json(INDEX_JSON)
    md = INDEX_MD.read_text(encoding="utf-8")

    if data.get("artifact_type") != "external_framework_registry":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("goal_id") != "external-framework-compatibility-testbench":
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
    for entry in entries:
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"entry {entry.get('framework_id')} missing field: {field}")
        path = entry.get("path")
        if isinstance(path, str) and not (ROOT / path).exists():
            failures.append(f"entry path missing: {path}")
        manifest_path = entry.get("manifest_path")
        if isinstance(manifest_path, str) and not (ROOT / manifest_path).exists():
            failures.append(f"manifest path missing: {manifest_path}")
        for claim_field in ["claims_certification", "claims_endorsement", "claims_execution_authority"]:
            if entry.get(claim_field) is not False:
                failures.append(f"entry {entry.get('framework_id')} boundary mismatch: {claim_field}")
        name = entry.get("name")
        if isinstance(name, str) and name not in md:
            failures.append(f"index markdown missing framework name: {name}")

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
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
