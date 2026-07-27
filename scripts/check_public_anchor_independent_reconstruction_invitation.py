#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVITATION = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.independent-reconstruction-invitation.v1.json"
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
SELF_REVIEW = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.self-review.v1.json"
PAGE = ROOT / "docs" / "stegverse" / "public-anchor-independent-reconstruction.md"
SIDEBAR = ROOT / "sidebars.js"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PUBLIC-ANCHOR INDEPENDENT RECONSTRUCTION INVITATION: FAIL - {message}")


def load(path: Path) -> dict:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PUBLIC-ANCHOR INDEPENDENT RECONSTRUCTION INVITATION: FAIL - invalid JSON in {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def main() -> int:
    invitation = load(INVITATION)
    manifest = load(MANIFEST)
    self_review = load(SELF_REVIEW)
    require(PAGE.exists(), "public invitation page missing")
    require(SIDEBAR.exists(), "sidebar missing")
    page = PAGE.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    require(invitation.get("schema_version") == "independent-reconstruction-invitation.v1", "schema version mismatch")
    require(invitation.get("review_id") == self_review.get("review_id"), "review id does not match self-review docket")
    require(invitation.get("frozen_commit") == manifest.get("frozen_commit"), "frozen commit does not match reconstruction manifest")
    require(invitation.get("status") == "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED", "invitation must remain open until an accountable reviewer is assigned")

    requested = invitation.get("requested_review", {})
    require(set(requested.get("permitted_results", [])) == {"REPRODUCED", "PARTIAL", "DIVERGENT", "BLOCKED"}, "permitted results must preserve divergence and blocked outcomes")
    require(len(requested.get("minimum_scope", [])) >= 5, "minimum review scope is incomplete")
    require(len(requested.get("required_outputs", [])) >= 8, "required output set is incomplete")

    reviewer = invitation.get("reviewer_requirements", {})
    for key in ("accountable_identity_required", "declared_conflicts_required", "method_required", "artifact_refs_required", "independence_claim_requires_basis"):
        require(reviewer.get(key) is True, f"reviewer requirement must be true: {key}")
    require(reviewer.get("anonymous_unattributed_result_changes_standing") is False, "anonymous results must not change standing")

    current = invitation.get("current_state", {})
    require(current.get("independent_reconstruction_status") == "NOT_RUN", "independent reconstruction must remain NOT_RUN before submission")
    require(current.get("neutral_reviewer_standing") == "NOT_ESTABLISHED", "neutral reviewer standing must remain unresolved")
    require(current.get("automatic_standing_change") is False, "submission must not automatically change standing")

    boundary = invitation.get("authority_boundary", {})
    for key in ("invitation_grants_reviewer_standing", "submission_automatically_changes_standing", "reconstruction_is_certification", "reconstruction_grants_execution_authority", "publication_establishes_government_recognition"):
        require(boundary.get(key) is False, f"authority boundary must remain false: {key}")

    required_page_markers = (
        invitation.get("invitation_id", ""),
        invitation.get("frozen_commit", ""),
        "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED",
        "anonymous result != standing change",
        "reconstruction != certification",
        "reconstruction != execution authority",
        "DIVERGENT",
        "BLOCKED",
    )
    for marker in required_page_markers:
        require(marker and marker in page, f"public page missing marker: {marker}")
    require("stegverse/public-anchor-independent-reconstruction" in sidebar, "public invitation route missing from sidebar")

    print("PUBLIC-ANCHOR INDEPENDENT RECONSTRUCTION INVITATION: PASS - invitation, public route, accountability requirements, and non-authority boundaries are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
