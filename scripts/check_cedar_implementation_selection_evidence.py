#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "external-frameworks" / "implementation-selections" / "cedar-policy-cli-4.11.0.selection-evidence.json"
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
APPLIED_PROMOTION_RECEIPT = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-promotion-receipt.applied-hash-only.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_COMMIT = "0807ec154afd7ffa14a658c9955d25bfe12770ca"
EXPECTED_VERSION = "4.11.0"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def validate_promoted_hash(compiled_hash: object, failures: list[str]) -> None:
    if not isinstance(compiled_hash, str) or not HEX64.fullmatch(compiled_hash):
        failures.append("compiled binary hash must be a lowercase sha256 after hash-only promotion")
        return
    if not APPLIED_PROMOTION_RECEIPT.exists():
        failures.append("applied Cedar hash-only promotion receipt missing")
        return
    try:
        receipt = load_json(APPLIED_PROMOTION_RECEIPT)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        failures.append(f"applied Cedar promotion receipt invalid: {exc}")
        return
    source = receipt.get("source_promotion_candidate", {})
    target = receipt.get("registry_target", {})
    review = receipt.get("review", {})
    if receipt.get("decision") != "ALLOW_REGISTRY_PROMOTION_ONLY":
        failures.append("applied promotion receipt decision mismatch")
    if receipt.get("promotion_state") != "APPLIED_HASH_ONLY":
        failures.append("applied promotion receipt state mismatch")
    if receipt.get("registry_mutation_applied") is not True:
        failures.append("applied promotion receipt must record hash-only mutation")
    if receipt.get("runtime_execution_authorized") is not False:
        failures.append("applied promotion receipt must not authorize execution")
    if receipt.get("external_consequence_allowed") is not False:
        failures.append("applied promotion receipt must not allow external consequence")
    if review.get("status") != "PASS" or not review.get("delegation_ref"):
        failures.append("applied promotion receipt requires completed delegated review")
    if source.get("candidate_state") != "READY_FOR_REGISTRY_PROMOTION_REVIEW":
        failures.append("applied promotion receipt candidate was not ready")
    if source.get("binary_sha256") != compiled_hash:
        failures.append("registry compiled hash differs from promotion candidate")
    if target.get("field") != "frameworks[cedar-policy].selection.compiled_binary_sha256":
        failures.append("applied promotion receipt targets wrong registry field")
    if target.get("proposed_value") != compiled_hash:
        failures.append("registry compiled hash differs from applied promotion target")


def main() -> int:
    failures: list[str] = []
    for path in (EVIDENCE, REGISTRY, APPLIED_PROMOTION_RECEIPT):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("CEDAR IMPLEMENTATION SELECTION EVIDENCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    try:
        evidence = load_json(EVIDENCE)
        registry = load_json(REGISTRY)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print("CEDAR IMPLEMENTATION SELECTION EVIDENCE: FAIL")
        print(f"- invalid evidence or registry: {exc}")
        return 1

    if evidence.get("artifact_type") != "external_framework_implementation_selection_evidence":
        failures.append("artifact_type mismatch")
    if evidence.get("framework_id") != "cedar-policy":
        failures.append("framework_id mismatch")
    if evidence.get("selection_state") != "implementation_selected_hash_bound":
        failures.append("selection_state mismatch")

    implementation = evidence.get("implementation", {})
    if implementation.get("identifier") != "cedar-policy-cli":
        failures.append("implementation identifier mismatch")
    if implementation.get("canonical_commit") != EXPECTED_COMMIT:
        failures.append("canonical commit mismatch")
    if implementation.get("version") != EXPECTED_VERSION:
        failures.append("version mismatch")

    source_rows = evidence.get("canonical_source_evidence", [])
    if len(source_rows) < 4:
        failures.append("insufficient canonical source evidence")
    canonical_parts = []
    for row in source_rows:
        blob = str(row.get("git_blob_sha", ""))
        path = str(row.get("path", ""))
        if not path or not HEX40.fullmatch(blob):
            failures.append(f"invalid source row: {row}")
        canonical_parts.append(f"{path}:{blob}")
    canonical = f"cedar-policy/cedar@{EXPECTED_COMMIT}|" + "|".join(canonical_parts)
    computed = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    recorded = evidence.get("source_evidence_bundle", {}).get("sha256")
    if recorded != computed or not HEX64.fullmatch(str(recorded or "")):
        failures.append("source evidence bundle hash mismatch")

    commands = evidence.get("commands", {})
    for key in ("version_command", "build_command", "evaluation_command_template"):
        if not str(commands.get(key, "")).strip():
            failures.append(f"commands.{key} missing")
    if "--locked" not in str(commands.get("build_command", "")):
        failures.append("build command must be lockfile-bound")

    boundary = evidence.get("authority_boundary", {})
    for key in ("selection_is_certification", "selection_is_compatibility", "selection_creates_standing", "selection_authorizes_execution", "source_bundle_hash_is_compiled_binary_hash"):
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary.{key} must be false")

    cedar = next((item for item in registry.get("frameworks", []) if item.get("framework_id") == "cedar-policy"), None)
    if not cedar:
        failures.append("Cedar registry record missing")
    else:
        if cedar.get("selection_state") != "implementation_selected_hash_bound":
            failures.append("registry Cedar state mismatch")
        if cedar.get("execution_authorized") is not False:
            failures.append("registry Cedar execution must remain unauthorized")
        selection = cedar.get("selection", {})
        expected_path = str(EVIDENCE.relative_to(ROOT))
        if selection.get("selection_evidence_path") != expected_path:
            failures.append("registry evidence path mismatch")
        expected_hash = f"source-evidence-bundle-sha256:{computed}"
        if selection.get("artifact_or_package_hash") != expected_hash:
            failures.append("registry source bundle hash mismatch")
        validate_promoted_hash(selection.get("compiled_binary_sha256"), failures)

    print("CEDAR IMPLEMENTATION SELECTION EVIDENCE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
