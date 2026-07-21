#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "discovery-governance-handoff-cases.json"
RECEIPT = ROOT / "reports" / "discovery-governance-handoff-proof-receipt.json"
REQUIRED_NON_AUTHORITY = {
    "CONSENT", "STANDING", "AUTHORITY", "ADMISSIBILITY", "COMMITMENT",
    "EXECUTION_PERMISSION", "CERTIFICATION", "ENDORSEMENT",
}
REQUIRED_FIELDS = {
    "schema_version", "handoff_id", "recommendation_id", "discovery_system",
    "opportunity", "declared_context", "inferred_context", "provenance",
    "confidence_basis", "participants", "prerequisites", "boundaries",
    "unresolved_assumptions", "proposed_action", "destination_layer",
    "required_consent", "required_authority", "evidence_refs",
    "non_authority_declaration", "generated_at", "expires_at",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def evaluate(record: dict) -> str:
    if not REQUIRED_FIELDS.issubset(record):
        return "FAIL_CLOSED"
    if record.get("schema_version") != "discovery_governance_handoff.v1":
        return "FAIL_CLOSED"
    if not record.get("provenance") or not record.get("evidence_refs"):
        return "FAIL_CLOSED"
    if not record.get("participants") or not record.get("boundaries"):
        return "FAIL_CLOSED"
    declarations = set(record.get("non_authority_declaration", []))
    if not REQUIRED_NON_AUTHORITY.issubset(declarations):
        return "FAIL_CLOSED"
    try:
        if parse_time(record["expires_at"]) <= parse_time(record["generated_at"]):
            return "FAIL_CLOSED"
    except (TypeError, ValueError):
        return "FAIL_CLOSED"
    authority_assertions = set(record.get("authority_assertions", []))
    if authority_assertions & REQUIRED_NON_AUTHORITY:
        return "DENY"
    if record.get("unresolved_assumptions"):
        return "REVIEW_REQUIRED"
    return "HANDOFF_READY"


def write_receipt(fixture_bytes: bytes, results: list[dict], failures: list[str]) -> None:
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "discovery_governance_handoff_proof_receipt.v1",
        "goal_id": "discovery-governance-minimum-handoff",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixture_path": str(FIXTURES.relative_to(ROOT)),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "results": results,
        "overall_result": "PASS" if not failures else "FAIL_CLOSED",
        "failure_reasons": failures,
        "outcome_coverage": sorted({item["actual"] for item in results}),
        "consent_granted": False,
        "standing_granted": False,
        "authority_granted": False,
        "admissibility_granted": False,
        "commitment_granted": False,
        "execution_permission_granted": False,
        "certification_granted": False,
        "endorsement_granted": False,
        "interoperability_verified": False,
        "downstream_mutation_authority_granted": False,
        "manual_task_requirement": "NONE",
        "user_manual_action_required": False,
        "non_claims": [
            "A passing fixture receipt establishes deterministic checker behavior only.",
            "The receipt does not grant consent, standing, authority, admissibility, commitment, execution permission, certification, endorsement, interoperability standing, or downstream mutation authority."
        ]
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    results: list[dict] = []
    if not FIXTURES.exists():
        failures.append(f"missing {FIXTURES.relative_to(ROOT)}")
        write_receipt(b"", results, failures)
        print("DISCOVERY GOVERNANCE HANDOFF: FAIL")
        print(f"- {failures[0]}")
        return 1

    fixture_bytes = FIXTURES.read_bytes()
    try:
        payload = json.loads(fixture_bytes)
    except json.JSONDecodeError as exc:
        failures.append(f"fixture JSON invalid: {exc}")
        write_receipt(fixture_bytes, results, failures)
        print("DISCOVERY GOVERNANCE HANDOFF: FAIL")
        print(f"- {failures[0]}")
        return 1

    cases = payload.get("cases", [])
    if not cases:
        failures.append("fixture set has no cases")
    for case in cases:
        case_id = case.get("case_id")
        actual = evaluate(case.get("record", {}))
        expected = case.get("expected")
        matched = actual == expected
        results.append({"case_id": case_id, "expected": expected, "actual": actual, "matched": matched})
        print(f"{case_id}: {actual}")
        if not matched:
            failures.append(f"{case_id} expected {expected}, got {actual}")

    required_outcomes = {"HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED"}
    observed = {item["actual"] for item in results}
    if not required_outcomes.issubset(observed):
        failures.append("fixture set does not exercise all deterministic outcomes")

    write_receipt(fixture_bytes, results, failures)
    print(f"wrote {RECEIPT.relative_to(ROOT)}")
    if failures:
        print("DISCOVERY GOVERNANCE HANDOFF: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
