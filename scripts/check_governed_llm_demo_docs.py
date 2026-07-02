#!/usr/bin/env python3
"""Validate governed LLM demo docs and navigation references."""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/governance/governed-llm-demo-overview.md",
    "docs/governance/governed-llm-demo-verification.md",
]
SIDEBAR_REFS = ["governance/governed-llm-demo-overview", "governance/governed-llm-demo-verification"]

def fail(msg: str) -> int:
    print(f"GOVERNED LLM DEMO DOCS: FAIL - {msg}"); return 1

def main() -> int:
    for rel in REQUIRED:
        if not (ROOT / rel).exists(): return fail(f"missing required file: {rel}")
    sidebar = (ROOT / "sidebars.js").read_text(encoding="utf-8")
    for ref in SIDEBAR_REFS:
        if ref not in sidebar: return fail(f"sidebars.js missing reference: {ref}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "governed-llm-demo-overview" not in readme: return fail("README missing demo overview reference")
    print("GOVERNED LLM DEMO DOCS: PASS - demo pages and navigation references present")
    return 0
if __name__ == "__main__": raise SystemExit(main())
