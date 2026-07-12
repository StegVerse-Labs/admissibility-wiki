#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-application-result.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TARGET_FIELD = "frameworks[cedar-policy].selection.compiled_binary_sha256"


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


def cedar_record(registry: dict[str, Any]) -> dict[str, Any]:
    matches = [item for item in registry.get("frameworks", []) if isinstance(item, dict) and item.get("framework_id") == "cedar-policy"]
    if len(matches) != 1:
        raise ValueError("registry must contain exactly one cedar-policy record")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply only the approved Cedar compiled-binary SHA-256 registry mutation.")
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--apply", action="store_true", help="Write the registry mutation. Without this flag, perform validation and produce a dry-run result only.")
    args = parser.parse_args()

    failures: list[str] = []
    receipt: dict[str, Any] = {}
    registry: dict[str, Any] = {}

    try:
        receipt = load(args.receipt)
    except Exception as exc:  # fail closed and preserve a result receipt
        failures.append(f"promotion receipt invalid: {exc}")
    try:
        registry = load(args.registry)
    except Exception as exc:
        failures.append(f"selection registry invalid: {exc}")

    source = receipt.get("source_promotion_candidate", {}) if receipt else {}
    review = receipt.get("review", {}) if receipt else {}
    target = receipt.get("registry_target", {}) if receipt else {}
    proposed = str(target.get("proposed_value", ""))

    checks = {
        "receipt_type": receipt.get("receipt_type") == "cedar_binary_registry_promotion_receipt",
        "framework_id": receipt.get("framework_id") == "cedar-policy",
        "decision": receipt.get("decision") == "ALLOW_REGISTRY_PROMOTION_ONLY",
        "promotion_state": receipt.get("promotion_state") in {"APPROVED_NOT_APPLIED", "APPLIED_HASH_ONLY"},
        "candidate_state": source.get("candidate_state") == "READY_FOR_REGISTRY_PROMOTION_REVIEW",
        "candidate_sha256": bool(HEX64.fullmatch(str(source.get("sha256", "")))),
        "binary_sha256": bool(HEX64.fullmatch(str(source.get("binary_sha256", "")))),
        "review_pass": review.get("status") == "PASS",
        "reviewer_identity": bool(review.get("reviewer_identity")),
        "delegation_ref": bool(review.get("delegation_ref")),
        "target_path": target.get("path") == str(args.registry.relative_to(ROOT)) if args.registry.is_absolute() and args.registry.is_relative_to(ROOT) else target.get("path") == str(args.registry),
        "target_field": target.get("field") == TARGET_FIELD,
        "target_hash_matches_candidate": proposed == source.get("binary_sha256") and bool(HEX64.fullmatch(proposed)),
        "runtime_execution_authorized_false": receipt.get("runtime_execution_authorized") is False,
        "external_consequence_allowed_false": receipt.get("external_consequence_allowed") is False,
    }
    for name, passed in checks.items():
        if not passed:
            failures.append(f"receipt predicate failed: {name}")

    original_registry_sha = sha256(args.registry) if args.registry.exists() else None
    updated_registry_sha: str | None = None
    mutation_applied = False
    idempotent_existing_match = False
    previous_value: Any = None

    if registry and not failures:
        try:
            record = cedar_record(registry)
            if record.get("execution_authorized") is not False:
                failures.append("Cedar execution_authorized must remain false")
            selection = record.get("selection")
            if not isinstance(selection, dict):
                failures.append("Cedar selection object missing")
            else:
                previous_value = selection.get("compiled_binary_sha256")
                expected_previous = target.get("expected_previous_value")
                if previous_value == proposed:
                    idempotent_existing_match = True
                elif previous_value != expected_previous:
                    failures.append("registry previous value does not match approved receipt")
                elif args.apply:
                    updated = deepcopy(registry)
                    updated_record = cedar_record(updated)
                    updated_record["selection"]["compiled_binary_sha256"] = proposed
                    if updated_record.get("execution_authorized") is not False:
                        failures.append("mutation would alter execution authorization")
                    else:
                        args.registry.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
                        mutation_applied = True
                        updated_registry_sha = sha256(args.registry)
        except Exception as exc:
            failures.append(f"registry mutation validation failed: {exc}")

    state = "BLOCKED"
    if not failures:
        if mutation_applied:
            state = "APPLIED_HASH_ONLY"
        elif idempotent_existing_match:
            state = "ALREADY_APPLIED_HASH_ONLY"
        else:
            state = "VALIDATED_DRY_RUN"

    result = {
        "artifact_type": "cedar_binary_hash_registry_application_result",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "framework_id": "cedar-policy",
        "source_promotion_receipt": {
            "path": str(args.receipt),
            "sha256": sha256(args.receipt) if args.receipt.exists() else None,
        },
        "registry": {
            "path": str(args.registry),
            "target_field": TARGET_FIELD,
            "original_sha256": original_registry_sha,
            "updated_sha256": updated_registry_sha,
            "previous_value": previous_value,
            "approved_value": proposed or None,
        },
        "application_state": state,
        "apply_requested": args.apply,
        "registry_mutation_applied": mutation_applied,
        "idempotent_existing_match": idempotent_existing_match,
        "runtime_execution_authorized": False,
        "runtime_execution_requested": False,
        "external_consequence_allowed": False,
        "failures": failures,
        "required_next_transition": "revalidate_selection_registry_and_regenerate_readiness_without_dispatch_or_execution" if state in {"APPLIED_HASH_ONLY", "ALREADY_APPLIED_HASH_ONLY"} else "complete_governed_hash_promotion_before_readiness_regeneration",
        "authority_boundary": {
            "hash_application_is_execution_authority": False,
            "hash_application_is_compatibility_proof": False,
            "hash_application_may_change_any_other_registry_field": False,
            "hash_application_may_dispatch_or_execute": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR BINARY HASH REGISTRY APPLICATION: {state} -> {args.output}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
