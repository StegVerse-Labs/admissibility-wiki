#!/usr/bin/env python3
"""Validate the admissibility-wiki HPS public mirror page."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "formalisms" / "hps" / "README.md"

REQUIRED_PHRASES = [
    "Harmonic Principle of Standing",
    "Admissible-Existence/HPS",
    "Integrity is not standing.",
    "Standing is not admissibility.",
    "Admissibility is not execution authority.",
    "A capability becomes available when the heartbeat restores the standing required for that transition class.",
    "No capability may borrow standing from a prior heartbeat after its window has closed.",
    "S(t) = B(t) + C(t) + A(t) + R(t) - D(t)",
    "master-records/orchestration",
    "This page is explanatory.",
]


def main() -> int:
    if not DOC.exists():
        print("FAIL: missing docs/formalisms/hps/README.md")
        return 1
    text = DOC.read_text(encoding="utf-8")
    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]
    if missing:
        print("FAIL: HPS public mirror missing required phrases")
        for phrase in missing:
            print(f"- {phrase}")
        return 1
    print("PASS: HPS public mirror page is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
