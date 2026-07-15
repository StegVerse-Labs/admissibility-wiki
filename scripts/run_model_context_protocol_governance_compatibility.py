#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/model-context-protocol-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports/external-frameworks/model-context-protocol/model-context-protocol-stegverse-governance-compatibility-receipt.json"

def evaluate(case: dict) -> tuple[str, str | None]:
    native = case["native_result"]
    t = case["transition"]
    if native == "ERROR": return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if native == "DENY": return "DENY", "FRAMEWORK_NEGATIVE_RESULT"
    if not t["tool_registered"] or not t["schema_valid"]: return "FAIL_CLOSED", "CAPABILITY_DEFINITION_INVALID"
    if not t["evidence_fresh"]: return "FAIL_CLOSED", "STALE_CAPABILITY_EVIDENCE"
    if not t["authorization_current"] or not t["target_in_scope"]: return "DENY", "CAPABILITY_AUTHORITY_DIVERGENCE"
    if not t["delegation_current"]: return "DENY", "AUTHORITY_DRIFT"
    if not t["policy_current"]: return "FAIL_CLOSED", "POLICY_DRIFT"
    if not t["recoverability_satisfied"]: return "ESCALATE", "RECOVERABILITY_UNRESOLVED"
    return "ALLOW", None

def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results=[]; all_match=True
    for case in fixture["cases"]:
        result, failure = evaluate(case)
        match = result == case["expected_stegverse_result"] and failure == case["expected_failure_class"]
        all_match = all_match and match
        results.append({"case_id":case["case_id"],"family":case["family"],"native_output":case["native_result"],"translation_mapping":"MCP capability and call artifacts enter as non-authorizing protocol evidence; consequence authority is evaluated independently.","expected_stegverse_result":case["expected_stegverse_result"],"observed_stegverse_result":result,"expected_failure_class":case["expected_failure_class"],"observed_failure_class":failure,"case_match":match})
    receipt={"schema":"model_context_protocol_stegverse_governance_compatibility_receipt.v1","framework_id":"model-context-protocol","created_at":datetime.now(timezone.utc).isoformat(),"evidence_posture":"SIMULATED_TRANSLATION_CONTRACT_RUNTIME_PENDING","results":results,"summary":{"total_cases":len(results),"matching_cases":sum(1 for x in results if x["case_match"]),"all_expected_results_matched":all_match,"bounded_compatibility_state":"TRANSLATION_CONTRACT_VALIDATED" if all_match else "COMPATIBILITY_MISMATCH"},"limitations":["No pinned MCP client or server was executed.","No raw protocol trace or authorization exchange was captured.","This receipt validates only the declared translation and StegVerse governance decision contract."],"authority_boundary":{"tool_discovery_is_execution_authority":False,"successful_call_is_transition_admissibility":False,"compatibility_receipt_is_execution_authority":False,"general_compatibility_claim_allowed":False}}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(f"MCP GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1

if __name__ == "__main__": raise SystemExit(main())
