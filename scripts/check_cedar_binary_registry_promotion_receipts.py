#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "cedar-binary-registry-promotion-receipt.schema.json"
FIXTURES = [
    ROOT / "tests" / "fixtures" / "cedar-binary-registry-promotion-receipt.blocked.json",
    ROOT / "tests" / "fixtures" / "cedar-binary-registry-promotion-receipt.approved-not-applied.json",
]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_NON_CLAIMS = {
    "binary hash promotion does not establish compatibility",
    "registry mutation does not authorize runtime execution",
}


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def main() -> int:
    failures: list[str] = []
    for path in [SCHEMA, *FIXTURES]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("CEDAR BINARY REGISTRY PROMOTION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema = load(SCHEMA)
    required = set(schema.get("required", []))

    for fixture in FIXTURES:
        receipt = load(fixture)
        name = fixture.name
        missing = sorted(required - set(receipt))
        if missing:
            failures.append(f"{name}: missing fields {', '.join(missing)}")
        if receipt.get("schema_version") != "0.1":
            failures.append(f"{name}: schema_version mismatch")
        if receipt.get("receipt_type") != "cedar_binary_registry_promotion_receipt":
            failures.append(f"{name}: receipt_type mismatch")
        if receipt.get("framework_id") != "cedar-policy":
            failures.append(f"{name}: framework_id mismatch")
        source = receipt.get("source_promotion_candidate", {})
        if not HEX64.fullmatch(str(source.get("sha256", ""))):
            failures.append(f"{name}: source candidate sha256 invalid")
        if receipt.get("runtime_execution_authorized") is not False:
            failures.append(f"{name}: runtime execution must remain false")
        if receipt.get("external_consequence_allowed") is not False:
            failures.append(f"{name}: external consequence must remain false")
        if not REQUIRED_NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
            failures.append(f"{name}: required non-claims missing")

        decision = receipt.get("decision")
        state = receipt.get("promotion_state")
        review = receipt.get("review", {})
        target = receipt.get("registry_target")
        applied = receipt.get("registry_mutation_applied")

        if decision == "ALLOW_REGISTRY_PROMOTION_ONLY":
            if state not in {"APPROVED_NOT_APPLIED", "APPLIED_HASH_ONLY"}:
                failures.append(f"{name}: allow decision has invalid state")
            if source.get("candidate_state") != "READY_FOR_REGISTRY_PROMOTION_REVIEW":
                failures.append(f"{name}: allow decision requires ready candidate")
            if not HEX64.fullmatch(str(source.get("binary_sha256", ""))):
                failures.append(f"{name}: allow decision requires binary sha256")
            if review.get("status") != "PASS" or not review.get("reviewer_identity") or not review.get("delegation_ref"):
                failures.append(f"{name}: allow decision requires completed delegated review")
            if not isinstance(target, dict):
                failures.append(f"{name}: allow decision requires registry target")
            else:
                if target.get("proposed_value") != source.get("binary_sha256"):
                    failures.append(f"{name}: target hash must equal candidate binary hash")
                if target.get("field") != "frameworks[cedar-policy].selection.compiled_binary_sha256":
                    failures.append(f"{name}: registry field mismatch")
            if state == "APPROVED_NOT_APPLIED" and applied is not False:
                failures.append(f"{name}: approved-not-applied must not claim mutation")
            if state == "APPLIED_HASH_ONLY" and applied is not True:
                failures.append(f"{name}: applied state must claim mutation")
        else:
            if applied is not False:
                failures.append(f"{name}: non-allow decision cannot apply mutation")
            if state == "BLOCKED_NO_VALID_CANDIDATE" and target is not None:
                failures.append(f"{name}: blocked receipt must not contain registry target")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in ("ALLOW_REGISTRY_PROMOTION_ONLY", "APPROVED_NOT_APPLIED", "APPLIED_HASH_ONLY", "runtime_execution_authorized", "external_consequence_allowed"):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("CEDAR BINARY REGISTRY PROMOTION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
