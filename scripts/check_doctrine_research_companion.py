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
    "handoff": [
        "SRC-PHASE3-001",
        "CLAIMED_FOR_IMPLEMENTATION",
        "CLAIMED_FOR_VALIDATION",
        "Group B",
        "Group H",
        "archive",
    ],
    "terminology": [
        "standing.evidentiary",
        "standing.interpretive",
        "standing.authority",
        "verification",
        "validation",
        "Prohibited unqualified terms",
    ],
    "claims": [
        "SRC-CLAIM-001",
        "SRC-CLAIM-018",
        "Adoption rule",
        "Known corpus limitation",
    ],
    "open_questions": [
        "SRC-OQ-001",
        "SRC-OQ-015",
        "Fail-closed rule",
        "Group B",
        "Group H",
    ],
    "formalism": [
        "Proposed StegVerse Formalism",
        "Transition Element",
        "Commit-Time Admissibility Reconstruction",
        "Dead Basis",
        "Standing Correction",
    ],
    "revision_matrix": [
        "SRC-REV-001",
        "SRC-REV-020",
        "Doctrine rewrite gate",
        "Propagation gate",
    ],
}

PROHIBITED_FALSE_COMPLETION = [
    re.compile(r"Phase 1[^\n]{0,80}\bCOMPLETE\b", re.IGNORECASE),
    re.compile(r"Phase 2[^\n]{0,80}\bCOMPLETE\b", re.IGNORECASE),
]


def fail(message: str) -> None:
    print(f"DOCTRINE RESEARCH COMPANION: FAILED - {message}")
    raise SystemExit(1)


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

    claim_ids = re.findall(r"SRC-CLAIM-(\d{3})", texts["claims"])
    if sorted(set(claim_ids)) != [f"{i:03d}" for i in range(1, 19)]:
        fail("claims register must contain contiguous SRC-CLAIM-001 through SRC-CLAIM-018")

    oq_ids = re.findall(r"SRC-OQ-(\d{3})", texts["open_questions"])
    if sorted(set(oq_ids)) != [f"{i:03d}" for i in range(1, 16)]:
        fail("open questions register must contain contiguous SRC-OQ-001 through SRC-OQ-015")

    rev_ids = re.findall(r"SRC-REV-(\d{3})", texts["revision_matrix"])
    if sorted(set(rev_ids)) != [f"{i:03d}" for i in range(1, 21)]:
        fail("revision matrix must contain contiguous SRC-REV-001 through SRC-REV-020")

    handoff = texts["handoff"]
    for pattern in PROHIBITED_FALSE_COMPLETION:
        if pattern.search(handoff) and "scaffold" not in handoff.lower():
            fail("handoff appears to claim Phase 1/2 completion without preserving scaffold caveat")

    if "Doctrine rewrite: NOT AUTHORIZED" not in handoff:
        fail("handoff must preserve the doctrine rewrite authority boundary")

    print(
        "DOCTRINE RESEARCH COMPANION: PASS - "
        "6 canonical files, 18 claims, 15 open questions, 20 revision rows validated"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
