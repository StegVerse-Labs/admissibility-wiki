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
        failures.append("receipt run_id does not match final event")
    if receipt.get("test_case_id") != final.get("test_case_id"):
        failures.append("receipt test_case_id does not match final event")
    if receipt.get("status") != "PROVISIONAL_SUPERSEDED_PENDING_CORRECTED_RUN":
        failures.append("receipt must preserve superseded provisional status")

    historical = receipt.get("historical_result", {})
    expected_historical = {
        "replay": final.get("replay_status"),
        "reconstruction": final.get("reconstruction_status"),
        "admissibility": final.get("admissibility"),
        "authority": final.get("authority"),
        "execution": final.get("execution"),
        "custody": "NONE",
    }
    for key, value in expected_historical.items():
        if historical.get(key) != value:
            failures.append(f"historical receipt result mismatch for {key}")
    if historical.get("correspondence") != "ESTABLISHED_FOR_THEN-DECLARED_PUBLIC_ARTIFACT":
        failures.append("historical correspondence must remain scoped to the then-declared public artifact")

    current = receipt.get("current_effect", {})
    if current.get("correspondence") != "UNRESOLVED_PENDING_CORRECTED_RUN_AND_RECOMPUTED_INTEGRITY":
        failures.append("current correspondence must remain unresolved pending corrected run")
    if current.get("external_asro_native_execution") != "NOT_TESTED":
        failures.append("external ASRO-native execution must remain NOT_TESTED")
    if current.get("reviewer_issuer") != "unresolved":
        failures.append("current reviewer issuer must remain unresolved")

    correction = receipt.get("provenance_correction", {})
    if correction.get("required") is not True:
        failures.append("provenance correction must remain required")
    if correction.get("historical_run_preserved") is not True:
        failures.append("historical run must remain preserved")
    if correction.get("corrected_run_required") is not True:
        failures.append("corrected run must remain required")
    if receipt.get("current_test_package_sha256") is not None:
        failures.append("current corrected package hash must remain unset before corrected run")

    non_claims = receipt.get("bounded_non_claims", {})
    for key in (
        "external_asro_execution_observed",
        "canonical_asro_schema_established",
        "truth_established",
        "sufficiency_established",
        "validity_established",
        "admissibility_established",
        "authority_inherited",
        "execution_authority_granted",
        "custody_transferred",
    ):
        if non_claims.get(key) is not False:
            failures.append(f"receipt must deny {key}")

    if receipt.get("reviewer_issuer") != "unresolved":
        failures.append("reviewer issuer must remain unresolved")
    if receipt.get("projection_authority") != "NONE":
        failures.append("projection authority must remain NONE")
    if receipt.get("finalization_status") != "UNFINALIZED_PENDING_CORRECTED_PACKAGE_HASH_AND_RUN":
        failures.append("receipt must remain unfinalized pending corrected evidence")

    if failures:
        print("ASRO BOUNDED COMPARISON RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON RECEIPT: PASS")
    print("Historical results remain preserved while current correspondence, corrected integrity, and external execution remain unresolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
