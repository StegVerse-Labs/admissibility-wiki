#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "governance" / "repo-standards-validation-runbook.md"
SIDEBAR = ROOT / "sidebars.js"

REQUIRED_RUNBOOK = [
    "Repo Standards Validation Runbook",
    "python scripts/check_repo_standards_bundle.py",
    "READY_FOR_LOCAL_VALIDATION",
]

REQUIRED_SIDEBAR = "governance/repo-standards-validation-runbook"


def read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"RUNBOOK: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    runbook = read(RUNBOOK)
    sidebar = read(SIDEBAR)
    missing = [item for item in REQUIRED_RUNBOOK if item not in runbook]
    if missing:
        raise SystemExit(f"RUNBOOK: FAIL - missing runbook text: {', '.join(missing)}")
    if REQUIRED_SIDEBAR not in sidebar:
        raise SystemExit("RUNBOOK: FAIL - sidebar entry missing")
    print("RUNBOOK: PASS - validation runbook and sidebar entry present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
