#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
DEFAULT_BUILD = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-build-receipt.json"
DEFAULT_CANDIDATE = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-promotion-candidate.json"
DEFAULT_PROMOTION = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-promotion-receipt.json"
DEFAULT_APPLICATION = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-application-result.json"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-provenance-reconciliation.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def cedar_hash(registry: dict[str, Any]) -> str | None:
    matches = [item for item in registry.get("frameworks", []) if isinstance(item, dict) and item.get("framework_id") == "cedar-policy"]
    if len(matches) != 1:
        raise ValueError("registry must contain exactly one cedar-policy record")
    if matches[0].get("execution_authorized") is not False:
        raise ValueError("Cedar execution_authorized must remain false")
    value = matches[0].get("selection", {}).get("compiled_binary_sha256")
    return value if isinstance(value, str) else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile Cedar canonical binary hash provenance without executing Cedar.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--build-receipt", type=Path, default=DEFAULT_BUILD)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--promotion-receipt", type=Path, default=DEFAULT_PROMOTION)
    parser.add_argument("--application-result", type=Path, default=DEFAULT_APPLICATION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    failures: list[str] = []
    payloads: dict[str, dict[str, Any]] = {}
    paths = {
        "registry": args.registry,
        "build_receipt": args.build_receipt,
        "candidate": args.candidate,
        "promotion_receipt": args.promotion_receipt,
        "application_result": args.application_result,
    }
    for name, path in paths.items():
        if not path.exists():
            failures.append(f"missing {name}: {path}")
            continue
        try:
            payloads[name] = load(path)
        except Exception as exc:
            failures.append(f"invalid {name}: {exc}")

    canonical_hash: str | None = None
    if "registry" in payloads:
        try:
            canonical_hash = cedar_hash(payloads["registry"])
        except Exception as exc:
            failures.append(str(exc))
    if not canonical_hash or not HEX64.fullmatch(canonical_hash):
        failures.append("canonical compiled_binary_sha256 missing or malformed")

    build_hash = payloads.get("build_receipt", {}).get("binary", {}).get("sha256")
    candidate_hash = payloads.get("candidate", {}).get("binary_sha256")
    promotion = payloads.get("promotion_receipt", {})
    promotion_hash = promotion.get("source_promotion_candidate", {}).get("binary_sha256")
    proposed_hash = promotion.get("registry_target", {}).get("proposed_value")
    application_hash = payloads.get("application_result", {}).get("registry", {}).get("approved_value")

    observed = {
        "canonical_registry": canonical_hash,
        "build_receipt": build_hash,
        "promotion_candidate": candidate_hash,
        "promotion_receipt_source": promotion_hash,
        "promotion_receipt_target": proposed_hash,
        "application_result": application_hash,
    }
    for name, value in observed.items():
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            failures.append(f"{name} hash missing or malformed")
    if all(isinstance(value, str) and HEX64.fullmatch(value) for value in observed.values()):
        if len(set(observed.values())) != 1:
            failures.append("binary hash mismatch across provenance chain")

    build = payloads.get("build_receipt", {})
    if build:
        if build.get("overall_status") != "BUILT_HASHED_UNEXECUTED":
            failures.append("build receipt status is not BUILT_HASHED_UNEXECUTED")
        if build.get("binary", {}).get("executed_after_build") is not False:
            failures.append("build receipt does not preserve unexecuted state")
        if build.get("authority_boundary", {}).get("runtime_execution_authorized") is not False:
            failures.append("build receipt claims runtime authority")

    candidate = payloads.get("candidate", {})
    if candidate:
        if candidate.get("candidate_state") != "READY_FOR_REGISTRY_PROMOTION_REVIEW":
            failures.append("promotion candidate is not ready for review")
        if candidate.get("registry_mutation_performed") is not False:
            failures.append("promotion candidate claims registry mutation")
        if candidate.get("runtime_execution_authorized") is not False:
            failures.append("promotion candidate claims runtime authority")

    if promotion:
        if promotion.get("decision") != "ALLOW_REGISTRY_PROMOTION_ONLY":
            failures.append("promotion receipt decision mismatch")
        if promotion.get("promotion_state") != "APPLIED_HASH_ONLY":
            failures.append("promotion receipt is not APPLIED_HASH_ONLY")
        if promotion.get("registry_mutation_applied") is not True:
            failures.append("promotion receipt does not claim hash-only mutation")
        if promotion.get("runtime_execution_authorized") is not False:
            failures.append("promotion receipt claims runtime authority")

    application = payloads.get("application_result", {})
    if application:
        if application.get("application_state") not in {"APPLIED_HASH_ONLY", "ALREADY_APPLIED_HASH_ONLY"}:
            failures.append("application result state is not hash-only applied")
        if application.get("runtime_execution_authorized") is not False:
            failures.append("application result claims runtime authority")
        if application.get("external_consequence_allowed") is not False:
            failures.append("application result permits external consequence")

    result = {
        "artifact_type": "cedar_binary_provenance_reconciliation",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "framework_id": "cedar-policy",
        "reconciliation_state": "PROVENANCE_RECONCILED_HASH_ONLY" if not failures else "PROVENANCE_UNRESOLVED_FAIL_CLOSED",
        "artifacts": {
            name: {"path": str(path), "sha256": sha256(path) if path.exists() else None}
            for name, path in paths.items()
        },
        "binary_hashes": observed,
        "all_hashes_equal": not failures and len(set(observed.values())) == 1,
        "runtime_execution_authorized": False,
        "runtime_execution_requested": False,
        "external_consequence_allowed": False,
        "failures": failures,
        "required_next_transition": "regenerate_readiness_and retain separate runtime authorization review" if not failures else "obtain and inspect missing or mismatched canonical artifacts",
        "authority_boundary": {
            "provenance_reconciliation_is_compatibility_proof": False,
            "provenance_reconciliation_is_execution_authority": False,
            "matching_hashes_authorize_dispatch": False,
            "matching_hashes_create_standing": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR BINARY PROVENANCE RECONCILIATION: {result['reconciliation_state']} -> {args.output}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
