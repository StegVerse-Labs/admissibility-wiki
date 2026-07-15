#!/usr/bin/env python3
"""Validate governed LLM demo docs and navigation references."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "docs/SITE_MIRROR_HANDOFF.md",
    "ADMISSIBILITY_MIRROR_HANDOFF.md",
    "docs/governance/governed-llm-demo-overview.md",
    "docs/governance/governed-llm-demo-verification.md",
    "docs/governance/governed-llm-activation-map.md",
)

REQUIRED_REFERENCES = {
    "sidebars.js": (
        "governance/governed-llm-demo-overview",
        "governance/governed-llm-demo-verification",
    ),
    "README.md": (
        "docs/governance/governed-llm-demo-overview.md",
        "docs/governance/governed-llm-demo-verification.md",
        "docs/SITE_MIRROR_HANDOFF.md",
    ),
    "docs/governance/governed-llm-activation-map.md": (
        "fixture-first",
        "replay",
        "reconstruction",
    ),
    "docs/governance/governed-llm-demo-overview.md": (
        "governed-llm-activation-map.md",
        "fixture success != live provider governance",
        "receipt handoff != Master-Records custody",
    ),
    "docs/governance/governed-llm-archive-handoff.md": (
        "docs/governance/governed-llm-demo-overview.md",
        "docs/governance/governed-llm-demo-verification.md",
        "scripts/check_governed_llm_demo_docs.py",
    ),
}


def main() -> int:
    failures: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required file: {relative_path}")

    for relative_path, needles in REQUIRED_REFERENCES.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"missing reference file: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                failures.append(f"missing reference in {relative_path}: {needle}")

    if failures:
        for failure in failures:
            print(f"GOVERNED LLM DEMO DOCS: FAIL - {failure}")
        return 1

    print("GOVERNED LLM DEMO DOCS: PASS - demo pages and bidirectional topology references present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
