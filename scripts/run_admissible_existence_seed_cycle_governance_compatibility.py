#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/admissible-existence-seed-cycle-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/admissible-existence-seed-cycle/admissible-existence-seed-cycle-stegverse-governance-compatibility-receipt.json"

def evaluate(case: dict) -> str:
    if case.get("malformed"):
        return "FAIL_CLOSED"
    if case.get("external_certification_claim"):
        return "FAIL_CLOSED"
    if case.get("seed_cycle_status") == "INCOMPLETE":
        return "DENY"
    if case.get("evidence_current") is False:
        return "FAIL_CLOSED"
    if case.get("authority_current") is False:
        return "DENY"
    if case.get("seed_cycle_status") == "SEED-CYCLE-COMPLETE" and case.get("evidence_current") is True and case.get("authority_current") is True:
        return "ALLOW"
    return "FAIL_CLOSED"

def main() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in data["cases"]:
        actual = evaluate(case)
        results.append({"case_id":case["case_id"],"family":case["family"],"expected":case["expected_stegverse_result"],"actual":actual,"matched":actual == case["expected_stegverse_result"]})
    receipt = {"schema":"internal_ecosystem_governance_compatibility_receipt.v1","framework_id":"admissible-existence-seed-cycle","record_type":"internal_ecosystem_record","simulation_only":True,"total_cases":len(results),"matching_cases":sum(1 for r in results if r["matched"]),"results":results,"native_execution_observed":False,"independent_reproduction_observed":False,"compatibility_observed":False,"seed_cycle_complete_means_execution_authority":False,"internal_artifact_presence_means_public_validation":False,"manual_tasks_required":[],"user_action_required":False}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if receipt["matching_cases"] != receipt["total_cases"]:
        raise SystemExit("AE SEED CYCLE GOVERNANCE COMPATIBILITY: FAIL")
    print("AE SEED CYCLE GOVERNANCE COMPATIBILITY: PASS")

if __name__ == "__main__":
    main()
