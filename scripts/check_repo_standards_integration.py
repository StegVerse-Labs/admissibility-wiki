#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "repo-standards-integration.md"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
STATUS = ROOT / "static" / "status" / "repo-standards-integration-status.json"
QUEUE = ROOT / "static" / "status" / "repo-standards-integration-release-update-queue.json"

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


def read_json(path: Path, label: str) -> dict:
    raw = require_file(path)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} JSON root must be an object")
    return data


def require_snippets(label: str, text: str, snippets: list[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} missing: {joined}")


def require_status() -> None:
    data = read_json(STATUS, "status")
    expected = {
        "status_id": "repo-standards-integration-status",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-pending-release",
        "status": "PENDING_UPSTREAM_TAG_RELEASE",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - status {key} expected {value!r}, got {data.get(key)!r}"
            )

    local = data.get("local_artifacts", {})
    if local.get("page") != "docs/governance/repo-standards-integration.md":
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - status local_artifacts.page is incorrect")
    if local.get("validator") != "scripts/check_repo_standards_integration.py":
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - status local_artifacts.validator is incorrect")


def require_queue() -> None:
    data = read_json(QUEUE, "queue")
    expected = {
        "queue_id": "repo-standards-integration-release-update-queue",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "status": "PENDING_UPSTREAM_TAG_RELEASE",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - queue {key} expected {value!r}, got {data.get(key)!r}"
            )
    pending = data.get("pending_updates")
    if not isinstance(pending, list) or len(pending) < 3:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - queue must define at least three pending updates")
    targets = {item.get("target") for item in pending if isinstance(item, dict)}
    required_targets = {
        "docs/governance/repo-standards-integration.md",
        "static/status/repo-standards-integration-status.json",
        "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    }
    missing = sorted(required_targets - targets)
    if missing:
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - queue missing targets: {', '.join(missing)}")


def main() -> int:
    page = require_file(PAGE)
    sidebar = require_file(SIDEBAR)
    handoff = require_file(HANDOFF)

    require_snippets("page", page, REQUIRED_PAGE_SNIPPETS)
    require_snippets("sidebar", sidebar, [REQUIRED_SIDEBAR_SNIPPET])
    require_snippets("handoff", handoff, REQUIRED_HANDOFF_SNIPPETS)
    require_status()
    require_queue()

    print("REPO STANDARDS INTEGRATION: PASS - page, sidebar, handoff, status artifact, and release-update queue present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
