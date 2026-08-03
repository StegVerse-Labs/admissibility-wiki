#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static/schemas/gsdp/governed-system-description.schema.json"
REFERENCE = ROOT / "static/data/standards/gsdp/examples/stegverse.pending.v0.1.json"
FIXTURES = ROOT / "static/data/standards/gsdp/fixtures"
STATUS = ROOT / "static/status/gsdp-reference-status.json"
HANDOFF = ROOT / "docs/standards/GSDP_MIRROR_HANDOFF.md"
FIRST_OBSERVATION = ROOT / "static/data/standards/gsdp/observations/canonical-workflow-observation.30568611934.v0.1.json"

REQUIRED_ROOT = {
    "$schema", "gsdp_version", "declaration_id", "system", "operators",
    "components", "authority", "governance", "evidence", "status",
    "dependencies", "history", "claims", "explicit_non_claims",
}
PROHIBITED_POSITIVE_AUTHORITY = {
    "government_certification", "external_certification",
    "independent_conformance_assessment", "unrestricted_execution_authority",
    "authority_over_external_systems", "production_activation_from_this_declaration",
}
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
ALLOWED_STATUS_STATES = {
    "CANONICAL_VALIDATION_BOUND_WORKFLOW_OBSERVATION_PENDING",
    "FIRST_CANONICAL_FAILURE_RETAINED_REPAIR_VALIDATION_PENDING",
    "INITIAL_REFERENCE_ACTIVATION_COMPLETE",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_reference(data: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(REQUIRED_ROOT - set(data))
    if missing:
        fail(errors, f"reference missing root fields: {', '.join(missing)}")

    if data.get("gsdp_version") != "0.1-draft":
        fail(errors, "reference gsdp_version must be 0.1-draft")

    operators = data.get("operators", [])
    components = data.get("components", [])
    if not operators or not components:
        fail(errors, "reference requires at least one operator and component")

    operator_ids = [item.get("id") for item in operators]
    component_ids = [item.get("id") for item in components]
    if len(operator_ids) != len(set(operator_ids)):
        fail(errors, "operator ids must be unique")
    if len(component_ids) != len(set(component_ids)):
        fail(errors, "component ids must be unique")

    known_operators = set(operator_ids)
    known_components = set(component_ids)
    for operator in operators:
        unresolved = set(operator.get("component_refs", [])) - known_components
        if unresolved:
            fail(errors, f"operator {operator.get('id')} has unresolved component refs: {sorted(unresolved)}")
        positive = set(operator.get("authority", []))
        prohibited = positive & PROHIBITED_POSITIVE_AUTHORITY
        if prohibited:
            fail(errors, f"operator {operator.get('id')} asserts prohibited authority: {sorted(prohibited)}")

    dependency_ids = {item.get("id") for item in data.get("dependencies", [])}
    for component in components:
        unresolved_operators = set(component.get("operator_refs", [])) - known_operators
        unresolved_dependencies = set(component.get("dependencies", [])) - dependency_ids
        if unresolved_operators:
            fail(errors, f"component {component.get('id')} has unresolved operator refs: {sorted(unresolved_operators)}")
        if unresolved_dependencies:
            fail(errors, f"component {component.get('id')} has unresolved dependencies: {sorted(unresolved_dependencies)}")
        overlap = set(component.get("authority", [])) & set(component.get("explicit_non_authority", []))
        if overlap:
            fail(errors, f"component {component.get('id')} contradicts its authority boundary: {sorted(overlap)}")
        prohibited = set(component.get("authority", [])) & PROHIBITED_POSITIVE_AUTHORITY
        if prohibited:
            fail(errors, f"component {component.get('id')} asserts prohibited authority: {sorted(prohibited)}")

    conformance = data.get("conformance", {})
    if conformance.get("claimed_classes"):
        fail(errors, "pending StegVerse fixture must not claim a conformance class")
    if conformance.get("schema_validated") is not False:
        fail(errors, "pending StegVerse fixture must preserve schema_validated=false")
    if conformance.get("independent_assessment") != "not_run":
        fail(errors, "pending StegVerse fixture must preserve independent_assessment=not_run")

    history = data.get("history", {})
    declaration_hash = history.get("declaration_hash")
    if declaration_hash is not None and not SHA256.fullmatch(declaration_hash):
        fail(errors, "history.declaration_hash must be null or canonical sha256")

    non_claims = " ".join(data.get("explicit_non_claims", [])).lower()
    for marker in ("independent", "certif", "execution authority", "external adoption"):
        if marker not in non_claims:
            fail(errors, f"explicit_non_claims missing boundary marker: {marker}")


def validate_fixtures(errors: list[str]) -> None:
    authority = load(FIXTURES / "authority-non-inheritance.invalid.v0.1.json")
    if authority.get("expected_result") != "REJECT":
        fail(errors, "authority non-inheritance fixture must expect REJECT")
    source = authority.get("source_component", {})
    inferred = set(source.get("authority", []))
    if "runtime_execution_authority" not in inferred or authority.get("delegation") is not None:
        fail(errors, "authority non-inheritance fixture no longer exercises unauthorized inference")

    historical = load(FIXTURES / "historical-supersession.valid.v0.1.json")
    previous = historical.get("previous", {})
    successor = historical.get("successor", {})
    if historical.get("expected_result") != "PASS":
        fail(errors, "historical supersession fixture must expect PASS")
    if successor.get("supersedes") != previous.get("declaration_id"):
        fail(errors, "historical successor must bind the exact prior declaration")
    if successor.get("previous_declaration") != previous.get("declaration_id"):
        fail(errors, "historical previous_declaration must bind the exact prior declaration")
    if successor.get("effective_from") != previous.get("effective_until"):
        fail(errors, "historical fixture must use a non-overlapping continuity boundary")
    if not SHA256.fullmatch(previous.get("declaration_hash", "")):
        fail(errors, "historical fixture requires canonical prior sha256")

    minimum = load(FIXTURES / "schema-minimum.invalid.v0.1.json")
    if minimum.get("expected_result") != "REJECT" or not minimum.get("expected_errors"):
        fail(errors, "minimum negative fixture must expect deterministic rejection errors")


def validate_observation(errors: list[str]) -> None:
    observation = load(FIRST_OBSERVATION)
    required = {
        "standard_id": "GSDP",
        "workflow_run_id": 30568611934,
        "workflow_conclusion": "failure",
        "observation_state": "FAIL_CLOSED_OBSERVED",
        "authority_effect": "NONE",
    }
    for key, expected in required.items():
        if observation.get(key) != expected:
            fail(errors, f"first observation {key} must equal {expected!r}")
    if observation.get("canonical_prescan", {}).get("status") != "PASS":
        fail(errors, "first observation must preserve canonical pre-scan PASS")
    gsdp_result = observation.get("gsdp_result", {})
    if gsdp_result.get("classification") != "GSDP_STATUS_CONTRACT_DRIFT":
        fail(errors, "first observation must classify the retained GSDP failure")
    if gsdp_result.get("repair_required") is not True:
        fail(errors, "first observation must preserve repair_required=true")


def validate_status(errors: list[str]) -> None:
    status = load(STATUS)
    required = {
        "standard_id": "GSDP",
        "draft_version": "0.1-draft",
        "schema_validation_effect": "STRUCTURAL_ONLY_NO_EXTERNAL_CONFORMANCE",
        "independent_conformance": "NOT_RUN",
        "certification_authority": False,
        "execution_authority": False,
    }
    for key, expected in required.items():
        if status.get(key) != expected:
            fail(errors, f"status {key} must equal {expected!r}")
    if status.get("state") not in ALLOWED_STATUS_STATES:
        fail(errors, f"status state must be one of {sorted(ALLOWED_STATUS_STATES)}")
    observation = status.get("canonical_binding", {}).get("workflow_observation")
    if status.get("state") == "CANONICAL_VALIDATION_BOUND_WORKFLOW_OBSERVATION_PENDING":
        if observation != "NOT_OBSERVED":
            fail(errors, "pending state requires workflow_observation=NOT_OBSERVED")
    else:
        if observation not in {"FAIL_CLOSED_OBSERVED", "PASS_OBSERVED"}:
            fail(errors, "observed state requires a retained workflow observation")


def main() -> int:
    errors: list[str] = []
    for path in (SCHEMA, REFERENCE, STATUS, HANDOFF, FIRST_OBSERVATION):
        if not path.exists():
            fail(errors, f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        print("GSDP reference validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    schema = load(SCHEMA)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(errors, "GSDP schema must use JSON Schema draft 2020-12")
    validate_reference(load(REFERENCE), errors)
    validate_fixtures(errors)
    validate_observation(errors)
    validate_status(errors)

    if errors:
        print("GSDP reference validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GSDP reference validation: PASS")
    print("effect: structural and boundary validation only")
    print("first canonical failure: retained fail-closed")
    print("external conformance: NOT ESTABLISHED")
    print("certification authority: false")
    print("execution authority: false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
