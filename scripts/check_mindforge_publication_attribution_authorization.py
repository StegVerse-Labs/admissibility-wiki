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

    if record.get("schema_version") != "mindforge_publication_attribution_authorization.v2":
        return fail("unexpected authorization schema version")
    if response.get("schema_version") != "mindforge_reviewer_attribution_response.v2":
        return fail("unexpected reviewer-response schema version")
    if intake.get("schema_version") != "0.2.0":
        return fail("unexpected review-intake schema version")
    if record.get("goal_id") != "mindforge-commit-time-boundary-activation":
        return fail("goal_id mismatch")
    if response.get("goal_id") != record.get("goal_id"):
        return fail("reviewer response goal_id mismatch")
    if record.get("requested_statement") != EXPECTED_STATEMENT:
        return fail("requested attribution statement drift")
    if response.get("requested_statement") != EXPECTED_STATEMENT:
        return fail("response requested statement drift")
    if intake.get("reviewer_approved_public_description") != EXPECTED_STATEMENT:
        return fail("intake approved statement drift")

    if record.get("authorization_state") != "AUTHORIZED_EXACT_WITH_BOUNDARIES":
        return fail("authorization must remain exact-with-boundaries")
    if response.get("response_state") != "APPROVED_EXACT_WITH_BOUNDARIES":
        return fail("response must remain exact-with-boundaries")
    if record.get("publication_permitted") is not True or response.get("publication_permitted") is not True:
        return fail("exact approved description must remain publishable")
    if record.get("authorized_statement") != EXPECTED_STATEMENT:
        return fail("authorized statement mismatch")
    if response.get("approved_statement") != EXPECTED_STATEMENT:
        return fail("response approved statement mismatch")
    if response.get("authorization_effect") != "EXACT_DESCRIPTION_ONLY":
        return fail("authorization effect must remain exact-description only")
    if not record.get("authorized_at") or not response.get("received_at"):
        return fail("authorization and response timestamps required")

    intake_ref = str(INTAKE.relative_to(ROOT))
    if record.get("evidence_reference") != intake_ref or response.get("evidence_reference") != intake_ref:
        return fail("evidence reference mismatch")

    for source, label in ((record, "authorization record"), (response, "reviewer response")):
        for field in (
            "official_mindforge_specification", "implementation_endorsed",
            "compatibility_certified", "execution_authority_granted",
        ):
            if source.get(field) is not False:
                return fail(f"{label} {field} must remain false")

    for field in (
        "no_scope_expansion", "private_correspondence_publication_permitted",
        "screenshot_publication_permitted", "unpublished_draft_publication_permitted",
        "stronger_attribution_requires_separate_approval", "stegverse_endorsed",
        "spe_implementation_readiness_validated",
    ):
        expected = {
            "no_scope_expansion": True,
            "private_correspondence_publication_permitted": False,
            "screenshot_publication_permitted": False,
            "unpublished_draft_publication_permitted": False,
            "stronger_attribution_requires_separate_approval": True,
            "stegverse_endorsed": False,
            "spe_implementation_readiness_validated": False,
        }[field]
        if record.get(field) is not expected:
            return fail(f"authorization boundary mismatch: {field}")

    boundaries = response.get("publication_boundaries", {})
    required_true = (
        "no_scope_expansion", "no_stegverse_endorsement", "no_spe_readiness_claim",
        "no_mindforge_compatibility_claim", "no_certification_claim",
        "no_execution_authority_claim", "no_private_correspondence_quote",
        "no_screenshot_publication", "no_unpublished_draft_publication",
        "no_stronger_attribution_without_separate_approval",
    )
    for field in required_true:
        if boundaries.get(field) is not True:
            return fail(f"reviewer response boundary missing: {field}")
    if response.get("reviewer_response_text_publicly_recorded") is not False:
        return fail("private response text must not be publicly recorded")

    conditions = intake.get("publication_conditions", {})
    if conditions.get("normalized_capture_complete") is not True:
        return fail("normalized publication boundaries must be complete")
    if conditions.get("private_verbatim_text_publication_permitted") is not False:
        return fail("private condition text must remain non-public")
    if conditions.get("gate") != "SATISFIED_FOR_EXACT_APPROVED_DESCRIPTION_ONLY":
        return fail("intake gate must remain exact-description only")

    registry_text = REGISTRY.read_text(encoding="utf-8").lower()
    handoff_text = HANDOFF.read_text(encoding="utf-8").lower()
    for marker in (
        "not an official mindforge specification",
        "private correspondence",
        "stronger claim",
        "exact approved",
    ):
        if marker not in registry_text and marker not in handoff_text:
            return fail(f"public boundary marker missing: {marker}")

    print(
        "MINDFORGE ATTRIBUTION AUTHORIZATION: PASS "
        "state=AUTHORIZED_EXACT_WITH_BOUNDARIES publication_permitted=true "
        "private_correspondence_publication=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
