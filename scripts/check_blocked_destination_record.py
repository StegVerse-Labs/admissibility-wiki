#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs" / "CHAIN_STATUS_BLOCKED_DESTINATION.json"

REQUIRED_FILES = [
    "docs/CHAIN_STATUS.md",
    "docs/CHAIN_STATUS_HANDOFF.md",
    "docs/CHAIN_STATUS_BLOCKED_DESTINATION.md",
    "docs/CHAIN_STATUS_BLOCKED_DESTINATION.json",
    "docs/CHAIN_STATUS_CONTINUATION.json",
    "docs/CHAIN_AUTO.json",
    "docs/CHAIN_SNAPSHOT_v0_1_0.md",
    "docs/CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json",
    "workflow_manifest.json",
]

REQUIRED_VALIDATORS = [
    "scripts/check_chain_status_continuation.py",
    "scripts/check_continuation_bundle.py",
    "scripts/check_chain_snapshot.py",
    "scripts/check_chain_snapshot_receipt.py",
    "scripts/check_chain_auto.py",
    "scripts/check_workflow_manifest.py",
    "scripts/check_guardian_destination.py",
]

REQUIRED_DESTINATIONS = [
    "StegVerse-Labs/stegguardian-wiki",
    "StegVerse-Labs/StegGuardian",
    "StegVerse-Labs/stegguardian",
]


def main() -> int:
    failures: list[str] = []
    data = json.loads(RECORD.read_text(encoding="utf-8"))

    if data.get("artifact_type") != "chain_status_blocked_destination":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("status") != "BLOCKED":
        failures.append("status mismatch")
    if data.get("resolver") != "scripts/check_guardian_destination.py":
        failures.append("resolver mismatch")
    if data.get("generated_report") != "reports/guardian_destination_status.json":
        failures.append("report path mismatch")

    for path in REQUIRED_FILES:
        if path not in data.get("current_files", []):
            failures.append(f"missing current file: {path}")
        elif not (ROOT / path).exists():
            failures.append(f"current file does not exist: {path}")

    for path in REQUIRED_VALIDATORS:
        if path not in data.get("validators", []):
            failures.append(f"missing validator: {path}")
        elif not (ROOT / path).exists():
            failures.append(f"validator does not exist: {path}")

    seen = {item.get("repository_full_name"): item.get("result") for item in data.get("checked_destinations", [])}
    for repo in REQUIRED_DESTINATIONS:
        if seen.get(repo) != "not_found":
            failures.append(f"destination result mismatch: {repo}")

    boundary = data.get("boundary", {})
    if boundary.get("do_not_invent_repository_name") is not True:
        failures.append("missing no-invention boundary")
    if boundary.get("resolver_creates_repository") is not False:
        failures.append("resolver creation boundary mismatch")

    print("BLOCKED DESTINATION RECORD:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
