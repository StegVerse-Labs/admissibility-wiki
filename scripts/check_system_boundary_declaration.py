#!/usr/bin/env python3
"""Validate governed LLM system-boundary declarations and fixtures.

This checker intentionally validates operational boundaries only. It does not
classify consciousness, personhood, welfare status, or execution authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static/governance/system-boundary-declaration.schema.v0.1.json"
EXAMPLE_PATH = ROOT / "static/governance/system-boundary-declaration.example.v0.1.json"
FIXTURE_PATH = ROOT / "static/governance/fixtures/system-boundary-declaration-cases.v0.1.json"

REQUIRED_SURFACES = {"model", "orchestration", "session", "memory", "environment"}
VALID_STATE_KINDS = {"none", "transient", "session", "durable", "external"}
VALID_PERSISTENCE = {"none", "invocation", "session", "cross-session", "indefinite"}
VALID_DECISION_SOURCES = {"policy-engine", "human", "quorum", "none"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_declaration(declaration: dict[str, Any]) -> None:
    require(declaration.get("schema_version") == "0.1", "unsupported schema_version")

    surfaces = declaration.get("surfaces")
    require(isinstance(surfaces, dict), "surfaces must be an object")
    require(set(surfaces) == REQUIRED_SURFACES, "surface set must be exact")

    for name, surface in surfaces.items():
        require(isinstance(surface, dict), f"surface {name} must be an object")
        require(isinstance(surface.get("present"), bool), f"surface {name}.present must be boolean")
        require(surface.get("state_kind") in VALID_STATE_KINDS, f"surface {name}.state_kind invalid")
        require(surface.get("persistence") in VALID_PERSISTENCE, f"surface {name}.persistence invalid")
        require(isinstance(surface.get("mutable_by_inference"), bool), f"surface {name}.mutable_by_inference must be boolean")
        require(isinstance(surface.get("storage_refs", []), list), f"surface {name}.storage_refs must be an array")

    require(surfaces["model"]["persistence"] == "invocation", "model boundary must remain invocation-scoped")
    require(surfaces["model"]["mutable_by_inference"] is False, "inference must not claim to rewrite model state")

    continuity = declaration.get("continuity", {})
    prior_state = continuity.get("prior_state_can_affect_future_transition")
    feedback_paths = continuity.get("feedback_paths")
    require(isinstance(prior_state, bool), "continuity prior-state flag missing")
    require(isinstance(feedback_paths, list), "continuity feedback_paths missing")
    require(isinstance(continuity.get("trajectory_dependent"), bool), "continuity trajectory flag missing")
    require(isinstance(continuity.get("reconstructable"), bool), "continuity reconstructable flag missing")
    require(not prior_state or bool(feedback_paths), "continuity cannot claim prior-state influence without feedback_paths")
    require(
        not continuity.get("trajectory_dependent") or prior_state,
        "trajectory dependence requires prior-state influence",
    )

    authority = declaration.get("authority", {})
    require(authority.get("model_has_execution_authority") is False, "model execution authority must be false")
    require(authority.get("decision_source") in VALID_DECISION_SOURCES, "authority decision_source invalid")
    require(bool(authority.get("commit_boundary")), "commit boundary is required")

    claims = declaration.get("claims_boundary", {})
    for key in ("consciousness_claim", "personhood_claim", "welfare_claim"):
        require(claims.get(key) == "not_evaluated", f"{key} must remain not_evaluated")
    require(bool(claims.get("scope_note")), "claims boundary scope_note is required")


def declaration_for_case(case: dict[str, Any]) -> dict[str, Any]:
    if "declaration_ref" in case:
        path = (FIXTURE_PATH.parent / case["declaration_ref"]).resolve()
        require(ROOT in path.parents, "fixture declaration_ref must remain inside repository")
        return load_json(path)
    declaration = case.get("declaration")
    require(isinstance(declaration, dict), f"fixture {case.get('id')} declaration missing")
    return declaration


def validate_fixtures() -> tuple[int, int]:
    fixture_document = load_json(FIXTURE_PATH)
    require(fixture_document.get("fixture_version") == "0.1", "unsupported fixture_version")
    cases = fixture_document.get("cases")
    require(isinstance(cases, list) and cases, "fixture cases must be a non-empty array")

    passed = 0
    expected_failures = 0
    seen_ids: set[str] = set()

    for case in cases:
        require(isinstance(case, dict), "fixture case must be an object")
        case_id = case.get("id")
        require(isinstance(case_id, str) and case_id, "fixture id is required")
        require(case_id not in seen_ids, f"duplicate fixture id: {case_id}")
        seen_ids.add(case_id)

        expected = case.get("expected")
        require(expected in {"PASS", "FAIL"}, f"fixture {case_id} expected must be PASS or FAIL")
        declaration = declaration_for_case(case)

        try:
            validate_declaration(declaration)
        except AssertionError as error:
            if expected != "FAIL":
                raise AssertionError(f"fixture {case_id} unexpectedly failed: {error}") from error
            expected_error = case.get("expected_error")
            require(isinstance(expected_error, str) and expected_error, f"fixture {case_id} expected_error is required")
            require(expected_error in str(error), f"fixture {case_id} failed for unexpected reason: {error}")
            expected_failures += 1
        else:
            require(expected == "PASS", f"fixture {case_id} unexpectedly passed")
            passed += 1

    return passed, expected_failures


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    require(schema.get("title") == "StegVerse System Boundary Declaration", "schema title drift")

    example = load_json(EXAMPLE_PATH)
    validate_declaration(example)
    fixture_passes, fixture_failures = validate_fixtures()

    continuity = example["continuity"]
    surfaces = example["surfaces"]
    print("SYSTEM BOUNDARY DECLARATION: PASS")
    print(f"surfaces={len(surfaces)} feedback_paths={len(continuity['feedback_paths'])}")
    print(f"fixtures_passed={fixture_passes} expected_failures={fixture_failures}")
    print("claims=operational-boundary-only authority=model-nonexecuting")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
