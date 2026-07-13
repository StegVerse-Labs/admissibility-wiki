#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "pages-build-verification-receipt.schema.json"
STATUS = ROOT / "static" / "status" / "pages-build-verification.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED_NON_CLAIMS = {
    "repair installation is not Pages build success",
    "regression guard installation is not Pages build success",
    "Pages build success is not deployment authority",
    "Pages artifact upload is not public verification",
    "receipt validation does not authorize release or downstream propagation",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, STATUS):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("PAGES BUILD VERIFICATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    receipt = load(STATUS)
    required = set(schema.get("required", []))
    missing = sorted(required - set(receipt))
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")

    if receipt.get("schema_version") != "0.1":
        failures.append("schema_version must be 0.1")
    if receipt.get("receipt_type") != "pages_build_verification_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if not HEX40.fullmatch(str(receipt.get("target_commit", ""))):
        failures.append("target_commit must be a 40-character lowercase commit SHA")

    state = receipt.get("verification_state")
    allowed_states = {
        "PENDING_CANONICAL_RUN",
        "VALIDATOR_PASS_BUILD_PENDING",
        "PAGES_BUILD_PASS_ARTIFACT_PENDING",
        "PAGES_ARTIFACT_PRESERVED",
        "FAIL_CLOSED",
    }
    if state not in allowed_states:
        failures.append("unsupported verification_state")

    checks = receipt.get("required_checks", {})
    check_names = (
        "formalism_publication_validator",
        "docusaurus_production_build",
        "pages_artifact_upload",
    )
    statuses: dict[str, str] = {}
    for name in check_names:
        check = checks.get(name, {})
        status = check.get("status")
        statuses[name] = status
        if status not in {"PENDING", "PASS", "FAIL"}:
            failures.append(f"{name}.status invalid")
        evidence_ref = check.get("evidence_ref")
        if status == "PASS" and not evidence_ref:
            failures.append(f"{name} PASS requires evidence_ref")
        if status != "PASS" and evidence_ref is not None:
            failures.append(f"{name} non-PASS must not claim evidence_ref")

    observed = receipt.get("observed_workflow", {})
    run_id = observed.get("run_id")
    job_id = observed.get("job_id")
    artifact_id = observed.get("artifact_id")
    artifact_digest = observed.get("artifact_digest")

    if state == "PENDING_CANONICAL_RUN":
        if any(value != "PENDING" for value in statuses.values()):
            failures.append("PENDING_CANONICAL_RUN requires every check PENDING")
        if any(value is not None for value in (run_id, job_id, artifact_id, artifact_digest)):
            failures.append("PENDING_CANONICAL_RUN must not claim workflow or artifact evidence")
    elif state == "VALIDATOR_PASS_BUILD_PENDING":
        if statuses["formalism_publication_validator"] != "PASS":
            failures.append("VALIDATOR_PASS_BUILD_PENDING requires validator PASS")
        if statuses["docusaurus_production_build"] != "PENDING" or statuses["pages_artifact_upload"] != "PENDING":
            failures.append("VALIDATOR_PASS_BUILD_PENDING requires build and upload PENDING")
        if not isinstance(run_id, int) or not isinstance(job_id, int):
            failures.append("VALIDATOR_PASS_BUILD_PENDING requires run_id and job_id")
    elif state == "PAGES_BUILD_PASS_ARTIFACT_PENDING":
        if statuses["formalism_publication_validator"] != "PASS" or statuses["docusaurus_production_build"] != "PASS":
            failures.append("PAGES_BUILD_PASS_ARTIFACT_PENDING requires validator and build PASS")
        if statuses["pages_artifact_upload"] != "PENDING":
            failures.append("PAGES_BUILD_PASS_ARTIFACT_PENDING requires artifact upload PENDING")
        if not isinstance(run_id, int) or not isinstance(job_id, int):
            failures.append("PAGES_BUILD_PASS_ARTIFACT_PENDING requires run_id and job_id")
    elif state == "PAGES_ARTIFACT_PRESERVED":
        if any(value != "PASS" for value in statuses.values()):
            failures.append("PAGES_ARTIFACT_PRESERVED requires every check PASS")
        if not all(isinstance(value, int) for value in (run_id, job_id, artifact_id)):
            failures.append("PAGES_ARTIFACT_PRESERVED requires run_id, job_id, and artifact_id")
        if not DIGEST.fullmatch(str(artifact_digest or "")):
            failures.append("PAGES_ARTIFACT_PRESERVED requires sha256 artifact_digest")

    if receipt.get("deployment_authorized") is not False:
        failures.append("deployment_authorized must remain false")
    if receipt.get("public_verification_complete") is not False:
        failures.append("public_verification_complete must remain false")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "PENDING_CANONICAL_RUN",
        "PAGES_ARTIFACT_PRESERVED",
        "formalism_publication_validator",
        "docusaurus_production_build",
        "pages_artifact_upload",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("PAGES BUILD VERIFICATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
