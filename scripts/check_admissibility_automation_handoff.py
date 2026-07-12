#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "ADMISSIBILITY_AUTOMATION_HANDOFF.md"
MESH_CHECK = ROOT / "scripts" / "check_documentation_mesh_status.py"
RUN_RECEIPT_CHECK = ROOT / "scripts" / "check_automated_transition_run_receipt.py"
CONCEPTUAL_INHERITANCE_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_claims.py"
CONCEPTUAL_INHERITANCE_STATUS_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_status.py"
REQUIRED = (
    "scripts/check_ios_workflow_mirror_status.py",
    "static/status/ios-workflow-mirror-status.json",
    "validate:ios-workflow-mirror",
    "canonical workflow remains source of truth",
    "schemas/automated-transition-run-receipt.schema.json",
    "examples/automated-transition-run-receipt.json",
    "Master-Records",
)


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return

    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout.rstrip())
    if result.returncode != 0:
        failures.append(f"{label} validation failed")


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("missing ADMISSIBILITY_AUTOMATION_HANDOFF.md")
    else:
        text = HANDOFF.read_text(encoding="utf-8")
        failures.extend(f"missing marker: {marker}" for marker in REQUIRED if marker not in text)

    run_check(MESH_CHECK, "documentation mesh", failures)
    run_check(RUN_RECEIPT_CHECK, "automated transition run receipt", failures)
    run_check(CONCEPTUAL_INHERITANCE_CHECK, "conceptual inheritance claims", failures)
    run_check(
        CONCEPTUAL_INHERITANCE_STATUS_CHECK,
        "conceptual inheritance activation status",
        failures,
    )

    if failures:
        print("ADMISSIBILITY AUTOMATION HANDOFF: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ADMISSIBILITY AUTOMATION HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
