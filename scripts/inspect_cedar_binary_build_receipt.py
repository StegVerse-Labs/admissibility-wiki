#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "reports" / "external-frameworks" / "cedar-build"
RECEIPT = BUILD_DIR / "cedar-binary-build-receipt.json"
OUTPUT = BUILD_DIR / "cedar-binary-registry-promotion-candidate.json"
EXPECTED_COMMIT = "0807ec154afd7ffa14a658c9955d25bfe12770ca"
EXPECTED_VERSION = "4.11.0"
EXPECTED_COMMAND = "cargo build --locked --release -p cedar-policy-cli"
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
        raise ValueError("build receipt must be a JSON object")
    return payload


def main() -> int:
    failures: list[str] = []
    receipt: dict[str, Any] = {}

    if not RECEIPT.exists():
        failures.append("build receipt missing")
    else:
        try:
            receipt = load(RECEIPT)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failures.append(f"build receipt invalid: {exc}")

    if receipt:
        checks = {
            "artifact_type": receipt.get("artifact_type") == "external_framework_selected_binary_build_receipt",
            "framework_id": receipt.get("framework_id") == "cedar-policy",
            "implementation_identifier": receipt.get("implementation_identifier") == "cedar-policy-cli",
            "selection_version": receipt.get("selection_version") == EXPECTED_VERSION,
            "pinned_commit": receipt.get("pinned_commit") == EXPECTED_COMMIT,
            "resolved_commit": receipt.get("resolved_commit") == EXPECTED_COMMIT,
            "build_command": receipt.get("build_command") == EXPECTED_COMMAND,
            "build_exit_code": receipt.get("build_exit_code") == 0,
            "overall_status": receipt.get("overall_status") == "BUILT_HASHED_UNEXECUTED",
            "failures_empty": receipt.get("failures") == [],
        }
        for name, passed in checks.items():
            if not passed:
                failures.append(f"receipt check failed: {name}")

        binary = receipt.get("binary", {})
        if not isinstance(binary, dict):
            failures.append("binary record missing")
            binary = {}
        binary_hash = str(binary.get("sha256", ""))
        if not HEX64.fullmatch(binary_hash):
            failures.append("binary sha256 missing or malformed")
        if not isinstance(binary.get("size_bytes"), int) or binary.get("size_bytes", 0) <= 0:
            failures.append("binary size missing or invalid")
        if binary.get("executed_after_build") is not False:
            failures.append("binary must remain unexecuted")

        lock_hash = str(receipt.get("cargo_lock_sha256", ""))
        if not HEX64.fullmatch(lock_hash):
            failures.append("Cargo.lock sha256 missing or malformed")

        boundary = receipt.get("authority_boundary", {})
        for key in (
            "binary_build_is_execution_authority",
            "binary_hash_is_compatibility_proof",
            "binary_was_used_for_authorization_decision",
            "runtime_execution_authorized",
            "external_consequence_allowed",
        ):
            if boundary.get(key) is not False:
                failures.append(f"authority boundary must remain false: {key}")

    valid = not failures
    binary = receipt.get("binary", {}) if receipt else {}
    result = {
        "artifact_type": "cedar_binary_registry_promotion_candidate",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "framework_id": "cedar-policy",
        "source_build_receipt": {
            "path": str(RECEIPT.relative_to(ROOT)),
            "sha256": sha256(RECEIPT) if RECEIPT.exists() else None,
        },
        "candidate_state": "READY_FOR_REGISTRY_PROMOTION_REVIEW" if valid else "BLOCKED_BUILD_RECEIPT_INVALID",
        "receipt_validated": valid,
        "binary_sha256": binary.get("sha256"),
        "binary_size_bytes": binary.get("size_bytes"),
        "cargo_lock_sha256": receipt.get("cargo_lock_sha256") if receipt else None,
        "resolved_commit": receipt.get("resolved_commit") if receipt else None,
        "selection_version": receipt.get("selection_version") if receipt else None,
        "registry_mutation_performed": False,
        "runtime_execution_requested": False,
        "runtime_execution_authorized": False,
        "authorization_decision_observed": False,
        "external_consequence_allowed": False,
        "failures": failures,
        "required_next_transition": (
            "inspect_candidate_and_apply_binary_hash_to_selection_registry_in_separate_governed_commit"
            if valid
            else "repair_or_rerun_build_before_registry_promotion_review"
        ),
        "authority_boundary": {
            "receipt_inspection_is_execution_authority": False,
            "binary_hash_promotion_is_compatibility_proof": False,
            "promotion_candidate_may_mutate_registry": False,
            "promotion_candidate_may_execute_binary": False,
            "promotion_candidate_may_authorize_external_consequence": False,
        },
    }

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR BUILD RECEIPT INSPECTION: {result['candidate_state']} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
