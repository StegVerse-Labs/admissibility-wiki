#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "external-frameworks" / "evidence" / "morrison-runtime-canonical-promotion-input.template.json"
PROMOTION_GATE = ROOT / "docs" / "external-frameworks" / "evidence" / "morrison-runtime-promotion-gate.v0.1.json"
ORCHESTRATION = ROOT / "docs" / "external-frameworks" / "evidence" / "morrison-runtime-orchestration-status.v0.1.json"
BINDING = ROOT / "docs" / "external-frameworks" / "evidence" / "morrison-runtime-formalism-tests-binding.v0.1.json"
PUBLIC_STATUS = ROOT / "static" / "status" / "morrison-runtime-promotion-status.json"

AUTHORITY = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"
PROHIBITED = {
    "CERTIFIED_COMPATIBLE",
    "STEGVERSE_EXECUTION_AUTHORITY",
    "FULL_FRESH_STATE_RECONSTRUCTION_BY_DEFAULT",
    "PRODUCTION_VALIDATION",
    "ENDORSEMENT",
}
TASKS = {
    "morrison_runtime_commit_time_scope_tests",
    "verify_morrison_runtime_commit_time_scope_artifacts",
    "check_morrison_runtime_canonical_evidence_gate",
}
HASHES = {
    "report_sha256",
    "receipts_sha256",
    "verification_sha256",
    "canonical_gate_sha256",
}
EQUIVALENCE = {
    "report",
    "receipts",
    "expected_outcomes",
    "canonical_gate",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def check_template(data: dict, failures: list[str]) -> str:
    if data.get("required_authority_posture") != AUTHORITY:
        failures.append("promotion input authority posture changed")
    if set(data.get("prohibited_promotions", [])) != PROHIBITED:
        failures.append("prohibited promotion set is incomplete or changed")
    if data.get("next_owner") != "StegVerse-Labs/admissibility-wiki#39":
        failures.append("next owner must remain admissibility-wiki#39")

    upstream = data.get("upstream", {})
    gate = data.get("promotion_gate", {})
    status = upstream.get("canonical_status")
    task_results = upstream.get("task_results", {})
    hashes = upstream.get("artifact_hashes", {})
    equivalence = upstream.get("artifact_equivalence", {})

    if set(task_results) != TASKS:
        failures.append("promotion input task set does not match canonical proof contract")
    if set(hashes) != HASHES:
        failures.append("promotion input artifact hash set does not match canonical proof contract")
    if set(equivalence) != EQUIVALENCE:
        failures.append("promotion input equivalence set does not match canonical proof contract")

    if status == "PENDING_CANONICAL_EXECUTION":
        if any(value != "PENDING" for value in task_results.values()):
            failures.append("pending task results must remain explicitly PENDING")
        if any(value != "PENDING" for value in hashes.values()):
            failures.append("pending artifact hashes must remain PENDING")
        if any(equivalence.values()):
            failures.append("pending artifact equivalence must remain false")
        if gate.get("all_upstream_tasks_pass") is not False:
            failures.append("pending gate cannot claim upstream task pass")
        if gate.get("all_artifacts_equivalent") is not False:
            failures.append("pending gate cannot claim artifact equivalence")
        if gate.get("eligible_for_compatibility_report_update") is not False:
            failures.append("pending gate cannot permit compatibility report update")
        return "PENDING_FAIL_CLOSED"

    if status == "VERIFIED_CANONICAL_RUN":
        if not SHA40.fullmatch(str(upstream.get("commit_sha", ""))):
            failures.append("verified input requires a 40-character commit SHA")
        if set(task_results.values()) != {"PASS"} or len(task_results) != len(TASKS):
            failures.append("verified input requires all three declared tasks to PASS")
        if len(hashes) != len(HASHES) or not all(SHA256.fullmatch(str(value)) for value in hashes.values()):
            failures.append("verified input requires four SHA-256 artifact hashes")
        if set(equivalence.values()) != {True}:
            failures.append("verified input requires all artifact equivalence checks true")
        required_true = (
            "all_upstream_tasks_pass",
            "all_artifacts_equivalent",
            "source_provenance_bound",
            "authority_posture_preserved",
            "eligible_for_compatibility_report_update",
        )
        if not all(gate.get(key) is True for key in required_true):
            failures.append("verified promotion gate is not fully satisfied")
        return "VERIFIED_BOUNDED_PROMOTION_ELIGIBLE"

    failures.append(f"unsupported canonical_status: {status!r}")
    return "INVALID"


def check_public_status(data: dict, template: dict, mode: str, failures: list[str]) -> None:
    if data.get("authority_posture") != AUTHORITY:
        failures.append("public status authority posture changed")
    if set(data.get("prohibited_claims", [])) != PROHIBITED:
        failures.append("public status prohibited claim set changed")
    if data.get("fail_closed") is not True:
        failures.append("public status must remain fail-closed")
    boundary = data.get("boundary", {})
    if boundary.get("runtime_re_evaluation_equals_full_reconstruction") is not False:
        failures.append("public status conflates runtime re-evaluation with full reconstruction")

    upstream = template.get("upstream", {})
    if data.get("required_task_results") != upstream.get("task_results"):
        failures.append("public status task results diverge from promotion input")
    if data.get("required_artifact_hashes") != upstream.get("artifact_hashes"):
        failures.append("public status artifact hashes diverge from promotion input")
    if data.get("required_equivalence") != upstream.get("artifact_equivalence"):
        failures.append("public status equivalence fields diverge from promotion input")

    if mode == "PENDING_FAIL_CLOSED":
        if data.get("state") != "PENDING_CANONICAL_EXECUTION":
            failures.append("pending public status state mismatch")
        blocked = (
            "canonical_execution_verified",
            "artifact_equivalence_verified",
            "compatibility_report_update_eligible",
            "public_promotion_eligible",
            "downstream_propagation_eligible",
        )
        if any(data.get(key) is not False for key in blocked):
            failures.append("pending public status contains premature eligibility")
        if data.get("required_next_transition") != "CANONICAL_EXECUTION_EVIDENCE_ATTACHED":
            failures.append("pending public status next transition changed")


def main() -> int:
    failures: list[str] = []
    try:
        template = load(TEMPLATE)
        load(PROMOTION_GATE)
        load(ORCHESTRATION)
        load(BINDING)
        public_status = load(PUBLIC_STATUS)
    except ValueError as exc:
        failures.append(str(exc))
        template = {}
        public_status = {}

    mode = check_template(template, failures) if template else "INVALID"
    if public_status:
        check_public_status(public_status, template, mode, failures)

    if failures:
        print("MORRISON RUNTIME PROMOTION GATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MORRISON RUNTIME PROMOTION GATE: PASS")
    print(f"mode: {mode}")
    print(f"authority_posture: {AUTHORITY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
