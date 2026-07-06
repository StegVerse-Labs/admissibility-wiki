#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "guardian_destination_status.json"
STATUS = ROOT / "static" / "status" / "guardian-destination-resolution-status.json"
CANONICAL_PUBLIC = "StegVerse-002/stegguardian-wiki"
CANONICAL_PRIVATE = "StegVerse-002/StegGuardian"
CANDIDATES = [
    "StegVerse-Labs/stegguardian-wiki",
    "StegVerse-Labs/StegGuardian",
    "StegVerse-Labs/stegguardian",
    CANONICAL_PUBLIC,
    CANONICAL_PRIVATE,
]


def repo_exists(full_name: str) -> bool:
    url = f"https://api.github.com/repos/{full_name}"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def build_report() -> dict[str, Any]:
    checked = []
    found = []
    for candidate in CANDIDATES:
        exists = repo_exists(candidate)
        item: dict[str, Any] = {"repository_full_name": candidate, "result": "found" if exists else "not_found"}
        if candidate == CANONICAL_PUBLIC:
            item["visibility"] = "public"
            item["role"] = "public_guardian_wiki_summary_destination"
        if candidate == CANONICAL_PRIVATE:
            item["visibility"] = "private"
            item["role"] = "private_guardian_implementation_standing_boundary"
        checked.append(item)
        if exists:
            found.append(candidate)

    public_found = CANONICAL_PUBLIC in found
    private_found = CANONICAL_PRIVATE in found
    status = "UNBLOCKED" if public_found and private_found else "BLOCKED"
    return {
        "artifact_type": "guardian_destination_resolution_report",
        "schema_version": "0.2",
        "status": status,
        "checked_destinations": checked,
        "resolved_destinations": found,
        "canonical_public_destination": CANONICAL_PUBLIC if public_found else None,
        "canonical_private_destination": CANONICAL_PRIVATE if private_found else None,
        "next_action": "continue Guardian-side propagation after wiki validation" if status == "UNBLOCKED" else "create or identify the Guardian standing-boundary repository",
        "boundary": {
            "do_not_invent_repository_name": True,
            "no_activation_claim": True,
            "no_closure_claim": True,
            "no_consequence_binding_standing_claim": True,
            "public_destination_is_private_repo": False,
        },
    }


def main() -> int:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if STATUS.exists():
        status_data = json.loads(STATUS.read_text(encoding="utf-8"))
        if status_data.get("canonical_public_destination") != report.get("canonical_public_destination"):
            print("GUARDIAN DESTINATION: STATIC STATUS PUBLIC DESTINATION MISMATCH")
            return 1
        if status_data.get("canonical_private_destination") != report.get("canonical_private_destination"):
            print("GUARDIAN DESTINATION: STATIC STATUS PRIVATE DESTINATION MISMATCH")
            return 1
    print("GUARDIAN DESTINATION:", report["status"])
    for item in report["checked_destinations"]:
        print(f"- {item['repository_full_name']}: {item['result']}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0 if report["status"] == "UNBLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
