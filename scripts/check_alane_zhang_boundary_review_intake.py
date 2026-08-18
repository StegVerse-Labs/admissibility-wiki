#!/usr/bin/env python3
"""Validate the bounded MindForge architectural-semantics review intake.

The validator permits publication only for the exact reviewer-approved narrow
architectural-boundary description after both publication conditions are
captured. It continues to reject certification, endorsement, implementation
validation, compatibility certification, execution authority, release
authority, cross-repository mutation authority, private correspondence
publication, and stronger attribution.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json"

APPROVED_DESCRIPTION = (
    "Reviewed for architectural boundary semantics. The reviewer found the "
    "boundary substantially correct subject to incorporated clarifications. "
    "This is not an official MindForge specification, implementation "
    "endorsement, compatibility certification, or execution-authority "
    "determination."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    data = json.loads(RECORD.read_text(encoding="utf-8"))

    require(
        data["status"] == "AUTHORIZED_NARROW_DESCRIPTION_WITH_PUBLICATION_BOUNDARIES",
        "unexpected review status",
    )
    require(data["publishable"] is True, "exact approved description should be publishable")
    require(data["review_scope"] == "architectural boundary semantics only", "scope expanded")
    require(
        data["reviewer_approved_public_description"] == APPROVED_DESCRIPTION,
        "reviewer-approved wording changed",
    )

    for field in (
        "certification",
        "endorsement",
        "implementation_validation",
        "compatibility_certification",
        "execution_authority_determination",
    ):
        require(data[field] is False, f"forbidden authority inflation: {field}")

    boundary = data["confirmed_boundary"]
    require(boundary["commitment_candidate_non_authorizing"] is True, "candidate authority drift")
    require(boundary["standing_reconstructed_fresh_at_commit_time"] is True, "standing freshness lost")
    require(boundary["allow_is_admissibility_not_execution"] is True, "ALLOW execution conflation")
    require(boundary["deny_means_reconstructable_standing_rejects_transition"] is True, "DENY semantics drift")
    require(boundary["fail_closed_when_current_state_cannot_be_safely_established"] is True, "FAIL-CLOSED semantics drift")
    require(
        boundary["standing_determination_receipt_distinct_from_candidate_and_execution_boundary"] is True,
        "standing-determination receipt boundary collapsed",
    )

    conditions = data["publication_conditions"]
    require(conditions["declared_count"] == 2, "publication-condition count changed")
    require(conditions["fully_captured_count"] == 2, "publication conditions incomplete")
    require(conditions["normalized_capture_complete"] is True, "normalized condition capture incomplete")
    require(
        conditions["private_verbatim_text_publication_permitted"] is False,
        "private correspondence publication boundary weakened",
    )
    require(
        conditions["condition_1"]["rule"] == "NO_SCOPE_EXPANSION",
        "condition 1 scope boundary changed",
    )
    require(
        conditions["condition_2"]["rule"] == "NO_PRIVATE_CORRESPONDENCE_PUBLICATION_OR_STRONGER_ATTRIBUTION",
        "condition 2 privacy/attribution boundary changed",
    )
    require(
        conditions["gate"] == "SATISFIED_FOR_EXACT_APPROVED_DESCRIPTION_ONLY",
        "publication gate changed",
    )

    custody = data["evidence_custody"]
    require(
        custody["posture"] == "PRIVATE_HASH_BOUND_NOT_PUBLICLY_REPRODUCED",
        "evidence custody posture changed",
    )
    require(custody["public_record_contains_private_verbatim_text"] is False, "private text leaked into public record")
    require(custody["public_record_contains_screenshots"] is False, "private screenshots leaked into public record")
    require(len(custody["current_session_image_hashes"]) > 0, "source-image hash custody missing")

    authority = data["authority"]
    require(authority["publication_of_exact_approved_description"] is True, "bounded publication authority missing")
    require(authority["publication_of_private_correspondence"] is False, "private correspondence publication authorized")
    require(authority["release"] is False, "release authority inflated")
    require(authority["certification"] is False, "certification authority inflated")
    require(authority["execution"] is False, "execution authority inflated")
    require(authority["cross_repository_mutation"] is False, "cross-repository authority inflated")

    print("PASS: bounded MindForge review intake preserves exact publication and non-authority boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
