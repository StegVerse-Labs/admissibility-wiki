#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "docs" / "GENERATED_PAGE_SURFACES_ROOT_ADDENDUM.md"
HANDOFF = ROOT / "docs" / "external-frameworks" / "GENERATED_PAGE_SURFACES_HANDOFF.md"
STATE = ROOT / "docs" / "external-frameworks" / "generated-page-surfaces.json"

REQUIRED_TEXT = [
    "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "docs/governance/current-task-sync.md",
    "docs/external-frameworks/GENERATED_PAGE_SURFACES_HANDOFF.md",
    "docs/external-frameworks/generated-page-surfaces.json",
    "metadata",
    "mapping",
    "page_status",
    "analysis_boundary",
    "scripts/check_external_framework_page_status.py",
    "no additional workflow is required",
]


def main() -> int:
    failures: list[str] = []
    if not ADDENDUM.exists():
        failures.append("root addendum missing")
    if not HANDOFF.exists():
        failures.append("surface handoff missing")
    if not STATE.exists():
        failures.append("surface inventory missing")
    if ADDENDUM.exists():
        text = ADDENDUM.read_text(encoding="utf-8")
        for item in REQUIRED_TEXT:
            if item not in text:
                failures.append(f"root addendum missing text: {item}")

    print("GENERATED PAGE SURFACES ROOT ADDENDUM:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
