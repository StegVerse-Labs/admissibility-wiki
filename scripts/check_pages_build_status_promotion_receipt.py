#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "pages-build-status-promotion-receipt.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "pages-build-status-promotion-receipt.blocked.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED_NON_CLAIMS = {
    "verification candidate does not authorize canonical status mutation",
    "formalism validator evidence must be observed before promotion",
    "Pages artifact identifiers and digest must be observed before promotion",
    "status promotion is not deployment authority",
    "Pages artifact preservation is not public verification",
    "fixture validation does not authorize release or downstream propagation",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("PAGES BUILD STATUS PROMOTION RECEIPT: FAIL")
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
    if receipt.get("receipt_type") != "pages_build_status_promotion_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")

    candidate = receipt.get("source_candidate", {})
    if candidate.get("path") != "reports/pages-build-verification-candidate.json":
        failures.append("source candidate path mismatch")
    if not HEX64.fullmatch(str(candidate.get("sha256", ""))):
        failures.append("source candidate sha256 malformed")

    formalism = receipt.get("formalism_validator_evidence", {})
    pages = receipt.get("pages_artifact_evidence", {})
    decision = receipt.get("decision")
    allowed = receipt.get("canonical_status_mutation_allowed")

    formalism_pass = formalism.get("status") == "PASS" and bool(formalism.get("evidence_ref"))
    pages_pass = (
        pages.get("status") == "PASS"
        and isinstance(pages.get("run_id"), int)
        and isinstance(pages.get("job_id"), int)
        and isinstance(pages.get("artifact_id"), int)
        and bool(pages.get("evidence_ref"))
        and DIGEST.fullmatch(str(pages.get("artifact_digest", ""))) is not None
    )

    if decision == "ALLOW_STATUS_PROMOTION_ONLY":
        if not formalism_pass:
            failures.append("ALLOW_STATUS_PROMOTION_ONLY requires observed formalism validator PASS")
        if not pages_pass:
            failures.append("ALLOW_STATUS_PROMOTION_ONLY requires complete Pages artifact evidence")
        if allowed is not True:
            failures.append("ALLOW_STATUS_PROMOTION_ONLY requires canonical_status_mutation_allowed true")
    else:
        if allowed is not False:
            failures.append("non-ALLOW decision requires canonical_status_mutation_allowed false")

    if receipt.get("deployment_authorized") is not False:
        failures.append("deployment_authorized must remain false")
    if receipt.get("public_verification_complete") is not False:
        failures.append("public_verification_complete must remain false")

    if receipt.get("decision") != "FAIL_CLOSED":
        failures.append("blocked fixture must remain FAIL_CLOSED")
    if formalism_pass or pages_pass:
        failures.append("blocked fixture must not contain complete promotion evidence")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        failures.append(f"missing non-claims: {', '.join(missing_non_claims)}")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "ALLOW_STATUS_PROMOTION_ONLY",
        "canonical_status_mutation_allowed",
        "formalism_validator_evidence",
        "pages_artifact_evidence",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("PAGES BUILD STATUS PROMOTION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
