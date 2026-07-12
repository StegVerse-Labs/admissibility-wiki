#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "external-framework-job-materialization-receipt.schema.json"
FIXTURES = (
    ROOT / "tests" / "fixtures" / "external-framework-job-materialization-receipt.blocked.json",
    ROOT / "tests" / "fixtures" / "external-framework-job-materialization-receipt.approved-non-executable.json",
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_STATES = {
    "BLOCKED_NOT_ELIGIBLE",
    "ELIGIBLE_REVIEW_REQUIRED",
    "DENIED",
    "MATERIALIZED_NOT_EXECUTABLE",
    "AUTHORIZED_FOR_SEPARATE_RUNTIME_TRANSITION",
}
ALLOWED_DECISIONS = {"FAIL_CLOSED", "REVIEW_REQUIRED", "DENY", "ALLOW_MATERIALIZATION_ONLY"}
REQUIRED_NON_CLAIMS = {
    "receipt existence does not create execution authority",
    "plan eligibility does not materialize a runtime job",
    "job materialization does not authorize runtime execution",
    "validation does not establish framework compatibility",
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
    if receipt.get("receipt_type") != "external_framework_job_materialization_receipt":
        failures.append(f"{label}: receipt_type mismatch")
    if receipt.get("materialization_state") not in ALLOWED_STATES:
        failures.append(f"{label}: unsupported materialization_state")
    if receipt.get("decision") not in ALLOWED_DECISIONS:
        failures.append(f"{label}: unsupported decision")

    for field in ("source_readiness", "source_execution_plan"):
        bound = receipt.get(field, {})
        if not isinstance(bound, dict):
            failures.append(f"{label}: {field} must be an object")
            continue
        if not bound.get("path"):
            failures.append(f"{label}: {field}.path is required")
        if not HEX64.fullmatch(str(bound.get("sha256", ""))):
            failures.append(f"{label}: {field}.sha256 must be a lowercase sha256")

    for field in ("authority_review", "consequence_boundary_review"):
        review = receipt.get(field, {})
        if review.get("status") not in {"NOT_STARTED", "PENDING", "PASS", "DENY"}:
            failures.append(f"{label}: {field}.status invalid")
        if not isinstance(review.get("evidence_refs"), list):
            failures.append(f"{label}: {field}.evidence_refs must be a list")

    if receipt.get("runtime_execution_authorized") is not False:
        failures.append(f"{label}: runtime_execution_authorized must remain false")

    decision = receipt.get("decision")
    state = receipt.get("materialization_state")
    runtime_job = receipt.get("runtime_job")
    authority_review = receipt.get("authority_review", {})
    consequence_review = receipt.get("consequence_boundary_review", {})

    if decision == "ALLOW_MATERIALIZATION_ONLY":
        if state != "MATERIALIZED_NOT_EXECUTABLE":
            failures.append(f"{label}: ALLOW_MATERIALIZATION_ONLY requires MATERIALIZED_NOT_EXECUTABLE")
        if not isinstance(runtime_job, dict):
            failures.append(f"{label}: ALLOW_MATERIALIZATION_ONLY requires a non-executable runtime_job object")
        else:
            if runtime_job.get("job_state") != "NON_EXECUTABLE_MATERIALIZED_DESCRIPTOR":
                failures.append(f"{label}: materialized job must remain a non-executable descriptor")
            if runtime_job.get("execution_endpoint") is not None:
                failures.append(f"{label}: materialized descriptor must not expose an execution endpoint")
            if runtime_job.get("command") is not None:
                failures.append(f"{label}: materialized descriptor must not contain a runtime command")
            if runtime_job.get("credentials_attached") is not False:
                failures.append(f"{label}: materialized descriptor must not attach credentials")
            if runtime_job.get("external_consequence_allowed") is not False:
                failures.append(f"{label}: materialized descriptor must forbid external consequence")
            if runtime_job.get("required_next_transition") != "separate_runtime_authorization_review":
                failures.append(f"{label}: materialized descriptor must require separate runtime authorization")
        if authority_review.get("status") != "PASS":
            failures.append(f"{label}: materialization-only approval requires authority review PASS")
        if consequence_review.get("status") != "PASS":
            failures.append(f"{label}: materialization-only approval requires consequence review PASS")
    elif runtime_job is not None:
        failures.append(f"{label}: non-materialization decisions must keep runtime_job null")

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
        print("EXTERNAL FRAMEWORK JOB MATERIALIZATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    for fixture in FIXTURES:
        failures.extend(validate_receipt(load(fixture), schema, fixture.name))

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "ALLOW_MATERIALIZATION_ONLY",
        "MATERIALIZED_NOT_EXECUTABLE",
        "runtime_execution_authorized",
        "source_execution_plan",
        "source_readiness",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL FRAMEWORK JOB MATERIALIZATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
