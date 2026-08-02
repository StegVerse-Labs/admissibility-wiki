#!/usr/bin/env python3
"""Validate TA-14 source PDF custody without halting unrelated development."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "static/evidence/ta14/TA-14-StegVerse-Public-Evidence-Gap-Review-v2.0.pdf"
STATUS = ROOT / "static/status/ta14-remediation-status.json"
EXPECTED_SHA256 = "4d9bfb86738601952ede6f5e83477ea3c086ce229c3403d2fa3bdaf4ae75bfbf"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    if not STATUS.is_file():
        return fail(f"missing status file: {STATUS.relative_to(ROOT)}")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    if status.get("development_halt") is not False:
        return fail("TA-14 status must preserve development_halt=false")
    if status.get("external_tasks") != []:
        return fail("TA-14 status must preserve external_tasks=[]")

    blocks = status.get("bounded_claim_blocks")
    if not isinstance(blocks, list):
        return fail("bounded_claim_blocks must be a list")
    custody = next((item for item in blocks if isinstance(item, dict) and item.get("claim") == "exact PDF public custody"), None)
    if custody is None:
        return fail("missing exact PDF public custody claim state")
    if custody.get("location") != str(PDF.relative_to(ROOT)):
        return fail("PDF custody claim location mismatch")

    if not PDF.is_file():
        if custody.get("state") != "EVIDENCE_ABSENT_FAIL_CLOSED":
            return fail("absent PDF must retain EVIDENCE_ABSENT_FAIL_CLOSED")
        print("PASS: TA-14 PDF absent; exact custody claim remains fail-closed; development continues")
        return 0

    data = PDF.read_bytes()
    if not data.startswith(b"%PDF-"):
        return fail("source artifact does not have a PDF header")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(f"source PDF digest mismatch: expected={EXPECTED_SHA256} actual={digest}")
    if custody.get("state") not in {"VERIFIED_BOUNDED", "COMPLETE"}:
        return fail("present, digest-verified PDF requires VERIFIED_BOUNDED or COMPLETE custody state")

    print(f"PASS: TA-14 source PDF custody verified sha256={digest} bytes={len(data)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
