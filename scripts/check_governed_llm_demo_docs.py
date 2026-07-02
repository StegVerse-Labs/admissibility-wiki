#!/usr/bin/env python3
"""Validate governed LLM demo docs and navigation references."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/governance/governed-llm-demo-overview.md",
    "docs/governance/governed-llm-demo-verification.md",
]

SIDEBAR_REFS = [
    "governance/governed-llm-demo-overview",
    "governance/governed-llm-demo-verification",
]

README_REFS = [
    "docs/governance/governed-llm-demo-overview.md",
    "docs/governance/governed-llm-demo-verification.md",
]


def fail(message: str) -> int:
    print(f"GOVERNED LLM DEMO DOCS: FAIL - {message}")
    return 1


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            return fail(f"missing required file: {rel}")

    sidebar = read("sidebars.js")
    for ref in SIDEBAR_REFS:
        if ref not in sidebar:
            return fail(f"sidebars.js missing reference: {ref}")

    readme = read("README.md")
    for ref in README_REFS:
        if ref not in readme:
            return fail(f"README.md missing reference: {ref}")

    activation = read("docs/governance/governed-llm-activation-map.md")
    if "governed-llm-demo-overview" not in activation:
        return fail("activation map missing demo overview reference")

    archive = read("docs/governance/governed-llm-archive-handoff.md")
    for ref in ["governed-llm-demo-overview", "governed-llm-demo-verification"]:
        if ref not in archive:
            return fail(f"archive handoff missing reference: {ref}")

    print("GOVERNED LLM DEMO DOCS: PASS - demo pages and navigation references present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
