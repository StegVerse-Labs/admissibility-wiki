#!/usr/bin/env python3
"""Validate the bounded Conectrr ITC interoperability package.

This validator intentionally accepts the pre-execution pending state. It fails if
that state asserts completed testing, source mutation, authority inheritance,
partial receipt of the required three-artifact source package, a false claim of
canonical workflow observation, or invalid AGREE / DISAGREE / DEFER fixtures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.interoperability-test-profile.v1.json"
RESULT_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.interoperability-result.pending.v1.json"
SOURCE_RECEIPT_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.source-package-receipt.pending.v1.json"
DISPOSITION_FIXTURES_PATH = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.disposition-fixtures.v1.json"
SCHEMA_PATH = ROOT / "static/schemas/conectrr-itc-interoperability-result.schema.json"
INTAKE_PATH = ROOT / "docs/external-frameworks/conectrr-itc-interoperability-intake.md"
RECORD_PATH = ROOT / "static/data/framework-evaluations/conectrr-itc.json"
BINDING_STATUS_PATH = ROOT / "static/status/conectrr-itc-canonical-validation-binding-status.json"
AGGREGATE_PATH = ROOT / "scripts/check_admissibility_automation_handoff.py"
PACKAGE_PATH = ROOT / "package.json"

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
EXPECTED_DISPOSITIONS = {
    "AGREE": "conectrr-itc-agree",
    "DISAGREE": "conectrr-itc-disagree",
    "DEFER": "conectrr-itc-defer",
}
SOURCE_KEYS = ("specification", "canonical_itc", "validation_report")


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


def validate_source_receipt(receipt: dict[str, Any], profile: dict[str, Any]) -> list[bool]:
    if receipt.get("schema") != "conectrr_itc_source_package_receipt.v1":
        fail("unexpected Conectrr source-package receipt schema")
    if receipt.get("framework_id") != "conectrr-itc":
        fail("Conectrr source-package receipt framework mismatch")
    if receipt.get("source_mutation_allowed") is not False:
        fail("source-package receipt must prohibit source mutation")
    require_false_authority(receipt.get("authority"), "source receipt")

    artifacts = receipt.get("artifacts")
    profile_package = profile.get("source_package")
    if not isinstance(artifacts, dict) or not isinstance(profile_package, dict):
        fail("source artifacts and profile source_package objects are required")

    receipt_states: list[bool] = []
    for key in SOURCE_KEYS:
        item = artifacts.get(key)
        profile_item = profile_package.get(key)
        if not isinstance(item, dict) or item.get("required") is not True:
            fail(f"source receipt missing required artifact member: {key}")
        if not isinstance(profile_item, dict) or profile_item.get("required") is not True:
            fail(f"test profile missing required source package member: {key}")
        received = item.get("received")
        if received not in {True, False}:
            fail(f"source receipt received flag must be boolean: {key}")
        if received != profile_item.get("received"):
            fail(f"source receipt/profile receipt-state mismatch: {key}")
        receipt_states.append(received)
        if received:
            if not item.get("path") or not item.get("sha256") or not item.get("media_type"):
                fail(f"received artifact requires path, sha256, and media_type: {key}")
        else:
            for field in ("path", "sha256", "media_type"):
                if item.get(field) is not None:
                    fail(f"pending artifact cannot assert {field}: {key}")
    if artifacts["canonical_itc"].get("immutable") is not True:
        fail("canonical ITC must be explicitly immutable")
    if any(receipt_states) and not all(receipt_states):
        fail("partial source-package receipt is not runnable")

    complete = all(receipt_states)
    if receipt.get("package_complete") is not complete:
        fail("source receipt package_complete does not match artifact receipt state")
    if receipt.get("testing_authorized") is not complete:
        fail("testing_authorized must be false until the complete source package is present")
    if complete:
        if receipt.get("state") != "CANONICAL_SOURCE_PACKAGE_RECEIVED":
            fail("complete source package requires CANONICAL_SOURCE_PACKAGE_RECEIVED state")
        if not receipt.get("received_at") or not receipt.get("received_from"):
            fail("complete source package requires received_at and received_from")
    else:
        if receipt.get("state") != "AWAITING_CANONICAL_SOURCE_ARTIFACTS":
            fail("incomplete source package must remain awaiting canonical source artifacts")
        if receipt.get("received_at") is not None or receipt.get("received_from") is not None:
            fail("pending source receipt cannot assert receipt actor or time")
    return receipt_states


def validate_disposition_fixtures(fixtures_doc: dict[str, Any], profile: dict[str, Any], source_complete: bool) -> None:
    if fixtures_doc.get("schema") != "conectrr_itc_disposition_fixtures.v1":
        fail("unexpected Conectrr disposition-fixture schema")
    if fixtures_doc.get("profile_id") != profile.get("profile_id"):
        fail("disposition fixture/profile id mismatch")
    if fixtures_doc.get("source_mutation_allowed") is not False:
        fail("disposition fixtures must prohibit source mutation")

    expected_state = "CANONICAL_SOURCE_PACKAGE_RECEIVED" if source_complete else "AWAITING_CANONICAL_SOURCE_ARTIFACTS"
    if fixtures_doc.get("source_package_state") != expected_state:
        fail("disposition fixture source-package state mismatch")

    fixtures = fixtures_doc.get("fixtures")
    if not isinstance(fixtures, list) or len(fixtures) != len(EXPECTED_DISPOSITIONS):
        fail("exactly three Conectrr disposition fixtures are required")

    observed: dict[str, str] = {}
    for fixture in fixtures:
        if not isinstance(fixture, dict):
            fail("disposition fixture entries must be objects")
        disposition = fixture.get("disposition")
        fixture_id = fixture.get("fixture_id")
        if disposition not in EXPECTED_DISPOSITIONS:
            fail(f"unsupported disposition fixture: {disposition}")
        if fixture_id != EXPECTED_DISPOSITIONS[disposition]:
            fail(f"unexpected fixture id for {disposition}")
        if disposition in observed:
            fail(f"duplicate disposition fixture: {disposition}")
        observed[disposition] = fixture_id
        if not isinstance(fixture.get("reason"), str) or not fixture.get("reason").strip():
            fail(f"disposition fixture requires a reason: {disposition}")
        if fixture.get("commitment_candidate_created") is not False:
            fail(f"pending disposition fixture cannot create a Commitment Candidate: {disposition}")
        if fixture.get("spe_determination") != "NOT_RUN":
            fail(f"pending disposition fixture cannot assert an SPE determination: {disposition}")
        require_false_authority(fixture.get("authority"), f"{disposition} fixture")

        if not source_complete:
            if fixture.get("execution_state") != "NOT_RUN":
                fail(f"pending source package cannot execute disposition fixture: {disposition}")
            if fixture.get("source_hash") is not None:
                fail(f"pending source package cannot assert disposition source hash: {disposition}")
            if fixture.get("reconstruction_result") != "NOT_RUN":
                fail(f"pending source package cannot assert reconstruction: {disposition}")

    if set(observed) != set(EXPECTED_DISPOSITIONS):
        fail("AGREE, DISAGREE, and DEFER fixtures are all required")

    non_claims = fixtures_doc.get("non_claims")
    if not isinstance(non_claims, list):
        fail("disposition fixture non_claims array is required")
    required_non_claim_fragments = (
        "not an executed interoperability result",
        "agreement does not grant execution authority",
        "disagreement does not invalidate the canonical source",
        "deferral is not failure",
        "Commitment Candidate remains non-authorizing",
        "SPE must reconstruct current standing",
    )
    joined = "\n".join(str(item) for item in non_claims)
    for marker in required_non_claim_fragments:
        if marker not in joined:
            fail(f"disposition fixture missing non-claim marker: {marker}")


def main() -> None:
    for path in (SCHEMA_PATH, INTAKE_PATH, RECORD_PATH, AGGREGATE_PATH, PACKAGE_PATH):
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")

    profile = load_json(PROFILE_PATH)
    result = load_json(RESULT_PATH)
    source_receipt = load_json(SOURCE_RECEIPT_PATH)
    disposition_fixtures = load_json(DISPOSITION_FIXTURES_PATH)
    binding = load_json(BINDING_STATUS_PATH)

    if profile.get("schema") != "conectrr_itc_interoperability_test_profile.v1":
        fail("unexpected test-profile schema")
    if profile.get("profile_id") != "conectrr-itc-first-interoperability-exercise":
        fail("unexpected test-profile id")
    if profile.get("authority_effect") != "NONE":
        fail("test profile must have no authority effect")

    received_states = validate_source_receipt(source_receipt, profile)
    source_complete = all(received_states)
    validate_disposition_fixtures(disposition_fixtures, profile, source_complete)

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
        if any(received_states):
            fail("pending result conflicts with received source artifacts")
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

    if binding.get("schema") != "conectrr_itc_canonical_validation_binding_status.v1":
        fail("unexpected canonical validation binding status schema")
    if binding.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("canonical validation binding repository mismatch")
    if binding.get("binding_state") != "BOUND_THROUGH_CANONICAL_AGGREGATE":
        fail("Conectrr validator must remain bound through the canonical aggregate")
    require_false_authority(binding.get("authority"), "binding status")

    aggregate_text = AGGREGATE_PATH.read_text(encoding="utf-8")
    if "check_conectrr_itc_interoperability.py" not in aggregate_text:
        fail("canonical aggregate does not reference the Conectrr validator")
    if "CONECTRR_ITC_INTEROPERABILITY_CHECK" not in aggregate_text:
        fail("canonical aggregate is missing the Conectrr check constant")

    package_text = PACKAGE_PATH.read_text(encoding="utf-8")
    if "validate:admissibility-automation-handoff" not in package_text:
        fail("package.json does not expose the canonical aggregate validation script")
    if "npm run validate:admissibility-automation-handoff" not in package_text:
        fail("npm run validate does not invoke the canonical aggregate")

    workflow_state = binding.get("workflow_observation_state")
    workflow_runs = binding.get("workflow_runs_observed")
    if workflow_state == "NOT_OBSERVED_FOR_LATEST_COMMIT" and workflow_runs != 0:
        fail("unobserved workflow state must report zero observed runs")
    if workflow_state == "OBSERVED_PASS" and (not isinstance(workflow_runs, int) or workflow_runs < 1):
        fail("observed workflow pass requires at least one workflow run")
    if workflow_state not in {"NOT_OBSERVED_FOR_LATEST_COMMIT", "OBSERVED_PASS", "OBSERVED_FAIL"}:
        fail("unsupported workflow observation state")

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
    print(f"OK: {SOURCE_RECEIPT_PATH.relative_to(ROOT)}")
    print(f"OK: {DISPOSITION_FIXTURES_PATH.relative_to(ROOT)}")
    print(f"OK: {SCHEMA_PATH.relative_to(ROOT)}")
    print(f"OK: {BINDING_STATUS_PATH.relative_to(ROOT)}")
    print(f"conectrr_itc_source_package={source_receipt.get('state')}")
    print("conectrr_itc_dispositions=AGREE,DISAGREE,DEFER")
    print("conectrr_itc_disposition_fixtures=BOUND")
    print("conectrr_itc_canonical_binding=BOUND_THROUGH_CANONICAL_AGGREGATE")
    print(f"conectrr_itc_workflow_observation={workflow_state}")
    print("conectrr_itc_authority_effect=NONE")
    print("conectrr_itc_source_mutation_allowed=false")
    print("conectrr_itc_validator=PASS")


if __name__ == "__main__":
    main()
