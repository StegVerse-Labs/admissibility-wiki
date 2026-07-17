#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tests/fixtures/external-frameworks/mitre-atlas-governance-compatibility-cases.v1.json'
OUT=ROOT/'reports/external-frameworks/mitre-atlas/mitre-atlas-stegverse-governance-compatibility-receipt.json'
def evaluate(case):
    n=case.get('native_result'); t=case.get('transition',{})
    if n=='mapping_error': return 'FAIL_CLOSED','ATLAS_MAPPING_ERROR'
    if not t.get('source_confirmed') or not t.get('technique_mapping_current') or not t.get('evidence_fresh'): return 'FAIL_CLOSED','STALE_THREAT_CONTEXT'
    if n=='critical_unmitigated_technique': return 'DENY','UNMITIGATED_THREAT'
    if not t.get('delegation_current'): return 'DENY','AUTHORITY_DRIFT'
    if not t.get('scope_matches'): return 'DENY','SCOPE_DIVERGENCE'
    if not t.get('policy_current'): return 'FAIL_CLOSED','POLICY_STALE'
    return 'ALLOW',None
def main():
    data=json.loads(FIXTURE.read_text())
    rows=[]
    for c in data['cases']:
        result,failure=evaluate(c)
        rows.append({'case_id':c['case_id'],'family':c['family'],'actual_stegverse_result':result,'actual_failure_class':failure,'matched':result==c['expected_stegverse_result'] and failure==c.get('expected_failure_class')})
    matched=sum(r['matched'] for r in rows)
    receipt={'schema':'external_framework_governance_compatibility_receipt.v1','framework_id':'mitre-atlas','evaluation_mode':'DETERMINISTIC_SIMULATION_ONLY','native_execution_observed':False,'stegverse_governance_compatibility_observed':False,'total_cases':len(rows),'matching_cases':matched,'result':'CONTRACT_SIMULATION_PASS' if matched==len(rows) else 'CONTRACT_SIMULATION_FAIL','manual_tasks_required':[],'user_action_required':False,'authority_granted':False,'execution_authority_granted':False,'cases':rows}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f"MITRE ATLAS GOVERNANCE COMPATIBILITY: {'PASS' if matched==len(rows) else 'FAIL'}")
    print(f'cases={len(rows)} matched={matched}')
    if matched!=len(rows): raise SystemExit(1)
if __name__=='__main__': main()
