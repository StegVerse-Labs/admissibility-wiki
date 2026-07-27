#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "mindforge-publication-attribution-authorization.json"
HANDOFF = ROOT / "docs" / "MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md"
REGISTRY = ROOT / "docs" / "external-frameworks" / "evidence" / "mindforge-source-location-registry.md"

EXPECTED_STATEMENT = (
    "Reviewed for architectural boundary semantics. The reviewer found the boundary "
    "substantially correct subject to incorporated clarifications. This is not an official "
    "MindForge specification, implementation endorsement, compatibility certification, or "
    "execution-authority determination."
)

VALID_STATES = {
    "PENDING_REVIEWER_RESPONSE",
    "AUTHORIZED_EXACT",
    "AUTHORIZED_MODIFIED",
    "REJECTED",
}


def fail(message: str) -> int:
    print(f"MINDFORGE ATTRIBUTION AUTHORIZATION: FAIL: {message}")
    return 1


def main() -> int:
    for path in (STATUS, HANDOFF, REGISTRY):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    try:
        record = json.loads(STATUS.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"authorization record unreadable: {exc}")

    if record.get("schema_version") != "mindforge_publication_attribution_authorization.v1":
        return fail("unexpected schema version")
    if record.get("goal_id") != "mindforge-commit-time-boundary-activation":
        return fail("goal_id mismatch")
    if record.get("requested_statement") != EXPECTED_STATEMENT:
        return fail("requested attribution statement drift")

    state = record.get("authorization_state")
    if state not in VALID_STATES:
        return fail(f"invalid authorization state: {state}")

    for field in (
        "official_mindforge_specification",
        "implementation_endorsed",
        "compatibility_certified",
        "execution_authority_granted",
    ):
        if record.get(field) is not False:
            return fail(f"{field} must remain false")

    permitted = record.get("publication_permitted")
    authorized_statement = record.get("authorized_statement")
    authorized_at = record.get("authorized_at")
    evidence_reference = record.get("evidence_reference")

    if state == "PENDING_REVIEWER_RESPONSE":
        if permitted is not False:
            return fail("pending authorization must not permit publication")
        if any(value is not None for value in (authorized_statement, authorized_at, evidence_reference)):
            return fail("pending authorization must not contain approval evidence")
    elif state == "AUTHORIZED_EXACT":
        if permitted is not True:
            return fail("exact authorization must permit publication")
        if authorized_statement != EXPECTED_STATEMENT:
            return fail("exact authorization statement mismatch")
        if not authorized_at or not evidence_reference:
            return fail("exact authorization requires timestamp and evidence reference")
    elif state == "AUTHORIZED_MODIFIED":
        if permitted is not True:
            return fail("modified authorization must permit publication")
        if not isinstance(authorized_statement, str) or not authorized_statement.strip():
            return fail("modified authorization requires approved statement")
        if not authorized_at or not evidence_reference:
            return fail("modified authorization requires timestamp and evidence reference")
    elif state == "REJECTED":
        if permitted is not False:
            return fail("rejected authorization must not permit publication")
        if not evidence_reference:
            return fail("rejection requires evidence reference")

    registry_text = REGISTRY.read_text(encoding="utf-8")
    handoff_text = HANDOFF.read_text(encoding="utf-8")
    for marker in (
        "not an official MindForge specification",
        "publication authority",
        "external canonical MindForge source",
    ):
        if marker.lower() not in registry_text.lower():
            return fail(f"source registry missing marker: {marker}")
    if "Silence does not constitute authorization" not in STATUS.read_text(encoding="utf-8"):
        return fail("authorization record must reject authorization by silence")
    if "Public statement boundary" not in handoff_text:
        return fail("handoff missing public statement boundary")

    print(
        "MINDFORGE ATTRIBUTION AUTHORIZATION: PASS "
        f"state={state} publication_permitted={str(permitted).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
