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
TOOLS = ROOT / ".tmp" / "opa-independent-replay"
UPSTREAM = ROOT / "reports" / "upstream-opa"
OUTPUT = ROOT / "reports" / "external-frameworks" / "opa-independent"
CAPTURE_SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
SUMMARY_SCRIPT = ROOT / "scripts" / "summarize_opa_evidence_pipeline.py"
COMPATIBILITY_SCRIPT = ROOT / "scripts" / "run_opa_governance_compatibility.py"
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
    return subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def emit_result(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)


def write_pipeline_summary() -> int:
    summary_path = OUTPUT / "opa-evidence-pipeline-status.json"
    result = run(
        [
            sys.executable,
            str(SUMMARY_SCRIPT),
            "--capture-root",
            str(UPSTREAM),
            "--replay-root",
            str(OUTPUT),
            "--output",
            str(summary_path),
        ]
    )
    emit_result(result)
    return result.returncode


def run_governance_compatibility() -> int:
    result = run([sys.executable, str(COMPATIBILITY_SCRIPT)])
    emit_result(result)
    return result.returncode


def main() -> int:
    required_upstream = {
        "allow": UPSTREAM / "opa-allow-capture.json",
        "deny": UPSTREAM / "opa-deny-capture.json",
        "receipt": UPSTREAM / "opa-replay-receipt.json",
        "status": UPSTREAM / "opa-capture-status.json",
    }
    missing = [str(path.relative_to(ROOT)) for path in required_upstream.values() if not path.exists()]
    if missing:
        print("OPA INDEPENDENT REPLAY: BLOCKED — missing upstream artifacts", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return 2

    upstream_receipt = load(required_upstream["receipt"])
    upstream_status = load(required_upstream["status"])
    if upstream_receipt.get("replay_state") != "replay_confirmed_same_environment":
        print("OPA INDEPENDENT REPLAY: BLOCKED — upstream same-environment replay not confirmed", file=sys.stderr)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return 2
    upstream_validation_passed = (
        upstream_status.get("capture_state") == "captured_unverified"
        and upstream_status.get("same_environment_replay_state") == "replay_confirmed_same_environment"
        and upstream_status.get("validation_failures") == []
    )
    if not upstream_validation_passed:
        print("OPA INDEPENDENT REPLAY: BLOCKED — upstream capture validation not PASS", file=sys.stderr)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return 2

    binary = TOOLS / OPA_ASSET
    checksum_file = TOOLS / f"{OPA_ASSET}.sha256"
    download(BINARY_URL, binary)
    download(CHECKSUM_URL, checksum_file)
    expected_binary_hash = checksum_file.read_text(encoding="utf-8").strip().split()[0]
    actual_binary_hash = sha256(binary)
    if expected_binary_hash != actual_binary_hash:
        print("OPA INDEPENDENT REPLAY: checksum mismatch", file=sys.stderr)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return 1
    binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    version_result = run([str(binary), "version"])
    if version_result.returncode != 0:
        print(version_result.stderr, file=sys.stderr)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return version_result.returncode
    version_output = version_result.stdout.strip()
    expected_version = OPA_VERSION.removeprefix("v")
    if expected_version not in version_output:
        print(
            f"OPA INDEPENDENT REPLAY: version mismatch expected={expected_version} output={version_output!r}",
            file=sys.stderr,
        )
        OUTPUT.mkdir(parents=True, exist_ok=True)
        write_pipeline_summary()
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    independent_paths: dict[str, Path] = {}
    comparisons: dict[str, dict[str, bool]] = {}
    all_match = True

    for name in ["allow", "deny"]:
        input_path = CAPTURE_DIR / f"input-{name}.json"
        output_path = OUTPUT / f"opa-{name}-independent-replay.json"
        command = [
            sys.executable,
            str(CAPTURE_SCRIPT),
            "--opa",
            str(binary),
            "--input",
            str(input_path),
            "--case-id",
            f"opa-{name}-read-001",
            "--output",
            str(output_path),
        ]
        result = run(command)
        if result.returncode != 0:
            emit_result(result)
            write_pipeline_summary()
            return result.returncode
        independent_paths[name] = output_path

        original = load(required_upstream[name])
        replay = load(output_path)
        checks = {
            "output_match": original.get("output") == replay.get("output"),
            "stdout_hash_match": original.get("hashes", {}).get("stdout_sha256") == replay.get("hashes", {}).get("stdout_sha256"),
            "policy_hash_match": original.get("hashes", {}).get("policy_sha256") == replay.get("hashes", {}).get("policy_sha256"),
            "input_hash_match": original.get("hashes", {}).get("input_sha256") == replay.get("hashes", {}).get("input_sha256"),
            "runtime_version_match": original.get("runtime", {}).get("version") == replay.get("runtime", {}).get("version"),
        }
        checks["case_match"] = all(checks.values())
        comparisons[name] = checks
        all_match = all_match and checks["case_match"]

    receipt = {
        "artifact_type": "external_framework_independent_environment_replay_receipt",
        "schema_version": "0.1",
        "framework_id": "opa",
        "runtime_version_pin": OPA_VERSION,
        "runtime_binary_sha256": actual_binary_hash,
        "runtime_version_output": version_output,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_capture": {
            "github_run_id": upstream_receipt.get("capture_environment", {}).get("github_run_id"),
            "github_sha": upstream_receipt.get("capture_environment", {}).get("github_sha"),
            "runtime_binary_sha256": upstream_receipt.get("runtime_binary_sha256"),
            "same_environment_replay_state": upstream_receipt.get("replay_state"),
            "validation_capture_state": upstream_status.get("capture_state"),
            "validation_failures": upstream_status.get("validation_failures"),
        },
        "independent_environment": {
            "runner": os.environ.get("RUNNER_NAME", "unknown"),
            "os": os.environ.get("RUNNER_OS", sys.platform),
            "architecture": os.environ.get("RUNNER_ARCH", "unknown"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_job": os.environ.get("GITHUB_JOB"),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "fresh_runner_job": True,
            "independent_organization_or_provider": False,
        },
        "comparisons": comparisons,
        "replay_state": "replay_confirmed_independent_environment" if all_match else "replay_mismatch",
        "authority_boundary": {
            "opa_decision_is_execution_authority": False,
            "replay_is_stegverse_standing": False,
            "replay_is_compatibility_proof": False,
            "independent_runner_is_independent_implementation": False,
            "independent_runner_is_independent_authority": False,
        },
        "limitations": [
            "fresh GitHub Actions runner but the same workflow provider and repository",
            "same pinned OPA implementation and version",
            "not an independent implementation, organization, or authority review",
            "matching deterministic output does not establish compatibility or execution authority",
        ],
        "artifacts": {
            name: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
            for name, path in independent_paths.items()
        },
    }
    receipt_path = OUTPUT / "opa-independent-replay-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    if not all_match:
        write_pipeline_summary()
        print(f"OPA INDEPENDENT REPLAY: MISMATCH -> {receipt_path.relative_to(ROOT)}")
        return 1

    compatibility_result = run_governance_compatibility()
    summary_result = write_pipeline_summary()
    if compatibility_result != 0:
        return compatibility_result
    if summary_result != 0:
        return summary_result

    print(f"OPA INDEPENDENT REPLAY: CONFIRMED_FRESH_RUNNER -> {receipt_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())