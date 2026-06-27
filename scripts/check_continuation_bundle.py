#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "CHAIN_STATUS_CONTINUATION.json"

REQUIRED_GROUPS = [
    "current_documents",
    "current_workflows",
    "current_validators",
]

REQUIRED_WORKFLOWS = [
    ".github/workflows/validate-chain-continuation.yml",
    "iosnoperiod/github/workflows/validate-chain-continuation.yml",
]

REQUIRED_VALIDATORS = [
    "scripts/check_chain_status_continuation.py",
    "scripts/check_chain_snapshot_receipt.py",
    "scripts/check_chain_auto.py",
    "scripts/check_workflow_manifest.py",
    "scripts/check_guardian_destination.py",
]


def main() -> int:
    failures: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for group in REQUIRED_GROUPS:
        values = data.get(group)
        if not isinstance(values, list):
            failures.append(f"missing list: {group}")
            continue
        for value in values:
            if not isinstance(value, str) or not (ROOT / value).exists():
                failures.append(f"missing path from {group}: {value}")

    for value in REQUIRED_WORKFLOWS:
        if value not in data.get("current_workflows", []):
            failures.append(f"missing workflow entry: {value}")

    for value in REQUIRED_VALIDATORS:
        if value not in data.get("current_validators", []):
            failures.append(f"missing validator entry: {value}")

    print("CONTINUATION BUNDLE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
