#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "commit-boundary-binding-cases.json"
SCHEMA = ROOT / "static" / "schemas" / "commit-boundary-binding-record.schema.json"
STATUS = ROOT / "static" / "status" / "commit-boundary-binding-status.json"
RECEIPT = ROOT / "receipts" / "commit-boundary-binding-proof-receipt.json"
DOCTRINE = ROOT / "docs" / "formalisms" / "commit-boundary-binding-predicate.md"
HANDOFF = ROOT / "docs" / "COMMIT_BOUNDARY_BINDING_MIRROR_HANDOFF.md"

VALID_RESULTS = {"BIND", "DENY", "FAIL_CLOSED"}


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def evaluate(record: dict[str, object]) -> tuple[str, list[str]]:
    reasons: list[str] = []

    evidence = record.get("evidence")
    unresolved_values = {
        record.get("origin"),
        record.get("authority"),
        record.get("invariants"),
        record.get("recoverability"),
    }

    if evidence in {"INCOMPLETE", "UNRESOLVED", "STALE"}:
        reasons.append(f"EVIDENCE_{evidence}")
        return "FAIL_CLOSED", reasons

    if "UNRESOLVED" in unresolved_values:
        reasons.append("REQUIRED_CONTROL_UNRESOLVED")
        return "FAIL_CLOSED", reasons

    if record.get("origin") != "VALID":
        reasons.append("ORIGIN_INVALID")
    if record.get("authority") != "VALID":
        reasons.append("AUTHORITY_INVALID")
    if record.get("admissibility") != "ALLOW":
        reasons.append("TRANSITION_INADMISSIBLE")
    if record.get("invariants") != "PRESERVED":
        reasons.append("INVARIANT_NOT_PRESERVED")
    if record.get("recoverability") != "PRESERVED":
        reasons.append("RECOVERABILITY_NOT_PRESERVED")
    if bool(record.get("candidate_replay")):
        reasons.append("CANDIDATE_REPLAY")

    try:
        margin = float(record.get("recoverability_margin"))
        minimum = float(record.get("minimum_margin"))
    except (TypeError, ValueError):
        reasons.append("RECOVERABILITY_MARGIN_INVALID")
    else:
        if margin < minimum:
            reasons.append("RECOVERABILITY_MARGIN_BELOW_MINIMUM")

    if reasons:
        return "DENY", reasons
    return "BIND", ["ALL_REQUIRED_CONTROLS_VALID"]


def require_file(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")


def main() -> int:
    failures: list[str] = []
    for path in (FIXTURES, SCHEMA, STATUS, RECEIPT, DOCTRINE, HANDOFF):
        require_file(path, failures)

    if failures:
        print("COMMIT BOUNDARY BINDING: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    fixture_doc = json.loads(FIXTURES.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    if fixture_doc.get("schema_version") != "commit_boundary_binding_cases.v1":
        failures.append("unexpected fixture schema version")
    if schema.get("title") != "Commit-Boundary Binding Record":
        failures.append("unexpected binding-record schema title")

    observed: list[dict[str, object]] = []
    ids: set[str] = set()
    for case in fixture_doc.get("cases", []):
        case_id = case.get("id")
        expected = case.get("expected")
        record = case.get("record")
        if not isinstance(case_id, str) or not case_id:
            failures.append("fixture has missing case id")
            continue
        if case_id in ids:
            failures.append(f"duplicate fixture id: {case_id}")
        ids.add(case_id)
        if expected not in VALID_RESULTS:
            failures.append(f"{case_id}: invalid expected result {expected}")
            continue
        if not isinstance(record, dict):
            failures.append(f"{case_id}: record must be an object")
            continue

        actual, reasons = evaluate(record)
        observed.append({"id": case_id, "expected": expected, "actual": actual, "reason_codes": reasons})
        if actual != expected:
            failures.append(f"{case_id}: expected {expected}, got {actual} ({', '.join(reasons)})")

    required_cases = {
        "BIND_VALID_TRANSITION",
        "DENY_ORIGIN_INVALID",
        "DENY_AUTHORITY_REVOKED",
        "FAIL_CLOSED_EVIDENCE_STALE",
        "DENY_STATE_DRIFT",
        "DENY_RECOVERABILITY_EROSION",
        "DENY_REPLAY",
        "FAIL_CLOSED_RECEIPT_INCOMPLETE",
    }
    missing_cases = sorted(required_cases - ids)
    if missing_cases:
        failures.append(f"missing required fixtures: {', '.join(missing_cases)}")

    fixture_digest = canonical_sha256(
        {
            "schema_version": fixture_doc.get("schema_version"),
            "cases": [(item["id"], item["actual"]) for item in observed],
        }
    )

    if status.get("goal_id") != "commit-boundary-binding-predicate":
        failures.append("status goal_id mismatch")
    if status.get("state") not in {"IMPLEMENTED", "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_VERIFICATION"}:
        failures.append("status state is not implementation-ready")
    if status.get("fixture_count") != len(observed):
        failures.append("status fixture_count mismatch")
    if status.get("fixture_digest") != f"sha256:{fixture_digest}":
        failures.append("status fixture_digest mismatch")

    receipt_cases = receipt.get("cases")
    if receipt.get("schema_version") != "commit_boundary_binding_proof_receipt.v1":
        failures.append("receipt schema version mismatch")
    if receipt.get("binding_result") != "PASS":
        failures.append("receipt binding_result must be PASS")
    if receipt.get("fixture_digest") != f"sha256:{fixture_digest}":
        failures.append("receipt fixture_digest mismatch")
    if receipt_cases != observed:
        failures.append("receipt case evidence does not match deterministic evaluation")

    doctrine_text = DOCTRINE.read_text(encoding="utf-8")
    for marker in (
        "binding of consequence",
        "OriginValid",
        "AuthorityValid",
        "RecoverabilityPreserved",
        "FAIL_CLOSED",
    ):
        if marker not in doctrine_text:
            failures.append(f"doctrine missing marker: {marker}")

    if failures:
        print("COMMIT BOUNDARY BINDING: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    counts = {result: sum(1 for item in observed if item["actual"] == result) for result in VALID_RESULTS}
    print(
        "COMMIT BOUNDARY BINDING: PASS "
        f"({len(observed)} cases; BIND={counts['BIND']}; DENY={counts['DENY']}; "
        f"FAIL_CLOSED={counts['FAIL_CLOSED']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
