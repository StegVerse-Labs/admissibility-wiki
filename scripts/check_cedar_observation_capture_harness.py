#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "docs" / "external-frameworks" / "capture" / "cedar" / "policy.cedar",
    ROOT / "docs" / "external-frameworks" / "capture" / "cedar" / "request-allow.json",
    ROOT / "docs" / "external-frameworks" / "capture" / "cedar" / "request-deny.json",
    ROOT / "docs" / "external-frameworks" / "cedar-observation-capture-runbook.md",
    ROOT / "scripts" / "capture_cedar_observation.py",
]


def main() -> int:
    failures: list[str] = []
    for path in FILES:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("CEDAR OBSERVATION CAPTURE HARNESS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    script_path = FILES[-1]
    script = script_path.read_text(encoding="utf-8")
    try:
        ast.parse(script)
    except SyntaxError as exc:
        failures.append(f"capture script syntax error: {exc}")

    for phrase in [
        '"capture_state": "captured_unverified"',
        '"cedar_decision_is_execution_authority": False',
        '"capture_is_compatibility_proof": False',
        '"current_delegation_attached": False',
        '"commit_time_authority_reconstructed": False',
        '"policy_sha256"',
        '"request_sha256"',
        '"stdout_sha256"',
        '"stderr_sha256"',
        '"version_command"',
        '"evaluate_command"',
        '"replay"',
    ]:
        if phrase not in script:
            failures.append(f"capture script missing phrase: {phrase}")

    runbook = FILES[-2].read_text(encoding="utf-8")
    for phrase in [
        "Cedar PERMIT != execution authority",
        "single run != replayability",
        "implementation-neutral",
        "captured_unverified",
    ]:
        if phrase not in runbook:
            failures.append(f"runbook missing phrase: {phrase}")

    policy = FILES[0].read_text(encoding="utf-8")
    if 'User::"alice"' not in policy or 'Action::"read"' not in policy:
        failures.append("policy does not preserve deterministic allow subject and action")

    print("CEDAR OBSERVATION CAPTURE HARNESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
