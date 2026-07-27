#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "stegverse" / "public-anchor-self-review-docket.md"
RECORD = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.self-review.v1.json"
SCHEMA = ROOT / "static" / "schemas" / "governed-framework-review.schema.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def load_json(path: Path, failures: list[str]) -> dict:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object", failures)
    return value if isinstance(value, dict) else {}


def valid_datetime(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def main() -> int:
    failures: list[str] = []
    record = load_json(RECORD, failures)
    schema = load_json(SCHEMA, failures)
    page = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    sidebar = SIDEBAR.read_text(encoding="utf-8") if SIDEBAR.exists() else ""
    handoff = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""

    require(schema.get("title") == "Governed Framework Review Record", "review schema title mismatch", failures)
    require(record.get("schema_version") == "governed-framework-review.v1", "unexpected schema version", failures)
    require(record.get("review_id") == "review-stegverse-public-anchor-self-2026-07-27", "unexpected review id", failures)
    require(valid_datetime(record.get("review_time")), "review_time must be ISO-8601", failures)
    require(valid_datetime(record.get("relevant_time_t")), "relevant_time_t must be ISO-8601", failures)

    framework = record.get("framework", {})
    require(framework.get("id") == "stegverse-public-anchor", "framework id mismatch", failures)
    require(record.get("current_standing") == "PROVISIONAL", "self-review standing must remain PROVISIONAL", failures)
    require(record.get("reconstruction_status") == "PARTIAL", "self-review reconstruction must remain PARTIAL", failures)
    require(record.get("challenge_status") == "OPEN", "self-review challenge path must remain OPEN", failures)
    require(record.get("verified_capabilities") == [], "self-review must not claim verified capabilities", failures)

    tests = record.get("test_results", [])
    require(any(item.get("test_id") == "public-anchor-internal-structural-validation-v1" and item.get("result") == "PASS" for item in tests if isinstance(item, dict)), "internal structural test must be PASS", failures)
    require(any(item.get("test_id") == "public-anchor-independent-reciprocal-reconstruction-v1" and item.get("result") == "NOT_RUN" for item in tests if isinstance(item, dict)), "independent reciprocal reconstruction must remain NOT_RUN", failures)

    unsupported = set(record.get("unsupported_claims", []))
    for claim in (
        "Independent external reconstruction is not established.",
        "Neutral reviewer standing is not established.",
        "Government recognition or certification authority is not established.",
        "Internal validator success does not establish substantive correctness.",
    ):
        require(claim in unsupported, f"missing unsupported claim: {claim}", failures)

    for marker in (
        "self-publication != correctness",
        "internal validator PASS != independent reconstruction",
        "repository ownership != reviewer standing",
        "Independent reciprocal reconstruction: NOT_RUN",
        "Publication creates no certification or execution authority",
    ):
        require(marker in page, f"self-review page missing marker: {marker}", failures)

    require("stegverse/public-anchor-self-review-docket" in sidebar, "self-review page missing from sidebar", failures)
    require("reciprocal StegVerse self-review" in handoff or "StegVerse self-review" in handoff, "handoff does not track self-review goal", failures)

    if failures:
        print("STEGVERSE PUBLIC-ANCHOR SELF-REVIEW: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("STEGVERSE PUBLIC-ANCHOR SELF-REVIEW: PASS - reciprocal self-review remains bounded, conflicted, provisional, and independently unresolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
