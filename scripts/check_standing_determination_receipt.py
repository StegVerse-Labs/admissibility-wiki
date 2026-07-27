#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "standing-determination-cases.json"
SCHEMA = ROOT / "static" / "schemas" / "standing-determination-receipt.schema.json"
STATUS = ROOT / "static" / "status" / "mindforge-boundary-review-status.json"
RECEIPT = ROOT / "receipts" / "mindforge-boundary-review-receipt.json"
CONTRACT = ROOT / "docs" / "external-frameworks" / "commit-time-interoperability-contract.md"
MIND_FORGE = ROOT / "docs" / "external-frameworks" / "mindforge.md"

VALID_RESULTS = {"ALLOW", "DENY", "FAIL_CLOSED"}

UNCERTAIN = {
    "policy_state": {"AMBIGUOUS", "MISSING", "STALE", "UNVERIFIABLE"},
    "delegation_state": {"PARTIALLY_REVOKED", "AMBIGUOUS", "MISSING", "UNVERIFIABLE"},
    "evidence_state": {"HASH_MISMATCH", "TAMPERED", "MISSING", "STALE", "UNVERIFIABLE", "CORRUPTED"},
    "time_state": {"UNAVAILABLE", "SKEWED", "AMBIGUOUS"},
    "actor_state": {"AMBIGUOUS", "MISSING", "UNVERIFIABLE"},
    "target_state": {"AMBIGUOUS", "ALIASED", "MISSING", "UNVERIFIABLE"},
    "action_state": {"SEMANTIC_DRIFT", "AMBIGUOUS", "MISSING", "UNVERIFIABLE"},
    "scope_state": {"AMBIGUOUS", "MISSING", "UNVERIFIABLE"},
    "recoverability_state": {"UNAVAILABLE", "AMBIGUOUS", "DEGRADED_UNSAFE", "UNVERIFIABLE"},
}

INVALID = {
    "policy_state": {"INVALID", "EXPIRED"},
    "delegation_state": {"REVOKED", "EXPIRED", "INVALID"},
    "actor_state": {"INVALID", "SUBSTITUTED"},
    "target_state": {"INVALID", "SUBSTITUTED"},
    "action_state": {"INVALID"},
    "scope_state": {"INVALID", "MISMATCH"},
    "recoverability_state": {"NOT_PRESERVED"},
}


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def evaluate(record: dict[str, object]) -> tuple[str, list[str]]:
    if record.get("candidate_authorizing") is not False:
        return "FAIL_CLOSED", ["CANDIDATE_AUTHORITY_INVARIANT_VIOLATED"]

    for field, states in UNCERTAIN.items():
        value = record.get(field)
        if value in states:
            return "FAIL_CLOSED", [f"{field.upper()}_{value}"]

    reasons: list[str] = []
    for field, states in INVALID.items():
        value = record.get(field)
        if value in states:
            reasons.append(f"{field.upper()}_{value}")

    if reasons:
        return "DENY", reasons

    required_valid = {
        "policy_state": "VALID",
        "delegation_state": "VALID",
        "evidence_state": "VERIFIED",
        "time_state": "VALID",
        "actor_state": "VALID",
        "target_state": "VALID",
        "action_state": "VALID",
        "scope_state": "VALID",
        "recoverability_state": "PRESERVED",
    }
    unresolved = [field for field, expected in required_valid.items() if record.get(field) != expected]
    if unresolved:
        return "FAIL_CLOSED", [f"UNRECOGNIZED_OR_MISSING_{field.upper()}" for field in unresolved]

    reasons = ["CURRENT_STANDING_RECONSTRUCTED"]
    if record.get("execution_requested") is True:
        reasons.append("ALLOW_IS_NOT_EXECUTION_COMMAND")
    return "ALLOW", reasons


