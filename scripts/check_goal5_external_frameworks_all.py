#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    "scripts/check_runtime_governance_benchmark_suite.py",
    "scripts/check_morrison_runtime_benchmark_fixtures.py",
    "scripts/check_external_framework_reports.py",
    "scripts/check_external_framework_benchmark_mappings.py",
    "scripts/check_external_framework_benchmark_fixtures.py",
    "scripts/check_expanded_external_framework_intake.py",
    "scripts/check_external_framework_intake_promotion.py",
    "scripts/check_goal5_external_blockers.py",
    "scripts/check_goal5_release_readiness.py",
    "scripts/check_external_frameworks_index.py",
]


def main() -> int:
    failures: list[str] = []

    print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE CHECK")
    print("=" * 52)

    for check in CHECKS:
        path = ROOT / check
        if not path.exists():
            print(f"MISSING: {check}")
            failures.append(check)
            continue

        print(f"RUN: {check}")
        result = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True)
        if result.returncode != 0:
            failures.append(check)

    print("=" * 52)
    if failures:
        print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: PASS")
    print("release_readiness: structure_ready_external_dependencies_open")
    return 0


if __name__ == "__main__":
    sys.exit(main())
