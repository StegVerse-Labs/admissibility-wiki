#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/external-frameworks/evidence/mindforge-source-location-registry.md"
PUBLICATION_HANDOFF = ROOT / "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md"
REVIEW_HANDOFF = ROOT / "data/external-reviews/mindforge/MINDFORGE_REVIEW_MIRROR_HANDOFF.md"
PROVENANCE = ROOT / "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json"
ROOT_HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
ROOT_POINTER = ROOT / "ADMISSIBILITY_MIRROR_HANDOFF.md"

REQUIRED_FILES = (
    "docs/external-frameworks/mindforge.md",
    "docs/external-frameworks/commit-time-interoperability-contract.md",
    "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md",
    "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json",
    "receipts/mindforge-provenance-date-correction-2026-08-18.json",
    "receipts/mindforge-provenance-source-recovery-search-2026-08-21.json",
    "data/external-reviews/mindforge/MINDFORGE_REVIEW_MIRROR_HANDOFF.md",
    "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json",
    "scripts/check_mindforge_review_intake.py",
    "scripts/check_alane_zhang_boundary_review_intake.py",
    "docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json",
    "scripts/check_mindforge_commit_time_boundary.py",
    "static/schemas/standing-determination-receipt.schema.json",
    "tests/fixtures/standing-determination-cases.json",
    "scripts/check_standing_determination_receipt.py",
    "static/status/mindforge-boundary-review-status.json",
    "receipts/mindforge-boundary-review-receipt.json",
    "static/status/mindforge-publication-attribution-authorization.json",
    "docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json",
    "scripts/check_mindforge_publication_attribution_authorization.py",
    "docs/external-frameworks/evidence/mindforge-publication-verification.template.json",
    "scripts/check_mindforge_publication_verification.py",
    "scripts/check_mindforge_source_location_registry.py",
    "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md",
    "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "ADMISSIBILITY_MIRROR_HANDOFF.md",
)

REGISTRY_MARKERS = (
    "External canonical MindForge source: NOT ATTACHED",
    "Review attribution: exact approved description only",
    "Private correspondence: hash-bound provenance only; not publicly quoted or reproduced",
    "Publication boundaries: no scope expansion, private correspondence, screenshots, unpublished drafts, or stronger attribution",
    "Publication verification: successful workflow, build, deployment, and route evidence required",
    "Source-date verification: exact recovery of one or more seven hash-bound captures required; negative search is not proof of absence",
    "Neither becomes an official MindForge specification",
    "authorization_state = AUTHORIZED_EXACT_WITH_BOUNDARIES",
    "private_correspondence_publication_permitted = false",
    "stronger_attribution_requires_separate_approval = true",
    "correspondence_date_status = UNVERIFIED",
    "bounded_library_candidates_hash_checked = 16",
    "exact_hash_matches = 0",
    "required_next_transition = recover_exact_bound_source_capture_and_verify_dates",
    "No downstream location becomes an independent editorial or canonical MindForge source",
)

PUBLICATION_HANDOFF_MARKERS = (
    "state: COMPLETE_PUBLIC_ROUTE_VERIFIED",
    "run_id: 30837466398",
    "STANDING DETERMINATION RECEIPT: auditable result, no execution command",
    "AUTHORIZED_EXACT_WITH_BOUNDARIES",
    "private_correspondence_publication_permitted: false",
    "NO publication of screenshots",
    "mindforge-publication-verification.template.json",
    "Full repository validation is not claimed",
)

REVIEW_HANDOFF_MARKERS = (
    "PUBLIC_DATE_ASSERTION_CORRECTED_SOURCE_DATE_VERIFICATION_PENDING",
    "bounded Library candidate images hash-checked: 16",
    "exact source-capture hash matches: 0",
    "captured_date_range: null",
    "required_next_transition: recover_exact_bound_source_capture_and_verify_dates",
    "archive_state: NOT_READY",
    "repository_release: NOT_AUTHORIZED",
    "repository_activation: NOT_COMPLETE",
)


def main() -> int:
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            failures.append(f"missing aligned source location: {relative}")

    registry_text = REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else ""
    publication_handoff_text = PUBLICATION_HANDOFF.read_text(encoding="utf-8") if PUBLICATION_HANDOFF.exists() else ""
    review_handoff_text = REVIEW_HANDOFF.read_text(encoding="utf-8") if REVIEW_HANDOFF.exists() else ""

    if not registry_text:
        failures.append("missing source-location registry")
    if not publication_handoff_text:
        failures.append("missing completed MindForge publication handoff")
    if not review_handoff_text:
        failures.append("missing active MindForge provenance-review handoff")

    for marker in REGISTRY_MARKERS:
        if marker not in registry_text:
            failures.append(f"registry missing boundary marker: {marker}")
    for relative in REQUIRED_FILES:
        if relative not in registry_text and relative not in {
            "docs/external-frameworks/evidence/mindforge-source-location-registry.md"
        }:
            failures.append(f"registry missing location entry: {relative}")
    for marker in PUBLICATION_HANDOFF_MARKERS:
        if marker not in publication_handoff_text:
            failures.append(f"publication handoff missing alignment marker: {marker}")
    for marker in REVIEW_HANDOFF_MARKERS:
        if marker not in review_handoff_text:
            failures.append(f"review handoff missing alignment marker: {marker}")

    if not ROOT_HANDOFF.exists():
        failures.append("missing canonical repository handoff")
    if not ROOT_POINTER.exists():
        failures.append("missing root compatibility pointer")
    elif "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md" not in ROOT_POINTER.read_text(encoding="utf-8"):
        failures.append("root compatibility pointer does not identify canonical repository handoff")

    if not PROVENANCE.exists():
        failures.append("missing machine-readable MindForge provenance")
    else:
        try:
            provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"unreadable MindForge provenance JSON: {exc}")
        else:
            basis = provenance.get("date_verification_basis", {})
            previous = provenance.get("previously_recorded_unverified_range", {})
            if provenance.get("correspondence_date_status") != "UNVERIFIED":
                failures.append("provenance correspondence_date_status must remain UNVERIFIED until direct source recovery")
            if provenance.get("captured_date_range") is not None:
                failures.append("provenance captured_date_range must remain null until direct source verification")
            if basis.get("exact_source_capture_hash_match_recovered") is not False:
                failures.append("provenance must not claim exact source recovery")
            if basis.get("bound_source_capture_count") != 7:
                failures.append("provenance must preserve seven bound source-capture hashes")
            if basis.get("bounded_library_candidates_hash_checked") != 16:
                failures.append("provenance recovery denominator must equal 16")
            if basis.get("exact_hash_matches") != 0:
                failures.append("provenance must preserve zero exact source-capture matches")
            if previous.get("status") != "RETRACTED_FROM_ASSERTED_PROVENANCE_UNTIL_DIRECTLY_VERIFIED":
                failures.append("previous unverified range must remain retracted from asserted provenance")
            if basis.get("later_correspondence_substitution_permitted") is not False:
                failures.append("later correspondence must not substitute for original source-date proof")

    if failures:
        print("MINDFORGE SOURCE LOCATION ALIGNMENT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "MINDFORGE SOURCE LOCATION ALIGNMENT: PASS "
        f"({len(REQUIRED_FILES)} locations; canonical_external_source=NOT_ATTACHED; "
        "attribution=AUTHORIZED_EXACT_WITH_BOUNDARIES; private_correspondence_publication=PROHIBITED; "
        "source_date=UNVERIFIED; source_candidates_checked=16; exact_source_matches=0; "
        "downstream_editorial_authority=NONE; publication_verification=RUN_BOUND_ONLY)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
