#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "external-frameworks" / "GENERATED_PAGE_SURFACES_HANDOFF.md"
STATE = ROOT / "docs" / "external-frameworks" / "generated-page-surfaces.json"
STATE_CHECK = ROOT / "scripts" / "check_external_framework_page_surfaces.py"

REQUIRED_TEXT = [
    "docs/external-frameworks/generated-page-surfaces.json",
    "scripts/check_external_framework_page_surfaces.py",
    "metadata",
    "mapping",
    "page_status",
    "analysis_boundary",
    "terms",
    "No generated surface listed as active requires a manual wiring task.",
]


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("handoff missing")
    if not STATE.exists():
        failures.append("surface inventory missing")
    if not STATE_CHECK.exists():
        failures.append("surface validator missing")
    if HANDOFF.exists():
        text = HANDOFF.read_text(encoding="utf-8")
        for item in REQUIRED_TEXT:
            if item not in text:
                failures.append(f"handoff missing text: {item}")

    print("GENERATED PAGE SURFACES HANDOFF:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
