#!/usr/bin/env python3
"""Verify governed LLM public pages, contracts, and validation are present."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "docs/governance/governed-llm-reconstructive-search.md",
    "docs/governance/governed-llm-activation-map.md",
    "docs/governance/governed-llm-site-verification.md",
    "docs/governance/governed-llm-deployment-status.md",
    "docs/governance/governed-llm-archive-handoff.md",
    "docs/governance/llm-consciousness-model-system-boundary.md",
    "docs/governance/SYSTEM_BOUNDARY_MIRROR_HANDOFF.md",
    "static/governance/system-boundary-declaration.schema.v0.1.json",
    "static/governance/system-boundary-declaration.example.v0.1.json",
    "static/governance/fixtures/system-boundary-declaration-cases.v0.1.json",
    "scripts/check_system_boundary_declaration.py",
)
REQUIRED_REFERENCES = {
    "sidebars.js": (
        "governance/governed-llm-reconstructive-search",
        "governance/governed-llm-activation-map",
        "governance/governed-llm-site-verification",
        "governance/governed-llm-deployment-status",
        "governance/governed-llm-archive-handoff",
    ),
    "docusaurus.config.js": (
        "/governance/governed-llm-activation-map",
        "Governed LLM",
    ),
    "README.md": (
        "docs/governance/governed-llm-reconstructive-search.md",
        "docs/governance/governed-llm-activation-map.md",
    ),
    "docs/governance/llm-consciousness-model-system-boundary.md": (
        "system-boundary-declaration.schema.v0.1.json",
        "system-boundary-declaration.example.v0.1.json",
        "check_system_boundary_declaration.py",
    ),
}


def main() -> int:
    missing: list[str] = []
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

    checker = ROOT / "scripts/check_system_boundary_declaration.py"
    result = subprocess.run(
        [sys.executable, str(checker)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        print("GOVERNED LLM PAGES: FAIL - system-boundary contract validation failed")
        return result.returncode

    print("GOVERNED LLM PAGES: PASS - docs, contracts, fixtures, and references present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