def main() -> int:
    failures: list[str] = []
    for path in (FIXTURES, SCHEMA, STATUS, RECEIPT, CONTRACT, MIND_FORGE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("STANDING DETERMINATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    fixture_doc = json.loads(FIXTURES.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    if fixture_doc.get("schema_version") != "standing_determination_cases.v1":
        failures.append("unexpected fixture schema version")
    if schema.get("title") != "Standing Determination Receipt":
        failures.append("unexpected standing receipt schema title")

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
        if expected not in VALID_RESULTS or not isinstance(record, dict):
            failures.append(f"{case_id}: malformed fixture")
            continue
        actual, reasons = evaluate(record)
        observed.append({"id": case_id, "expected": expected, "actual": actual, "reason_codes": reasons})
        if actual != expected:
            failures.append(f"{case_id}: expected {expected}, got {actual}")

    required_cases = {
        "ALLOW_RECONSTRUCTED_CURRENT_STANDING",
        "DENY_KNOWN_INVALID_STANDING",
        "FAIL_CLOSED_EVIDENCE_HASH_MISMATCH",
        "FAIL_CLOSED_POLICY_VERSION_AMBIGUOUS",
        "FAIL_CLOSED_PARTIAL_DELEGATION_REVOCATION",
        "FAIL_CLOSED_TRUSTED_TIME_UNAVAILABLE",
        "FAIL_CLOSED_TARGET_IDENTITY_AMBIGUOUS",
        "FAIL_CLOSED_ACTION_SEMANTIC_DRIFT",
        "FAIL_CLOSED_RECOVERY_PATH_UNAVAILABLE",
        "ALLOW_DOES_NOT_EXECUTE",
    }
    missing = sorted(required_cases - ids)
    if missing:
        failures.append(f"missing required fixtures: {', '.join(missing)}")

    digest = canonical_sha256({
        "schema_version": fixture_doc.get("schema_version"),
        "cases": [(item["id"], item["actual"]) for item in observed],
    })

    if status.get("goal_id") != "mindforge-commit-time-boundary-activation":
        failures.append("status goal_id mismatch")
    if status.get("state") not in {"IMPLEMENTED", "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_VERIFICATION"}:
        failures.append("status state is not implementation-ready")
    if status.get("fixture_count") != len(observed):
        failures.append("status fixture_count mismatch")
    if status.get("fixture_digest") != f"sha256:{digest}":
        failures.append("status fixture_digest mismatch")

    if receipt.get("schema_version") != "mindforge_boundary_review_receipt.v1":
        failures.append("receipt schema version mismatch")
    if receipt.get("review_scope") != "BOUNDARY_SEMANTICS_ONLY":
        failures.append("receipt scope must remain boundary semantics only")
    if receipt.get("implementation_endorsed") is not False:
        failures.append("receipt must not endorse implementation")
    if receipt.get("compatibility_certified") is not False:
        failures.append("receipt must not certify compatibility")
    if receipt.get("execution_authority_granted") is not False:
        failures.append("receipt must not grant execution authority")
    if receipt.get("fixture_digest") != f"sha256:{digest}":
        failures.append("receipt fixture_digest mismatch")
    if receipt.get("cases") != observed:
        failures.append("receipt case evidence does not match deterministic evaluation")

    contract_text = CONTRACT.read_text(encoding="utf-8")
    mindforge_text = MIND_FORGE.read_text(encoding="utf-8")
    for marker in (
        "Standing Determination Receipt",
        "ALLOW",
        "DENY",
        "FAIL-CLOSED",
        "does not authorize execution",
    ):
        if marker not in contract_text:
            failures.append(f"contract missing marker: {marker}")
    for marker in ("discussion-derived", "does not certify MindForge", "execution authority"):
        if marker not in mindforge_text:
            failures.append(f"MindForge page missing marker: {marker}")

    if failures:
        print("STANDING DETERMINATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    counts = {result: sum(1 for item in observed if item["actual"] == result) for result in VALID_RESULTS}
    print(
        "STANDING DETERMINATION RECEIPT: PASS "
        f"({len(observed)} cases; ALLOW={counts['ALLOW']}; DENY={counts['DENY']}; "
        f"FAIL_CLOSED={counts['FAIL_CLOSED']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
