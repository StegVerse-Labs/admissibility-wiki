#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / "docs" / "external-frameworks" / "capture" / "opa"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "opa-observation-capture.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture an exact, non-authorizing OPA observation receipt.")
    parser.add_argument("--opa", default="opa", help="OPA executable path")
    parser.add_argument("--policy", default=str(CAPTURE_DIR / "policy.rego"))
    parser.add_argument("--input", default=str(CAPTURE_DIR / "input-allow.json"))
    parser.add_argument("--query", default="data.stegverse.capture")
    parser.add_argument("--case-id", default="opa-allow-read-001")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    opa_path = shutil.which(args.opa) if Path(args.opa).name == args.opa else args.opa
    if not opa_path or not Path(opa_path).exists():
        print("OPA CAPTURE: BLOCKED — executable not found", file=sys.stderr)
        return 2

    policy = Path(args.policy).resolve()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    for required in [policy, input_path]:
        if not required.exists():
            print(f"OPA CAPTURE: BLOCKED — missing {required}", file=sys.stderr)
            return 2

    version_result = run([str(opa_path), "version", "--format=json"])
    if version_result.returncode != 0:
        print(version_result.stderr, file=sys.stderr)
        return version_result.returncode

    eval_cmd = [
        str(opa_path),
        "eval",
        "--format=json",
        "--data",
        str(policy),
        "--input",
        str(input_path),
        args.query,
    ]
    eval_result = run(eval_cmd)

    captured_at = datetime.now(timezone.utc).isoformat()
    policy_bytes = read_bytes(policy)
    input_bytes = read_bytes(input_path)
    stdout_bytes = eval_result.stdout.encode("utf-8")
    stderr_bytes = eval_result.stderr.encode("utf-8")

    try:
        version_payload: Any = json.loads(version_result.stdout)
    except json.JSONDecodeError:
        version_payload = {"raw": version_result.stdout}

    try:
        output_payload: Any = json.loads(eval_result.stdout) if eval_result.stdout else None
    except json.JSONDecodeError:
        output_payload = {"raw": eval_result.stdout}

    receipt = {
        "artifact_type": "external_framework_observed_evidence_capture",
        "schema_version": "0.1",
        "framework_id": "opa",
        "case_id": args.case_id,
        "capture_state": "captured_unverified",
        "captured_at_utc": captured_at,
        "runtime": {
            "executable": str(opa_path),
            "version": version_payload,
            "command": eval_cmd,
            "exit_code": eval_result.returncode,
        },
        "source": {
            "canonical_reference": "https://www.openpolicyagent.org/docs",
            "policy_path": str(policy.relative_to(ROOT)),
            "input_path": str(input_path.relative_to(ROOT)),
            "query": args.query,
        },
        "input": json.loads(input_bytes.decode("utf-8")),
        "output": output_payload,
        "stderr": eval_result.stderr,
        "hashes": {
            "policy_sha256": sha256_bytes(policy_bytes),
            "input_sha256": sha256_bytes(input_bytes),
            "stdout_sha256": sha256_bytes(stdout_bytes),
            "stderr_sha256": sha256_bytes(stderr_bytes),
        },
        "authority_context": {
            "opa_decision_is_execution_authority": False,
            "capture_is_stegverse_standing": False,
            "capture_is_compatibility_proof": False,
            "current_delegation_attached": False,
            "commit_time_authority_reconstructed": False,
        },
        "freshness_context": {
            "policy_version_pinned_by_hash": True,
            "input_pinned_by_hash": True,
            "runtime_version_captured": True,
            "external_policy_freshness_independently_verified": False,
        },
        "limitations": [
            "single local execution",
            "no independent replay yet",
            "no external authority or delegation artifacts attached",
            "OPA output is policy-decision evidence only",
        ],
        "replay": {
            "command": eval_cmd,
            "required_files": [str(policy.relative_to(ROOT)), str(input_path.relative_to(ROOT))],
            "expected_hashes": {
                "policy_sha256": sha256_bytes(policy_bytes),
                "input_sha256": sha256_bytes(input_bytes),
            },
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    if eval_result.returncode != 0:
        print(f"OPA CAPTURE: CAPTURED ERROR -> {output_path.relative_to(ROOT)}")
        return eval_result.returncode

    print(f"OPA CAPTURE: CAPTURED_UNVERIFIED -> {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
