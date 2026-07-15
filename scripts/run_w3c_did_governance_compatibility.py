#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tests/fixtures/external-frameworks/w3c-did-governance-compatibility-cases.v1.json'
OUTPUT=ROOT/'reports/external-frameworks/w3c-did/w3c-did-stegverse-governance-compatibility-receipt.json'

def evaluate(case):
    r=case['resolution_result']; t=case['transition']
    if r=='ERROR': return 'FAIL_CLOSED','FRAMEWORK_RUNTIME_ERROR'
    if r=='INVALID': return 'DENY','IDENTIFIER_OR_PROOF_INVALID'
    if not t['verification_method_current'] or not t['evidence_fresh']: return 'FAIL_CLOSED','STALE_DID_EVIDENCE'
    if not t['delegation_current']: return 'DENY','AUTHORITY_DRIFT'
    if not t['policy_reference_current']: return 'FAIL_CLOSED','POLICY_DRIFT'
    if not t['controller_matches_actor'] or not t['target_matches_scope']: return 'DENY','ACTOR_OR_SCOPE_DIVERGENCE'
    if not t['execution_context_current']: return 'FAIL_CLOSED','EXECUTION_CONTEXT_DRIFT'
    if not t['recoverability_satisfied']: return 'ESCALATE','RECOVERABILITY_UNRESOLVED'
    return 'ALLOW',None

def main():
    fixture=json.loads(FIXTURE.read_text())
    results=[]; all_match=True
    for case in fixture['cases']:
        result,failure=evaluate(case)
        match=result==case['expected_stegverse_result'] and failure==case['expected_failure_class']
        all_match=all_match and match
        results.append({'case_id':case['case_id'],'family':case['family'],'native_output':case['resolution_result'],'translation_mapping':'DID resolution and verification-method evidence populate identifier and control evidence; StegVerse evaluates actor control, current delegation, policy, scope, freshness, recoverability, and consequence authority independently.','expected_stegverse_result':case['expected_stegverse_result'],'observed_stegverse_result':result,'expected_failure_class':case['expected_failure_class'],'observed_failure_class':failure,'case_match':match})
    receipt={'schema':'w3c_did_stegverse_governance_compatibility_receipt.v1','framework_id':'w3c-did','created_at':datetime.now(timezone.utc).isoformat(),'evidence_posture':'SIMULATED_TRANSLATION_CONTRACT_RUNTIME_PENDING','results':results,'summary':{'total_cases':len(results),'matching_cases':sum(1 for x in results if x['case_match']),'all_expected_results_matched':all_match,'bounded_compatibility_state':'TRANSLATION_CONTRACT_VALIDATED' if all_match else 'COMPATIBILITY_MISMATCH'},'limitations':['No DID method, resolver, DID document, method-state source, or proof verification was executed.','This receipt validates only the declared DID-to-StegVerse translation and governance decision contract.'],'authority_boundary':{'did_control_is_universal_authority':False,'resolution_success_is_current_delegation':False,'compatibility_receipt_is_execution_authority':False,'general_compatibility_claim_allowed':False,'certification_claim_allowed':False}}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f"W3C DID GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1
if __name__=='__main__': raise SystemExit(main())
