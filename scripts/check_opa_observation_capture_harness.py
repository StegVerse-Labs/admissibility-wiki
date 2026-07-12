#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
PINNED_RUNNER = ROOT / "scripts" / "run_pinned_opa_ci_capture.py"
GENERATED_VALIDATOR = ROOT / "scripts" / "validate_opa_capture_artifacts.py"
RUNBOOK = ROOT / "docs" / "external-frameworks" / "opa-observation-capture-runbook.md"
POLICY = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "policy.rego"
ALLOW_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-allow.json"
DENY_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-deny.json"
FIXTURE = ROOT / "docs" / "external-frameworks" / "fixtures" / "opa-benchmark-fixture.v0.1.json"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
WORKFLOW_MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"


def normalized_workflow_text(text: str) -> str:
    """Compare mirrored workflows by exact logical lines, ignoring only line-ending form and final newline."""
    return "\n".join(text.splitlines())


def main() -> int:
    failures: list[str] = []
    required_paths = [
        SCRIPT,
        PINNED_RUNNER,
        GENERATED_VALIDATOR,
        RUNBOOK,
        POLICY,
        ALLOW_INPUT,
        DENY_INPUT,
        FIXTURE,
        WORKFLOW,
        WORKFLOW_MIRROR,
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("OPA OBSERVATION CAPTURE HARNESS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    script_text = SCRIPT.read_text(encoding="utf-8")
    pinned_runner_text = PINNED_RUNNER.read_text(encoding="utf-8")
    generated_validator_text = GENERATED_VALIDATOR.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    workflow = WORKFLOW.read_text(encoding="utf-8")
    workflow_mirror = WORKFLOW_MIRROR.read_text(encoding="utf-8")

    for label, source in [
        ("capture script", script_text),
        ("pinned runner", pinned_runner_text),
        ("generated artifact validator", generated_validator_text),
    ]:
        try:
            ast.parse(source)
        except SyntaxError as exc:
            failures.append(f"{label} syntax error: {exc}")

    for input_path in [ALLOW_INPUT, DENY_INPUT]:
        try:
            payload = json.loads(input_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON {input_path.relative_to(ROOT)}: {exc}")
            continue
        for key in ["actor", "action", "resource", "approval"]:
            if key not in payload:
                failures.append(f"input missing {key}: {input_path.relative_to(ROOT)}")

    for phrase in [
        '"capture_state": "captured_unverified"',
        '"opa_decision_is_execution_authority": False',
        '"capture_is_compatibility_proof": False',
        '"policy_sha256"',
        '"stdout_sha256"',
        '"replay"',
        '"limitations"',
    ]:
        if phrase not in script_text:
            failures.append(f"capture script missing phrase: {phrase}")

    for phrase in [
        'OPA_VERSION = "v1.0.0"',
        'CHECKSUM_URL',
        '"replay_confirmed_same_environment"',
        '"same_environment_replay_is_independent_replay": False',
        '"runtime_binary_sha256"',
        '"github_run_id"',
    ]:
        if phrase not in pinned_runner_text:
            failures.append(f"pinned runner missing phrase: {phrase}")

    for phrase in [
        '"capture_state": "captured_unverified"',
        '"independent_environment_replay_state": "not_performed"',
        '"compatibility_state": "not_claimed"',
        '"same_environment_replay_is_independent_replay": False',
        '"validation_failures"',
    ]:
        if phrase not in generated_validator_text:
            failures.append(f"generated artifact validator missing phrase: {phrase}")

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

    for phrase in [
        "capture-opa-evidence:",
        "python scripts/run_pinned_opa_ci_capture.py",
        "python scripts/validate_opa_capture_artifacts.py",
        "opa-pinned-capture-replay",
        "Upload OPA capture, replay, and validation receipts",
        "continue-on-error: true",
    ]:
        if phrase not in workflow:
            failures.append(f"canonical workflow missing phrase: {phrase}")

    if normalized_workflow_text(workflow) != normalized_workflow_text(workflow_mirror):
        failures.append("canonical workflow and iOS workflow mirror differ")

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
