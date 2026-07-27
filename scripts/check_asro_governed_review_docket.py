#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "governed-framework-review.schema.json"
RECORD = ROOT / "static" / "data" / "governed-framework-reviews" / "asro.reference-docket.v1.json"
PAGE = ROOT / "docs" / "external-frameworks" / "asro-public-review-docket.md"
SIDEBAR = ROOT / "sidebars.js"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def load(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def valid_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def main() -> int:
    failures: list[str] = []
    schema = load(SCHEMA, failures)
    record = load(RECORD, failures)
    if not schema or not record:
        for failure in failures:
            print(f"- {failure}")
        return 1

    for field in schema.get("required", []):
        require(field in record, f"record missing required field: {field}", failures)

    require(record.get("schema_version") == "governed-framework-review.v1", "unexpected schema_version", failures)
    require(record.get("review_id") == "review-asro-reference-docket-2026-07-27", "unexpected review_id", failures)
    require(valid_datetime(record.get("review_time")), "review_time must be ISO-8601", failures)
    require(valid_datetime(record.get("relevant_time_t")), "relevant_time_t must be ISO-8601", failures)

    framework = record.get("framework", {})
    require(isinstance(framework, dict) and framework.get("id") == "asro", "docket must target asro", failures)

    evidence = record.get("evidence_refs", [])
    require(isinstance(evidence, list) and bool(evidence), "evidence_refs must be non-empty", failures)
    evidence_ids = {item.get("id") for item in evidence if isinstance(item, dict) and isinstance(item.get("id"), str)}
    require(len(evidence_ids) == len(evidence), "evidence ids must be present and unique", failures)

    for section in ("declared_capabilities", "observed_capabilities", "verified_capabilities"):
        values = record.get(section)
        require(isinstance(values, list), f"{section} must be an array", failures)
        for capability in values if isinstance(values, list) else []:
            require(isinstance(capability, dict), f"{section} entry must be an object", failures)
            if isinstance(capability, dict):
                for ref in capability.get("evidence_refs", []):
                    require(ref in evidence_ids, f"{section} references unknown evidence: {ref}", failures)

    tests = record.get("test_results", [])
    require(isinstance(tests, list) and len(tests) >= 2, "test_results must include bounded and native tests", failures)
    bounded = [item for item in tests if isinstance(item, dict) and item.get("test_id") == "asro-declared-reference-membership-v1"]
    native = [item for item in tests if isinstance(item, dict) and item.get("test_id") == "asro-native-execution-v1"]
    require(bool(bounded) and bounded[0].get("result") == "PASS", "bounded ASRO test must remain PASS", failures)
    require(bool(native) and native[0].get("result") == "NOT_RUN", "external ASRO-native execution must remain NOT_RUN", failures)

    require(record.get("verified_capabilities") == [], "no ASRO capability may be marked verified before native evidence", failures)
    require(record.get("current_standing") == "PROVISIONAL", "ASRO standing must remain PROVISIONAL", failures)
    require(record.get("reconstruction_status") == "PARTIAL", "ASRO reconstruction must remain PARTIAL", failures)
    require(record.get("challenge_status") == "OPEN", "ASRO challenge path must remain OPEN", failures)

    page = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    sidebar = SIDEBAR.read_text(encoding="utf-8") if SIDEBAR.exists() else ""
    for marker in (
        "review-asro-reference-docket-2026-07-27",
        "External ASRO-native execution: NOT_RUN",
        "Public Reconstruction Procedure",
        "Publication creates no execution authority",
    ):
        require(marker in page, f"ASRO docket page missing marker: {marker}", failures)
    require("external-frameworks/asro-public-review-docket" in sidebar, "ASRO docket missing from sidebar", failures)

    if failures:
        print("ASRO GOVERNED REVIEW DOCKET: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO GOVERNED REVIEW DOCKET: PASS - second public-anchor docket is bounded and reconstructable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
