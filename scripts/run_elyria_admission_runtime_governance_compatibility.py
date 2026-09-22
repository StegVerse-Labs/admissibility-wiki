#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/elyria-admission-runtime-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports/external-frameworks/elyria-admission-runtime/elyria-admission-runtime-stegverse-governance-compatibility-receipt.json"

def evaluate(case: dict) -> str:
    if case.get("foreign_verdict_claimed_as_stegverse_authority") is True:
        return "FAIL_CLOSED"
    if case.get("endpoint_evidence_qualified") is not True or case.get("evidence_current") is not True:
        return "FAIL_CLOSED"
    if case.get("authority_current") is not True or case.get("foreign_verdict") == "REFUSE":
        return "DENY"
    return "ALLOW"

def main() -> None:
    fixture=json.loads(FIXTURE.read_text(encoding="utf-8"))
    results=[]
    for case in fixture["cases"]:
        actual=evaluate(case)
        results.append({"case_id":case["case_id"],"expected":case["expected_stegverse_result"],"actual":actual,"matched":actual==case["expected_stegverse_result"]})
    receipt={
      "schema":"external_framework_governance_compatibility_receipt.v1",
      "framework_id":"elyria-admission-runtime",
      "execution_mode":"DETERMINISTIC_SIMULATION_ONLY",
      "native_execution_observed":False,
      "source_reviewed":True,
      "official_source_confirmed":True,
      "runtime_endpoint_observed":False,
      "authentic_stegverse_roundtrip_observed":False,
      "stegverse_governance_compatibility_observed":False,
      "total_cases":len(results),
      "matching_cases":sum(item["matched"] for item in results),
      "results":results,
      "boundaries":{"foreign_verdict_means_stegverse_authority":False,"simulation_means_native_execution":False,"source_release_means_runtime_endpoint":False,"compatibility_receipt_grants_execution_authority":False},
      "manual_tasks_required":[],
      "user_action_required":False
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    if receipt["matching_cases"] != receipt["total_cases"]:
        raise SystemExit("ELYRIA ADMISSION RUNTIME COMPATIBILITY CONTRACT: FAIL")
    print("ELYRIA ADMISSION RUNTIME COMPATIBILITY CONTRACT: PASS")

if __name__=="__main__":
    main()
