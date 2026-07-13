#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static/schemas/external-chat-activation-status-promotion-receipt.schema.json"
FIXTURE = ROOT / "tests/fixtures/external-chat-activation-status-promotion-receipt.blocked.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA, FIXTURE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("EXTERNAL CHAT ACTIVATION STATUS PROMOTION: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    schema = load(SCHEMA)
    receipt = load(FIXTURE)
    missing = sorted(set(schema.get("required", [])) - set(receipt))
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")

    if receipt.get("schema_version") != "1.0.0":
        failures.append("schema_version mismatch")
    if receipt.get("receipt_type") != "external_chat_activation_status_promotion_receipt":
        failures.append("receipt_type mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if receipt.get("target_path") != "static/status/external-chat-activation-observation.json":
        failures.append("target path mismatch")

    candidate = receipt.get("source_candidate", {})
    evidence = receipt.get("source_evidence", {})
    if candidate.get("path") != "reports/external-chat-activation-observation-candidate.json":
        failures.append("source candidate path mismatch")
    if not HEX64.fullmatch(str(candidate.get("sha256", ""))):
        failures.append("candidate sha256 malformed")
    if evidence.get("repository") != "StegVerse-Labs/Site":
        failures.append("source evidence repository mismatch")
    if not HEX40.fullmatch(str(evidence.get("commit_sha", ""))):
        failures.append("source commit malformed")
    if not HEX64.fullmatch(str(evidence.get("evidence_sha256", ""))):
        failures.append("source evidence sha256 malformed")
    if evidence.get("mutation_required_disabled") is not True:
        failures.append("mutation_required_disabled must be true")

    allow = receipt.get("decision") == "ALLOW_CANONICAL_STATUS_PROMOTION_ONLY"
    if allow:
        if candidate.get("candidate_state") != "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE":
            failures.append("ALLOW requires observed candidate state")
        if receipt.get("canonical_status_mutation_allowed") is not True:
            failures.append("ALLOW requires canonical status mutation allowed")
    elif receipt.get("canonical_status_mutation_allowed") is not False:
        failures.append("non-ALLOW decision requires canonical status mutation false")

    if receipt.get("decision") != "FAIL_CLOSED":
        failures.append("blocked fixture must remain FAIL_CLOSED")

    expected_boundary = {
        "promotion_is_deployment_authority": False,
        "promotion_is_repository_mutation_authority": False,
        "promotion_is_publication_authority": False,
        "promotion_is_certification": False,
        "promotion_creates_standing": False,
        "mutation_remains_separately_authorized": True,
    }
    if receipt.get("authority_boundary") != expected_boundary:
        failures.append("authority boundary mismatch")

    schema_text = SCHEMA.read_text(encoding="utf-8")
    for marker in (
        "ALLOW_CANONICAL_STATUS_PROMOTION_ONLY",
        "canonical_status_mutation_allowed",
        "mutation_required_disabled",
        "external-chat-activation-observation.json",
    ):
        if marker not in schema_text:
            failures.append(f"schema missing marker: {marker}")

    print("EXTERNAL CHAT ACTIVATION STATUS PROMOTION:", "FAIL" if failures else "PASS")
    for item in failures:
        print(f"- {item}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
