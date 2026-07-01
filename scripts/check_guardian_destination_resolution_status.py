#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "guardian-destination-resolution-status.json"

EXPECTED_PUBLIC = "StegVerse-002/stegguardian-wiki"
EXPECTED_PRIVATE = "StegVerse-002/StegGuardian"


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists():
        print("GUARDIAN DESTINATION RESOLUTION STATUS: FAIL")
        print("- status file missing")
        return 1

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "guardian_destination_resolution_status":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("status") != "UNBLOCKED":
        failures.append("status mismatch")
    if data.get("canonical_public_destination") != EXPECTED_PUBLIC:
        failures.append("public destination mismatch")
    if data.get("canonical_private_destination") != EXPECTED_PRIVATE:
        failures.append("private destination mismatch")

    checked = {item.get("repository_full_name"): item for item in data.get("checked_destinations", [])}
    expected = {
        EXPECTED_PUBLIC: ("found", "public"),
        EXPECTED_PRIVATE: ("found", "private"),
        "StegVerse-Labs/stegguardian-wiki": ("not_found", None),
        "StegVerse-Labs/StegGuardian": ("not_found", None),
        "StegVerse-Labs/stegguardian": ("not_found", None),
    }
    for repo, (result, visibility) in expected.items():
        item = checked.get(repo)
        if not item:
            failures.append(f"missing checked destination: {repo}")
            continue
        if item.get("result") != result:
            failures.append(f"destination result mismatch: {repo}")
        if visibility and item.get("visibility") != visibility:
            failures.append(f"destination visibility mismatch: {repo}")

    boundary = data.get("boundary", {})
    required_boundaries = {
        "do_not_invent_repository_name": True,
        "no_activation_claim": True,
        "no_closure_claim": True,
        "no_consequence_binding_standing_claim": True,
        "public_destination_is_private_repo": False,
    }
    for key, expected_value in required_boundaries.items():
        if boundary.get(key) is not expected_value:
            failures.append(f"boundary mismatch: {key}")

    print("GUARDIAN DESTINATION RESOLUTION STATUS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
