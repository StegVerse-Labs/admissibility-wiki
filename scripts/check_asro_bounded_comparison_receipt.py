#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts" / "asro-bounded-comparison-run-001.json"
RUN = ROOT / "static" / "data" / "framework-evaluations" / "runs" / "asro-declared-reference-membership-v1-stegverse-run-001.jsonl"


def main() -> int:
    failures: list[str] = []
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    events = [json.loads(line) for line in RUN.read_text(encoding="utf-8").splitlines() if line.strip()]
    final = events[-1] if events else {}

    if receipt.get("schema") != "bounded_non_authoritative_comparison_receipt.v1":
        failures.append("unexpected receipt schema")
    if receipt.get("run_id") != final.get("run_id"):
        failures.append("receipt run_id does not match final historical event")
    if receipt.get("test_case_id") != final.get("test_case_id"):
        failures.append("receipt test_case_id does not match final historical event")

    status = receipt.get("status")
    if status != "PROVISIONAL_SUPERSEDED_PENDING_CORRECTED_RUN":
        failures.append("historical receipt must remain provisional and superseded pending corrected run")

    historical_result = receipt.get("historical_result", {})
    expected_historical = {
        "correspondence": "ESTABLISHED_FOR_THEN-DECLARED_PUBLIC_ARTIFACT",
        "replay": final.get("replay_status"),
        "reconstruction": final.get("reconstruction_status"),
        "admissibility": final.get("admissibility"),
        "authority": final.get("authority"),
        "execution": final.get("execution"),
        "custody": "NONE",
    }
    for key, value in expected_historical.items():
        if historical_result.get(key) != value:
            failures.append(f"historical receipt result mismatch for {key}")

    current_effect = receipt.get("current_effect", {})
    if current_effect.get("correspondence") != "UNRESOLVED_PENDING_CORRECTED_RUN_AND_RECOMPUTED_INTEGRITY":
        failures.append("current correspondence effect must remain unresolved pending corrected run")
    if current_effect.get("external_asro_native_execution") != "NOT_TESTED":
        failures.append("external ASRO-native execution must remain NOT_TESTED")
    if current_effect.get("reviewer_issuer") != "unresolved":
        failures.append("current reviewer issuer must remain unresolved")

    correction = receipt.get("provenance_correction", {})
    if correction.get("required") is not True:
        failures.append("receipt must preserve required provenance correction")
    if correction.get("historical_run_preserved") is not True:
        failures.append("receipt must preserve historical run")
    if correction.get("corrected_run_required") is not True:
        failures.append("receipt must require corrected run")

    if receipt.get("current_test_package_sha256") is not None:
        failures.append("current package hash must remain unset before corrected package finalization")
    if receipt.get("receipt_hash") is not None:
        failures.append("receipt hash must remain unset before corrected receipt finalization")
    if receipt.get("finalization_status") != "UNFINALIZED_PENDING_CORRECTED_PACKAGE_HASH_AND_RUN":
        failures.append("receipt finalization state must remain pending corrected package hash and run")

    non_claims = receipt.get("bounded_non_claims", {})
    for key in (
        "external_asro_execution_observed",
        "canonical_asro_schema_established",
        "original_source_json_hashed",
        "original_source_correspondence_established",
        "truth_established",
        "sufficiency_established",
        "validity_established",
        "admissibility_established",
        "authority_inherited",
        "execution_authority_granted",
        "custody_transferred",
        "certification_issued",
        "joint_issuance_claimed",
    ):
        if non_claims.get(key) is not False:
            failures.append(f"receipt must deny {key}")

    if receipt.get("reviewer_issuer") != "unresolved":
        failures.append("reviewer issuer must remain unresolved")
    if receipt.get("projection_authority") != "NONE":
        failures.append("projection authority must remain NONE")

    if failures:
        print("ASRO BOUNDED COMPARISON RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON RECEIPT: PASS")
    print("Historical result is preserved while current correspondence, integrity, and execution claims remain fail-closed pending the corrected run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
