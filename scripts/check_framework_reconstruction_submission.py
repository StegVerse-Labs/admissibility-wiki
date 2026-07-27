#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "framework-reconstruction-submission.schema.json"
EXAMPLE = ROOT / "static" / "data" / "governed-framework-reviews" / "examples" / "ta-14.reconstruction-submission.example.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FRAMEWORK RECONSTRUCTION SUBMISSION: FAIL - {message}")


def load(path: Path) -> dict:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    schema = load(SCHEMA)
    example = load(EXAMPLE)
    require(schema.get("title") == "Framework Reconstruction Submission", "schema title mismatch")
    require(example.get("schema_version") == "framework-reconstruction-submission.v1", "schema version mismatch")
    require(example.get("review_id") == "review-ta14-reference-docket-2026-07-27", "review binding mismatch")
    require(example.get("result") in {"REPRODUCED", "PARTIAL", "DIVERGENT", "BLOCKED"}, "invalid result")
    require(bool(example.get("artifact_refs")), "artifact_refs must not be empty")
    boundary = example.get("authority_boundary", {})
    require(boundary.get("certification_granted") is False, "submission must not grant certification")
    require(boundary.get("execution_authority_granted") is False, "submission must not grant execution authority")
    require(boundary.get("automatic_standing_change") is False, "submission must not change standing automatically")
    require(example.get("claimed_determination_effect") == "NONE", "example must not alter the TA-14 determination")
    print("FRAMEWORK RECONSTRUCTION SUBMISSION: PASS")


if __name__ == "__main__":
    main()
