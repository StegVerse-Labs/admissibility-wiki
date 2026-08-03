#!/usr/bin/env python3
"""Fail-closed structural validator for the Standing Research Companion package."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "handoff": ROOT / "docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md",
    "source_index": ROOT / "docs/research/standing-research-companion-source-index.md",
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

REQUIRED_REPLACEMENT_TASKS = {
    "SRC-P1-B-CT",
    "SRC-P1-B-DS",
    "SRC-P1-B-NS",
    "SRC-P1-B-CAS",
    "SRC-P1-B-SB",
    "SRC-P1-H-NEURO",
    "SRC-P1-H-BCI",
    "SRC-P1-H-BIOINFO",
    "SRC-P1-H-COMP-BIO",
}

REQUIRED_MARKERS = {
    "handoff": ["SRC-PHASE3-001", "Group B", "Group H", "archive"],
    "source_index": [
        "SCAFFOLD_RESEARCH_PLAN",
        "SCAFFOLD_REVIEW_PROMPT",
        "MISSING_SUBSTANTIVE_REVIEW",
        "SRC-P2-RERUN-BH",
        "source presence != substantive completion",
    ],
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

    missing_tasks = sorted(task for task in REQUIRED_REPLACEMENT_TASKS if task not in texts["source_index"])
    if missing_tasks:
        fail(f"source index missing Group B/H replacement tasks: {', '.join(missing_tasks)}")

    if texts["source_index"].count("MISSING_SUBSTANTIVE_REVIEW") < 9:
        fail("source index must explicitly classify all nine Group B/H reviews as missing until substantive chapters pass")

    require_contiguous(texts["claims"], "SRC-CLAIM-", 1, 18)
    require_contiguous(texts["open_questions"], "SRC-OQ-", 1, 15)
    require_contiguous(texts["revision_matrix"], "SRC-REV-", 1, 20)

    handoff_lower = texts["handoff"].lower()
    if "phase 1" not in handoff_lower or "phase 2" not in handoff_lower or "scaffold" not in handoff_lower:
        fail("handoff must preserve the Group B/H scaffold limitation for Phase 1 and Phase 2")
    if "Doctrine rewrite: NOT AUTHORIZED" not in texts["handoff"]:
        fail("handoff must preserve the doctrine rewrite authority boundary")

    if "chat-only requirements remaining after this commit: none" not in texts["source_index"]:
        fail("source index must preserve the session-consolidation transfer state")

    print(
        "DOCTRINE RESEARCH COMPANION: PASS - "
        "7 canonical control files, 9 Group B/H replacement tasks, "
        "18 claims, 15 open questions, and 20 revision rows validated"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
