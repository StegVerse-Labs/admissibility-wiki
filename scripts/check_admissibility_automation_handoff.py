#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "ADMISSIBILITY_AUTOMATION_HANDOFF.md"
REQUIRED = (
    "scripts/check_ios_workflow_mirror_status.py",
    "static/status/ios-workflow-mirror-status.json",
    "validate:ios-workflow-mirror",
    "canonical workflow remains source of truth",
)


def main() -> int:
    if not HANDOFF.exists():
        print("ADMISSIBILITY AUTOMATION HANDOFF: FAIL")
        print("- missing ADMISSIBILITY_AUTOMATION_HANDOFF.md")
        return 1
    text = HANDOFF.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED if marker not in text]
    if missing:
        print("ADMISSIBILITY AUTOMATION HANDOFF: FAIL")
        for marker in missing:
            print(f"- missing marker: {marker}")
        return 1
    print("ADMISSIBILITY AUTOMATION HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
