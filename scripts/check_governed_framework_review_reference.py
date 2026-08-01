#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static" / "schemas" / "governed-framework-review.schema.json"
RECORD_PATH = ROOT / "static" / "data" / "governed-framework-reviews" / "ta-14.reference-docket.v1.json"
PAGE_PATH = ROOT / "docs" / "external-frameworks" / "ta-14-public-review-docket.md"
HANDOFF_PATH = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
SIDEBAR_PATH = ROOT / "sidebars.js"
STATUS_PATH = ROOT / "static" / "status" / "wiki-public-anchor-reference-docket-status.json"
RECONSTRUCTION_CHECK = ROOT / "scripts" / "check_framework_reconstruction_submission.py"
CORRECTION_CHECK = ROOT / "scripts" / "check_framework_review_correction_receipt.py"


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


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return
    result = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    print(result.stdout.rstrip())
    if result.returncode != 0:
        failures.append(f"{label} validation failed")


def main() -> int:
    failures: list[str] = []
    schema = load_json(SCHEMA_PATH, failures)
    record = load_json(RECORD_PATH, failures)
    status = load_json(STATUS_PATH, failures)

    required = schema.get("required", []) if schema else []
    require(isinstance(required, list), "schema required must be an array", failures)
    for key in required if isinstance(required, list) else []:
        require(key in record, f"record missing required field: {key}", failures)

    require(record.get("schema_version") == "governed-framework-review.v1", "unexpected schema_version", failures)
    require(record.get("review_id") == "review-ta14-reference-docket-2026-07-27", "unexpected review_id", failures)
    require(valid_datetime(record.get("review_time")), "review_time must be ISO-8601", failures)
    require(valid_datetime(record.get("relevant_time_t")), "relevant_time_t must be ISO-8601", failures)
    require(record.get("current_standing") == "PUBLICLY_UNRESOLVED", "TA-14 standing must remain PUBLICLY_UNRESOLVED", failures)
    require(record.get("reconstruction_status") == "PARTIAL", "TA-14 reconstruction status must remain PARTIAL", failures)
    require(record.get("verified_capabilities") == [], "TA-14 must not claim verified capabilities before a live result", failures)

    evidence = record.get("evidence_refs", [])
    require(isinstance(evidence, list) and bool(evidence), "evidence_refs must be non-empty", failures)
    evidence_ids = {item.get("id") for item in evidence if isinstance(item, dict) and isinstance(item.get("id"), str)}
    require(len(evidence_ids) == len(evidence), "evidence ids must be present and unique", failures)
    for section in ("declared_capabilities", "observed_capabilities", "verified_capabilities"):
        values = record.get(section, [])
        require(isinstance(values, list), f"{section} must be an array", failures)
        for item in values if isinstance(values, list) else []:
            for ref in item.get("evidence_refs", []) if isinstance(item, dict) else []:
                require(ref in evidence_ids, f"{section} references unknown evidence id: {ref}", failures)

    tests = record.get("test_results", [])
    require(any(isinstance(item, dict) and item.get("test_id") == "ta14-continuous-standing-revalidation-001" and item.get("result") == "NOT_RUN" for item in tests), "standing test must remain NOT_RUN", failures)
    for item in record.get("determinations", []):
        if isinstance(item, dict):
            require(valid_datetime(item.get("issued_at")), "determination issued_at must be ISO-8601", failures)
            for ref in item.get("basis_refs", []):
                require(ref in evidence_ids, f"determination references unknown evidence id: {ref}", failures)

    page_text = PAGE_PATH.read_text(encoding="utf-8") if PAGE_PATH.exists() else ""
    sidebar_text = SIDEBAR_PATH.read_text(encoding="utf-8") if SIDEBAR_PATH.exists() else ""
    handoff_text = HANDOFF_PATH.read_text(encoding="utf-8") if HANDOFF_PATH.exists() else ""
    for marker in ("review-ta14-reference-docket-2026-07-27", "PUBLICLY_UNRESOLVED", "Public Reconstruction Procedure", "Publication creates no execution authority"):
        require(marker in page_text, f"reference page missing marker: {marker}", failures)
    require("external-frameworks/ta-14-public-review-docket" in sidebar_text, "reference docket missing from sidebar", failures)
    for marker in (
        "Manifest id: public-anchor-three-docket-freeze-2026-07-27",
        "Dockets: TA-14, ASRO, StegVerse public-anchor self-review",
        "TA-14: standing PUBLICLY_UNRESOLVED; reconstruction PARTIAL",
    ):
        require(marker in handoff_text, f"handoff does not bind review governance marker: {marker}", failures)

    require(status.get("reference_review_id") == record.get("review_id"), "status review binding mismatch", failures)
    require(status.get("reference_boundary", {}).get("current_standing") == "PUBLICLY_UNRESOLVED", "status standing mismatch", failures)
    require(status.get("reference_boundary", {}).get("verified_capabilities") == 0, "status must record zero verified capabilities", failures)
    authority = status.get("authority_boundary", {})
    require(authority.get("certification_granted") is False, "status must deny certification", failures)
    require(authority.get("execution_authority_granted") is False, "status must deny execution authority", failures)

    run_check(RECONSTRUCTION_CHECK, "reconstruction submission", failures)
    run_check(CORRECTION_CHECK, "correction receipt", failures)

    if failures:
        print("GOVERNED FRAMEWORK REVIEW REFERENCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("GOVERNED FRAMEWORK REVIEW REFERENCE: PASS - docket, reconstruction submissions, correction receipts, and status are structurally bounded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
