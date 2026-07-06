#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "external-frameworks"

REQUIRED_STANDARD_FILES = [
    DOCS / "evaluation-standard.md",
    DOCS / "failure-class-catalog.md",
    DOCS / "external-framework-template.md",
    DOCS / "EXPANSION_POLICY.json",
]

REQUIRED_INDEX_LINKS = [
    "./evaluation-standard.md",
    "./failure-class-catalog.md",
    "./external-framework-template.md",
]

REQUIRED_STANDARD_TERMS = [
    "Evidence Provenance",
    "Claim Traceability Rule",
    "Comparative Fairness Rule",
    "Observed Behavior Rule",
    "Required Runtime Result Artifact Set",
    "Machine-Readable Companion Requirement",
]

REQUIRED_FAILURE_CLASSES = [
    "FC-001",
    "Semantic Equivalence Divergence",
    "FC-007",
    "Fail-Open Runtime Error",
    "FC-012",
    "Evidence Class Confusion",
]

REQUIRED_TEMPLATE_SECTIONS = [
    "## Evidence Provenance",
    "## Parameterized Test Cases",
    "## StegVerse Analysis",
    "## Failure Classes",
    "## Non-Claims",
]

REQUIRED_MORRISON_TERMS = [
    "Evidence Provenance",
    "Parameterized Boundary Case",
    "Semantic Value Movement Versus Tool Label",
    "FC-001",
    "raw audit payload",
    "timestamp",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    for path in REQUIRED_STANDARD_FILES:
        if not path.exists():
            failures.append(f"missing standard file: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    index = read(DOCS / "index.md")
    standard = read(DOCS / "evaluation-standard.md")
    catalog = read(DOCS / "failure-class-catalog.md")
    template = read(DOCS / "external-framework-template.md")
    morrison = read(DOCS / "morrison-runtime.md")

    for link in REQUIRED_INDEX_LINKS:
        if link not in index:
            failures.append(f"index missing link: {link}")

    for term in REQUIRED_STANDARD_TERMS:
        if term not in standard:
            failures.append(f"evaluation standard missing term: {term}")

    for term in REQUIRED_FAILURE_CLASSES:
        if term not in catalog:
            failures.append(f"failure catalog missing term: {term}")

    for section in REQUIRED_TEMPLATE_SECTIONS:
        if section not in template:
            failures.append(f"template missing section: {section}")

    for term in REQUIRED_MORRISON_TERMS:
        if term not in morrison:
            failures.append(f"Morrison page missing term: {term}")

    # The page must not present the remembered historical six-test table as public validation evidence.
    banned_morrison_fragments = [
        "| 1 | ALLOW | BLOCK | False allow",
        "| Test | Observed Result | StegVerse Expected Result | Validation Meaning |",
    ]
    for fragment in banned_morrison_fragments:
        if fragment in morrison:
            failures.append("Morrison page still contains unsupported historical public result table")

    print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
