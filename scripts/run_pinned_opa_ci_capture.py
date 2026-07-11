#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPA_VERSION = "v1.0.0"
OPA_ASSET = "opa_linux_amd64_static"
BASE_URL = f"https://github.com/open-policy-agent/opa/releases/download/{OPA_VERSION}"
BINARY_URL = f"{BASE_URL}/{OPA_ASSET}"
CHECKSUM_URL = f"{BINARY_URL}.sha256"
TOOLS = ROOT / ".tmp" / "opa-capture"
REPORTS = ROOT / "reports" / "external-frameworks" / "opa"
CAPTURE_SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
CAPTURE_DIR = ROOT / "docs" / "external-frameworks" / "capture" / "opa"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        destination.write_bytes(response.read())


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    binary = TOOLS / OPA_ASSET
    checksum_file = TOOLS / f"{OPA_ASSET}.sha256"
    download(BINARY_URL, binary)
    download(CHECKSUM_URL, checksum_file)

    checksum_text = checksum_file.read_text(encoding="utf-8").strip()
    expected = checksum_text.split()[0]
    actual = sha256(binary)
    if expected != actual:
        print(f"OPA PINNED CAPTURE: checksum mismatch expected={expected} actual={actual}", file=sys.stderr)
        return 1

    binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    version = run([str(binary), "version", "--format=json"])
    if version.returncode != 0:
        print(version.stderr, file=sys.stderr)
        return version.returncode

    REPORTS.mkdir(parents=True, exist_ok=True)
    cases = {
        "allow": CAPTURE_DIR / "input-allow.json",
        "deny": CAPTURE_DIR / "input-deny.json",
    }
    first_paths: dict[str, Path] = {}
    replay_paths: dict[str, Path] = {}

    for name, input_path in cases.items():
        first = REPORTS / f"opa-{name}-capture.json"
        replay = REPORTS / f"opa-{name}-replay.json"
        case_id = f"opa-{name}-read-001"
        base = [
            sys.executable,
            str(CAPTURE_SCRIPT),
            "--opa",
            str(binary),
            "--input",
            str(input_path),
            "--case-id",
            case_id,
        ]
        first_result = run(base + ["--output", str(first)])
        if first_result.returncode != 0:
            print(first_result.stdout)
            print(first_result.stderr, file=sys.stderr)
            return first_result.returncode
        replay_result = run(base + ["--output", str(replay)])
        if replay_result.returncode != 0:
            print(replay_result.stdout)
            print(replay_result.stderr, file=sys.stderr)
            return replay_result.returncode
        first_paths[name] = first
        replay_paths[name] = replay

    comparisons: dict[str, dict] = {}
    all_match = True
    for name in cases:
        first = load(first_paths[name])
        replay = load(replay_paths[name])
        output_match = first.get("output") == replay.get("output")
        stdout_hash_match = first.get("hashes", {}).get("stdout_sha256") == replay.get("hashes", {}).get("stdout_sha256")
        policy_hash_match = first.get("hashes", {}).get("policy_sha256") == replay.get("hashes", {}).get("policy_sha256")
        input_hash_match = first.get("hashes", {}).get("input_sha256") == replay.get("hashes", {}).get("input_sha256")
        case_match = output_match and stdout_hash_match and policy_hash_match and input_hash_match
        all_match = all_match and case_match
        comparisons[name] = {
            "output_match": output_match,
            "stdout_hash_match": stdout_hash_match,
            "policy_hash_match": policy_hash_match,
            "input_hash_match": input_hash_match,
            "case_match": case_match,
        }

    receipt = {
        "artifact_type": "external_framework_replay_receipt",
        "schema_version": "0.1",
        "framework_id": "opa",
        "runtime_version_pin": OPA_VERSION,
        "runtime_binary_sha256": actual,
        "runtime_version_output": json.loads(version.stdout),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "capture_environment": {
            "runner": os.environ.get("RUNNER_NAME", "unknown"),
            "os": os.environ.get("RUNNER_OS", sys.platform),
            "architecture": os.environ.get("RUNNER_ARCH", "unknown"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_sha": os.environ.get("GITHUB_SHA"),
        },
        "capture_files": {name: str(path.relative_to(ROOT)) for name, path in first_paths.items()},
        "replay_files": {name: str(path.relative_to(ROOT)) for name, path in replay_paths.items()},
        "comparisons": comparisons,
        "replay_state": "replay_confirmed_same_environment" if all_match else "replay_mismatch",
        "authority_boundary": {
            "opa_decision_is_execution_authority": False,
            "capture_is_stegverse_standing": False,
            "replay_is_compatibility_proof": False,
            "same_environment_replay_is_independent_replay": False,
        },
        "limitations": [
            "capture and replay occur in separate processes on the same GitHub Actions runner",
            "no independent environment replay has occurred",
            "no current delegation or external authority artifact is attached",
            "matching deterministic output is not compatibility or execution authority",
        ],
    }
    receipt_path = REPORTS / "opa-replay-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    if not all_match:
        print(f"OPA PINNED CAPTURE: REPLAY_MISMATCH -> {receipt_path.relative_to(ROOT)}")
        return 1

    print(f"OPA PINNED CAPTURE: REPLAY_CONFIRMED_SAME_ENVIRONMENT -> {receipt_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
