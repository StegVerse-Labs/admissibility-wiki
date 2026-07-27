#!/usr/bin/env python3
"""Validate the bounded Conectrr ITC interoperability package.

This validator intentionally accepts the pre-execution pending state. It fails if
that state asserts completed testing, source mutation, authority inheritance, or
partial receipt of the required three-artifact source package.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.interoperability-test-profile.v1.json"
RESULT_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.interoperability-result.pending.v1.json"
SCHEMA_PATH = ROOT / "static/schemas/conectrr-itc-interoperability-result.schema.json"
INTAKE_PATH = ROOT / "docs/external-frameworks/conectrr-itc-interoperability-intake.md"
RECORD_PATH = ROOT / "static/data/framework-evaluations/conectrr-itc.json"

EXPECTED_DRIFT_CASES = {
    "EXPIRED_DELEGATION",
    "CHANGED_TARGET_SCOPE",
    "STALE_EVIDENCE",
    "CHANGED_POLICY_VERSION",
    "DEGRADED_RECOVERABILITY",
    "ACTOR_SUBSTITUTION",
    "TARGET_SUBSTITUTION",
    "SUPERSEDED_RECOMMENDATION",
    "CHANGED_DEPENDENCY_STATE",
    "INVALIDATED_SOURCE_REFERENCE",
}
EXPECTED_CHECKS = {
    "source-integrity",
    "specification-conformance",
    "prohibited-authority-semantics",
    "empty-field-fidelity",
    "independent-reconstruction",
    "independent-disposition",
    "replay-stability",
    "commit-time-authority-non-inheritance",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing required artifact: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"top-level JSON object required: {path.relative_to(ROOT)}")
    return value


def require_false_authority(authority: Any, label: str) -> None:
    if not isinstance(authority, dict):
        fail(f"{label} authority object is required")
    for field in ("certification", "execution", "custody", "endorsement"):
        if authority.get(field) is not False:
            fail(f"{label} must keep authority.{field}=false")


def main() -> None:
    for path in (SCHEMA_PATH, INTAKE_PATH, RECORD_PATH):
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")

    profile = load_json(PROFILE_PATH)
    result = load_json(RESULT_PATH)

    if profile.get("schema") != "conectrr_itc_interoperability_test_profile.v1":
        fail("unexpected test-profile schema")
    if profile.get("profile_id") != "conectrr-itc-first-interoperability-exercise":
        fail("unexpected test-profile id")
    if profile.get("authority_effect") != "NONE":
        fail("test profile must have no authority effect")

    package = profile.get("source_package")
    if not isinstance(package, dict):
        fail("source_package object is required")
    received_states = []
    for key in ("specification", "canonical_itc", "validation_report"):
        item = package.get(key)
        if not isinstance(item, dict) or item.get("required") is not True:
            fail(f"required source package member missing: {key}")
        received_states.append(item.get("received"))
    if any(received_states) and not all(received_states):
        fail("partial source-package receipt is not a runnable interoperability package")

    check_ids = {
        item.get("check_id")
        for item in profile.get("required_checks", [])
        if isinstance(item, dict)
    }
    if check_ids != EXPECTED_CHECKS:
        fail(f"required check set drift: {sorted(check_ids)}")

    drift_cases = set(profile.get("drift_cases", []))
    if drift_cases != EXPECTED_DRIFT_CASES:
        fail(f"profile drift-case set mismatch: {sorted(drift_cases)}")

    if result.get("schema") != "conectrr_itc_interoperability_result.v1":
        fail("unexpected result schema")
    if result.get("profile_id") != profile.get("profile_id"):
        fail("result/profile id mismatch")
    if result.get("source_mutated") is not False:
        fail("source mutation is prohibited")
    require_false_authority(result.get("authority"), "result")

    result_cases = {
        item.get("case")
        for item in result.get("drift_results", [])
        if isinstance(item, dict)
    }
    if result_cases != EXPECTED_DRIFT_CASES:
        fail(f"result drift-case set mismatch: {sorted(result_cases)}")

    pending = result.get("source_artifact_state") == "AWAITING_CANONICAL_SOURCE_ARTIFACTS"
    if pending:
        forbidden_progress = {
            "reconstruction": result.get("reconstruction"),
            "disposition": result.get("disposition"),
            "replay": result.get("replay"),
            "commit_time_non_inheritance": result.get("commit_time_non_inheritance"),
        }
        for field, value in forbidden_progress.items():
            if value != "NOT_RUN":
                fail(f"pending source state cannot assert {field}={value}")
        if result.get("source_hash_before") is not None or result.get("source_hash_after") is not None:
            fail("pending source state cannot assert canonical source hashes")
        for item in result.get("drift_results", []):
            if item.get("result") != "NOT_RUN":
                fail(f"pending source state cannot assert drift result for {item.get('case')}")
    else:
        if not all(received_states):
            fail("non-pending result requires all three source artifacts")
        before = result.get("source_hash_before")
        after = result.get("source_hash_after")
        if not before or before != after:
            fail("executed result requires identical pre/post immutable source hashes")

    intake = INTAKE_PATH.read_text(encoding="utf-8")
    for marker in (
        "non-authorizing",
        "AGREE",
        "DISAGREE",
        "DEFER",
        "ALLOW",
        "DENY",
        "FAIL-CLOSED",
    ):
        if marker not in intake:
            fail(f"intake page missing boundary marker: {marker}")

    print(f"OK: {PROFILE_PATH.relative_to(ROOT)}")
    print(f"OK: {RESULT_PATH.relative_to(ROOT)}")
    print(f"OK: {SCHEMA_PATH.relative_to(ROOT)}")
    print("conectrr_itc_source_package=AWAITING_CANONICAL_SOURCE_ARTIFACTS")
    print("conectrr_itc_authority_effect=NONE")
    print("conectrr_itc_source_mutation_allowed=false")
    print("conectrr_itc_validator=PASS")


if __name__ == "__main__":
    main()
