#!/usr/bin/env python3
"""Run downstream wiki visibility validation for external reviewable artifact repos."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "tools/validate_external_reviewable_artifact_repos_wiki.py"],
]


def run(command: list[str]) -> int:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return result.returncode


def main() -> int:
    failures = []
    for command in COMMANDS:
        code = run(command)
        if code != 0:
            failures.append((command, code))
    if failures:
        print("DENY external_reviewable_artifact_repos_wiki_automation_failed")
        for command, code in failures:
            print(f"- exit={code} command={' '.join(command)}")
        return 1
    print("ALLOW external_reviewable_artifact_repos_wiki_automation_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
