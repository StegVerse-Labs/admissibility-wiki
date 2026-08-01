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
        "embedded relationship-transition closure differs from standalone receipt",
        "relationship-transition authority boundary mismatch: ${key}",
        "relationship-transition receipt binding mismatch",
        "publication_authority_granted",
        "release_authority_granted",
        "execution_authority_granted",
        "admissibility_granted",
        "downstream_mutation_authority_granted",
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
