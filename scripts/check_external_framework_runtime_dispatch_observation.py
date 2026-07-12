#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "external-framework-runtime-dispatch-observation.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation.not-dispatched.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
STATES = {"NOT_DISPATCHED", "DISPATCH_ATTEMPTED", "DISPATCHED", "EXECUTION_OBSERVED"}
REQUIRED_NON_CLAIMS = {
    "observation receipt does not initiate dispatch",
    "runtime authorization does not prove dispatch",
    "dispatch state does not prove framework compatibility",
    "execution observation does not create execution authority",
    "fixture validation does not cause external consequence",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK RUNTIME DISPATCH OBSERVATION: FAIL")
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
    if receipt.get("receipt_type") != "external_framework_runtime_dispatch_observation":
        failures.append("receipt_type mismatch")

    source = receipt.get("source_runtime_authorization", {})
    if not isinstance(source, dict) or not source.get("path"):
        failures.append("source_runtime_authorization.path required")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append("source_runtime_authorization.sha256 must be lowercase sha256")
    if not receipt.get("authorized_transition_id"):
        failures.append("authorized_transition_id required")

    state = receipt.get("dispatch_state")
    if state not in STATES:
        failures.append("unsupported dispatch_state")

    observation = receipt.get("observation", {})
    result = receipt.get("execution_result", {})
    if not observation.get("observed_at"):
        failures.append("observation.observed_at required")
    if not isinstance(observation.get("evidence_refs"), list) or not observation.get("evidence_refs"):
        failures.append("observation.evidence_refs must contain observed evidence")

    started = result.get("execution_started")
    completed = result.get("execution_completed")
    consequence = result.get("external_consequence_observed")

    if state == "NOT_DISPATCHED":
        for field in ("dispatch_attempt_id", "dispatcher_ref", "transport_ref"):
            if observation.get(field) is not None:
                failures.append(f"NOT_DISPATCHED requires observation.{field} null")
        if started is not False or completed is not False:
            failures.append("NOT_DISPATCHED requires execution_started and execution_completed false")
        if result.get("exit_status") is not None or result.get("output_ref") is not None:
            failures.append("NOT_DISPATCHED requires no exit status or output")
        if consequence is not False:
            failures.append("NOT_DISPATCHED requires external_consequence_observed false")
    elif state == "DISPATCH_ATTEMPTED":
        if not observation.get("dispatch_attempt_id"):
            failures.append("DISPATCH_ATTEMPTED requires dispatch_attempt_id")
        if started is True or completed is True:
            failures.append("DISPATCH_ATTEMPTED cannot claim execution")
    elif state == "DISPATCHED":
        for field in ("dispatch_attempt_id", "dispatcher_ref", "transport_ref"):
            if not observation.get(field):
                failures.append(f"DISPATCHED requires observation.{field}")
        if completed is True:
            failures.append("DISPATCHED alone cannot claim completed execution")
    elif state == "EXECUTION_OBSERVED":
        for field in ("dispatch_attempt_id", "dispatcher_ref", "transport_ref"):
            if not observation.get(field):
                failures.append(f"EXECUTION_OBSERVED requires observation.{field}")
        if started is not True:
            failures.append("EXECUTION_OBSERVED requires execution_started true")
        if not result.get("output_ref"):
            failures.append("EXECUTION_OBSERVED requires output_ref")

    if receipt.get("receipt_id") != "ef-runtime-dispatch-cedar-not-dispatched-001":
        failures.append("unsupported fixture receipt_id")
    if state != "NOT_DISPATCHED":
        failures.append("fixture must remain NOT_DISPATCHED")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in ("NOT_DISPATCHED", "DISPATCH_ATTEMPTED", "DISPATCHED", "EXECUTION_OBSERVED"):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL FRAMEWORK RUNTIME DISPATCH OBSERVATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
