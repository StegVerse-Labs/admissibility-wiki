#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static" / "schemas" / "pages-artifact-binding-receipt.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "pages-artifact-binding-receipt.preserved.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("PAGES ARTIFACT BINDING RECEIPT: FAIL")
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
        failures.append("schema_version mismatch")
    if receipt.get("receipt_type") != "pages_artifact_binding_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if not HEX40.fullmatch(str(receipt.get("target_commit", ""))):
        failures.append("target_commit malformed")

    source = receipt.get("source_candidate", {})
    if source.get("path") != "reports/pages-build-verification-candidate.json":
        failures.append("source candidate path mismatch")
    if not HEX64.fullmatch(str(source.get("sha256", ""))):
        failures.append("source candidate sha256 malformed")
    if source.get("verification_state") != "PAGES_BUILD_PASS_ARTIFACT_PENDING":
        failures.append("source candidate state mismatch")
    if not HEX64.fullmatch(str(source.get("build_manifest_sha256", ""))):
        failures.append("build manifest sha256 malformed")

    workflow = receipt.get("observed_workflow", {})
    for key in ("run_id", "job_id", "run_attempt"):
        if not isinstance(workflow.get(key), int) or workflow.get(key, 0) <= 0:
            failures.append(f"observed_workflow.{key} invalid")

    artifact = receipt.get("artifact", {})
    if artifact.get("name") != "github-pages":
        failures.append("artifact name mismatch")
    if not isinstance(artifact.get("artifact_id"), int) or artifact.get("artifact_id", 0) <= 0:
        failures.append("artifact_id invalid")
    if not DIGEST.fullmatch(str(artifact.get("artifact_digest", ""))):
        failures.append("artifact digest malformed")
    if artifact.get("preserved") is not True:
        failures.append("artifact must be preserved")

    if receipt.get("verification_state") != "PAGES_ARTIFACT_PRESERVED":
        failures.append("verification state mismatch")
    for key in (
        "canonical_status_mutation_applied",
        "deployment_authorized",
        "public_verification_complete",
        "release_authorized",
        "downstream_propagation_authorized",
    ):
        if receipt.get(key) is not False:
            failures.append(f"{key} must remain false")

    if receipt.get("required_next_transition") != "apply_observed_pages_artifact_evidence_to_canonical_status_in_separate_governed_commit":
        failures.append("required_next_transition mismatch")

    non_claims = set(receipt.get("non_claims", []))
    required_non_claims = {
        "artifact preservation is not deployment authority",
        "artifact preservation is not public verification",
        "artifact binding does not mutate canonical status",
        "artifact binding does not authorize release",
        "artifact binding does not authorize downstream propagation",
        "build success and artifact upload do not establish governance standing",
    }
    if not required_non_claims.issubset(non_claims):
        failures.append("required non-claims missing")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "PAGES_ARTIFACT_PRESERVED",
        "canonical_status_mutation_applied",
        "deployment_authorized",
        "public_verification_complete",
        "release_authorized",
        "downstream_propagation_authorized",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("PAGES ARTIFACT BINDING RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
