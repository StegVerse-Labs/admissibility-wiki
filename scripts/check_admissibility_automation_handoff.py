#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "ADMISSIBILITY_AUTOMATION_HANDOFF.md"
MESH_CHECK = ROOT / "scripts" / "check_documentation_mesh_status.py"
REQUIRED = (
    "scripts/check_ios_workflow_mirror_status.py",
    "static/status/ios-workflow-mirror-status.json",
    "validate:ios-workflow-mirror",
    "canonical workflow remains source of truth",
)


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("missing ADMISSIBILITY_AUTOMATION_HANDOFF.md")
    else:
        text = HANDOFF.read_text(encoding="utf-8")
        failures.extend(f"missing marker: {marker}" for marker in REQUIRED if marker not in text)

    if not MESH_CHECK.exists():
        failures.append("missing scripts/check_documentation_mesh_status.py")
    else:
        result = subprocess.run(
            [sys.executable, str(MESH_CHECK)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(result.stdout.rstrip())
        if result.returncode != 0:
            failures.append("documentation mesh validation failed")

    if failures:
        print("ADMISSIBILITY AUTOMATION HANDOFF: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ADMISSIBILITY AUTOMATION HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
