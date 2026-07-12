#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "external-framework-runtime-authorization-receipt.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "external-framework-runtime-authorization-receipt.blocked.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PREDICATES = ("authority", "delegation", "policy", "freshness", "scope", "consequence_boundary")
REQUIRED_NON_CLAIMS = {
    "materialization approval does not create runtime authority",
    "runtime authorization does not prove framework compatibility",
    "missing commit-time evidence must fail closed",
    "receipt validation does not cause external consequence",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK RUNTIME AUTHORIZATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    receipt = load(FIXTURE)

    required = set(schema.get("required", []))
    missing = sorted(required - set(receipt))
    if missing:
        failures.append(f"fixture missing fields: {', '.join(missing)}")

    if receipt.get("schema_version") != "0.1":
        failures.append("schema_version must be 0.1")
    if receipt.get("receipt_type") != "external_framework_runtime_authorization_receipt":
        failures.append("receipt_type mismatch")

    source = receipt.get("source_materialization_receipt", {})
    if not isinstance(source, dict) or not source.get("path"):
        failures.append("source_materialization_receipt.path required")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append("source_materialization_receipt.sha256 must be lowercase sha256")
    if not HEX64.fullmatch(str(receipt.get("materialized_descriptor_hash", ""))):
        failures.append("materialized_descriptor_hash must be lowercase sha256")

    evidence = receipt.get("commit_time_evidence", {})
    pass_count = 0
    for name in PREDICATES:
        predicate = evidence.get(name, {})
        status = predicate.get("status")
        if status not in {"PASS", "FAIL", "MISSING", "STALE", "UNRESOLVED"}:
            failures.append(f"invalid {name} status")
        if status == "PASS":
            pass_count += 1
            if not predicate.get("reference") or not predicate.get("checked_at"):
                failures.append(f"PASS {name} requires reference and checked_at")

    decision = receipt.get("decision")
    authorized = receipt.get("runtime_execution_authorized")
    transition = receipt.get("runtime_transition")
    all_pass = pass_count == len(PREDICATES)

    if decision == "ALLOW_RUNTIME_TRANSITION":
        if not all_pass:
            failures.append("ALLOW_RUNTIME_TRANSITION requires every commit-time predicate PASS")
        if authorized is not True:
            failures.append("ALLOW_RUNTIME_TRANSITION requires runtime_execution_authorized true")
        if not isinstance(transition, dict):
            failures.append("ALLOW_RUNTIME_TRANSITION requires runtime_transition object")
    else:
        if authorized is not False:
            failures.append("non-ALLOW decision requires runtime_execution_authorized false")
        if transition is not None:
            failures.append("non-ALLOW decision requires runtime_transition null")

    if receipt.get("receipt_id") == "ef-runtime-auth-cedar-blocked-001":
        if decision != "FAIL_CLOSED":
            failures.append("blocked fixture must remain FAIL_CLOSED")
        if all_pass:
            failures.append("blocked fixture must not satisfy every commit-time predicate")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "source_materialization_receipt",
        "materialized_descriptor_hash",
        "commit_time_evidence",
        "ALLOW_RUNTIME_TRANSITION",
        "runtime_execution_authorized",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL FRAMEWORK RUNTIME AUTHORIZATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
