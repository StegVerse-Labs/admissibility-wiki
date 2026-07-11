#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_DIR = ROOT / "reports" / "external-frameworks"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: str, stdin_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        shlex.split(command),
        cwd=ROOT,
        input=stdin_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture a non-authorizing observed-evidence receipt for an external framework command."
    )
    parser.add_argument("--manifest", required=True, help="Capture manifest JSON path")
    parser.add_argument("--implementation", required=True, help="Exact runtime, client, model, or implementation identifier")
    parser.add_argument("--version-command", required=True, help="Command that prints the exact implementation version")
    parser.add_argument("--execute-command", required=True, help="Command that consumes manifest input JSON on stdin")
    parser.add_argument("--output", help="Receipt output path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.exists():
        print(f"EXTERNAL CAPTURE: BLOCKED — missing manifest {manifest_path}", file=sys.stderr)
        return 2

    manifest_bytes = manifest_path.read_bytes()
    try:
        manifest: dict[str, Any] = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"EXTERNAL CAPTURE: BLOCKED — invalid manifest: {exc}", file=sys.stderr)
        return 2

    framework_id = str(manifest.get("framework_id", "")).strip()
    case_id = str(manifest.get("case_id", "")).strip()
    source_reference = str(manifest.get("source_reference", "")).strip()
    input_payload = manifest.get("input_payload")
    if not framework_id or not case_id or not source_reference or input_payload is None:
        print("EXTERNAL CAPTURE: BLOCKED — manifest requires framework_id, case_id, source_reference, and input_payload", file=sys.stderr)
        return 2

    input_bytes = (json.dumps(input_payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    version_result = run(args.version_command)
    if version_result.returncode != 0:
        print(version_result.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        return version_result.returncode

    execute_result = run(args.execute_command, stdin_bytes=input_bytes)
    captured_at = datetime.now(timezone.utc).isoformat()

    version_text = version_result.stdout.decode("utf-8", errors="replace")
    stdout_text = execute_result.stdout.decode("utf-8", errors="replace")
    stderr_text = execute_result.stderr.decode("utf-8", errors="replace")
    try:
        output_payload: Any = json.loads(stdout_text) if stdout_text else None
    except json.JSONDecodeError:
        output_payload = {"raw": stdout_text}

    output_path = Path(args.output).resolve() if args.output else (
        DEFAULT_REPORT_DIR / f"{framework_id}-{case_id}-capture.json"
    )

    receipt = {
        "artifact_type": "external_framework_observed_evidence_capture",
        "schema_version": "0.1",
        "framework_id": framework_id,
        "case_id": case_id,
        "capture_state": "captured_unverified",
        "captured_at_utc": captured_at,
        "implementation": {
            "identifier": args.implementation,
            "version_command": args.version_command,
            "version_stdout": version_text,
            "execute_command": args.execute_command,
            "exit_code": execute_result.returncode,
        },
        "source": {
            "canonical_reference": source_reference,
            "manifest_path": str(manifest_path.relative_to(ROOT)),
            "source_version_or_date": manifest.get("source_version_or_date"),
        },
        "input": input_payload,
        "output": output_payload,
        "stderr": stderr_text,
        "hashes": {
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "input_sha256": sha256_bytes(input_bytes),
            "stdout_sha256": sha256_bytes(execute_result.stdout),
            "stderr_sha256": sha256_bytes(execute_result.stderr),
            "version_stdout_sha256": sha256_bytes(version_result.stdout),
        },
        "authority_context": {
            "external_output_is_execution_authority": False,
            "capture_is_stegverse_standing": False,
            "capture_is_compatibility_proof": False,
            "current_delegation_attached": False,
            "commit_time_authority_reconstructed": False,
        },
        "freshness_context": {
            "manifest_pinned_by_hash": True,
            "input_pinned_by_hash": True,
            "runtime_or_model_version_captured": True,
            "external_configuration_freshness_independently_verified": False,
        },
        "limitations": [
            "single execution",
            "no independent replay yet",
            "no external authority or delegation artifacts attached",
            "output remains framework evidence only",
            *list(manifest.get("limitations", [])),
        ],
        "replay": {
            "version_command": args.version_command,
            "execute_command": args.execute_command,
            "stdin_encoding": "canonical-json-sort-keys-compact-plus-newline",
            "expected_hashes": {
                "manifest_sha256": sha256_bytes(manifest_bytes),
                "input_sha256": sha256_bytes(input_bytes),
            },
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    state = "CAPTURED_UNVERIFIED" if execute_result.returncode == 0 else "CAPTURED_ERROR"
    print(f"EXTERNAL CAPTURE: {state} -> {output_path.relative_to(ROOT)}")
    return execute_result.returncode


if __name__ == "__main__":
    sys.exit(main())
