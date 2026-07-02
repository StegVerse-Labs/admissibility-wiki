#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    [sys.executable, "scripts/check_repo_standards_integration.py"],
    [sys.executable, "scripts/check_repo_standards_downstream_activation.py"],
]


def main() -> int:
    for command in CHECKS:
        result = subprocess.run(command, cwd=ROOT, text=True)
        if result.returncode != 0:
            print(f"REPO STANDARDS BUNDLE: FAIL - {' '.join(command)}")
            return result.returncode
    print("REPO STANDARDS BUNDLE: PASS - integration and downstream activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
