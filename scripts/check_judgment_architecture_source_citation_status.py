#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "static/status/judgment-architecture-source-citation-status.json"
PAGE_PATH = ROOT / "docs/external-frameworks/judgment-architecture.md"
HANDOFF_PATH = ROOT / "docs/external-frameworks/JUDGMENT_ARCHITECTURE_MIRROR_HANDOFF.md"


def main() -> int:
    failures: list[str] = []

    for path in [STATUS_PATH, PAGE_PATH, HANDOFF_PATH]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("JUDGMENT ARCHITECTURE SOURCE CITATION STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    page = PAGE_PATH.read_text(encoding="utf-8")
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")

    expected_identity = {
        "title": "Judgment Architecture: A Field Doctrine for Designing Human Judgment at Scale",
        "creator": "Orli Shull",
        "publisher": "Seedling & Star, LLC",
        "publication_year": 2026,
    }
    identity = status.get("publication_identity", {})
    for key, expected in expected_identity.items():
        if identity.get(key) != expected:
            failures.append(f"publication identity mismatch: {key}")

    locator_state = status.get("source_locator_state")
    citation_state = status.get("citation_state")
    promotion_state = status.get("promotion_state")

    allowed_locator_states = {
        "BLOCKED_NO_STABLE_PUBLIC_LOCATOR_FOUND",
        "STABLE_PUBLIC_LOCATOR_BOUND",
        "DURABLE_SOURCE_ARTIFACT_BOUND",
    }
    if locator_state not in allowed_locator_states:
        failures.append("invalid source_locator_state")

    if locator_state == "BLOCKED_NO_STABLE_PUBLIC_LOCATOR_FOUND":
        if citation_state != "PENDING_STABLE_SOURCE":
            failures.append("blocked locator must preserve pending citation state")
        if promotion_state != "FAIL_CLOSED_AT_FIXTURE_READY":
            failures.append("blocked locator must fail closed at fixture_ready")

    boundary = status.get("authority_boundary", {})
    for key in [
        "user_supplied_publication_is_public_locator",
        "search_failure_invalidates_framework",
        "uncited_summary_is_creator_endorsement",
        "citation_intake_grants_interoperability",
        "citation_intake_grants_execution_authority",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"authority boundary must be false: {key}")

    required_page_phrases = [
        "source_state: supplied primary publication observed",
        "validation_state: not validated by StegVerse",
        "compatibility_state: not established",
        "canonical source locator",
        "stable concept citations",
    ]
    for phrase in required_page_phrases:
        if phrase not in page:
            failures.append(f"research page missing bounded source phrase: {phrase}")

    if "judgment-architecture-stable-source-citation-intake" not in handoff:
        failures.append("handoff missing active source citation goal")
    if "stable canonical public source locator" not in handoff:
        failures.append("handoff missing stable source requirement")

    if failures:
        print("JUDGMENT ARCHITECTURE SOURCE CITATION STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("JUDGMENT ARCHITECTURE SOURCE CITATION STATUS: PASS")
    print(f"source_locator_state: {locator_state}")
    print(f"citation_state: {citation_state}")
    print(f"promotion_state: {promotion_state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
