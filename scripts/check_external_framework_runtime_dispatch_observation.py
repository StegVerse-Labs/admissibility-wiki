#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "external-framework-runtime-dispatch-observation.schema.json"
FIXTURES = (
    ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation.not-dispatched.json",
    ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation.dispatch-attempted.json",
    ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation.dispatched.json",
    ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation.execution-observed.json",
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
STATES = {"NOT_DISPATCHED", "DISPATCH_ATTEMPTED", "DISPATCHED", "EXECUTION_OBSERVED"}
EXPECTED_RECEIPTS = {
    "ef-runtime-dispatch-cedar-not-dispatched-001": "NOT_DISPATCHED",
    "ef-runtime-dispatch-cedar-attempted-001": "DISPATCH_ATTEMPTED",
    "ef-runtime-dispatch-cedar-dispatched-001": "DISPATCHED",
    "ef-runtime-dispatch-cedar-execution-observed-001": "EXECUTION_OBSERVED",
}
REQUIRED_NON_CLAIMS = {
    "observation receipt does not initiate dispatch",
    "runtime authorization does not prove dispatch",
    "dispatch state does not prove framework compatibility",
    "execution observation does not create execution authority",
    "fixture validation does not cause external consequence",
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
    if receipt.get("receipt_type") != "external_framework_runtime_dispatch_observation":
        failures.append(f"{label}: receipt_type mismatch")

    source = receipt.get("source_runtime_authorization", {})
    if not isinstance(source, dict) or not source.get("path"):
        failures.append(f"{label}: source_runtime_authorization.path required")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append(f"{label}: source_runtime_authorization.sha256 must be lowercase sha256")
    if not receipt.get("authorized_transition_id"):
        failures.append(f"{label}: authorized_transition_id required")

    receipt_id = receipt.get("receipt_id")
    state = receipt.get("dispatch_state")
    expected_state = EXPECTED_RECEIPTS.get(str(receipt_id))
    if expected_state is None:
        failures.append(f"{label}: unsupported fixture receipt_id")
    elif state != expected_state:
        failures.append(f"{label}: receipt_id requires state {expected_state}")
    if state not in STATES:
        failures.append(f"{label}: unsupported dispatch_state")

    observation = receipt.get("observation", {})
    result = receipt.get("execution_result", {})
    observer = receipt.get("observer", {})
    if not observation.get("observed_at"):
        failures.append(f"{label}: observation.observed_at required")
    if not isinstance(observation.get("evidence_refs"), list) or not observation.get("evidence_refs"):
        failures.append(f"{label}: observation.evidence_refs must contain observed evidence")
    if not observer.get("observer_ref"):
        failures.append(f"{label}: observer.observer_ref required")

    started = result.get("execution_started")
    completed = result.get("execution_completed")
    consequence = result.get("external_consequence_observed")
    attempt_id = observation.get("dispatch_attempt_id")
    dispatcher_ref = observation.get("dispatcher_ref")
    transport_ref = observation.get("transport_ref")
    exit_status = result.get("exit_status")
    output_ref = result.get("output_ref")

    if state == "NOT_DISPATCHED":
        for field in ("dispatch_attempt_id", "dispatcher_ref", "transport_ref"):
            if observation.get(field) is not None:
                failures.append(f"{label}: NOT_DISPATCHED requires observation.{field} null")
        if started is not False or completed is not False:
            failures.append(f"{label}: NOT_DISPATCHED requires execution_started and execution_completed false")
        if exit_status is not None or output_ref is not None:
            failures.append(f"{label}: NOT_DISPATCHED requires no exit status or output")
        if consequence is not False:
            failures.append(f"{label}: NOT_DISPATCHED requires external_consequence_observed false")

    elif state == "DISPATCH_ATTEMPTED":
        if not attempt_id or not dispatcher_ref:
            failures.append(f"{label}: DISPATCH_ATTEMPTED requires attempt and dispatcher references")
        if started is not False or completed is not False:
            failures.append(f"{label}: DISPATCH_ATTEMPTED cannot claim execution")
        if exit_status is not None or output_ref is not None:
            failures.append(f"{label}: DISPATCH_ATTEMPTED cannot claim exit status or output")
        if consequence is not False:
            failures.append(f"{label}: DISPATCH_ATTEMPTED cannot claim external consequence")

    elif state == "DISPATCHED":
        if not attempt_id or not dispatcher_ref or not transport_ref:
            failures.append(f"{label}: DISPATCHED requires attempt, dispatcher, and transport references")
        if started is not False or completed is not False:
            failures.append(f"{label}: DISPATCHED alone cannot claim execution")
        if exit_status is not None or output_ref is not None:
            failures.append(f"{label}: DISPATCHED alone cannot claim exit status or output")
        if consequence is not False:
            failures.append(f"{label}: DISPATCHED fixture cannot claim external consequence")

    elif state == "EXECUTION_OBSERVED":
        if not attempt_id or not dispatcher_ref or not transport_ref:
            failures.append(f"{label}: EXECUTION_OBSERVED requires attempt, dispatcher, and transport references")
        if started is not True:
            failures.append(f"{label}: EXECUTION_OBSERVED requires execution_started true")
        if not output_ref:
            failures.append(f"{label}: EXECUTION_OBSERVED requires output_ref")
        if completed is True and exit_status is None:
            failures.append(f"{label}: completed execution requires exit_status")
        if consequence is not False:
            failures.append(f"{label}: fixture must not claim external consequence")

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
        print("EXTERNAL FRAMEWORK RUNTIME DISPATCH OBSERVATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    observed_states: set[str] = set()
    for fixture in FIXTURES:
        receipt = load(fixture)
        observed_states.add(str(receipt.get("dispatch_state")))
        failures.extend(validate_receipt(receipt, schema, fixture.name))

    if observed_states != STATES:
        failures.append(f"fixture state coverage mismatch: {sorted(observed_states)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in STATES:
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL FRAMEWORK RUNTIME DISPATCH OBSERVATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
