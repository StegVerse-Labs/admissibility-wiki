#!/usr/bin/env python3
"""Validate admissibility wiki local standards index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

INDEX_PATH = ROOT / "docs" / "standards" / "README.md"
REQUIRED_TEXT = [
    "docs/standards/registry_backed_visibility_pattern.md",
    "docs/standards/registry_backed_visibility_pattern_status.md",
    "python tools/registry_backed_visibility_pattern_automation.py",
    "docs/standards/external-reviewable-artifact-repos.md",
    "docs/standards/external-reviewable-artifact-repos-status.md",
    "python tools/external_reviewable_artifact_repos_wiki_automation.py",
    "downstream visibility surface",
]


def main() -> int:
    errors: list[str] = []
    if not INDEX_PATH.exists():
        errors.append("missing_index")
        text = ""
    else:
        text = INDEX_PATH.read_text(encoding="utf-8")
        for required in REQUIRED_TEXT:
            if required not in text:
                errors.append("missing_text=" + required)
    report = {
        "goal": "local standards index validation",
        "decision": "ALLOW" if not errors else "DENY",
        "index": str(INDEX_PATH.relative_to(ROOT)),
        "errors": errors,
        "boundary": "Standards index validation only; does not change source registry scope or standards authority.",
    }
    out_path = REPORT_DIR / "standards_index_validation.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{report['decision']} standards_index_validation report={out_path.relative_to(ROOT)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
