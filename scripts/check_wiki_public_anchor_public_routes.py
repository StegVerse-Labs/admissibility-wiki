#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static" / "status" / "wiki-public-anchor-route-observation-receipt.json"
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
STATUS = ROOT / "static" / "status" / "wiki-public-anchor-multi-docket-status.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"WIKI PUBLIC-ANCHOR PUBLIC ROUTES: FAIL - {message}")


def main() -> None:
    require(RECEIPT.exists(), "route observation receipt missing")
    require(MANIFEST.exists(), "reconstruction manifest missing")
    require(STATUS.exists(), "multi-docket status missing")
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    require(receipt.get("schema_version") == "wiki-public-anchor-route-observation-receipt.v1", "schema version mismatch")
    require(receipt.get("overall_state") in {"PENDING", "OBSERVED", "PARTIAL", "FAILED_CLOSED"}, "invalid overall state")
    routes = receipt.get("routes", [])
    expected_routes = {item.get("public_route") for item in manifest.get("dockets", [])}
    expected_routes.add("/data/governed-framework-reviews/public-anchor-reconstruction-manifest.v1.json")
    require({item.get("route") for item in routes} == expected_routes, "receipt routes do not match frozen manifest")
    if receipt.get("overall_state") == "PENDING":
        require(all(item.get("observation") == "PENDING_CANONICAL_WORKFLOW" for item in routes), "pending receipt has non-pending route")
        require(status.get("validation", {}).get("public_route_observation") == "PENDING", "status and receipt disagree")
    boundary = receipt.get("authority_boundary", {})
    for field in (
        "reachability_establishes_truth",
        "reachability_establishes_certification",
        "reachability_establishes_execution_authority",
        "pending_observation_is_failure",
    ):
        require(boundary.get(field) is False, f"authority boundary must remain false: {field}")
    print("WIKI PUBLIC-ANCHOR PUBLIC ROUTES: PASS - receipt is bounded, fail-closed, and aligned with frozen routes")


if __name__ == "__main__":
    main()
