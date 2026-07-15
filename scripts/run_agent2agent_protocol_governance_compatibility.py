#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/agent2agent-protocol-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/agent2agent-protocol/agent2agent-protocol-stegverse-governance-compatibility-receipt.json"


def decide(case: dict) -> tuple[str, str]:
    native = case["native_output"]
    gov = case["governance_inputs"]
    if native.get("task_state") in {None, "unknown"} or native.get("agent_card_valid") is not True:
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if native.get("task_state") != "completed" or native.get("artifact_hash_match") is not True:
        return "DENY", "FRAMEWORK_NEGATIVE_RESULT"
    if gov.get("delegation_current") is not True:
        return "DENY", "AUTHORITY_DRIFT"
    if gov.get("evidence_fresh") is not True or gov.get("policy_current") is not True:
        return "FAIL_CLOSED", "STALE_EVIDENCE"
    if gov.get("scope_valid") is not True:
        return "DENY", "SCOPE_DIVERGENCE"
    if gov.get("recoverability_valid") is not True:
        return "FAIL_CLOSED", "RECOVERABILITY_FAILURE"
    return "ALLOW", "NONE"


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in fixture["cases"]:
        observed, failure = decide(case)
        expected = case["expected_stegverse_result"]
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "expected_stegverse_result": expected,
            "observed_stegverse_result": observed,
            "expected_failure_class": case["failure_class"],
            "observed_failure_class": failure,
            "matched": observed == expected and failure == case["failure_class"],
        })
    passed = all(item["matched"] for item in results)
    receipt = {
        "schema": "agent2agent_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "agent2agent-protocol",
        "evidence_posture": fixture["evidence_posture"],
        "native_execution_observed": False,
        "governance_translation_simulation_passed": passed,
        "case_count": len(results),
        "results": results,
        "authority_boundary": fixture["authority_boundary"],
        "limitations": [
            "No pinned A2A implementation or runtime trace is attached.",
            "Simulated native outputs do not establish framework compatibility.",
            "This receipt grants no execution authority or general compatibility claim."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if not passed:
        raise SystemExit("AGENT2AGENT GOVERNANCE COMPATIBILITY: FAIL")
    print("AGENT2AGENT GOVERNANCE COMPATIBILITY: PASS_SIMULATION_RUNTIME_PENDING")


if __name__ == "__main__":
    main()
