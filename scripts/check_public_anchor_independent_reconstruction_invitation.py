#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "public-anchor-independent-reconstruction-invitation.json"
MANIFEST = ROOT / "static" / "data" / "governed-framework-reviews" / "public-anchor-reconstruction-manifest.v1.json"
PAGE = ROOT / "docs" / "governance" / "public-anchor-independent-reconstruction-invitation.md"


def fail(message: str) -> None:
    raise SystemExit(f"PUBLIC-ANCHOR INDEPENDENT RECONSTRUCTION INVITATION: FAIL - {message}")


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
    status = load(STATUS)
    manifest = load(MANIFEST)
    if not PAGE.exists():
        fail("invitation page missing")

    if status.get("schema_version") != "public-anchor-independent-reconstruction-invitation.v1":
        fail("schema version mismatch")
    if status.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if status.get("target_manifest_id") != manifest.get("manifest_id"):
        fail("target manifest id mismatch")
    if status.get("target_manifest_path") != str(MANIFEST.relative_to(ROOT)):
        fail("target manifest path mismatch")
    if status.get("submission_schema") != "static/schemas/framework-reconstruction-submission.schema.json":
        fail("submission schema mismatch")

    state = status.get("state")
    reconstruction = status.get("independent_reconstruction_status")
    reviewer_assigned = status.get("accountable_reviewer_assigned")
    accepted_path = status.get("accepted_submission_path")

    if state == "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED":
        if reviewer_assigned is not False:
            fail("open invitation must not claim an assigned reviewer")
        if reconstruction != "NOT_RUN":
            fail("open invitation must preserve reconstruction as NOT_RUN")
        if accepted_path is not None:
            fail("open invitation must not claim an accepted submission")
        if status.get("neutral_reviewer_standing") != "NOT_ESTABLISHED":
            fail("neutral reviewer standing must remain NOT_ESTABLISHED")
    elif state == "ACCEPTED_FOR_REVIEW":
        if reviewer_assigned is not True:
            fail("accepted review must identify an assigned reviewer")
        if not isinstance(accepted_path, str) or not accepted_path:
            fail("accepted review must bind a submission path")
        if not (ROOT / accepted_path).exists():
            fail("accepted reconstruction submission is missing")
    else:
        fail(f"unsupported invitation state: {state}")

    boundary = status.get("authority_boundary", {})
    for key in (
        "invitation_creates_reviewer_standing",
        "invitation_creates_certification",
        "invitation_creates_execution_authority",
        "invitation_creates_custody",
        "submission_automatically_changes_standing",
    ):
        if boundary.get(key) is not False:
            fail(f"authority boundary {key} must be false")

    release = status.get("machine_release_condition", {})
    for key in (
        "reviewer_identity_required",
        "reviewer_conflicts_disclosed_required",
        "frozen_manifest_binding_required",
        "schema_validation_required",
        "run_record_required",
    ):
        if release.get(key) is not True:
            fail(f"machine release condition {key} must be true")

    page = PAGE.read_text(encoding="utf-8")
    for token in (
        "OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED",
        "Independent reconstruction: NOT_RUN",
        "Neutral reviewer standing: NOT_ESTABLISHED",
        "submission accepted != determination adopted",
        "publication != execution authority",
    ):
        if token not in page:
            fail(f"invitation page missing required token: {token}")

    print("PUBLIC-ANCHOR INDEPENDENT RECONSTRUCTION INVITATION: PASS - invitation is open, attributable, and fail-closed")


if __name__ == "__main__":
    main()
