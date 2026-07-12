#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "external-frameworks" / "opa"
STATUS_PATH = REPORT_DIR / "opa-capture-status.json"

CASES = ("allow", "deny")
REQUIRED_CAPTURE_KEYS = {
    "artifact_type",
    "schema_version",
    "framework_id",
    "case_id",
    "capture_state",
    "captured_at_utc",
    "runtime",
    "source",
    "input",
    "output",
    "hashes",
    "authority_context",
    "freshness_context",
    "limitations",
    "replay",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    captures: dict[str, dict[str, Any]] = {}
    replays: dict[str, dict[str, Any]] = {}

    for case in CASES:
        capture_path = REPORT_DIR / f"opa-{case}-capture.json"
        replay_path = REPORT_DIR / f"opa-{case}-replay.json"
        for path in (capture_path, replay_path):
            if not path.exists():
                failures.append(f"missing generated artifact: {path.relative_to(ROOT)}")
                continue
            try:
                payload = load(path)
            except (json.JSONDecodeError, OSError) as exc:
                failures.append(f"invalid generated artifact {path.relative_to(ROOT)}: {exc}")
                continue
            missing = sorted(REQUIRED_CAPTURE_KEYS - payload.keys())
            if missing:
                failures.append(f"{path.name} missing keys: {', '.join(missing)}")
            if payload.get("artifact_type") != "external_framework_observed_evidence_capture":
                failures.append(f"{path.name} artifact type mismatch")
            if payload.get("framework_id") != "opa":
                failures.append(f"{path.name} framework mismatch")
            if payload.get("capture_state") != "captured_unverified":
                failures.append(f"{path.name} must remain captured_unverified")
            authority = payload.get("authority_context", {})
            for key in (
                "opa_decision_is_execution_authority",
                "capture_is_stegverse_standing",
                "capture_is_compatibility_proof",
                "current_delegation_attached",
                "commit_time_authority_reconstructed",
            ):
                if authority.get(key) is not False:
                    failures.append(f"{path.name} authority boundary must be false: {key}")
            if case == "allow":
                captures[case] = payload if path == capture_path else captures.get(case, {})
                replays[case] = payload if path == replay_path else replays.get(case, {})
            else:
                captures[case] = payload if path == capture_path else captures.get(case, {})
                replays[case] = payload if path == replay_path else replays.get(case, {})

    receipt_path = REPORT_DIR / "opa-replay-receipt.json"
    receipt: dict[str, Any] = {}
    if not receipt_path.exists():
        failures.append(f"missing generated artifact: {receipt_path.relative_to(ROOT)}")
    else:
        try:
            receipt = load(receipt_path)
        except (json.JSONDecodeError, OSError) as exc:
            failures.append(f"invalid replay receipt: {exc}")
        if receipt:
            if receipt.get("artifact_type") != "external_framework_replay_receipt":
                failures.append("replay receipt artifact type mismatch")
            if receipt.get("framework_id") != "opa":
                failures.append("replay receipt framework mismatch")
            if receipt.get("replay_state") != "replay_confirmed_same_environment":
                failures.append("replay receipt did not confirm same-environment replay")
            boundary = receipt.get("authority_boundary", {})
            for key in (
                "opa_decision_is_execution_authority",
                "capture_is_stegverse_standing",
                "replay_is_compatibility_proof",
                "same_environment_replay_is_independent_replay",
            ):
                if boundary.get(key) is not False:
                    failures.append(f"replay authority boundary must be false: {key}")
            for case in CASES:
                comparison = receipt.get("comparisons", {}).get(case, {})
                for key in ("output_match", "stdout_hash_match", "policy_hash_match", "input_hash_match", "case_match"):
                    if comparison.get(key) is not True:
                        failures.append(f"replay comparison failed: {case}:{key}")

    files = sorted(path for path in REPORT_DIR.glob("*.json") if path.name != STATUS_PATH.name)
    status = {
        "artifact_type": "external_framework_capture_status",
        "schema_version": "0.1",
        "framework_id": "opa",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "capture_state": "captured_unverified" if not failures else "capture_validation_failed",
        "same_environment_replay_state": receipt.get("replay_state") if receipt else "missing",
        "independent_environment_replay_state": "not_performed",
        "compatibility_state": "not_claimed",
        "execution_authority_state": "not_created",
        "validated_files": [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in files
        ],
        "validation_failures": failures,
        "authority_boundary": {
            "capture_is_execution_authority": False,
            "same_environment_replay_is_independent_replay": False,
            "capture_is_compatibility_proof": False,
            "capture_is_stegverse_standing": False,
        },
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    print("OPA GENERATED CAPTURE ARTIFACTS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    print(f"status: {STATUS_PATH.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
