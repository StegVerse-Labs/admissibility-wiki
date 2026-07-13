#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "pages-public-endpoint-verification-receipt.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "pages-public-endpoint-verification-receipt.fail-closed.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PATHS = {
    "/admissibility-wiki/",
    "/admissibility-wiki/status/admissibility-wiki-status.json",
    "/admissibility-wiki/status/ios-workflow-mirror-status.json",
    "/admissibility-wiki/formalisms/inference-window-irreversibility-governance",
}
REQUIRED_NON_CLAIMS = {
    "deployment observation is not public endpoint verification",
    "a reachable root page does not verify all required routes",
    "HTTP status without content evidence is incomplete verification",
    "public endpoint verification is not release authority",
    "public endpoint verification is not downstream propagation authority",
    "fixture validation does not establish a live deployment",
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
        print("PAGES PUBLIC ENDPOINT VERIFICATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    receipt = load(FIXTURE)
    missing = sorted(set(schema.get("required", [])) - set(receipt))
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")
    if receipt.get("schema_version") != "0.1":
        failures.append("schema_version mismatch")
    if receipt.get("receipt_type") != "pages_public_endpoint_verification_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")

    source = receipt.get("source_deployment_observation", {})
    if source.get("deployment_state") != "DEPLOYMENT_OBSERVED":
        failures.append("source deployment state mismatch")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append("source deployment receipt hash malformed")
    if not str(receipt.get("deployment_url", "")).startswith("https://"):
        failures.append("deployment_url must use https")

    endpoints = receipt.get("required_endpoints", [])
    paths = {item.get("path") for item in endpoints if isinstance(item, dict)}
    if not REQUIRED_PATHS.issubset(paths):
        failures.append("required endpoint set incomplete")

    complete = True
    for endpoint in endpoints:
        if not isinstance(endpoint, dict):
            complete = False
            failures.append("endpoint entry must be an object")
            continue
        if endpoint.get("expected_status") != 200:
            failures.append(f"endpoint expected_status must be 200: {endpoint.get('path')}")
        if endpoint.get("observed_status") != 200:
            complete = False
        if not HEX64.fullmatch(str(endpoint.get("content_sha256", ""))):
            complete = False
        if not endpoint.get("evidence_ref"):
            complete = False

    run = receipt.get("verification_run", {})
    run_complete = all(isinstance(run.get(key), int) and run.get(key) > 0 for key in ("run_id", "job_id", "run_attempt")) and bool(run.get("evidence_ref"))
    verified = complete and run_complete

    if receipt.get("verification_state") == "PUBLIC_ENDPOINTS_VERIFIED":
        if not verified:
            failures.append("PUBLIC_ENDPOINTS_VERIFIED requires complete run and endpoint evidence")
        if receipt.get("required_next_transition") != "separate_release_and_destination_propagation_review":
            failures.append("verified state next transition mismatch")
    else:
        if receipt.get("verification_state") != "FAIL_CLOSED":
            failures.append("unsupported verification state")
        if verified:
            failures.append("fail-closed fixture unexpectedly contains complete verification evidence")
        if receipt.get("required_next_transition") != "repeat_public_endpoint_verification_from_observed_deployment":
            failures.append("fail-closed next transition mismatch")

    if receipt.get("release_authorized") is not False:
        failures.append("release_authorized must remain false")
    if receipt.get("downstream_propagation_authorized") is not False:
        failures.append("downstream_propagation_authorized must remain false")
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - set(receipt.get("non_claims", [])))
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in ("PUBLIC_ENDPOINTS_VERIFIED", "release_authorized", "downstream_propagation_authorized", "required_endpoints"):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("PAGES PUBLIC ENDPOINT VERIFICATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
