#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
CAPTURE_DIR = ROOT / "docs" / "external-frameworks" / "capture" / "cedar"
CAPTURE_SCRIPT = ROOT / "scripts" / "capture_cedar_observation.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_cedar_capture_artifacts.py"
WORK = ROOT / ".tmp" / "cedar-capture"
SOURCE = WORK / "cedar"
REPORTS = ROOT / "reports" / "external-frameworks" / "cedar"
SUMMARY = REPORTS / "cedar-pinned-ci-capture-summary.json"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def cedar_record(registry: dict) -> dict:
    matches = [x for x in registry.get("frameworks", []) if isinstance(x, dict) and x.get("framework_id") == "cedar-policy"]
    if len(matches) != 1:
        raise ValueError("registry must contain exactly one cedar-policy record")
    return matches[0]


def fail(summary: dict, message: str) -> int:
    summary["capture_state"] = "BLOCKED_FAIL_CLOSED"
    summary.setdefault("failures", []).append(message)
    REPORTS.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR PINNED CI CAPTURE: BLOCKED_FAIL_CLOSED - {message}", file=sys.stderr)
    return 1


def main() -> int:
    summary = {
        "artifact_type": "cedar_pinned_ci_capture_summary",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "framework_id": "cedar-policy",
        "capture_state": "STARTED",
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "authority_boundary": {
            "repository_local_test_execution_only": True,
            "credentials_permitted": False,
            "external_writes_permitted": False,
            "external_consequence_allowed": False,
            "cedar_decision_is_execution_authority": False,
            "capture_is_compatibility_proof": False,
            "capture_creates_standing": False,
            "certification_claimed": False,
        },
        "failures": [],
    }

    try:
        registry = load(REGISTRY)
        record = cedar_record(registry)
        selection = record.get("selection", {})
        if record.get("execution_authorized") is not True:
            return fail(summary, "cedar-policy repository-local capture execution is not authorized in the registry")
        if registry.get("gate", {}).get("execution_jobs_may_be_added") is not True:
            return fail(summary, "registry execution_jobs_may_be_added gate is not enabled")
        source_ref = str(selection.get("implementation_source", ""))
        if not source_ref.startswith("cedar-policy/cedar@"):
            return fail(summary, "unexpected Cedar implementation source")
        commit = source_ref.split("@", 1)[1]
        expected_binary_hash = str(selection.get("compiled_binary_sha256", ""))
        if len(expected_binary_hash) != 64:
            return fail(summary, "missing canonical compiled binary SHA-256")
        implementation_id = str(selection.get("implementation_identifier", ""))
        if implementation_id != "cedar-policy-cli":
            return fail(summary, "unexpected implementation identifier")
    except Exception as exc:
        return fail(summary, f"registry validation failed: {exc}")

    WORK.mkdir(parents=True, exist_ok=True)
    if SOURCE.exists():
        cleanup = run(["rm", "-rf", str(SOURCE)])
        if cleanup.returncode != 0:
            return fail(summary, "could not reset Cedar source workspace")

    clone = run(["git", "clone", "--filter=blob:none", "https://github.com/cedar-policy/cedar.git", str(SOURCE)])
    if clone.returncode != 0:
        return fail(summary, f"source clone failed: {clone.stderr.strip()}")
    checkout = run(["git", "checkout", commit], cwd=SOURCE)
    if checkout.returncode != 0:
        return fail(summary, f"pinned source checkout failed: {checkout.stderr.strip()}")
    resolved = run(["git", "rev-parse", "HEAD"], cwd=SOURCE)
    if resolved.returncode != 0 or resolved.stdout.strip() != commit:
        return fail(summary, "resolved Cedar source commit does not equal the registry pin")

    build = run(["cargo", "build", "--locked", "--release", "-p", "cedar-policy-cli"], cwd=SOURCE)
    if build.returncode != 0:
        return fail(summary, f"locked Cedar build failed: {build.stderr[-4000:]}")
    binary = SOURCE / "target" / "release" / "cedar"
    if not binary.exists():
        return fail(summary, "built Cedar CLI binary not found")
    actual_binary_hash = sha256(binary)
    summary["runtime"] = {
        "implementation_id": implementation_id,
        "pinned_commit": commit,
        "resolved_commit": resolved.stdout.strip(),
        "expected_binary_sha256": expected_binary_hash,
        "observed_binary_sha256": actual_binary_hash,
        "binary_hash_match": actual_binary_hash == expected_binary_hash,
        "build_command": "cargo build --locked --release -p cedar-policy-cli",
    }
    if actual_binary_hash != expected_binary_hash:
        return fail(summary, "rebuilt Cedar binary hash does not match the governed registry hash")

    version_command = shlex.join([str(binary), "--version"])
    cases = {
        "allow": CAPTURE_DIR / "request-allow.json",
        "deny": CAPTURE_DIR / "request-deny.json",
    }
    capture_paths: dict[str, str] = {}
    for label, request_path in cases.items():
        request = load(request_path)
        command = [
            str(binary),
            "authorize",
            "--policies",
            "{policy}",
            "--principal",
            str(request["principal"]),
            "--action",
            str(request["action"]),
            "--resource",
            str(request["resource"]),
        ]
        evaluate_command = shlex.join(command)
        output = REPORTS / f"cedar-{label}-capture.json"
        capture = run([
            sys.executable,
            str(CAPTURE_SCRIPT),
            "--policy",
            str(CAPTURE_DIR / "policy.cedar"),
            "--request",
            str(request_path),
            "--case-id",
            f"cedar-{label}-read-001",
            "--version-command",
            version_command,
            "--evaluate-command",
            evaluate_command,
            "--implementation-id",
            implementation_id,
            "--output",
            str(output),
        ])
        if capture.returncode != 0:
            return fail(summary, f"{label} capture failed: {(capture.stdout + capture.stderr)[-4000:]}")
        capture_paths[label] = str(output.relative_to(ROOT))

    validate = run([sys.executable, str(VALIDATE_SCRIPT)])
    summary["captures"] = capture_paths
    summary["capture_validation_exit_code"] = validate.returncode
    summary["capture_validation_output"] = (validate.stdout + validate.stderr)[-4000:]
    if validate.returncode != 0:
        return fail(summary, "Cedar capture artifact validation failed")

    summary["capture_state"] = "CAPTURED_VALIDATED_BOUNDED"
    summary["limitations"] = [
        "native Cedar authorization execution is confined to repository fixtures on a GitHub-hosted CI runner",
        "no same-environment or fresh-runner replay is claimed by this transition",
        "no independent implementation/provider reproduction is claimed",
        "native authorization output is evidence only and does not bind consequence",
        "StegVerse governance compatibility remains a separate transition",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR PINNED CI CAPTURE: CAPTURED_VALIDATED_BOUNDED -> {SUMMARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
