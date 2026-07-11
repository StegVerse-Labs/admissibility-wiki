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
CAPTURE_DIR = ROOT / "docs" / "external-frameworks" / "capture" / "cedar"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "cedar-observation-capture.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def expand_command(template: str, policy: Path, request: Path) -> list[str]:
    expanded = template.format(policy=str(policy), request=str(request))
    return shlex.split(expanded)


def parse_json_or_raw(text: str) -> Any:
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture an exact, non-authorizing Cedar authorization observation receipt.")
    parser.add_argument("--policy", default=str(CAPTURE_DIR / "policy.cedar"))
    parser.add_argument("--request", default=str(CAPTURE_DIR / "request-allow.json"))
    parser.add_argument("--case-id", default="cedar-allow-read-001")
    parser.add_argument("--version-command", required=True, help="Command that prints the exact Cedar runtime or implementation version")
    parser.add_argument(
        "--evaluate-command",
        required=True,
        help="Authorization command template. Use {policy} and {request} placeholders.",
    )
    parser.add_argument("--implementation-id", required=True, help="Exact Cedar implementation or CLI identifier")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    policy = Path(args.policy).resolve()
    request = Path(args.request).resolve()
    output_path = Path(args.output).resolve()
    for required in [policy, request]:
        if not required.exists():
            print(f"CEDAR CAPTURE: BLOCKED — missing {required}", file=sys.stderr)
            return 2

    version_cmd = shlex.split(args.version_command)
    eval_cmd = expand_command(args.evaluate_command, policy, request)
    if not version_cmd or not eval_cmd:
        print("CEDAR CAPTURE: BLOCKED — empty command", file=sys.stderr)
        return 2

    version_result = run(version_cmd)
    if version_result.returncode != 0:
        print("CEDAR CAPTURE: BLOCKED — version command failed", file=sys.stderr)
        print(version_result.stderr, file=sys.stderr)
        return version_result.returncode or 2

    eval_result = run(eval_cmd)
    captured_at = datetime.now(timezone.utc).isoformat()
    policy_bytes = policy.read_bytes()
    request_bytes = request.read_bytes()
    stdout_bytes = eval_result.stdout.encode("utf-8")
    stderr_bytes = eval_result.stderr.encode("utf-8")

    receipt = {
        "artifact_type": "external_framework_observed_evidence_capture",
        "schema_version": "0.1",
        "framework_id": "cedar-policy",
        "case_id": args.case_id,
        "capture_state": "captured_unverified",
        "captured_at_utc": captured_at,
        "runtime": {
            "implementation_id": args.implementation_id,
            "version_command": version_cmd,
            "version_output": parse_json_or_raw(version_result.stdout),
            "evaluate_command": eval_cmd,
            "exit_code": eval_result.returncode,
        },
        "source": {
            "canonical_reference": "https://docs.cedarpolicy.com/",
            "policy_path": str(policy.relative_to(ROOT)),
            "request_path": str(request.relative_to(ROOT)),
        },
        "input": json.loads(request_bytes.decode("utf-8")),
        "output": parse_json_or_raw(eval_result.stdout),
        "stderr": eval_result.stderr,
        "hashes": {
            "policy_sha256": sha256_bytes(policy_bytes),
            "request_sha256": sha256_bytes(request_bytes),
            "stdout_sha256": sha256_bytes(stdout_bytes),
            "stderr_sha256": sha256_bytes(stderr_bytes),
        },
        "authority_context": {
            "cedar_decision_is_execution_authority": False,
            "capture_is_stegverse_standing": False,
            "capture_is_compatibility_proof": False,
            "current_delegation_attached": False,
            "commit_time_authority_reconstructed": False,
        },
        "freshness_context": {
            "policy_pinned_by_hash": True,
            "request_pinned_by_hash": True,
            "runtime_version_captured": True,
            "external_policy_freshness_independently_verified": False,
        },
        "limitations": [
            "implementation-neutral command adapter; caller must identify the exact Cedar implementation",
            "single local execution",
            "no independent replay yet",
            "no external authority or delegation artifacts attached",
            "authorization output is evidence only and does not bind consequence",
        ],
        "replay": {
            "version_command": version_cmd,
            "evaluate_command": eval_cmd,
            "required_files": [str(policy.relative_to(ROOT)), str(request.relative_to(ROOT))],
            "expected_hashes": {
                "policy_sha256": sha256_bytes(policy_bytes),
                "request_sha256": sha256_bytes(request_bytes),
            },
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    if eval_result.returncode != 0:
        print(f"CEDAR CAPTURE: CAPTURED ERROR -> {output_path.relative_to(ROOT)}")
        return eval_result.returncode

    print(f"CEDAR CAPTURE: CAPTURED_UNVERIFIED -> {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
