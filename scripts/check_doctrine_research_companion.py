#!/usr/bin/env python3
"""Fail-closed structural validator for the Standing Research Companion Phase 3 package."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "handoff": ROOT / "docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md",
    "terminology": ROOT / "docs/research/standing-research-companion-volume-iii-comparative-terminology.md",
    "claims": ROOT / "docs/research/standing-research-companion-volume-iv-claims-register.md",
    "open_questions": ROOT / "docs/research/standing-research-companion-volume-v-open-questions.md",
    "formalism": ROOT / "docs/research/stegverse-formalism-declaration.md",
    "revision_matrix": ROOT / "docs/research/doctrine-revision-matrix.md",
}

REQUIRED_CLASSIFICATIONS = {
    "NATURAL_ALIGNMENT",
    "COMPATIBLE_EXTENSION",
    "TERMINOLOGY_CONFLICT",
    "REQUIRES_MODIFICATION",
    "EVIDENCE_INSUFFICIENT",
    "NEW_STEGVERSE_FORMALISM",
    "CONTRADICTED",
    "UNKNOWN",
}

REQUIRED_MARKERS = {
    "handoff": ["SRC-PHASE3-001", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "Group B", "Group H", "archive"],
    "terminology": ["standing.evidentiary", "standing.interpretive", "standing.authority", "verification", "validation", "Prohibited unqualified terms"],
    "claims": ["SRC-CLAIM-001", "SRC-CLAIM-018", "Adoption rule", "Known corpus limitation"],
    "open_questions": ["SRC-OQ-001", "SRC-OQ-015", "Fail-closed rule", "Group B", "Group H"],
    "formalism": ["Proposed StegVerse formalism", "Transition Element", "Commit-Time Admissibility Reconstruction", "Dead Basis", "Standing Correction"],
    "revision_matrix": ["SRC-REV-001", "SRC-REV-020", "Doctrine rewrite gate", "Propagation gate"],
}


def fail(message: str) -> None:
    print(f"DOCTRINE RESEARCH COMPANION: FAILED - {message}")
    raise SystemExit(1)


def require_contiguous(text: str, prefix: str, start: int, end: int) -> None:
    found = sorted(set(re.findall(rf"{re.escape(prefix)}(\d{{3}})", text)))
    expected = [f"{i:03d}" for i in range(start, end + 1)]
    if found != expected:
        fail(f"{prefix} register must contain contiguous {prefix}{start:03d} through {prefix}{end:03d}")


def main() -> int:
    texts: dict[str, str] = {}
    for key, path in REQUIRED_FILES.items():
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 200:
            fail(f"required file is empty or stub-like: {path.relative_to(ROOT)}")
        texts[key] = text
        for marker in REQUIRED_MARKERS[key]:
            if marker not in text:
                fail(f"{path.relative_to(ROOT)} missing marker: {marker}")

    combined = "\n".join(texts.values())
    missing_classes = sorted(c for c in REQUIRED_CLASSIFICATIONS if c not in combined)
    if missing_classes:
        fail(f"missing canonical classifications: {', '.join(missing_classes)}")

    require_contiguous(texts["claims"], "SRC-CLAIM-", 1, 18)
    require_contiguous(texts["open_questions"], "SRC-OQ-", 1, 15)
    require_contiguous(texts["revision_matrix"], "SRC-REV-", 1, 20)

    handoff_lower = texts["handoff"].lower()
    if "phase 1" not in handoff_lower or "phase 2" not in handoff_lower or "scaffold" not in handoff_lower:
        fail("handoff must preserve the Group B/H scaffold limitation for Phase 1 and Phase 2")
    if "Doctrine rewrite: NOT AUTHORIZED" not in texts["handoff"]:
        fail("handoff must preserve the doctrine rewrite authority boundary")

    print("DOCTRINE RESEARCH COMPANION: PASS - 6 canonical files, 18 claims, 15 open questions, 20 revision rows validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
