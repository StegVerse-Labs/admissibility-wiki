#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DIR = ROOT / ".github" / "workflows"
MIRROR_DIR = ROOT / "iosnoperiod" / "github" / "workflows"
CANONICAL = "validate-chain-continuation.yml"


def names(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.glob("*.yml")) + sorted(item.name for item in path.glob("*.yaml"))


def main() -> int:
    failures: list[str] = []
    active = names(ACTIVE_DIR)
    mirror = names(MIRROR_DIR)

    if active != [CANONICAL]:
        failures.append(f"active workflows must equal [{CANONICAL}], found {active}")
    if mirror != [CANONICAL]:
        failures.append(f"iOS mirror workflows must equal [{CANONICAL}], found {mirror}")

    print("WORKFLOW SPRAWL:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
