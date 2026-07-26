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

AUTHORITY = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"
PROHIBITED = {
    "CERTIFIED_COMPATIBLE",
    "STEGVERSE_EXECUTION_AUTHORITY",
    "FULL_FRESH_STATE_RECONSTRUCTION_BY_DEFAULT",
    "PRODUCTION_VALIDATION",
    "ENDORSEMENT",
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

    if status == "PENDING_CANONICAL_EXECUTION":
        expected_pending = {
            "morrison_runtime_commit_time_scope_tests": "PENDING",
            "verify_morrison_runtime_commit_time_scope_artifacts": "PENDING",
        }
        if upstream.get("task_results") != expected_pending:
            failures.append("pending task results must remain explicitly PENDING")
        hashes = upstream.get("artifact_hashes", {})
        if any(value != "PENDING" for value in hashes.values()):
            failures.append("pending artifact hashes must remain PENDING")
        if any(upstream.get("artifact_equivalence", {}).values()):
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
        task_results = upstream.get("task_results", {})
        if set(task_results.values()) != {"PASS"} or len(task_results) != 2:
            failures.append("verified input requires both declared tasks to PASS")
        hashes = upstream.get("artifact_hashes", {})
        if len(hashes) != 3 or not all(SHA256.fullmatch(str(value)) for value in hashes.values()):
            failures.append("verified input requires three SHA-256 artifact hashes")
        if set(upstream.get("artifact_equivalence", {}).values()) != {True}:
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


def main() -> int:
    failures: list[str] = []
    try:
        template = load(TEMPLATE)
        load(PROMOTION_GATE)
        load(ORCHESTRATION)
        load(BINDING)
    except ValueError as exc:
        failures.append(str(exc))
        template = {}

    mode = check_template(template, failures) if template else "INVALID"

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
