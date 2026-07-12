#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "reports" / "external-frameworks" / "cedar-build"
OUTPUT = OUTPUT_DIR / "cedar-binary-build-receipt.json"
REPOSITORY = "https://github.com/cedar-policy/cedar.git"
COMMIT = "0807ec154afd7ffa14a658c9955d25bfe12770ca"
VERSION = "4.11.0"
BUILD_COMMAND = ["cargo", "build", "--locked", "--release", "-p", "cedar-policy-cli"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    failures: list[str] = []
    checkout_sha: str | None = None
    binary_sha256: str | None = None
    binary_size: int | None = None
    cargo_lock_sha256: str | None = None
    build_stdout = ""
    build_stderr = ""
    build_exit_code: int | None = None

    with tempfile.TemporaryDirectory(prefix="cedar-build-") as temporary:
        work = Path(temporary) / "cedar"
        clone = run(["git", "clone", "--filter=blob:none", "--no-checkout", REPOSITORY, str(work)])
        if clone.returncode != 0:
            failures.append("canonical repository clone failed")
        else:
            checkout = run(["git", "checkout", "--detach", COMMIT], cwd=work)
            if checkout.returncode != 0:
                failures.append("pinned commit checkout failed")
            else:
                resolved = run(["git", "rev-parse", "HEAD"], cwd=work)
                checkout_sha = resolved.stdout.strip() if resolved.returncode == 0 else None
                if checkout_sha != COMMIT:
                    failures.append("resolved checkout does not match pinned commit")

                lockfile = work / "Cargo.lock"
                if not lockfile.exists():
                    failures.append("Cargo.lock missing at pinned commit")
                else:
                    cargo_lock_sha256 = sha256(lockfile)

                if not failures:
                    build = run(BUILD_COMMAND, cwd=work)
                    build_stdout = build.stdout
                    build_stderr = build.stderr
                    build_exit_code = build.returncode
                    if build.returncode != 0:
                        failures.append("locked release build failed")
                    else:
                        binary = work / "target" / "release" / "cedar"
                        if not binary.exists():
                            failures.append("cedar binary missing after build")
                        else:
                            binary_sha256 = sha256(binary)
                            binary_size = binary.stat().st_size

    receipt = {
        "artifact_type": "external_framework_selected_binary_build_receipt",
        "schema_version": "0.1",
        "framework_id": "cedar-policy",
        "implementation_identifier": "cedar-policy-cli",
        "selection_version": VERSION,
        "canonical_repository": REPOSITORY,
        "pinned_commit": COMMIT,
        "resolved_commit": checkout_sha,
        "build_started_at_utc": started,
        "build_completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "build_environment": {
            "runner_os": os.environ.get("RUNNER_OS"),
            "runner_arch": os.environ.get("RUNNER_ARCH"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "rustc_path": shutil.which("rustc"),
            "cargo_path": shutil.which("cargo"),
        },
        "build_command": " ".join(BUILD_COMMAND),
        "build_exit_code": build_exit_code,
        "cargo_lock_sha256": cargo_lock_sha256,
        "binary": {
            "name": "cedar",
            "sha256": binary_sha256,
            "size_bytes": binary_size,
            "executed_after_build": False,
        },
        "build_stdout": build_stdout,
        "build_stderr": build_stderr,
        "overall_status": "BUILT_HASHED_UNEXECUTED" if not failures else "BUILD_FAILED",
        "failures": failures,
        "authority_boundary": {
            "binary_build_is_execution_authority": False,
            "binary_hash_is_compatibility_proof": False,
            "binary_was_used_for_authorization_decision": False,
            "runtime_execution_authorized": False,
            "external_consequence_allowed": False,
        },
        "required_next_transition": "inspect_binary_build_receipt_then_attach_separate_authority_and_consequence_boundary_review",
    }
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR SELECTED BINARY BUILD: {receipt['overall_status']} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
