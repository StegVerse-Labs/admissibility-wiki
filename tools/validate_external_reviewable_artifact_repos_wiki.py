#!/usr/bin/env python3
"""Validate downstream wiki visibility for external reviewable artifact repos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REQUIRED_FILES = [
    "docs/standards/external-reviewable-artifact-repos.md",
    "docs/standards/external-reviewable-artifact-repos-status.md",
]

REQUIRED_TEXT = {
    "docs/standards/external-reviewable-artifact-repos.md": [
        "StegVerse-Labs/repo-standards",
        "registries/external-reviewable-artifact-repos.json",
        "standards/external-reviewable-artifact-repos.md",
        "StegVerse-Labs/Site: docs/standards/external-reviewable-artifact-repos.md",
        "StegVerse-Labs/soil-to-structure-matrix",
        "downstream visibility only",
    ],
    "docs/standards/external-reviewable-artifact-repos-status.md": [
        "StegVerse-Labs/repo-standards",
        "registries/external-reviewable-artifact-repos.json",
        "StegVerse-Labs/Site: docs/standards/external-reviewable-artifact-repos.md",
        "informational only",
    ],
}


def file_state(path_text: str) -> dict[str, Any]:
    path = ROOT / path_text
    errors: list[str] = []
    if not path.exists():
        errors.append("missing_file")
    else:
        text = path.read_text(encoding="utf-8")
        for required in REQUIRED_TEXT.get(path_text, []):
            if required not in text:
                errors.append("missing_text=" + required)
    return {
        "path": path_text,
        "present": path.exists(),
        "decision": "ALLOW" if not errors else "DENY",
        "errors": errors,
    }


def main() -> int:
    results = [file_state(path) for path in REQUIRED_FILES]
    failed = [item for item in results if item["decision"] != "ALLOW"]
    report = {
        "goal": "wiki registry backed standards visibility validation",
        "decision": "ALLOW" if not failed else "DENY",
        "results": results,
        "boundary": "Downstream wiki visibility validation only; repo-standards remains authoritative.",
    }
    out_path = REPORT_DIR / "external_reviewable_artifact_repos_wiki_validation.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{report['decision']} external_reviewable_artifact_repos_wiki_validation report={out_path.relative_to(ROOT)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
