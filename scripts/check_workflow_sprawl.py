#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DIR = ROOT / ".github" / "workflows"
MIRROR_DIR = ROOT / "iosnoperiod" / "github" / "workflows"
CANONICAL = "validate-chain-continuation.yml"
MIGRATED_CHECKS = [
    "scripts/check_correctability_projection.py",
    "scripts/check_nist_ai_rmf_source_receipt.py",
    "scripts/check_governance_observatory_release_awareness.py",
    "scripts/check_stegclaw_release_awareness.py",
]


def names(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.glob("*.yml")) + sorted(item.name for item in path.glob("*.yaml"))


def run_migrated_check(relative_path: str) -> tuple[int, str]:
    path = ROOT / relative_path
    if not path.exists():
        return 127, f"missing migrated validator: {relative_path}"
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout.rstrip()


def main() -> int:
    failures: list[str] = []
    active = names(ACTIVE_DIR)
    mirror = names(MIRROR_DIR)

    if active != [CANONICAL]:
        failures.append(f"active workflows must equal [{CANONICAL}], found {active}")
    if mirror != [CANONICAL]:
        failures.append(f"iOS mirror workflows must equal [{CANONICAL}], found {mirror}")

    migrated_results: list[tuple[str, int]] = []
    for relative_path in MIGRATED_CHECKS:
        return_code, output = run_migrated_check(relative_path)
        migrated_results.append((relative_path, return_code))
        if output:
            print(output)
        if return_code != 0:
            failures.append(f"migrated single-workflow validator failed: {relative_path}")

    print("WORKFLOW SPRAWL:", "FAIL" if failures else "PASS")
    print(f"migrated_validators={len(migrated_results)}")
    for relative_path, return_code in migrated_results:
        print(f"- {relative_path}: {'PASS' if return_code == 0 else 'FAIL'}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
