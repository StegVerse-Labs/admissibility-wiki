#!/usr/bin/env python3
"""Validate the bounded Alane Zhang architectural-semantics review intake.

This validator deliberately fails closed against publication, certification,
endorsement, implementation-validation, compatibility, and execution-authority
inflation while the reviewer's two publication conditions remain incomplete.
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

    require(data["status"] == "CONDITION_CAPTURE_PENDING", "unexpected review status")
    require(data["publishable"] is False, "incomplete conditions must not be publishable")
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
    require(
        boundary["standing_determination_receipt_distinct_from_candidate_and_execution_boundary"] is True,
        "receipt boundary collapsed",
    )

    conditions = data["publication_conditions"]
    require(conditions["declared_count"] == 2, "publication-condition count changed")
    require(conditions["verbatim_capture_complete"] is False, "conditions falsely marked complete")
    require(conditions["gate"] == "FAIL_CLOSED_UNTIL_COMPLETE", "publication gate weakened")

    suite = data["reported_suite"]
    require(suite["independently_reproduced_in_this_repository"] is False, "unsupported reproduction claim")
    require(suite["claim_posture"] == "REPORTED_NOT_INDEPENDENTLY_REPRODUCED", "suite posture inflated")

    authority = data["authority"]
    require(not any(authority.values()), "intake must grant no authority")

    print("PASS: bounded external-review intake remains fail-closed and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
