#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/external-frameworks/evidence/mindforge-source-location-registry.md"
HANDOFF = ROOT / "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md"
ROOT_HANDOFF = ROOT / "ADMISSIBILITY_MIRROR_HANDOFF.md"

REQUIRED_FILES = (
    "docs/external-frameworks/mindforge.md",
    "docs/external-frameworks/commit-time-interoperability-contract.md",
    "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md",
    "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json",
    "docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json",
    "scripts/check_mindforge_commit_time_boundary.py",
    "static/schemas/standing-determination-receipt.schema.json",
    "tests/fixtures/standing-determination-cases.json",
    "scripts/check_standing_determination_receipt.py",
    "static/status/mindforge-boundary-review-status.json",
    "receipts/mindforge-boundary-review-receipt.json",
    "static/status/mindforge-publication-attribution-authorization.json",
    "scripts/check_mindforge_publication_attribution_authorization.py",
    "scripts/check_mindforge_source_location_registry.py",
    "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md",
    "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "ADMISSIBILITY_MIRROR_HANDOFF.md",
)

REGISTRY_MARKERS = (
    "External canonical MindForge source: NOT ATTACHED",
    "Private correspondence: provenance evidence only",
    "StegVerse doctrine: discussion-derived interpretation",
    "Reviewer attribution authorization: explicit response required; silence creates no authorization",
    "nine-case reconstruction of the original private boundary discussion",
    "ten-case StegVerse conformance suite",
    "Neither becomes an official MindForge specification",
    "Publication attribution remains prohibited",
    "No downstream location becomes an independent editorial or canonical MindForge source",
)

HANDOFF_MARKERS = (
    "mindforge-source-location-registry.md",
    "IMPLEMENTED_CANONICAL_CHECK_PASSED_REPOSITORY_CHAIN_FAILED_UNRELATED_GATES",
    "Canonical run: 30244212970",
    "STANDING DETERMINATION RECEIPT: PASS",
    "repository-wide validation: FAIL_CLOSED_OBSERVED",
    "A passing goal-local checker does not override the repository-wide fail-closed gate",
)


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            failures.append(f"missing aligned source location: {relative}")

    if not REGISTRY.exists():
        failures.append(f"missing registry: {REGISTRY.relative_to(ROOT)}")
        registry_text = ""
    else:
        registry_text = REGISTRY.read_text(encoding="utf-8")

    for marker in REGISTRY_MARKERS:
        if marker not in registry_text:
            failures.append(f"registry missing boundary marker: {marker}")

    for relative in REQUIRED_FILES:
        if relative not in registry_text and relative not in {
            "docs/external-frameworks/evidence/mindforge-source-location-registry.md"
        }:
            failures.append(f"registry missing location entry: {relative}")

    if not HANDOFF.exists():
        failures.append(f"missing handoff: {HANDOFF.relative_to(ROOT)}")
        handoff_text = ""
    else:
        handoff_text = HANDOFF.read_text(encoding="utf-8")

    for marker in HANDOFF_MARKERS:
        if marker not in handoff_text:
            failures.append(f"handoff missing alignment marker: {marker}")

    if not ROOT_HANDOFF.exists():
        failures.append("missing root handoff pointer")
    else:
        root_text = ROOT_HANDOFF.read_text(encoding="utf-8")
        if "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md" not in root_text:
            failures.append("root handoff does not point to MindForge goal handoff")

    if failures:
        print("MINDFORGE SOURCE LOCATION ALIGNMENT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "MINDFORGE SOURCE LOCATION ALIGNMENT: PASS "
        f"({len(REQUIRED_FILES)} locations; canonical_external_source=NOT_ATTACHED; "
        "downstream_editorial_authority=NONE; attribution_authorization=EXPLICIT_ONLY)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
