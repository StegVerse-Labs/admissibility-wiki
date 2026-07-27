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

    if intake.get("record_type") != "external_architectural_boundary_review_intake":
        return fail("unexpected intake record type")
    if intake.get("status") != "CONDITION_CAPTURE_PENDING":
        return fail("intake must remain condition-capture pending until both conditions are complete")
    if intake.get("reviewer_approved_public_description") != EXPECTED_STATEMENT:
        return fail("reviewer-approved description drift")
    if intake.get("approval_observed") is not True:
        return fail("approval observation missing")

    conditions = intake.get("publication_conditions", {})
    if conditions.get("declared_count") != 2:
        return fail("expected two declared publication conditions")
    if conditions.get("verbatim_capture_complete") is not False:
        return fail("verbatim condition capture must remain incomplete")
    if conditions.get("gate") != "FAIL_CLOSED_UNTIL_COMPLETE":
        return fail("incomplete conditions must fail closed")

    for field in (
        "publishable", "certification", "endorsement", "implementation_validation",
        "compatibility_certification", "execution_authority_determination",
    ):
        if intake.get(field) is not False:
            return fail(f"{field} must remain false")

    authority = intake.get("authority", {})
    for field in ("publication", "release", "certification", "execution", "cross_repository_mutation"):
        if authority.get(field) is not False:
            return fail(f"authority.{field} must remain false")

    if auth.get("authorization_state") != "CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE":
        return fail("authorization state must reflect observed conditional approval")
    if auth.get("publication_permitted") is not False:
        return fail("conditional approval must not permit publication")
    if auth.get("authorized_statement") != EXPECTED_STATEMENT:
        return fail("conditional authorization statement mismatch")
    if auth.get("evidence_reference") != str(INTAKE.relative_to(ROOT)):
        return fail("authorization evidence reference mismatch")

    if response.get("response_state") != "CONDITIONAL_APPROVAL_INCOMPLETE":
        return fail("response evidence must record incomplete conditional approval")
    if response.get("approved_statement") != EXPECTED_STATEMENT:
        return fail("response approved statement mismatch")
    if response.get("authorization_effect") != "FAIL_CLOSED_PENDING_CONDITION_CAPTURE":
        return fail("response authorization effect mismatch")
    if response.get("publication_permitted") is not False:
        return fail("response evidence must not permit publication")
    if response.get("evidence_reference") != str(INTAKE.relative_to(ROOT)):
        return fail("response evidence reference mismatch")

    print("MINDFORGE REVIEW INTAKE: PASS state=CONDITIONAL_APPROVAL_INCOMPLETE publication_permitted=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
