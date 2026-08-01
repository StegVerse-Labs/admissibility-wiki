#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-public-evidence-gap-review-v2.intake.json"
PAGE = ROOT / "docs/external-frameworks/ta-14-stegverse-public-evidence-gap-review-v2-intake.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TA-14 STEGVERSE GAP REVIEW V2 INTAKE: FAIL - {message}")


def main() -> None:
    require(RECORD.exists(), "machine-readable intake missing")
    require(PAGE.exists(), "public intake page missing")
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "external-review-intake.v1", "schema mismatch")
    require(data.get("artifact", {}).get("sha256") == "4d9bfb86738601952ede6f5e83477ea3c086ce229c3403d2fa3bdaf4ae75bfbf", "source hash mismatch")
    require(data.get("classification", {}).get("status") == "RECEIVED_UNADJUDICATED", "intake must remain unadjudicated")
    require(data.get("adjudication", {}).get("state") == "NOT_STARTED", "adjudication cannot be implied")
    require(set(data.get("adjudication", {}).get("allowed_dispositions", [])) == {"AGREE", "PARTIAL", "DISAGREE", "DEFER"}, "disposition set drift")
    require(data.get("gap_findings") == [f"G-{i:02d}" for i in range(1, 19)], "all eighteen findings must be preserved in order")
    require(data.get("standing", {}).get("ta14") == "PUBLICLY_UNRESOLVED", "TA-14 standing drift")
    require(data.get("standing", {}).get("stegverse_self_review") == "PROVISIONAL", "StegVerse self-review standing drift")
    require(data.get("standing", {}).get("standing_changed_by_intake") is False, "intake cannot change standing")
    for key, value in data.get("authority_boundary", {}).items():
        require(value is False, f"authority boundary must remain false: {key}")
    page = PAGE.read_text(encoding="utf-8")
    for marker in ("preserved as externally asserted findings", "BUILD_STARTED", "RECEIVED_UNADJUDICATED", "no certification"):
        require(marker.lower() in page.lower(), f"public page missing marker: {marker}")
    print("TA-14 STEGVERSE GAP REVIEW V2 INTAKE: PASS - source preserved, standing unchanged, adjudication pending")


if __name__ == "__main__":
    main()
