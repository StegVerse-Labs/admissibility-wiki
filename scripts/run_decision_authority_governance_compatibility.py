#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/decision-authority-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/decision-authority/decision-authority-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> str:
    if case.get("malformed"):
        return "FAIL_CLOSED"
    if case.get("mapping_claims_execution_authority"):
        return "FAIL_CLOSED"
    value = case.get("mapped_value")
    if value == "denied":
        return "DENY"
    if value != "allowed":
        return "FAIL_CLOSED"
    if case.get("delegation_current") is False:
        return "DENY"
    if case.get("evidence_current") is False or case.get("policy_current") is False:
        return "FAIL_CLOSED"
    return "ALLOW"


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in fixture["cases"]:
        actual = evaluate(case)
        expected = case["expected_stegverse_result"]
        results.append({"case_id":case["case_id"],"family":case["family"],"expected":expected,"actual":actual,"matched":actual == expected})
    receipt = {
        "schema":"decision_authority_stegverse_governance_compatibility_receipt.v1",
        "framework_id":"decision-authority",
        "record_type":"internal_ecosystem_record",
        "state":"CONTRACT_AUTHORED_RUNTIME_PENDING",
        "simulation_only":True,
        "source_reviewed":True,
        "native_execution_observed":False,
        "independent_reproduction_observed":False,
        "stegverse_governance_compatibility_observed":False,
        "total_cases":len(results),
        "matching_cases":sum(1 for result in results if result["matched"]),
        "results":results,
        "boundaries":{"decision_vocabulary_means_execution_authority":False,"mapped_allow_means_commit_time_admissibility":False,"publication_creates_standing":False},
        "manual_tasks_required":[],
        "user_action_required":False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if receipt["matching_cases"] != receipt["total_cases"]:
        raise SystemExit("DECISION AUTHORITY GOVERNANCE COMPATIBILITY: FAIL")
    print("DECISION AUTHORITY GOVERNANCE COMPATIBILITY: PASS")


if __name__ == "__main__":
    main()
