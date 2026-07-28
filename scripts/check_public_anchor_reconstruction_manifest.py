#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"


def fail(message: str) -> None:
    raise SystemExit(f"PUBLIC-ANCHOR RECONSTRUCTION MANIFEST: FAIL - {message}")


def main() -> None:
    if not MANIFEST.exists():
        fail("manifest missing")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != "public-anchor-reconstruction-manifest.v1":
        fail("schema version mismatch")
    commit = data.get("frozen_commit", "")
    if not isinstance(commit, str) or len(commit) != 40:
        fail("frozen commit must be a 40-character SHA")
    dockets = data.get("dockets", [])
    if len(dockets) != 3:
        fail("exactly three governed dockets are required")
    expected = {
        "review-ta14-reference-docket-2026-07-27",
        "review-asro-reference-docket-2026-07-27",
        "review-stegverse-public-anchor-self-2026-07-27",
    }
    if {item.get("review_id") for item in dockets} != expected:
        fail("docket review ids do not match the three-docket freeze")
    for item in dockets:
        for field in ("page", "record", "validator"):
            path = ROOT / item[field]
            if not path.exists():
                fail(f"missing frozen component: {item[field]}")
    controls = data.get("governance_controls", {})
    for field in ("multi_docket_status", "canonical_validation_entry", "canonical_workflow"):
        path = ROOT / controls.get(field, "")
        if not path.exists():
            fail(f"missing governance control: {field}")
    boundary = data.get("authority_boundary", {})
    if any(boundary.get(key) is not False for key in (
        "manifest_creates_certification",
        "manifest_creates_execution_authority",
        "manifest_establishes_substantive_truth",
        "route_reachability_establishes_validity",
    )):
        fail("authority boundary must remain false")
    if data.get("independent_reconstruction_status") != "NOT_RUN":
        fail("independent reconstruction must remain NOT_RUN until evidence exists")
    handoff = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""
    required_handoff_markers = (
        "Frozen Public-Anchor Boundary",
        "Manifest: static/data/governed-framework-reviews/public-anchor-reconstruction-manifest.v1.json",
        "Independent reconstruction: NOT_RUN",
        "Reconstruction invitation: OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED",
    )
    for marker in required_handoff_markers:
        if marker not in handoff:
            fail(f"handoff missing reconstruction-boundary marker: {marker}")
    print("PUBLIC-ANCHOR RECONSTRUCTION MANIFEST: PASS - three-docket freeze is bounded and independently consumable")


if __name__ == "__main__":
    main()
