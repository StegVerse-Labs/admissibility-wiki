#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "repo-standards-integration.md"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"

REQUIRED_PAGE_SNIPPETS = [
    "StegVerse-Labs/repo-standards",
    "Release-Gated Reference Rule",
    "PENDING_UPSTREAM_TAG_RELEASE",
    "repository validation equals admissibility",
]

REQUIRED_SIDEBAR_SNIPPET = "governance/repo-standards-integration"
REQUIRED_HANDOFF_SNIPPETS = [
    "repo-standards-integration-pending-release",
    "docs/governance/repo-standards-integration.md",
    "UPSTREAM_TAG_RELEASE_PENDING_OUTSIDE_CONNECTOR",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_snippets(label: str, text: str, snippets: list[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} missing: {joined}")


def main() -> int:
    page = require_file(PAGE)
    sidebar = require_file(SIDEBAR)
    handoff = require_file(HANDOFF)

    require_snippets("page", page, REQUIRED_PAGE_SNIPPETS)
    require_snippets("sidebar", sidebar, [REQUIRED_SIDEBAR_SNIPPET])
    require_snippets("handoff", handoff, REQUIRED_HANDOFF_SNIPPETS)

    print("REPO STANDARDS INTEGRATION: PASS - page, sidebar, and handoff references present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
