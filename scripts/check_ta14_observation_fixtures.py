#!/usr/bin/env python3
"""Validate TA-14 non-halting observation fixtures and category completion."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "static/reviews/ta14/fixtures/observation-cases.v0.1.json"
CATEGORY_MANIFEST = ROOT / "static/reviews/ta14/fixtures/category-manifest.v0.1.json"

REQUIRED_CATEGORIES = {
    "authority",
    "receipt_trust",
    "object_binding",
    "atomic_commit",
    "execution_boundary",
    "refusal",
    "outcome",
    "neutral_review",
}
ALLOWED_STATES = {
    "BUILD_INTERNAL",
    "OBSERVE",
    "EVIDENCE_ABSENT_FAIL_CLOSED",
    "SIMULATED_ONLY",
    "VERIFIED_BOUNDED",
    "DISPUTED_REVIEWER_BURDEN",
    "COMPLETE",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        fail(f"missing fixture file: {path.relative_to(ROOT)}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"unreadable JSON {path.relative_to(ROOT)}: {exc}")
    if not isinstance(payload, dict):
        fail(f"fixture root must be an object: {path.relative_to(ROOT)}")
    return payload


def main() -> int:
    data = load_json(FIXTURES)
    manifest = load_json(CATEGORY_MANIFEST)

    if data.get("schema_version") != "0.1.0":
        fail("unexpected observation fixture schema_version")
    if manifest.get("schema_version") != "0.1.0":
        fail("unexpected category manifest schema_version")
    if manifest.get("source") != str(FIXTURES.relative_to(ROOT)):
        fail("category manifest source does not point to the aggregate fixture file")
    if manifest.get("development_halt") is not False:
        fail("category manifest must preserve development_halt=false")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty list")

    ids: set[str] = set()
    case_categories: dict[str, str] = {}
    categories: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            fail("every case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail("every case requires a non-empty id")
        if case_id in ids:
            fail(f"duplicate case id: {case_id}")
        ids.add(case_id)

        category = case.get("category")
        if category not in REQUIRED_CATEGORIES:
            fail(f"unknown category for {case_id}: {category}")
        categories.add(category)
        case_categories[case_id] = str(category)

        state = case.get("expected_task_state")
        if state not in ALLOWED_STATES:
            fail(f"invalid expected_task_state for {case_id}: {state}")
        if case.get("development_halt") is not False:
            fail(f"fixture must not halt development: {case_id}")

        claim_effect = case.get("expected_claim_effect")
        if not isinstance(claim_effect, str) or not claim_effect:
            fail(f"missing expected_claim_effect: {case_id}")

    missing = REQUIRED_CATEGORIES - categories
    if missing:
        fail(f"missing required fixture categories: {sorted(missing)}")

    manifest_categories = manifest.get("categories")
    if not isinstance(manifest_categories, dict):
        fail("category manifest categories must be an object")
    if set(manifest_categories) != REQUIRED_CATEGORIES:
        fail(
            "category manifest category set mismatch: "
            f"expected={sorted(REQUIRED_CATEGORIES)} actual={sorted(manifest_categories)}"
        )

    manifested_ids: list[str] = []
    for category, listed_ids in manifest_categories.items():
        if not isinstance(listed_ids, list) or not listed_ids:
            fail(f"category manifest entry must be a non-empty list: {category}")
        for case_id in listed_ids:
            if not isinstance(case_id, str) or not case_id:
                fail(f"invalid case id in category manifest: {category}")
            if case_id not in ids:
                fail(f"category manifest references unknown case: {case_id}")
            if case_categories[case_id] != category:
                fail(
                    f"category manifest mismatch for {case_id}: "
                    f"aggregate={case_categories[case_id]} manifest={category}"
                )
            manifested_ids.append(case_id)

    if len(manifested_ids) != len(set(manifested_ids)):
        fail("a fixture id appears more than once in the category manifest")
    if set(manifested_ids) != ids:
        fail(
            "category manifest does not cover aggregate fixture ids exactly: "
            f"missing={sorted(ids - set(manifested_ids))} "
            f"extra={sorted(set(manifested_ids) - ids)}"
        )

    print(
        f"PASS: {len(cases)} TA-14 observation fixtures across "
        f"{len(REQUIRED_CATEGORIES)} categories; development_halt=false for all"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
