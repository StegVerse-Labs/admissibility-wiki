#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tests/fixtures/external-frameworks/agent-governance-playbook-governance-compatibility-cases.v1.json'
OUT=ROOT/'reports/external-frameworks/agent-governance-playbook/agent-governance-playbook-stegverse-governance-compatibility-receipt.json'

def evaluate(case:dict)->tuple[str,str|None]:
    native=case.get('native_result'); t=case.get('transition',{})
    if native=='playbook_application_error': return 'FAIL_CLOSED','PLAYBOOK_APPLICATION_ERROR'
    if not t.get('source_version_pinned') or not t.get('evidence_fresh'): return 'FAIL_CLOSED','PLAYBOOK_EVIDENCE_STALE'
    if native=='continuation_not_recommended': return 'DENY','PLAYBOOK_CONTINUATION_DENIED'
    if not t.get('delegation_current'): return 'DENY','AUTHORITY_DRIFT'
    if not t.get('scope_matches'): return 'DENY','CONTINUATION_SCOPE_DIVERGENCE'
    if not all(t.get(k) for k in ('actor_identity_verified','policy_reference_current','recoverability_satisfied')): return 'FAIL_CLOSED','CURRENT_STANDING_INCOMPLETE'
    return 'ALLOW',None

def main()->None:
    data=json.loads(FIXTURE.read_text())
    results=[]
    for case in data['cases']:
        actual,failure=evaluate(case)
        results.append({'case_id':case['case_id'],'family':case['family'],'expected_stegverse_result':case['expected_stegverse_result'],'actual_stegverse_result':actual,'expected_failure_class':case['expected_failure_class'],'actual_failure_class':failure,'matched':actual==case['expected_stegverse_result'] and failure==case['expected_failure_class']})
    matched=sum(r['matched'] for r in results)
    receipt={'schema':'external_framework_governance_compatibility_receipt.v1','framework_id':'agent-governance-playbook','evaluation_mode':'DETERMINISTIC_SIMULATION_ONLY','native_execution_observed':False,'source_reviewed':True,'stegverse_governance_compatibility_observed':False,'created_at':datetime.now(timezone.utc).isoformat(),'total_cases':len(results),'matching_cases':matched,'result':'CONTRACT_SIMULATION_PASS' if matched==len(results) else 'CONTRACT_SIMULATION_FAIL','manual_tasks_required':[],'user_action_required':False,'authority_granted':False,'execution_authority_granted':False,'cases':results}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f"AGENT GOVERNANCE PLAYBOOK COMPATIBILITY: {'PASS' if matched==len(results) else 'FAIL'}")
    print(f'cases={len(results)} matched={matched}')
    if matched!=len(results): raise SystemExit(1)

if __name__=='__main__': main()
