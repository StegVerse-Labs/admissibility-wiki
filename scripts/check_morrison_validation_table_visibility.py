#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "external-frameworks" / "morrison-runtime.md"
CSS = ROOT / "src" / "css" / "custom.css"

EXPECTED_CASES = [
    "Safe read-only policy request",
    "Unapproved funds transfer",
    "Approval spoofing",
    "Delayed intent",
    "Multi-agent delegation",
    "Unauthorized state transition",
    "Runtime evaluator error",
    "Runtime ALLOW but StegVerse authority missing",
    "Runtime BLOCK but StegVerse evidence complete",
    "Semantic value movement under alternate tool label",
]

REQUIRED_CSS_MARKERS = [
    "--cooperative-agreement-bg",
    "--cooperative-disagreement-bg",
    "--cooperative-caution-bg",
    "h2#cooperative-validation-suite",
    "tbody tr:nth-child(8)",
    "tbody tr:nth-child(10)",
    "[data-theme='dark']",
]


def main() -> int:
    failures: list[str] = []

    for path in [PAGE, CSS]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("MORRISON VALIDATION TABLE VISIBILITY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    page = PAGE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    for case in EXPECTED_CASES:
        if case not in page:
            failures.append(f"missing cooperative validation case: {case}")

    for marker in REQUIRED_CSS_MARKERS:
        if marker not in css:
            failures.append(f"missing visibility CSS marker: {marker}")

    if "Color is supplementary" not in css:
        failures.append("CSS must preserve a non-color-only accessibility note")

    print("MORRISON VALIDATION TABLE VISIBILITY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
