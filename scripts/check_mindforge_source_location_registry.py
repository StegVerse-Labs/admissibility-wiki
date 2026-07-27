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
    "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json",
    "scripts/check_mindforge_review_intake.py",
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
    "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "ADMISSIBILITY_MIRROR_HANDOFF.md",
)

REGISTRY_MARKERS = (
    "External canonical MindForge source: NOT ATTACHED",
    "Conditional review intake: approval observed, conditions incomplete, fail closed",
    "Reviewer attribution authorization: explicit complete conditions required",
    "Reviewer response evidence: preserve what is observed; do not invent missing verbatim text",
    "Publication verification: successful workflow, build, deployment, and route evidence required",
    "Neither becomes an official MindForge specification",
    "CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE",
    "FAIL_CLOSED_UNTIL_COMPLETE",
    "No downstream location becomes an independent editorial or canonical MindForge source",
)

HANDOFF_MARKERS = (
    "IMPLEMENTED_CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE_AND_CANONICAL_VERIFICATION",
    "Canonical workflow: .github/workflows/validate-chain-continuation.yml",
    "Last observed run: 30244212970",
    "STANDING DETERMINATION RECEIPT: PASS",
    "repository-wide fail-closed gate",
    "data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json",
    "scripts/check_mindforge_review_intake.py",
    "CONDITIONAL_APPROVAL_INCOMPLETE",
    "mindforge-publication-verification.template.json",
)


def main() -> int:
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            failures.append(f"missing aligned source location: {relative}")

    registry_text = REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else ""
    handoff_text = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""

    if not registry_text:
        failures.append("missing source-location registry")
    if not handoff_text:
        failures.append("missing MindForge goal handoff")

    for marker in REGISTRY_MARKERS:
        if marker not in registry_text:
            failures.append(f"registry missing boundary marker: {marker}")
    for relative in REQUIRED_FILES:
        if relative not in registry_text and relative not in {
            "docs/external-frameworks/evidence/mindforge-source-location-registry.md"
        }:
            failures.append(f"registry missing location entry: {relative}")
    for marker in HANDOFF_MARKERS:
        if marker not in handoff_text:
            failures.append(f"handoff missing alignment marker: {marker}")

    if not ROOT_HANDOFF.exists():
        failures.append("missing root handoff pointer")
    elif "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md" not in ROOT_HANDOFF.read_text(encoding="utf-8"):
        failures.append("root handoff does not point to MindForge goal handoff")

    if failures:
        print("MINDFORGE SOURCE LOCATION ALIGNMENT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "MINDFORGE SOURCE LOCATION ALIGNMENT: PASS "
        f"({len(REQUIRED_FILES)} locations; canonical_external_source=NOT_ATTACHED; "
        "condition_capture=FAIL_CLOSED; downstream_editorial_authority=NONE; "
        "publication_verification=RUN_BOUND_ONLY)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
