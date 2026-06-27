#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTINUATION = ROOT / "docs" / "CHAIN_STATUS_CONTINUATION.json"
SCHEMA = ROOT / "docs" / "CHAIN_STATUS_CONTINUATION.schema.json"

REQUIRED_KEYS = [
    "$schema",
    "artifact_type",
    "schema_version",
    "current_stage",
    "current_status",
    "source_repo",
    "verification_repo",
    "wiki_repo",
    "current_documents",
    "blocking_condition",
    "next_required_action",
    "non_claims",
    "resume_when",
]

REQUIRED_NON_CLAIMS = [
    "no_activation_claim",
    "no_closure_claim",
    "no_adoption_claim",
    "no_endorsement_claim",
    "no_consequence_binding_standing_claim",
    "do_not_invent_repository_name",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not CONTINUATION.exists():
        failures.append("missing continuation manifest")
    if not SCHEMA.exists():
        failures.append("missing continuation schema")
    if failures:
        print("CHAIN CONTINUATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    continuation = load_json(CONTINUATION)
    schema = load_json(SCHEMA)

    for key in REQUIRED_KEYS:
        if key not in continuation:
            failures.append(f"missing key: {key}")

    if continuation.get("$schema") != "docs/CHAIN_STATUS_CONTINUATION.schema.json":
        failures.append("schema reference mismatch")
    if continuation.get("artifact_type") != "chain_status_continuation":
        failures.append("artifact type mismatch")
    if continuation.get("current_status") != "BLOCKED_ON_DESTINATION_REPOSITORY":
        failures.append("blocked status mismatch")
    if continuation.get("blocking_condition", {}).get("type") != "missing_destination_repository":
        failures.append("blocking condition mismatch")

    checked = continuation.get("blocking_condition", {}).get("checked_destinations", [])
    for destination in [
        "StegVerse-Labs/stegguardian-wiki",
        "StegVerse-Labs/StegGuardian",
        "StegVerse-Labs/stegguardian",
    ]:
        if destination not in checked:
            failures.append(f"missing checked destination: {destination}")

    non_claims = continuation.get("non_claims", {})
    for claim in REQUIRED_NON_CLAIMS:
        if non_claims.get(claim) is not True:
            failures.append(f"non-claim not enforced: {claim}")

    documents = continuation.get("current_documents", [])
    for document in documents:
        if not (ROOT / document).exists():
            failures.append(f"listed document missing: {document}")

    if schema.get("title") != "Chain Status Continuation":
        failures.append("schema title mismatch")

    print("CHAIN CONTINUATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
