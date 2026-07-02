#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "scripts/check_repo_standards_all.py"],
    [sys.executable, "scripts/check_repo_standards_validation_receipt_template.py"],
]


def main() -> int:
    for command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, text=True)
        if result.returncode != 0:
            print("REPO STANDARDS RELEASE READY: FAIL")
            return result.returncode
    print("REPO STANDARDS RELEASE READY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
