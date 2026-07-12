#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "external-framework-runtime-authorization-receipt.schema.json"
FIXTURES = (
    ROOT / "tests" / "fixtures" / "external-framework-runtime-authorization-receipt.blocked.json",
    ROOT / "tests" / "fixtures" / "external-framework-runtime-authorization-receipt.allowed-non-dispatched.json",
)
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


def validate_receipt(receipt: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    failures: list[str] = []
    required = set(schema.get("required", []))
    missing = sorted(required - set(receipt))
    if missing:
        failures.append(f"{label}: missing fields: {', '.join(missing)}")

    if receipt.get("schema_version") != "0.1":
        failures.append(f"{label}: schema_version must be 0.1")
    if receipt.get("receipt_type") != "external_framework_runtime_authorization_receipt":
        failures.append(f"{label}: receipt_type mismatch")

    source = receipt.get("source_materialization_receipt", {})
    if not isinstance(source, dict) or not source.get("path"):
        failures.append(f"{label}: source_materialization_receipt.path required")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append(f"{label}: source_materialization_receipt.sha256 must be lowercase sha256")
    if not HEX64.fullmatch(str(receipt.get("materialized_descriptor_hash", ""))):
        failures.append(f"{label}: materialized_descriptor_hash must be lowercase sha256")

    evidence = receipt.get("commit_time_evidence", {})
    pass_count = 0
    for name in PREDICATES:
        predicate = evidence.get(name, {})
        status = predicate.get("status")
        if status not in {"PASS", "FAIL", "MISSING", "STALE", "UNRESOLVED"}:
            failures.append(f"{label}: invalid {name} status")
        if status == "PASS":
            pass_count += 1
            if not predicate.get("reference") or not predicate.get("checked_at"):
                failures.append(f"{label}: PASS {name} requires reference and checked_at")

    decision = receipt.get("decision")
    authorized = receipt.get("runtime_execution_authorized")
    transition = receipt.get("runtime_transition")
    all_pass = pass_count == len(PREDICATES)

    if decision == "ALLOW_RUNTIME_TRANSITION":
        if not all_pass:
            failures.append(f"{label}: ALLOW_RUNTIME_TRANSITION requires every commit-time predicate PASS")
        if authorized is not True:
            failures.append(f"{label}: ALLOW_RUNTIME_TRANSITION requires runtime_execution_authorized true")
        if not isinstance(transition, dict):
            failures.append(f"{label}: ALLOW_RUNTIME_TRANSITION requires runtime_transition object")
        else:
            expected = {
                "transition_state": "AUTHORIZED_NOT_DISPATCHED",
                "scheduled": False,
                "dispatched": False,
                "execution_started": False,
                "execution_endpoint": None,
                "command": None,
                "credentials_attached": False,
                "external_consequence_allowed": False,
                "required_next_transition": "separate_observed_runtime_dispatch_transition",
            }
            if not transition.get("transition_id"):
                failures.append(f"{label}: authorized transition requires transition_id")
            for field, expected_value in expected.items():
                if transition.get(field) != expected_value:
                    failures.append(f"{label}: runtime_transition.{field} must be {expected_value!r}")
    else:
        if authorized is not False:
            failures.append(f"{label}: non-ALLOW decision requires runtime_execution_authorized false")
        if transition is not None:
            failures.append(f"{label}: non-ALLOW decision requires runtime_transition null")

    receipt_id = receipt.get("receipt_id")
    if receipt_id == "ef-runtime-auth-cedar-blocked-001":
        if decision != "FAIL_CLOSED":
            failures.append(f"{label}: blocked fixture must remain FAIL_CLOSED")
        if all_pass:
            failures.append(f"{label}: blocked fixture must not satisfy every commit-time predicate")
    elif receipt_id == "ef-runtime-auth-cedar-allowed-non-dispatched-001":
        if decision != "ALLOW_RUNTIME_TRANSITION":
            failures.append(f"{label}: positive fixture must remain ALLOW_RUNTIME_TRANSITION")
        if not all_pass:
            failures.append(f"{label}: positive fixture must preserve six PASS predicates")
        if not isinstance(transition, dict) or transition.get("dispatched") is not False:
            failures.append(f"{label}: positive fixture must remain non-dispatched")
        if "runtime authorization receipt does not schedule dispatch or execute a transition" not in receipt.get("non_claims", []):
            failures.append(f"{label}: positive fixture missing non-dispatch non-claim")
    else:
        failures.append(f"{label}: unsupported fixture receipt_id")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        failures.append(f"{label}: missing non-claims: {', '.join(missing_non_claims)}")
    return failures


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, *FIXTURES):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK RUNTIME AUTHORIZATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    for fixture in FIXTURES:
        failures.extend(validate_receipt(load(fixture), schema, fixture.name))

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "source_materialization_receipt",
        "materialized_descriptor_hash",
        "commit_time_evidence",
        "ALLOW_RUNTIME_TRANSITION",
        "runtime_execution_authorized",
        "AUTHORIZED_NOT_DISPATCHED",
        "separate_observed_runtime_dispatch_transition",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL FRAMEWORK RUNTIME AUTHORIZATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
