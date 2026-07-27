#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json"
AUTH = ROOT / "static/status/mindforge-publication-attribution-authorization.json"
RESPONSE = ROOT / "docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json"

EXPECTED_STATEMENT = (
    "Reviewed for architectural boundary semantics. The reviewer found the boundary "
    "substantially correct subject to incorporated clarifications. This is not an official "
    "MindForge specification, implementation endorsement, compatibility certification, or "
    "execution-authority determination."
)


def fail(message: str) -> int:
    print(f"MINDFORGE REVIEW INTAKE: FAIL: {message}")
    return 1


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (INTAKE, AUTH, RESPONSE):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    try:
        intake, auth, response = load(INTAKE), load(AUTH), load(RESPONSE)
    except Exception as exc:
        return fail(f"unreadable JSON: {exc}")

    if intake.get("schema_version") != "0.2.0":
        return fail("unexpected intake schema version")
    if intake.get("record_type") != "external_architectural_boundary_review_intake":
        return fail("unexpected intake record type")
    if intake.get("status") != "AUTHORIZED_NARROW_DESCRIPTION_WITH_PUBLICATION_BOUNDARIES":
        return fail("review intake authorization state mismatch")
    if intake.get("reviewer_approved_public_description") != EXPECTED_STATEMENT:
        return fail("reviewer-approved description drift")
    if intake.get("approval_observed") is not True:
        return fail("approval observation missing")

    conditions = intake.get("publication_conditions", {})
    if conditions.get("declared_count") != 2 or conditions.get("fully_captured_count") != 2:
        return fail("two publication boundaries must be captured")
    if conditions.get("normalized_capture_complete") is not True:
        return fail("normalized condition capture must be complete")
    if conditions.get("private_verbatim_text_publication_permitted") is not False:
        return fail("private condition text must remain non-public")
    if conditions.get("gate") != "SATISFIED_FOR_EXACT_APPROVED_DESCRIPTION_ONLY":
        return fail("publication gate must remain exact-description only")

    c1 = conditions.get("condition_1", {})
    c2 = conditions.get("condition_2", {})
    if c1.get("rule") != "NO_SCOPE_EXPANSION":
        return fail("condition 1 normalization mismatch")
    if c2.get("rule") != "NO_PRIVATE_CORRESPONDENCE_PUBLICATION_OR_STRONGER_ATTRIBUTION":
        return fail("condition 2 normalization mismatch")

    for field in (
        "certification", "endorsement", "implementation_validation",
        "compatibility_certification", "execution_authority_determination",
    ):
        if intake.get(field) is not False:
            return fail(f"{field} must remain false")
    if intake.get("publishable") is not True:
        return fail("exact approved description should be publishable")

    custody = intake.get("evidence_custody", {})
    if custody.get("posture") != "PRIVATE_HASH_BOUND_NOT_PUBLICLY_REPRODUCED":
        return fail("private evidence custody posture mismatch")
    if custody.get("public_record_contains_private_verbatim_text") is not False:
        return fail("public record must not contain private verbatim text")
    if custody.get("public_record_contains_screenshots") is not False:
        return fail("public record must not contain screenshots")
    hashes = custody.get("current_session_image_hashes", [])
    if len(hashes) != 4 or not all(isinstance(value, str) and value.startswith("sha256:") for value in hashes):
        return fail("expected four hash-bound private evidence references")

    authority = intake.get("authority", {})
    if authority.get("publication_of_exact_approved_description") is not True:
        return fail("exact description publication authorization missing")
    for field in (
        "publication_of_private_correspondence", "release", "certification",
        "execution", "cross_repository_mutation",
    ):
        if authority.get(field) is not False:
            return fail(f"authority.{field} must remain false")

    if auth.get("authorization_state") != "AUTHORIZED_EXACT_WITH_BOUNDARIES":
        return fail("authorization state mismatch")
    if auth.get("publication_permitted") is not True:
        return fail("authorized exact description must permit publication")
    if auth.get("authorized_statement") != EXPECTED_STATEMENT:
        return fail("authorization statement mismatch")
    if auth.get("evidence_reference") != str(INTAKE.relative_to(ROOT)):
        return fail("authorization evidence reference mismatch")

    if response.get("response_state") != "APPROVED_EXACT_WITH_BOUNDARIES":
        return fail("reviewer response state mismatch")
    if response.get("approved_statement") != EXPECTED_STATEMENT:
        return fail("response approved statement mismatch")
    if response.get("authorization_effect") != "EXACT_DESCRIPTION_ONLY":
        return fail("response authorization effect mismatch")
    if response.get("publication_permitted") is not True:
        return fail("response must permit exact description publication")
    if response.get("reviewer_response_text_publicly_recorded") is not False:
        return fail("private reviewer response must not be publicly recorded verbatim")

    print("MINDFORGE REVIEW INTAKE: PASS state=AUTHORIZED_EXACT_WITH_BOUNDARIES publication_permitted=true private_correspondence_publication=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
