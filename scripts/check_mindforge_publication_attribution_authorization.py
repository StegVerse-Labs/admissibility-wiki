#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/mindforge-publication-attribution-authorization.json"
RESPONSE = ROOT / "docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json"
INTAKE = ROOT / "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json"
HANDOFF = ROOT / "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md"
REGISTRY = ROOT / "docs/external-frameworks/evidence/mindforge-source-location-registry.md"

EXPECTED_STATEMENT = (
    "Reviewed for architectural boundary semantics. The reviewer found the boundary "
    "substantially correct subject to incorporated clarifications. This is not an official "
    "MindForge specification, implementation endorsement, compatibility certification, or "
    "execution-authority determination."
)

VALID_STATES = {
    "PENDING_REVIEWER_RESPONSE",
    "CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE",
    "AUTHORIZED_EXACT",
    "AUTHORIZED_MODIFIED",
    "REJECTED",
}
VALID_RESPONSE_STATES = {
    "NOT_RECEIVED",
    "CONDITIONAL_APPROVAL_INCOMPLETE",
    "APPROVED_EXACT",
    "APPROVED_MODIFIED",
    "REJECTED",
}


def fail(message: str) -> int:
    print(f"MINDFORGE ATTRIBUTION AUTHORIZATION: FAIL: {message}")
    return 1


def main() -> int:
    for path in (STATUS, RESPONSE, INTAKE, HANDOFF, REGISTRY):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    try:
        record = json.loads(STATUS.read_text(encoding="utf-8"))
        response = json.loads(RESPONSE.read_text(encoding="utf-8"))
        intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"authorization evidence unreadable: {exc}")

    if record.get("schema_version") != "mindforge_publication_attribution_authorization.v1":
        return fail("unexpected schema version")
    if response.get("schema_version") != "mindforge_reviewer_attribution_response.v1":
        return fail("unexpected reviewer-response schema version")
    if record.get("goal_id") != "mindforge-commit-time-boundary-activation":
        return fail("goal_id mismatch")
    if response.get("goal_id") != record.get("goal_id"):
        return fail("reviewer response goal_id mismatch")
    if record.get("requested_statement") != EXPECTED_STATEMENT or response.get("requested_statement") != EXPECTED_STATEMENT:
        return fail("requested attribution statement drift")

    state = record.get("authorization_state")
    response_state = response.get("response_state")
    if state not in VALID_STATES:
        return fail(f"invalid authorization state: {state}")
    if response_state not in VALID_RESPONSE_STATES:
        return fail(f"invalid reviewer response state: {response_state}")

    for source, label in ((record, "authorization record"), (response, "reviewer response")):
        for field in (
            "official_mindforge_specification", "implementation_endorsed",
            "compatibility_certified", "execution_authority_granted",
        ):
            if source.get(field) is not False:
                return fail(f"{label} {field} must remain false")

    permitted = record.get("publication_permitted")
    authorized_statement = record.get("authorized_statement")
    authorized_at = record.get("authorized_at")
    evidence_reference = record.get("evidence_reference")
    intake_ref = str(INTAKE.relative_to(ROOT))

    if state == "PENDING_REVIEWER_RESPONSE":
        if permitted is not False or response_state != "NOT_RECEIVED":
            return fail("pending state must remain non-publishable with no response")
        if any(record.get(field) is not None for field in ("authorized_statement", "authorized_at", "evidence_reference")):
            return fail("pending authorization must not contain approval evidence")
    elif state == "CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE":
        if permitted is not False:
            return fail("conditional approval must remain non-publishable")
        if authorized_statement != EXPECTED_STATEMENT:
            return fail("conditional approved statement mismatch")
        if authorized_at is not None:
            return fail("conditional approval must not claim final authorization time")
        if evidence_reference != intake_ref:
            return fail("conditional approval evidence reference mismatch")
        if response_state != "CONDITIONAL_APPROVAL_INCOMPLETE":
            return fail("conditional authorization requires incomplete conditional response state")
        if response.get("approved_statement") != EXPECTED_STATEMENT:
            return fail("conditional response statement mismatch")
        if response.get("authorization_effect") != "FAIL_CLOSED_PENDING_CONDITION_CAPTURE":
            return fail("conditional response must fail closed")
        if response.get("publication_permitted") is not False:
            return fail("conditional response must not permit publication")
        conditions = intake.get("publication_conditions", {})
        if conditions.get("verbatim_capture_complete") is not False or conditions.get("gate") != "FAIL_CLOSED_UNTIL_COMPLETE":
            return fail("conditional intake must remain fail-closed until verbatim condition capture")
    elif state == "AUTHORIZED_EXACT":
        if permitted is not True or authorized_statement != EXPECTED_STATEMENT:
            return fail("exact authorization mismatch")
        if not authorized_at or not evidence_reference or response_state != "APPROVED_EXACT":
            return fail("exact authorization requires complete response evidence")
    elif state == "AUTHORIZED_MODIFIED":
        if permitted is not True or not isinstance(authorized_statement, str) or not authorized_statement.strip():
            return fail("modified authorization mismatch")
        if not authorized_at or not evidence_reference or response_state != "APPROVED_MODIFIED":
            return fail("modified authorization requires complete response evidence")
        if response.get("approved_statement") != authorized_statement:
            return fail("modified approved statements must match")
    elif state == "REJECTED":
        if permitted is not False or not evidence_reference or response_state != "REJECTED":
            return fail("rejected authorization evidence mismatch")

    if response_state != "NOT_RECEIVED":
        if not response.get("evidence_reference") or not response.get("response_channel"):
            return fail("observed response requires evidence reference and response channel")
        if response.get("evidence_reference") != evidence_reference:
            return fail("authorization and response evidence references must match")
        if response.get("publication_permitted") is not permitted:
            return fail("authorization and response publication flags must match")

    registry_text = REGISTRY.read_text(encoding="utf-8").lower()
    handoff_text = HANDOFF.read_text(encoding="utf-8")
    for marker in (
        "not an official mindforge specification", "publication authority",
        "external canonical mindforge source", "mindforge-reviewer-attribution-response.template.json",
        "alane-zhang-boundary-semantics-review-intake.json",
    ):
        if marker not in registry_text:
            return fail(f"source registry missing marker: {marker}")
    if "Public statement boundary" not in handoff_text:
        return fail("handoff missing public statement boundary")

    print(
        "MINDFORGE ATTRIBUTION AUTHORIZATION: PASS "
        f"state={state} response_state={response_state} publication_permitted={str(permitted).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
