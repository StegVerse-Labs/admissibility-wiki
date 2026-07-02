#!/usr/bin/env python3
"""Verify governed LLM public pages are present and discoverable."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "docs/governance/governed-llm-reconstructive-search.md",
    "docs/governance/governed-llm-activation-map.md",
    "docs/governance/governed-llm-site-verification.md",
    "docs/governance/governed-llm-deployment-status.md",
)
REQUIRED_REFERENCES = {
    "sidebars.js": (
        "governance/governed-llm-reconstructive-search",
        "governance/governed-llm-activation-map",
        "governance/governed-llm-site-verification",
        "governance/governed-llm-deployment-status",
    ),
    "docusaurus.config.js": (
        "/governance/governed-llm-activation-map",
        "Governed LLM",
    ),
    "README.md": (
        "docs/governance/governed-llm-reconstructive-search.md",
        "docs/governance/governed-llm-activation-map.md",
    ),
}


def main() -> int:
    missing = []
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            missing.append("missing file: {}".format(relative_path))

    for relative_path, needles in REQUIRED_REFERENCES.items():
        path = ROOT / relative_path
        if not path.exists():
            missing.append("missing reference file: {}".format(relative_path))
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                missing.append("missing reference in {}: {}".format(relative_path, needle))

    if missing:
        for item in missing:
            print("GOVERNED LLM PAGES: FAIL - {}".format(item))
        return 1

    print("GOVERNED LLM PAGES: PASS - docs and navigation references present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
