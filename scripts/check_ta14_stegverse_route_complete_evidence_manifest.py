#!/usr/bin/env python3
"""Validate the nonblocking TA-14 route-complete evidence manifest.

The manifest may remain partial. This check requires every requested evidence
component to have an internal work location and prevents missing evidence from
halting unrelated development or being promoted into a route-complete claim.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-route-complete-evidence-manifest.v1.json"
EXPECTED_COMPONENTS = {
    "architecture",
    "authority",
    "reality",
    "determination",
    "bind_commit",
    "execution_refusal",
    "continuity",
    "replay",
    "outcome",
    "adversarial",
}
ALLOWED_STATES = {"OPEN", "PARTIAL", "COMPLETE_INTERNAL", "COMPLETE_ROUTE_EVIDENCE"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TA-14 ROUTE-COMPLETE EVIDENCE MANIFEST: FAIL - {message}")


def main() -> None:
    require(MANIFEST.is_file(), "manifest missing")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "route-complete-evidence-manifest.v1", "schema mismatch")
    policy = data.get("non_blocking_policy", {})
    require(policy.get("missing_component_stops_claim_promotion") is True, "missing components must stop claim promotion")
    require(policy.get("missing_component_stops_unrelated_development") is False, "missing components must not halt unrelated work")
    require(policy.get("each_component_has_repository_path") is True, "repository path rule missing")
    require(policy.get("partial_completion_is_preserved") is True, "partial completion must be preserved")

    components = data.get("components", [])
    require(isinstance(components, list), "components must be a list")
    ids = {item.get("component_id") for item in components if isinstance(item, dict)}
    require(ids == EXPECTED_COMPONENTS, f"component coverage mismatch: {sorted(ids)}")

    for item in components:
        require(isinstance(item, dict), "component must be an object")
        component_id = item.get("component_id")
        require(item.get("state") in ALLOWED_STATES, f"invalid state for {component_id}")
        work_path = item.get("work_path")
        require(isinstance(work_path, str) and work_path, f"missing work_path for {component_id}")
        require(not work_path.startswith(("http://", "https://")), f"external work path prohibited for {component_id}")
        require((ROOT / work_path).exists(), f"work_path does not exist for {component_id}: {work_path}")
        required_evidence = item.get("required_evidence")
        require(isinstance(required_evidence, list) and required_evidence, f"required_evidence missing for {component_id}")

    complete = all(item.get("state") == "COMPLETE_ROUTE_EVIDENCE" for item in components)
    if complete:
        require(data.get("claim_state") == "ROUTE_COMPLETE_EVIDENCE_AVAILABLE", "complete components require route-complete claim state")
    else:
        require(data.get("claim_state") == "NO_ROUTE_COMPLETE_CLAIM", "partial manifest must prohibit route-complete claim")

    boundary = data.get("authority_boundary", {})
    for key in (
        "manifest_establishes_truth",
        "manifest_grants_certification",
        "manifest_grants_execution_authority",
        "manifest_establishes_independent_reconstruction",
    ):
        require(boundary.get(key) is False, f"authority boundary drift: {key}")

    partial_count = sum(item.get("state") == "PARTIAL" for item in components)
    open_count = sum(item.get("state") == "OPEN" for item in components)
    print(
        "TA-14 ROUTE-COMPLETE EVIDENCE MANIFEST: PASS - "
        f"10/10 components located; {partial_count} partial, {open_count} open; development remains nonblocking"
    )


if __name__ == "__main__":
    main()
