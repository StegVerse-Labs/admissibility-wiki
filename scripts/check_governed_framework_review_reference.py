#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static" / "schemas" / "governed-framework-review.schema.json"
RECORD_PATH = ROOT / "static" / "data" / "governed-framework-reviews" / "ta-14.reference-docket.v1.json"
PAGE_PATH = ROOT / "docs" / "external-frameworks" / "ta-14-public-review-docket.md"
HANDOFF_PATH = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
SIDEBAR_PATH = ROOT / "sidebars.js"


def load_json(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return value


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


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
    schema = load_json(SCHEMA_PATH, failures)
    record = load_json(RECORD_PATH, failures)

    if not schema or not record:
        for failure in failures:
            print(f"- {failure}")
        return 1

    required = schema.get("required", [])
    require(isinstance(required, list), "schema required must be an array", failures)
    for key in required if isinstance(required, list) else []:
        require(key in record, f"record missing required field: {key}", failures)

    require(record.get("schema_version") == "governed-framework-review.v1", "unexpected schema_version", failures)
    require(record.get("review_id") == "review-ta14-reference-docket-2026-07-27", "unexpected review_id", failures)
    require(valid_datetime(record.get("review_time")), "review_time must be ISO-8601", failures)
    require(valid_datetime(record.get("relevant_time_t")), "relevant_time_t must be ISO-8601", failures)

    framework = record.get("framework")
    require(isinstance(framework, dict), "framework must be an object", failures)
    if isinstance(framework, dict):
        for key in ("id", "name", "version"):
            require(isinstance(framework.get(key), str) and bool(framework.get(key)), f"framework.{key} is required", failures)
        require(framework.get("id") == "ta-14", "reference docket must target ta-14", failures)

    enum_fields = {
        "challenge_status": {"OPEN", "UNCHALLENGED", "CHALLENGED", "RESOLVED", "CLOSED_WITH_DISSENT"},
        "reconstruction_status": {"NOT_ATTEMPTED", "PARTIAL", "REPRODUCED", "DIVERGENT", "BLOCKED_BY_EVIDENCE"},
        "current_standing": {"INTAKE", "PROVISIONAL", "PARTIALLY_VERIFIED", "VERIFIED_WITHIN_SCOPE", "CONTRADICTED", "PUBLICLY_UNRESOLVED", "SUPERSEDED", "WITHDRAWN", "REVOKED"},
    }
    for field, allowed in enum_fields.items():
        require(record.get(field) in allowed, f"invalid {field}: {record.get(field)!r}", failures)

    evidence = record.get("evidence_refs")
    require(isinstance(evidence, list) and bool(evidence), "evidence_refs must be a non-empty array", failures)
    evidence_ids: set[str] = set()
    if isinstance(evidence, list):
        for index, item in enumerate(evidence):
            require(isinstance(item, dict), f"evidence_refs[{index}] must be an object", failures)
            if not isinstance(item, dict):
                continue
            evidence_id = item.get("id")
            require(isinstance(evidence_id, str) and bool(evidence_id), f"evidence_refs[{index}].id is required", failures)
            if isinstance(evidence_id, str):
                require(evidence_id not in evidence_ids, f"duplicate evidence id: {evidence_id}", failures)
                evidence_ids.add(evidence_id)
            require(item.get("access") in {"PUBLIC", "AUTHORIZED", "DERIVED_PROOF", "WITHHELD"}, f"invalid evidence access at index {index}", failures)

    capability_sections = ("declared_capabilities", "observed_capabilities", "verified_capabilities")
    for section in capability_sections:
        values = record.get(section)
        require(isinstance(values, list), f"{section} must be an array", failures)
        if not isinstance(values, list):
            continue
        for index, capability in enumerate(values):
            require(isinstance(capability, dict), f"{section}[{index}] must be an object", failures)
            if not isinstance(capability, dict):
                continue
            for ref in capability.get("evidence_refs", []):
                require(ref in evidence_ids, f"{section}[{index}] references unknown evidence id: {ref}", failures)

    tests = record.get("test_results")
    require(isinstance(tests, list) and bool(tests), "test_results must be a non-empty array", failures)
    if isinstance(tests, list):
        for index, test in enumerate(tests):
            require(isinstance(test, dict), f"test_results[{index}] must be an object", failures)
            if not isinstance(test, dict):
                continue
            require(test.get("result") in {"PASS", "FAIL", "PARTIAL", "ERROR", "NOT_RUN", "INCONCLUSIVE"}, f"invalid test result at index {index}", failures)
            for ref in test.get("evidence_refs", []):
                require(ref in evidence_ids, f"test_results[{index}] references unknown evidence id: {ref}", failures)

    verified = record.get("verified_capabilities", [])
    not_run_tests = [test for test in tests if isinstance(test, dict) and test.get("result") == "NOT_RUN"] if isinstance(tests, list) else []
    require(not verified, "TA-14 reference docket must not claim verified capabilities before a live result", failures)
    require(bool(not_run_tests), "TA-14 reference docket must preserve the proposed test as NOT_RUN", failures)
    require(record.get("current_standing") == "PUBLICLY_UNRESOLVED", "TA-14 standing must remain PUBLICLY_UNRESOLVED", failures)
    require(record.get("reconstruction_status") == "PARTIAL", "TA-14 reconstruction status must remain PARTIAL", failures)

    determinations = record.get("determinations")
    require(isinstance(determinations, list) and bool(determinations), "determinations must be a non-empty array", failures)
    if isinstance(determinations, list):
        for index, determination in enumerate(determinations):
            require(isinstance(determination, dict), f"determinations[{index}] must be an object", failures)
            if not isinstance(determination, dict):
                continue
            require(valid_datetime(determination.get("issued_at")), f"determinations[{index}].issued_at must be ISO-8601", failures)
            for ref in determination.get("basis_refs", []):
                require(ref in evidence_ids, f"determinations[{index}] references unknown evidence id: {ref}", failures)

    page_text = PAGE_PATH.read_text(encoding="utf-8") if PAGE_PATH.exists() else ""
    sidebar_text = SIDEBAR_PATH.read_text(encoding="utf-8") if SIDEBAR_PATH.exists() else ""
    handoff_text = HANDOFF_PATH.read_text(encoding="utf-8") if HANDOFF_PATH.exists() else ""

    for marker in (
        "review-ta14-reference-docket-2026-07-27",
        "PUBLICLY_UNRESOLVED",
        "Public Reconstruction Procedure",
        "Publication creates no execution authority",
    ):
        require(marker in page_text, f"reference page missing marker: {marker}", failures)

    require("external-frameworks/ta-14-public-review-docket" in sidebar_text, "reference docket missing from sidebar", failures)
    require("REFERENCE_DOCKET_IMPLEMENTED_PENDING_CANONICAL_VALIDATION" in handoff_text, "handoff does not record reference docket implementation", failures)

    if failures:
        print("GOVERNED FRAMEWORK REVIEW REFERENCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("GOVERNED FRAMEWORK REVIEW REFERENCE: PASS - TA-14 docket is structurally bounded and reconstructable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
