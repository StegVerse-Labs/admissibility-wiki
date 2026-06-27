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
CANDIDATES = [
    "StegVerse-Labs/stegguardian-wiki",
    "StegVerse-Labs/StegGuardian",
    "StegVerse-Labs/stegguardian",
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
        checked.append({"repository_full_name": candidate, "result": "found" if exists else "not_found"})
        if exists:
            found.append(candidate)

    return {
        "artifact_type": "guardian_destination_resolution_report",
        "schema_version": "0.1",
        "status": "FOUND" if found else "BLOCKED",
        "checked_destinations": checked,
        "resolved_destinations": found,
        "next_action": "continue Guardian-side propagation" if found else "create or identify the Guardian standing-boundary repository",
        "boundary": {
            "do_not_invent_repository_name": True,
            "no_activation_claim": True,
            "no_closure_claim": True,
            "no_consequence_binding_standing_claim": True,
        },
    }


def main() -> int:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("GUARDIAN DESTINATION:", report["status"])
    for item in report["checked_destinations"]:
        print(f"- {item['repository_full_name']}: {item['result']}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
