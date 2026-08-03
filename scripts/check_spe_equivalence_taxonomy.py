#!/usr/bin/env python3
"""Validate the SPE equivalence taxonomy registry.

This validator is intentionally structural and fail-closed. It does not certify
external frameworks and does not claim that the taxonomy is complete.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "status" / "spe-equivalence-taxonomy.json"
PAGE = ROOT / "docs" / "external-frameworks" / "spe-equivalence-taxonomy.md"

REQUIRED_CLASSES = {
    "closest_conceptual_equivalent",
    "similar",
    "overlapping",
    "adjacent",
    "not_equivalent",
}

REQUIRED_FALSE_BOUNDARIES = {
    "creates_execution_authority",
    "creates_certification",
    "claims_market_exclusivity",
    "claims_final_research_closure",
    "adopts_external_framework_claims",
}


def fail(message: str) -> None:
    raise SystemExit(f"SPE EQUIVALENCE TAXONOMY: FAIL - {message}")


def main() -> None:
    if not REGISTRY.exists():
        fail(f"missing registry: {REGISTRY}")
    if not PAGE.exists():
        fail(f"missing source page: {PAGE}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    page_text = PAGE.read_text(encoding="utf-8")

    if data.get("standing") != "PROVISIONAL_TAXONOMY":
        fail("standing must remain PROVISIONAL_TAXONOMY")

    boundaries = data.get("authority_boundary")
    if not isinstance(boundaries, dict):
        fail("authority_boundary must be an object")

    for key in REQUIRED_FALSE_BOUNDARIES:
        if boundaries.get(key) is not False:
            fail(f"authority boundary {key} must be false")

    classes = data.get("classes")
    if not isinstance(classes, list):
        fail("classes must be a list")

    class_ids = {entry.get("class_id") for entry in classes if isinstance(entry, dict)}
    missing_classes = sorted(REQUIRED_CLASSES - class_ids)
    if missing_classes:
        fail(f"missing relationship classes: {', '.join(missing_classes)}")

    frameworks = data.get("frameworks")
    if not isinstance(frameworks, list) or len(frameworks) < 10:
        fail("frameworks must include at least ten classified records")

    seen_names: set[str] = set()
    seen_relationship_classes: set[str] = set()
    for index, framework in enumerate(frameworks, start=1):
        if not isinstance(framework, dict):
            fail(f"framework record {index} must be an object")
        name = framework.get("name")
        relationship_class = framework.get("relationship_class")
        boundary = framework.get("boundary")
        summary = framework.get("relationship_summary")
        if not name or not isinstance(name, str):
            fail(f"framework record {index} missing name")
        if name in seen_names:
            fail(f"duplicate framework name: {name}")
        seen_names.add(name)
        if relationship_class not in REQUIRED_CLASSES:
            fail(f"framework {name} has invalid relationship_class {relationship_class!r}")
        if not boundary or not isinstance(boundary, str):
            fail(f"framework {name} missing boundary")
        if not summary or not isinstance(summary, str):
            fail(f"framework {name} missing relationship_summary")
        seen_relationship_classes.add(relationship_class)

    required_observed = {
        "closest_conceptual_equivalent",
        "similar",
        "overlapping",
        "adjacent",
    }
    missing_observed = sorted(required_observed - seen_relationship_classes)
    if missing_observed:
        fail(f"taxonomy lacks framework records for classes: {', '.join(missing_observed)}")

    equivalents = data.get("equivalent_frameworks_confirmed")
    if equivalents != []:
        fail("equivalent_frameworks_confirmed must remain empty unless independently supported")

    unique = data.get("unique_stegverse_combination")
    if not isinstance(unique, list) or len(unique) < 7:
        fail("unique_stegverse_combination must list the composite StegVerse elements")

    required_page_phrases = [
        "No located external framework",
        "not as a claim of market exclusivity",
        "Equivalent: none confirmed",
        "This taxonomy does not prove novelty.",
    ]
    for phrase in required_page_phrases:
        if phrase not in page_text:
            fail(f"source page missing required phrase: {phrase}")

    print("SPE EQUIVALENCE TAXONOMY: PASS")


if __name__ == "__main__":
    main()
