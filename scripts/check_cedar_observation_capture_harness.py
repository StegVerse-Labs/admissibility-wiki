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
    ROOT / "scripts" / "validate_cedar_capture_artifacts.py",
    ROOT / "scripts" / "summarize_cedar_evidence_pipeline.py",
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

    capture_script = FILES[4].read_text(encoding="utf-8")
    validator = FILES[5].read_text(encoding="utf-8")
    summary = FILES[6].read_text(encoding="utf-8")
    for label, source in [
        ("capture script", capture_script),
        ("artifact validator", validator),
        ("pipeline summary", summary),
    ]:
        try:
            ast.parse(source)
        except SyntaxError as exc:
            failures.append(f"{label} syntax error: {exc}")

    capture_phrases = [
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
    ]
    for phrase in capture_phrases:
        if phrase not in capture_script:
            failures.append(f"capture script missing phrase: {phrase}")

    validator_phrases = [
        '"capture_state": "captured_unverified"',
        '"same_environment_replay_state": "not_performed"',
        '"fresh_runner_replay_state": "not_performed"',
        '"compatibility_state": "not_claimed"',
        '"standing_state": "not_created"',
        '"execution_authority_state": "not_created"',
        '"implementation_identification_is_certification": False',
    ]
    for phrase in validator_phrases:
        if phrase not in validator:
            failures.append(f"artifact validator missing phrase: {phrase}")

    summary_phrases = [
        '"pipeline_state": pipeline_state',
        '"independent_implementation_or_provider_review": "not_performed"',
        '"implementation_selection_is_certification": False',
        '"matching_decisions_create_stegverse_standing": False',
        '"No Cedar implementation is selected or pinned by this summary."',
    ]
    for phrase in summary_phrases:
        if phrase not in summary:
            failures.append(f"pipeline summary missing phrase: {phrase}")

    runbook = FILES[3].read_text(encoding="utf-8")
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
