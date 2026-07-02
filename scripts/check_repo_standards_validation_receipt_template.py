#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "static" / "status" / "repo-standards-local-validation-receipt-template.json"


def main() -> int:
    if not TEMPLATE.exists():
        raise SystemExit("RECEIPT TEMPLATE: FAIL - template missing")
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    expected = {
        "receipt_id": "repo-standards-local-validation-receipt-template",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "status": "TEMPLATE_READY",
        "command": "python scripts/check_repo_standards_all.py",
        "expected_result": "REPO STANDARDS ALL: PASS",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f"RECEIPT TEMPLATE: FAIL - {key} expected {value!r}, got {data.get(key)!r}")
    fill = data.get("fill_after_run")
    if not isinstance(fill, dict):
        raise SystemExit("RECEIPT TEMPLATE: FAIL - fill_after_run missing")
    for key in ["run_timestamp_utc", "runner", "commit", "result", "stdout_excerpt", "stderr_excerpt", "follow_up_required"]:
        if key not in fill:
            raise SystemExit(f"RECEIPT TEMPLATE: FAIL - fill_after_run missing {key}")
    print("RECEIPT TEMPLATE: PASS - local validation receipt template present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
