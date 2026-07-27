#!/usr/bin/env python3
"""Check canonical custody binding for governed relationship publication evidence."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    ".github/workflows/validate-chain-continuation.yml": (
        "name: public-activation-receipt",
        "reports/public-activation-receipt.json",
        "retention-days: 30",
        "run: node scripts/write-public-activation-receipt.mjs",
    ),
    "scripts/write-public-activation-receipt.mjs": (
        "reports/governed-relationship-transition-publication-observation.json",
        "governed_relationship_transitions",
        "governed_relationship_transition_publication_observation",
        "receipt_preserved_despite_source_block",
    ),
    "scripts/check-public-activation-receipt-writer.mjs": (
        "standalone relationship receipt differs from embedded closure",
        "relationship publication authority mismatch",
        "relationship release authority mismatch",
        "relationship execution authority mismatch",
        "relationship admissibility mismatch",
        "relationship downstream authority mismatch",
    ),
    "docs/governance/GOVERNED_RELATIONSHIP_TRANSITIONS_MIRROR_HANDOFF.md": (
        "reports/public-activation-receipt.json",
        "reports/governed-relationship-transition-publication-observation.json",
        "observer receipt included in existing public-activation artifact custody: true",
    ),
}


def main() -> int:
    failures = []
    for relative, markers in CHECKS.items():
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(f"missing marker in {relative}: {marker}")
    if failures:
        for failure in failures:
            print(f"GOVERNED RELATIONSHIP CUSTODY: FAIL - {failure}")
        return 1
    print("GOVERNED RELATIONSHIP CUSTODY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
