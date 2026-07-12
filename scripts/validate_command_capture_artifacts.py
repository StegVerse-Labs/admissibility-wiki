#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a reusable external-command capture receipt without promoting its authority state.")
    parser.add_argument("--framework-id", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    receipt_path = Path(args.receipt).resolve()
    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()
    failures: list[str] = []

    for path in [receipt_path, manifest_path]:
        if not path.exists():
            failures.append(f"missing path: {path}")

    receipt: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    if not failures:
        try:
            receipt = load(receipt_path)
            manifest = load(manifest_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failures.append(str(exc))

    expected_framework = args.framework_id
    if receipt:
        if receipt.get("artifact_type") != "external_framework_observed_evidence_capture":
            failures.append("receipt artifact_type mismatch")
        if receipt.get("framework_id") != expected_framework:
            failures.append("receipt framework_id mismatch")
        if receipt.get("capture_state") != "captured_unverified":
            failures.append("receipt must remain captured_unverified")
        implementation = receipt.get("implementation", {})
        for key in ["identifier", "version_command", "version_stdout", "execute_command", "exit_code"]:
            if key not in implementation:
                failures.append(f"implementation missing {key}")
        for key in ["manifest_sha256", "input_sha256", "stdout_sha256", "stderr_sha256", "version_stdout_sha256"]:
            if key not in receipt.get("hashes", {}):
                failures.append(f"hashes missing {key}")
        authority = receipt.get("authority_context", {})
        required_false = [
            "external_output_is_execution_authority",
            "capture_is_stegverse_standing",
            "capture_is_compatibility_proof",
            "current_delegation_attached",
            "commit_time_authority_reconstructed",
        ]
        for key in required_false:
            if authority.get(key) is not False:
                failures.append(f"authority_context.{key} must be false")
        if not receipt.get("limitations"):
            failures.append("limitations missing")
        if not receipt.get("replay"):
            failures.append("replay instructions missing")

    if manifest:
        if manifest.get("artifact_type") != "external_framework_capture_manifest":
            failures.append("manifest artifact_type mismatch")
        if manifest.get("framework_id") != expected_framework:
            failures.append("manifest framework_id mismatch")
        if receipt and receipt.get("hashes", {}).get("manifest_sha256") != sha256(manifest_path):
            failures.append("manifest hash mismatch")
        if receipt and receipt.get("case_id") != manifest.get("case_id"):
            failures.append("case_id mismatch")

    status = {
        "artifact_type": "external_framework_capture_validation_status",
        "schema_version": "0.1",
        "framework_id": expected_framework,
        "overall_status": "PASS" if not failures else "FAIL",
        "capture_state": "captured_unverified" if not failures else "unverified_or_invalid",
        "same_runner_replay_state": "not_performed",
        "fresh_runner_replay_state": "not_performed",
        "independent_implementation_or_provider_review": "not_performed",
        "compatibility_state": "not_claimed",
        "standing_state": "not_created",
        "execution_authority_state": "not_created",
        "artifacts": {
            "receipt": {"path": str(receipt_path.relative_to(ROOT)) if receipt_path.exists() else str(receipt_path), "sha256": sha256(receipt_path) if receipt_path.exists() else None},
            "manifest": {"path": str(manifest_path.relative_to(ROOT)) if manifest_path.exists() else str(manifest_path), "sha256": sha256(manifest_path) if manifest_path.exists() else None},
        },
        "validation_failures": failures,
        "authority_boundary": {
            "validation_is_execution_authority": False,
            "capture_is_compatibility_proof": False,
            "protocol_response_creates_standing": False,
            "validation_creates_delegation": False,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"COMMAND CAPTURE ARTIFACT VALIDATION: {status['overall_status']} -> {output_path.relative_to(ROOT)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
