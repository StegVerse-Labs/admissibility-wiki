#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
ENTITIES = CAPTURE_DIR / "entities.json"
CAPTURE_SCRIPT = ROOT / "scripts" / "capture_cedar_observation.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_cedar_capture_artifacts.py"
REPORTS = ROOT / "reports" / "external-frameworks" / "cedar"
SUMMARY = REPORTS / "cedar-pinned-ci-capture-summary.json"
EXPECTED_COMMIT = "0807ec154afd7ffa14a658c9955d25bfe12770ca"
EXPECTED_CARGO_LOCK_SHA256 = "6efd3893a3c32d463748edfbd8361152e26dd17964d61bbe94cc4a390cd887b1"


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
    parser = argparse.ArgumentParser(description="Execute bounded Cedar fixtures with the exact binary bound by an inspected build receipt.")
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--build-receipt", required=True, type=Path)
    args = parser.parse_args()

    summary = {
        "artifact_type": "cedar_pinned_ci_capture_summary",
        "schema_version": "0.2",
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
        if record.get("execution_authority_ref") != "https://github.com/StegVerse-Labs/admissibility-wiki/issues/63#issuecomment-5227967090":
            return fail(summary, "Cedar bounded execution authority receipt reference mismatch")
        source_ref = str(selection.get("implementation_source", ""))
        if source_ref != f"cedar-policy/cedar@{EXPECTED_COMMIT}":
            return fail(summary, "unexpected Cedar implementation source")
        implementation_id = str(selection.get("implementation_identifier", ""))
        if implementation_id != "cedar-policy-cli":
            return fail(summary, "unexpected implementation identifier")
        promoted_reference_hash = str(selection.get("compiled_binary_sha256", ""))
        receipt = load(args.build_receipt)
    except Exception as exc:
        return fail(summary, f"governed input validation failed: {exc}")

    binary = args.binary.resolve()
    if not binary.exists() or not binary.is_file():
        return fail(summary, "inspected Cedar build binary is unavailable")
    if not ENTITIES.exists() or not ENTITIES.is_file():
        return fail(summary, "Cedar entity-store fixture is unavailable")
    try:
        entities_payload = json.loads(ENTITIES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(summary, f"Cedar entity-store fixture is invalid JSON: {exc}")
    if not isinstance(entities_payload, list):
        return fail(summary, "Cedar entity-store fixture must be a JSON array")

    current_hash = sha256(binary)
    receipt_binary = receipt.get("binary", {})
    checks = {
        "receipt_artifact_type": receipt.get("artifact_type") == "external_framework_selected_binary_build_receipt",
        "receipt_framework": receipt.get("framework_id") == "cedar-policy",
        "receipt_implementation": receipt.get("implementation_identifier") == implementation_id,
        "receipt_pinned_commit": receipt.get("pinned_commit") == EXPECTED_COMMIT,
        "receipt_resolved_commit": receipt.get("resolved_commit") == EXPECTED_COMMIT,
        "receipt_lockfile": receipt.get("cargo_lock_sha256") == EXPECTED_CARGO_LOCK_SHA256,
        "receipt_build_success": receipt.get("build_exit_code") == 0 and receipt.get("overall_status") == "BUILT_HASHED_UNEXECUTED",
        "receipt_hash_matches_exact_binary": receipt_binary.get("sha256") == current_hash,
        "receipt_pre_capture_unexecuted": receipt_binary.get("executed_after_build") is False,
        "receipt_no_external_consequence": receipt.get("authority_boundary", {}).get("external_consequence_allowed") is False,
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        return fail(summary, "exact build receipt predicates failed: " + ", ".join(failed_checks))

    summary["runtime"] = {
        "implementation_id": implementation_id,
        "pinned_commit": EXPECTED_COMMIT,
        "cargo_lock_sha256": EXPECTED_CARGO_LOCK_SHA256,
        "build_receipt_path": str(args.build_receipt),
        "build_receipt_sha256": sha256(args.build_receipt),
        "executed_binary_sha256": current_hash,
        "registry_promoted_reference_sha256": promoted_reference_hash,
        "registry_reference_hash_matches_current_binary": promoted_reference_hash == current_hash,
        "binary_hash_reproducibility_claimed": False,
        "execution_binding": "exact_same_binary_as_inspected_build_receipt",
        "entities_path": str(ENTITIES.relative_to(ROOT)),
        "entities_sha256": sha256(ENTITIES),
    }

    version_command = shlex.join([str(binary), "--version"])
    cases = {
        "allow": CAPTURE_DIR / "request-allow.json",
        "deny": CAPTURE_DIR / "request-deny.json",
    }
    capture_paths: dict[str, str] = {}
    for label, request_path in cases.items():
        request = load(request_path)
        command = [
            str(binary), "authorize",
            "--entities", str(ENTITIES),
            "--policies", "{policy}",
            "--principal", str(request["principal"]),
            "--action", str(request["action"]),
            "--resource", str(request["resource"]),
        ]
        output = REPORTS / f"cedar-{label}-capture.json"
        capture = run([
            sys.executable, str(CAPTURE_SCRIPT),
            "--policy", str(CAPTURE_DIR / "policy.cedar"),
            "--request", str(request_path),
            "--case-id", f"cedar-{label}-read-001",
            "--version-command", version_command,
            "--evaluate-command", shlex.join(command),
            "--implementation-id", implementation_id,
            "--output", str(output),
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
        "the executed binary is exactly the binary hashed by the current inspected build receipt",
        "the registry binary hash is a prior observed build reference and is not treated as a reproducible-build invariant",
        "the explicit entity-store fixture is empty because the retained policy uses only literal entity UIDs and no entity attributes or parents",
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
