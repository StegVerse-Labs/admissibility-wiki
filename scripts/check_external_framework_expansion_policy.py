#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "external-frameworks" / "EXPANSION_POLICY.json"
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"

REQUIRED_SOURCE_STATES = [
    "SOURCE_RECORDED_CROSSWALK_PROVISIONAL",
    "SOURCE_BLOCKED_FAIL_CLOSED",
    "ARTIFACT_PACKAGE_REQUIRED_FAIL_CLOSED",
    "FIRST_FRAMEWORK_CYCLE_COMPLETE",
]

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

REQUIRED_MANIFEST_FIELDS = [
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

REQUIRED_PAGE_SECTIONS = [
    "Framework-Term Definitions",
    "Reconciliation Class",
    "Admissibility Relationship",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [POLICY, REGISTRY]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK EXPANSION POLICY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    policy = load_json(POLICY)
    registry = load_json(REGISTRY)

    if policy.get("artifact_type") != "external_framework_expansion_policy":
        failures.append("artifact type mismatch")
    if policy.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if policy.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if policy.get("goal_id") != "external-framework-expansion-cycle":
        failures.append("goal id mismatch")

    for state in REQUIRED_SOURCE_STATES:
        if state not in policy.get("allowed_source_states", []):
            failures.append(f"missing source state: {state}")
    for field in REQUIRED_ENTRY_FIELDS:
        if field not in policy.get("required_new_entry_fields", []):
            failures.append(f"missing required entry field: {field}")
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in policy.get("required_manifest_fields", []):
            failures.append(f"missing required manifest field: {field}")
    for section in REQUIRED_PAGE_SECTIONS:
        if section not in policy.get("required_page_sections", []):
            failures.append(f"missing required page section: {section}")

    required_boundaries = policy.get("required_boundaries", {})
    for key in [
        "claims_certification",
        "claims_endorsement",
        "claims_execution_authority",
        "certification_claim",
        "endorsement_claim",
        "execution_authority_claim",
        "commit_time_authority_claim",
        "compatibility_manifest_is_authority",
    ]:
        if required_boundaries.get(key) is not False:
            failures.append(f"required boundary mismatch: {key}")

    boundary = policy.get("boundary", {})
    for key in [
        "expansion_policy_is_authority",
        "expansion_policy_is_certification",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"false boundary mismatch: {key}")
    for key in [
        "new_entries_require_source_state",
        "new_entries_require_native_terminology",
        "new_entries_require_transition_table_mapping",
        "new_entries_preserve_non_authority_boundary",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"true boundary mismatch: {key}")

    allowed = set(policy.get("allowed_source_states", []))
    for entry in registry.get("entries", []):
        framework_id = entry.get("framework_id", "UNKNOWN")
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"{framework_id} missing registry field: {field}")
        if entry.get("testbench_state") not in allowed:
            failures.append(f"{framework_id} source state not allowed: {entry.get('testbench_state')}")
        for key in ["claims_certification", "claims_endorsement", "claims_execution_authority"]:
            if entry.get(key) is not False:
                failures.append(f"{framework_id} registry authority boundary mismatch: {key}")

    print("EXTERNAL FRAMEWORK EXPANSION POLICY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
