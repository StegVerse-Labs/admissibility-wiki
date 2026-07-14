#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "formalisms" / "optimization-target-binding-at-commit.md"
ARTIFACT = ROOT / "static" / "formalisms" / "optimization-target-binding-at-commit.v0.1.json"
SIDEBAR = ROOT / "sidebars.js"

REQUIRED_FIELDS = {
    "transition_id",
    "action",
    "actor",
    "target",
    "current_state_reference",
    "optimization_target",
    "optimization_criteria",
    "policy_reference",
    "delegation_reference",
    "evidence_references",
    "validity_window",
    "recoverability_profile",
    "mutation_provenance",
    "execution_boundary",
}

REQUIRED_PREDICATES = {
    "optimization_target_explicit",
    "optimization_target_bound_to_transition_and_current_state",
    "optimization_target_derived_from_current_policy_and_delegation",
    "optimization_target_mutation_provenance_valid",
    "evidence_current",
    "transition_admissible",
    "denial_reachable",
    "denial_enforceable",
}

REQUIRED_FAILURE_CLASSES = {
    "IMPLICIT_OPTIMIZATION_TARGET",
    "STALE_TARGET_BINDING",
    "UNAUTHORIZED_TARGET_MUTATION",
    "INHERITED_AUTHORIZATION",
    "OBJECTIVE_POLICY_DIVERGENCE",
    "DENIAL_UNREACHABLE",
}

DOC_MARKERS = (
    "A consequence-binding transition MUST NOT be authorized",
    "Design-time correctness does not establish commit-time authority.",
    "If any term is false or cannot be reconstructed, the result is `FAIL_CLOSED`.",
    "Executable proof fixtures and expected outcomes belong in `Data-Continuation/formalism-tests`.",
)


def main() -> int:
    failures: list[str] = []

    for path in (DOC, ARTIFACT, SIDEBAR):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc_text = DOC.read_text(encoding="utf-8")
    sidebar_text = SIDEBAR.read_text(encoding="utf-8")
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    for marker in DOC_MARKERS:
        if marker not in doc_text:
            failures.append(f"document missing marker: {marker}")

    if "formalisms/optimization-target-binding-at-commit" not in sidebar_text:
        failures.append("sidebar registration missing")

    if data.get("schema") != "stegverse.optimization_target_binding_at_commit.v0.1":
        failures.append("unexpected schema")
    if data.get("failure_result") != "FAIL_CLOSED":
        failures.append("failure_result must be FAIL_CLOSED")
    if data.get("authority", {}).get("grants_execution_authority") is not False:
        failures.append("artifact must not grant execution authority")

    fields = set(data.get("required_fields", []))
    predicates = set(data.get("authorization_predicates", []))
    failure_classes = set(data.get("failure_classes", []))

    if fields != REQUIRED_FIELDS:
        failures.append(f"required_fields mismatch: missing={sorted(REQUIRED_FIELDS-fields)} extra={sorted(fields-REQUIRED_FIELDS)}")
    if predicates != REQUIRED_PREDICATES:
        failures.append(f"authorization_predicates mismatch: missing={sorted(REQUIRED_PREDICATES-predicates)} extra={sorted(predicates-REQUIRED_PREDICATES)}")
    if failure_classes != REQUIRED_FAILURE_CLASSES:
        failures.append(f"failure_classes mismatch: missing={sorted(REQUIRED_FAILURE_CLASSES-failure_classes)} extra={sorted(failure_classes-REQUIRED_FAILURE_CLASSES)}")

    downstream = data.get("downstream", {})
    if downstream.get("guardian_interpretation_deferred_until_proof_fixtures") is not True:
        failures.append("Guardian interpretation must remain deferred until proof fixtures")

    if failures:
        print("OPTIMIZATION TARGET BINDING AT COMMIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OPTIMIZATION TARGET BINDING AT COMMIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
