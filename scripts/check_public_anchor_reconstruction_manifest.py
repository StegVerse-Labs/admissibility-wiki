#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
TRACK_HANDOFF = ROOT / "docs" / "PUBLIC_ANCHOR_RECONSTRUCTION_MIRROR_HANDOFF.md"
INVITATION_STATUS = ROOT / "static" / "status" / "public-anchor-independent-reconstruction-invitation.json"


def fail(message: str) -> None:
    raise SystemExit(f"PUBLIC-ANCHOR RECONSTRUCTION MANIFEST: FAIL - {message}")


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def main() -> None:
    data = load(MANIFEST)
    if data.get("schema_version") != "public-anchor-reconstruction-manifest.v1":
        fail("schema version mismatch")
    if data.get("manifest_id") != "public-anchor-three-docket-freeze-2026-07-27":
        fail("manifest id mismatch")

    commit = data.get("frozen_commit", "")
    if not isinstance(commit, str) or len(commit) != 40:
        fail("frozen commit must be a 40-character SHA")

    dockets = data.get("dockets", [])
    if not isinstance(dockets, list) or len(dockets) != 3:
        fail("exactly three governed dockets are required")
    expected = {
        "review-ta14-reference-docket-2026-07-27",
        "review-asro-reference-docket-2026-07-27",
        "review-stegverse-public-anchor-self-2026-07-27",
    }
    if {item.get("review_id") for item in dockets if isinstance(item, dict)} != expected:
        fail("docket review ids do not match the three-docket freeze")

    for item in dockets:
        if not isinstance(item, dict):
            fail("docket entry must be an object")
        for field in ("page", "record", "validator"):
            value = item.get(field)
            if not isinstance(value, str) or not value:
                fail(f"docket field missing: {field}")
            path = ROOT / value
            if not path.exists():
                fail(f"missing frozen component: {value}")

    controls = data.get("governance_controls", {})
    if not isinstance(controls, dict):
        fail("governance_controls must be an object")
    for field in ("multi_docket_status", "canonical_validation_entry", "canonical_workflow"):
        value = controls.get(field)
        if not isinstance(value, str) or not value:
            fail(f"governance control missing: {field}")
        if not (ROOT / value).exists():
            fail(f"missing governance control: {field}")

    boundary = data.get("authority_boundary", {})
    for key in (
        "manifest_creates_certification",
        "manifest_creates_execution_authority",
        "manifest_establishes_substantive_truth",
        "route_reachability_establishes_validity",
    ):
        if boundary.get(key) is not False:
            fail(f"authority boundary {key} must remain false")

    if data.get("independent_reconstruction_status") != "NOT_RUN":
        fail("independent reconstruction must remain NOT_RUN until evidence exists")
    if data.get("hash_status") != "PENDING_CANONICAL_CUSTODY":
        fail("hash status must remain PENDING_CANONICAL_CUSTODY")
    if data.get("signature_status") != "NOT_SIGNED":
        fail("signature status must remain NOT_SIGNED")

    handoff = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""
    track_handoff = TRACK_HANDOFF.read_text(encoding="utf-8") if TRACK_HANDOFF.exists() else ""
    if "wiki-public-anchor-independent-reconstruction-activation" not in handoff:
        fail("overall handoff does not track the current independent-reconstruction activation goal")
    if "public-anchor reconstruction repair track" not in track_handoff:
        fail("track handoff does not own the reconstruction repair")
    if "independent reconstruction as NOT_RUN" not in track_handoff:
        fail("track handoff does not preserve independent reconstruction as NOT_RUN")

    invitation = load(INVITATION_STATUS)
    if invitation.get("target_manifest_id") != data.get("manifest_id"):
        fail("independent reconstruction invitation is not bound to this frozen manifest")
    if invitation.get("state") != "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED":
        fail("invitation must remain open until an accountable reviewer is assigned")
    if invitation.get("independent_reconstruction_status") != "NOT_RUN":
        fail("invitation must preserve independent reconstruction as NOT_RUN")

    print("PUBLIC-ANCHOR RECONSTRUCTION MANIFEST: PASS - frozen three-docket target, current handoffs, and invitation remain aligned")


if __name__ == "__main__":
    main()
