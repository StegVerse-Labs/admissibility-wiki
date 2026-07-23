#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static/status/sv-continuity-109-admissibility-verification.json"
REQUIRED_TRUE = (
    "schemas_and_evaluator_resolve",
    "reconstructability_distinct_from_recreatability",
    "continuity_receipt_is_evidence_not_authority",
    "verification_surplus_not_partial_credit",
    "external_ai_returns_non_authoritative",
    "governance_freshness_current_at_intake",
)


def main() -> int:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = receipt.get("checks", {})
    for key in REQUIRED_TRUE:
        if checks.get(key) is not True:
            failures.append(f"required check failed: {key}")
    for key, value in receipt.get("authority", {}).items():
        if value is not False:
            failures.append(f"authority must remain false: {key}")
    decision = receipt.get("decision")
    if decision == "PASS" and checks.get("site_and_downstream_evidence_complete") is not True:
        failures.append("PASS requires complete Site and downstream evidence")
    if decision not in {"PASS", "BLOCK"}:
        failures.append("decision must be PASS or BLOCK")
    if failures:
        print("SV-CONTINUITY-109 ADMISSIBILITY VERIFICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"SV-CONTINUITY-109 ADMISSIBILITY VERIFICATION: {decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
