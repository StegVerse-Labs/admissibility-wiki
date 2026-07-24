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

    result = receipt.get("result", {})
    expected = {
        "correspondence": final.get("correspondence"),
        "replay": final.get("replay_status"),
        "reconstruction": final.get("reconstruction_status"),
        "admissibility": final.get("admissibility"),
        "authority": final.get("authority"),
        "execution": final.get("execution"),
        "custody": "NONE",
    }
    for key, value in expected.items():
        if result.get(key) != value:
            failures.append(f"receipt result mismatch for {key}")

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

    if failures:
        print("ASRO BOUNDED COMPARISON RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON RECEIPT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
