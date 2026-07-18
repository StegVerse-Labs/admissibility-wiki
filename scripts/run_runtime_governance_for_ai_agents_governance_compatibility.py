#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/runtime-governance-for-ai-agents-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports/external-frameworks/runtime-governance-for-ai-agents/runtime-governance-for-ai-agents-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> str:
    if case.get("framework_claims_execution_authority") is True:
        return "FAIL_CLOSED"
    if case.get("path_evaluation") == "ERROR" or case.get("evidence_current") is not True:
        return "FAIL_CLOSED"
    if case.get("authority_current") is not True or case.get("path_evaluation") == "DENY":
        return "DENY"
    return "ALLOW"


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in fixture["cases"]:
        actual = evaluate(case)
        results.append({"case_id": case["case_id"], "expected": case["expected_stegverse_result"], "actual": actual, "matched": actual == case["expected_stegverse_result"]})
    receipt = {
        "schema": "external_framework_governance_compatibility_receipt.v1",
        "framework_id": "runtime-governance-for-ai-agents",
        "execution_mode": "DETERMINISTIC_SIMULATION_ONLY",
        "native_execution_observed": False,
        "source_reviewed": True,
        "official_source_confirmed": True,
        "implementation_attached": False,
        "path_evaluation_observed": False,
        "independent_reproduction_observed": False,
        "stegverse_governance_compatibility_observed": False,
        "total_cases": len(results),
        "matching_cases": sum(item["matched"] for item in results),
        "results": results,
        "boundaries": {"path_evaluation_means_action_authority": False, "policy_violation_probability_means_commit_time_admissibility": False, "compatibility_receipt_grants_execution_authority": False},
        "manual_tasks_required": [],
        "user_action_required": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if receipt["matching_cases"] != receipt["total_cases"]:
        raise SystemExit("RUNTIME GOVERNANCE FOR AI AGENTS: FAIL")
    print("RUNTIME GOVERNANCE FOR AI AGENTS: PASS")


if __name__ == "__main__":
    main()
