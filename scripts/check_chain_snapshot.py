#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs" / "CHAIN_SNAPSHOT_v0_1_0.md"

REQUIRED_TEXT = [
    "# Chain Snapshot v0.1.0",
    ".github/workflows/validate-chain-continuation.yml",
    "docs/CHAIN_AUTO.json",
    "docs/CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json",
    "scripts/check_chain_status_continuation.py",
    "scripts/check_continuation_bundle.py",
    "scripts/check_chain_snapshot.py",
    "scripts/check_chain_snapshot_receipt.py",
    "scripts/check_chain_auto.py",
    "scripts/check_blocked_destination_record.py",
    "scripts/check_workflow_manifest.py",
    "scripts/check_guardian_destination.py",
    "CHAIN CONTINUATION: PASS",
    "CONTINUATION BUNDLE: PASS",
    "CHAIN SNAPSHOT: PASS",
    "CHAIN SNAPSHOT RECEIPT: PASS",
    "CHAIN AUTO: PASS",
    "BLOCKED DESTINATION RECORD: PASS",
    "WORKFLOW MANIFEST: PASS",
    "GUARDIAN DESTINATION: BLOCKED",
    "reports/guardian_destination_status.json",
]


def main() -> int:
    failures: list[str] = []

    if not SNAPSHOT.exists():
        print("CHAIN SNAPSHOT: FAIL")
        print("- missing docs/CHAIN_SNAPSHOT_v0_1_0.md")
        return 1

    content = SNAPSHOT.read_text(encoding="utf-8")
    for text in REQUIRED_TEXT:
        if text not in content:
            failures.append(f"missing snapshot text: {text}")

    print("CHAIN SNAPSHOT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
