#!/usr/bin/env python3
"""Validate the Conectrr synthetic capability canonical-workflow observation receipt."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static/status/conectrr-itc-canonical-workflow-observation.pending.v1.json"
LOCAL_RECEIPT = ROOT / "static/status/conectrr-itc-synthetic-local-execution-receipt.v1.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_false_authority(value: Any) -> None:
    if not isinstance(value, dict):
        fail("authority object required")
    for field in ("certification", "execution", "custody", "endorsement"):
        if value.get(field) is not False:
            fail(f"authority.{field} must remain false")


def main() -> int:
    for path in (RECEIPT, LOCAL_RECEIPT):
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    local = json.loads(LOCAL_RECEIPT.read_text(encoding="utf-8"))

    if receipt.get("schema") != "conectrr_itc_canonical_workflow_observation.v1":
        fail("unexpected workflow observation schema")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if receipt.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        fail("canonical workflow mismatch")
    if receipt.get("canonical_validation") != "npm run validate":
        fail("canonical validation mismatch")
    if not SHA_RE.fullmatch(str(receipt.get("observed_commit", ""))):
        fail("observed_commit must be a lowercase 40-character Git SHA")
    if receipt.get("local_execution_receipt") != "static/status/conectrr-itc-synthetic-local-execution-receipt.v1.json":
        fail("local execution receipt path mismatch")
    if receipt.get("local_execution_result") != local.get("result") or local.get("result") != "PASS":
        fail("local execution result correlation failed")
    if receipt.get("external_validation_claimed") is not False:
        fail("workflow receipt cannot claim external validation")
    require_false_authority(receipt.get("authority"))

    state = receipt.get("state")
    if state == "NOT_OBSERVED":
        for field in (
            "workflow_run_id",
            "workflow_run_url",
            "workflow_conclusion",
            "validation_job_id",
            "validation_job_conclusion",
        ):
            if receipt.get(field) is not None:
                fail(f"unobserved receipt cannot assert {field}")
        if receipt.get("first_observation_preserved") is not False:
            fail("unobserved receipt cannot claim first observation preservation")
        if receipt.get("canonical_result") != "NOT_YET_OBSERVED":
            fail("unobserved receipt must retain NOT_YET_OBSERVED")
    elif state in {"OBSERVED_PASS", "OBSERVED_FAIL"}:
        if not isinstance(receipt.get("workflow_run_id"), int):
            fail("observed receipt requires workflow_run_id")
        if not receipt.get("workflow_run_url"):
            fail("observed receipt requires workflow_run_url")
        expected = "success" if state == "OBSERVED_PASS" else "failure"
        if receipt.get("workflow_conclusion") != expected:
            fail("workflow conclusion/state mismatch")
        if receipt.get("validation_job_conclusion") != expected:
            fail("validation job conclusion/state mismatch")
        if not isinstance(receipt.get("validation_job_id"), int):
            fail("observed receipt requires validation_job_id")
        if receipt.get("first_observation_preserved") is not True:
            fail("observed receipt must preserve first observation")
        if receipt.get("canonical_result") != ("PASS" if state == "OBSERVED_PASS" else "FAIL"):
            fail("canonical result/state mismatch")
    else:
        fail("unsupported workflow observation state")

    non_claims = "\n".join(str(item) for item in receipt.get("non_claims", []))
    for marker in (
        "local PASS is not a canonical workflow PASS",
        "neither PASS nor FAIL",
        "preserve the first observed conclusion",
        "does not establish Conectrr interoperability",
        "does not grant reviewer standing",
    ):
        if marker not in non_claims:
            fail(f"missing workflow observation non-claim: {marker}")

    print(f"OK: {RECEIPT.relative_to(ROOT)}")
    print(f"conectrr_itc_local_execution={local.get('result')}")
    print(f"conectrr_itc_canonical_workflow_observation={state}")
    print("conectrr_itc_external_validation_claimed=false")
    print("conectrr_itc_canonical_workflow_observation_validator=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
