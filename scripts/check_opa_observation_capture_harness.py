#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
RUNBOOK = ROOT / "docs" / "external-frameworks" / "opa-observation-capture-runbook.md"
POLICY = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "policy.rego"
ALLOW_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-allow.json"
DENY_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-deny.json"
FIXTURE = ROOT / "docs" / "external-frameworks" / "fixtures" / "opa-benchmark-fixture.v0.1.json"


def main() -> int:
    failures: list[str] = []
    for path in [SCRIPT, RUNBOOK, POLICY, ALLOW_INPUT, DENY_INPUT, FIXTURE]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("OPA OBSERVATION CAPTURE HARNESS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    script_text = SCRIPT.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    try:
        ast.parse(script_text)
    except SyntaxError as exc:
        failures.append(f"capture script syntax error: {exc}")

    for input_path in [ALLOW_INPUT, DENY_INPUT]:
        try:
            payload = json.loads(input_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON {input_path.relative_to(ROOT)}: {exc}")
            continue
        for key in ["actor", "action", "resource", "approval"]:
            if key not in payload:
                failures.append(f"input missing {key}: {input_path.relative_to(ROOT)}")

    required_script_phrases = [
        '"capture_state": "captured_unverified"',
        '"opa_decision_is_execution_authority": False',
        '"capture_is_compatibility_proof": False',
        '"policy_sha256"',
        '"stdout_sha256"',
        '"replay"',
        '"limitations"',
    ]
    for phrase in required_script_phrases:
        if phrase not in script_text:
            failures.append(f"capture script missing phrase: {phrase}")

    for phrase in [
        "OPA ALLOW != execution authority",
        "single capture != replayability",
        "capture_state: captured_unverified",
        "Current authority and admissibility must still be reconstructed",
    ]:
        if phrase not in runbook:
            failures.append(f"runbook missing phrase: {phrase}")

    for phrase in ["default allow := false", 'input.action == "read"', "test material only"]:
        if phrase not in policy:
            failures.append(f"policy missing phrase: {phrase}")

    if fixture.get("framework_id") != "opa":
        failures.append("OPA fixture framework id mismatch")
    if not fixture.get("fixture_cases"):
        failures.append("OPA fixture missing cases")

    print("OPA OBSERVATION CAPTURE HARNESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
