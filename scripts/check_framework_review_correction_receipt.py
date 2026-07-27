#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "framework-review-correction-receipt.schema.json"
EXAMPLE = ROOT / "static" / "data" / "governed-framework-reviews" / "examples" / "ta-14.correction-receipt.example.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FRAMEWORK REVIEW CORRECTION RECEIPT: FAIL - {message}")


def load(path: Path) -> dict:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    schema = load(SCHEMA)
    example = load(EXAMPLE)
    require(schema.get("title") == "Framework Review Correction Receipt", "schema title mismatch")
    require(example.get("schema_version") == "framework-review-correction-receipt.v1", "schema version mismatch")
    require(example.get("review_id") == "review-ta14-reference-docket-2026-07-27", "review binding mismatch")
    require(bool(example.get("changes")), "changes must not be empty")
    require(bool(example.get("prior_record_ref")), "prior record must be preserved")
    require(bool(example.get("corrected_record_ref")), "corrected record must be identified")
    require(example.get("dissent_preserved") is True, "example must preserve dissent")
    require(example.get("standing_effect") == "NONE", "illustrative receipt must not alter standing")
    boundary = example.get("authority_boundary", {})
    require(boundary.get("correction_is_public_record") is True, "correction must remain a public record")
    require(boundary.get("certification_granted") is False, "correction must not grant certification")
    require(boundary.get("execution_authority_granted") is False, "correction must not grant execution authority")
    print("FRAMEWORK REVIEW CORRECTION RECEIPT: PASS")


if __name__ == "__main__":
    main()
