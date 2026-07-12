#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
PINNED_RUNNER = ROOT / "scripts" / "run_pinned_opa_ci_capture.py"
INDEPENDENT_RUNNER = ROOT / "scripts" / "run_independent_opa_ci_replay.py"
SUMMARY_SCRIPT = ROOT / "scripts" / "summarize_opa_evidence_pipeline.py"
GENERATED_VALIDATOR = ROOT / "scripts" / "validate_opa_capture_artifacts.py"
RUNBOOK = ROOT / "docs" / "external-frameworks" / "opa-observation-capture-runbook.md"
POLICY = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "policy.rego"
ALLOW_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-allow.json"
DENY_INPUT = ROOT / "docs" / "external-frameworks" / "capture" / "opa" / "input-deny.json"
FIXTURE = ROOT / "docs" / "external-frameworks" / "fixtures" / "opa-benchmark-fixture.v0.1.json"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
WORKFLOW_MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"


def normalized_workflow_text(text: str) -> str:
    return "\n".join(text.splitlines())


def main() -> int:
    failures: list[str] = []
    required_paths = [
        SCRIPT,
        PINNED_RUNNER,
        INDEPENDENT_RUNNER,
        SUMMARY_SCRIPT,
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

    sources = {
        "capture script": SCRIPT.read_text(encoding="utf-8"),
        "pinned runner": PINNED_RUNNER.read_text(encoding="utf-8"),
        "independent runner": INDEPENDENT_RUNNER.read_text(encoding="utf-8"),
        "pipeline summary": SUMMARY_SCRIPT.read_text(encoding="utf-8"),
        "generated artifact validator": GENERATED_VALIDATOR.read_text(encoding="utf-8"),
    }
    for label, source in sources.items():
        try:
            ast.parse(source)
        except SyntaxError as exc:
            failures.append(f"{label} syntax error: {exc}")

    for input_path in [ALLOW_INPUT, DENY_INPUT]:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        for key in ["actor", "action", "resource", "approval"]:
            if key not in payload:
                failures.append(f"input missing {key}: {input_path.relative_to(ROOT)}")

    phrase_sets = {
        "capture script": [
            '"capture_state": "captured_unverified"',
            '"opa_decision_is_execution_authority": False',
            '"capture_is_compatibility_proof": False',
            '"policy_sha256"',
            '"stdout_sha256"',
            '"replay"',
            '"limitations"',
        ],
        "pinned runner": [
            'OPA_VERSION = "v1.0.0"',
            "CHECKSUM_URL",
            '"replay_confirmed_same_environment"',
            '"same_environment_replay_is_independent_replay": False',
            '"runtime_binary_sha256"',
            '"github_run_id"',
        ],
        "independent runner": [
            '"replay_confirmed_independent_environment"',
            '"fresh_runner_job": True',
            '"independent_organization_or_provider": False',
            '"independent_runner_is_independent_implementation": False',
            '"independent_runner_is_independent_authority": False',
            "summarize_opa_evidence_pipeline.py",
            "opa-evidence-pipeline-status.json",
        ],
        "pipeline summary": [
            '"artifact_type": "external_framework_evidence_pipeline_status"',
            '"fresh_runner_replay_confirmed"',
            '"independent_implementation_or_provider_review": "not_performed"',
            '"compatibility_state": "not_claimed"',
            '"pipeline_summary_is_execution_authority": False',
            '"matching_outputs_are_compatibility_proof": False',
        ],
        "generated artifact validator": [
            '"capture_state": "captured_unverified"',
            '"independent_environment_replay_state": "not_performed"',
            '"compatibility_state": "not_claimed"',
            '"same_environment_replay_is_independent_replay": False',
            '"validation_failures"',
        ],
    }
    for label, phrases in phrase_sets.items():
        for phrase in phrases:
            if phrase not in sources[label]:
                failures.append(f"{label} missing phrase: {phrase}")

    runbook = RUNBOOK.read_text(encoding="utf-8")
    for phrase in [
        "OPA ALLOW != execution authority",
        "single capture != replayability",
        "capture_state: captured_unverified",
        "Current authority and admissibility must still be reconstructed",
    ]:
        if phrase not in runbook:
            failures.append(f"runbook missing phrase: {phrase}")

    policy = POLICY.read_text(encoding="utf-8")
    for phrase in ["default allow := false", 'input.action == "read"', "test material only"]:
        if phrase not in policy:
            failures.append(f"policy missing phrase: {phrase}")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    workflow_mirror = WORKFLOW_MIRROR.read_text(encoding="utf-8")
    for phrase in [
        "capture-opa-evidence:",
        "replay-opa-fresh-runner:",
        "python scripts/run_pinned_opa_ci_capture.py",
        "python scripts/validate_opa_capture_artifacts.py",
        "python scripts/run_independent_opa_ci_replay.py",
        "actions/download-artifact@v4",
        "opa-pinned-capture-replay",
        "opa-fresh-runner-replay",
        "continue-on-error: true",
    ]:
        if phrase not in workflow:
            failures.append(f"canonical workflow missing phrase: {phrase}")

    if normalized_workflow_text(workflow) != normalized_workflow_text(workflow_mirror):
        failures.append("canonical workflow and iOS workflow mirror differ")

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
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
