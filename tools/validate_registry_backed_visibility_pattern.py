#!/usr/bin/env python3
"""Validate registry-backed visibility pattern documentation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REQUIRED_FILES = [
    "docs/standards/registry_backed_visibility_pattern.md",
    "docs/standards/registry_backed_visibility_pattern_status.md",
]

REQUIRED_TEXT = {
    "docs/standards/registry_backed_visibility_pattern.md": [
        "authoritative source repository",
        "authoritative standard path",
        "authoritative registry path",
        "display-only",
        "must not become the registry authority",
    ],
    "docs/standards/registry_backed_visibility_pattern_status.md": [
        "docs/standards/registry_backed_visibility_pattern.md",
        "docs/standards/external-reviewable-artifact-repos.md",
        "python tools/external_reviewable_artifact_repos_wiki_automation.py",
        "downstream visibility surface",
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
        "goal": "registry backed visibility pattern validation",
        "decision": "ALLOW" if not failed else "DENY",
        "results": results,
        "boundary": "Pattern validation only; does not change source registry scope or standards authority.",
    }
    out_path = REPORT_DIR / "registry_backed_visibility_pattern_validation.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{report['decision']} registry_backed_visibility_pattern_validation report={out_path.relative_to(ROOT)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
