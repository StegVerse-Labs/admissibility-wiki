#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVITATION = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.independent-reconstruction-invitation.v1.json"
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
SCHEMA = ROOT / "static" / "schemas" / "framework-reconstruction-submission.schema.json"
SELF_REVIEW = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.self-review.v1.json"
PAGE = ROOT / "docs" / "stegverse" / "public-anchor-independent-reconstruction.md"
SIDEBAR = ROOT / "sidebars.js"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PUBLIC-ANCHOR RECONSTRUCTION INVITATION: FAIL - {message}")


def load(path: Path) -> dict:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    invitation = load(INVITATION)
    manifest = load(MANIFEST)
    schema = load(SCHEMA)
    self_review = load(SELF_REVIEW)
    require(PAGE.exists(), "public invitation page missing")
    require(SIDEBAR.exists(), "sidebar missing")
    page = PAGE.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    require(invitation.get("schema_version") == "independent-reconstruction-invitation.v1", "schema version mismatch")
    require(invitation.get("review_id") == self_review.get("review_id"), "self-review binding mismatch")
    require(invitation.get("frozen_commit") == manifest.get("frozen_commit"), "frozen commit mismatch")
    require(invitation.get("status") == "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED", "invitation must remain open until a reviewer is accountable")
    require(schema.get("title") == "Framework Reconstruction Submission", "submission schema mismatch")

    current = invitation.get("current_state", {})
    require(current.get("independent_reconstruction_status") == "NOT_RUN", "independent reconstruction must remain NOT_RUN")
    require(current.get("neutral_reviewer_standing") == "NOT_ESTABLISHED", "neutral reviewer standing must remain unestablished")
    require(current.get("automatic_standing_change") is False, "standing must not change automatically")
    require(current.get("current_docket_standing") == "PROVISIONAL", "self-review standing must remain PROVISIONAL")

    reviewer = invitation.get("reviewer_requirements", {})
    require(reviewer.get("accountable_identity_required") is True, "accountable reviewer identity must be required")
    require(reviewer.get("declared_conflicts_required") is True, "conflicts must be declared")
    require(reviewer.get("method_required") is True, "method must be required")
    require(reviewer.get("artifact_refs_required") is True, "artifact references must be required")
    require(reviewer.get("independence_claim_requires_basis") is True, "independence claims require a basis")
    require(reviewer.get("anonymous_unattributed_result_changes_standing") is False, "anonymous output must not change standing")

    boundary = invitation.get("authority_boundary", {})
    for key in (
        "invitation_grants_reviewer_standing",
        "submission_automatically_changes_standing",
        "reconstruction_is_certification",
        "reconstruction_grants_execution_authority",
        "publication_establishes_government_recognition",
    ):
        require(boundary.get(key) is False, f"authority boundary must remain false: {key}")

    require(set(invitation.get("requested_review", {}).get("permitted_results", [])) == {"REPRODUCED", "PARTIAL", "DIVERGENT", "BLOCKED"}, "permitted result set mismatch")

    for marker in (
        invitation.get("invitation_id", ""),
        invitation.get("frozen_commit", ""),
        "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED",
        "anonymous result != standing change",
        "reconstruction != certification",
        "reconstruction != execution authority",
        "DIVERGENT",
        "BLOCKED",
    ):
        require(marker and marker in page, f"public page missing marker: {marker}")
    require("stegverse/public-anchor-independent-reconstruction" in sidebar, "public invitation route missing from sidebar")

    print("PUBLIC-ANCHOR RECONSTRUCTION INVITATION: PASS - invitation, public route, accountability requirements, divergence paths, and non-authority boundaries are aligned")


if __name__ == "__main__":
    main()
