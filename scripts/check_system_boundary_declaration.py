#!/usr/bin/env python3
"""Validate the governed LLM system-boundary declaration example.

This checker intentionally validates operational boundaries only. It does not
classify consciousness, personhood, welfare status, or execution authority.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static/governance/system-boundary-declaration.schema.v0.1.json"
EXAMPLE_PATH = ROOT / "static/governance/system-boundary-declaration.example.v0.1.json"

REQUIRED_SURFACES = {"model", "orchestration", "session", "memory", "environment"}
VALID_STATE_KINDS = {"none", "transient", "session", "durable", "external"}
VALID_PERSISTENCE = {"none", "invocation", "session", "cross-session", "indefinite"}
VALID_DECISION_SOURCES = {"policy-engine", "human", "quorum", "none"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    declaration = load_json(EXAMPLE_PATH)

    require(schema.get("title") == "StegVerse System Boundary Declaration", "schema title drift")
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

    require(surfaces["model"]["persistence"] == "invocation", "example model boundary must remain invocation-scoped")
    require(surfaces["model"]["mutable_by_inference"] is False, "inference must not claim to rewrite model state")

    continuity = declaration.get("continuity", {})
    require(isinstance(continuity.get("prior_state_can_affect_future_transition"), bool), "continuity prior-state flag missing")
    require(isinstance(continuity.get("feedback_paths"), list), "continuity feedback_paths missing")
    require(isinstance(continuity.get("trajectory_dependent"), bool), "continuity trajectory flag missing")
    require(isinstance(continuity.get("reconstructable"), bool), "continuity reconstructable flag missing")

    authority = declaration.get("authority", {})
    require(authority.get("model_has_execution_authority") is False, "model execution authority must be false")
    require(authority.get("decision_source") in VALID_DECISION_SOURCES, "authority decision_source invalid")
    require(bool(authority.get("commit_boundary")), "commit boundary is required")

    claims = declaration.get("claims_boundary", {})
    for key in ("consciousness_claim", "personhood_claim", "welfare_claim"):
        require(claims.get(key) == "not_evaluated", f"{key} must remain not_evaluated")
    require(bool(claims.get("scope_note")), "claims boundary scope_note is required")

    print("SYSTEM BOUNDARY DECLARATION: PASS")
    print(f"surfaces={len(surfaces)} feedback_paths={len(continuity['feedback_paths'])}")
    print("claims=operational-boundary-only authority=model-nonexecuting")


if __name__ == "__main__":
    main()
