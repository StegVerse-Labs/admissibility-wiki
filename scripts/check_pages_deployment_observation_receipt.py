#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "pages-deployment-observation-receipt.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "pages-deployment-observation-receipt.fail-closed.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED_NON_CLAIMS = {
    "artifact preservation is not deployment observation",
    "deployment job existence is not deployment success",
    "deployment observation is not public endpoint verification",
    "deployment observation is not release authority",
    "deployment observation is not downstream propagation authority",
    "fixture validation does not establish a production deployment",
}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("PAGES DEPLOYMENT OBSERVATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    receipt = load(FIXTURE)
    missing = sorted(set(schema.get("required", [])) - set(receipt))
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")

    if receipt.get("schema_version") != "0.1":
        failures.append("schema_version must be 0.1")
    if receipt.get("receipt_type") != "pages_deployment_observation_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if not HEX40.fullmatch(str(receipt.get("target_commit", ""))):
        failures.append("target_commit must be lowercase 40-character SHA")

    status = receipt.get("source_status", {})
    binding = receipt.get("source_artifact_binding", {})
    deployment = receipt.get("deployment", {})

    if status.get("path") != "static/status/pages-build-verification.json":
        failures.append("source status path mismatch")
    if status.get("verification_state") != "PAGES_ARTIFACT_PRESERVED":
        failures.append("source status must be PAGES_ARTIFACT_PRESERVED")
    if not HEX64.fullmatch(str(status.get("sha256", ""))):
        failures.append("source status sha256 malformed")

    if not binding.get("path"):
        failures.append("artifact binding path required")
    if not HEX64.fullmatch(str(binding.get("sha256", ""))):
        failures.append("artifact binding sha256 malformed")
    if not isinstance(binding.get("artifact_id"), int) or binding.get("artifact_id", 0) < 1:
        failures.append("artifact binding artifact_id invalid")
    if not DIGEST.fullmatch(str(binding.get("artifact_digest", ""))):
        failures.append("artifact digest malformed")

    for field in ("run_id", "job_id"):
        if not isinstance(deployment.get(field), int) or deployment.get(field, 0) < 1:
            failures.append(f"deployment.{field} invalid")
    if deployment.get("environment") != "github-pages":
        failures.append("deployment environment must be github-pages")
    if not str(deployment.get("page_url", "")).startswith("https://"):
        failures.append("deployment page_url must use https")
    if deployment.get("deployment_status") not in {"SUCCESS", "FAILURE", "UNRESOLVED"}:
        failures.append("deployment status invalid")

    observed = receipt.get("observation_state") == "DEPLOYMENT_OBSERVED"
    success = deployment.get("deployment_status") == "SUCCESS"
    evidence = bool(deployment.get("evidence_ref"))
    if observed:
        if not (success and evidence):
            failures.append("DEPLOYMENT_OBSERVED requires SUCCESS and evidence_ref")
        if receipt.get("required_next_transition") != "separate_public_endpoint_verification":
            failures.append("observed deployment must require separate public endpoint verification")
    else:
        if receipt.get("observation_state") != "FAIL_CLOSED":
            failures.append("unsupported observation_state")
        if success or evidence:
            failures.append("fail-closed state must not contain successful deployment evidence")
        if receipt.get("required_next_transition") != "repair_or_obtain_deployment_evidence":
            failures.append("fail-closed state must require deployment evidence repair")

    if receipt.get("public_verification_complete") is not False:
        failures.append("public verification must remain false")
    if receipt.get("release_authorized") is not False:
        failures.append("release authorization must remain false")
    if receipt.get("downstream_propagation_authorized") is not False:
        failures.append("downstream propagation must remain false")

    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - set(receipt.get("non_claims", [])))
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    if receipt.get("observation_state") != "FAIL_CLOSED":
        failures.append("fixture must remain FAIL_CLOSED")
    if deployment.get("deployment_status") != "UNRESOLVED":
        failures.append("fixture must remain UNRESOLVED")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "PAGES_ARTIFACT_PRESERVED",
        "DEPLOYMENT_OBSERVED",
        "FAIL_CLOSED",
        "separate_public_endpoint_verification",
        "repair_or_obtain_deployment_evidence",
        "public_verification_complete",
        "release_authorized",
        "downstream_propagation_authorized",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("PAGES DEPLOYMENT OBSERVATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
