#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "pages-build-receipt.json"
BUILD_DIR = ROOT / "build"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    build_outcome = os.environ.get("BUILD_OUTCOME", "unknown").strip().lower()
    build_present = BUILD_DIR.is_dir()
    files = sorted(path for path in BUILD_DIR.rglob("*") if path.is_file()) if build_present else []
    manifest_lines = [
        f"{path.relative_to(BUILD_DIR).as_posix()}\t{path.stat().st_size}\t{sha256(path)}"
        for path in files
    ]
    manifest_sha256 = hashlib.sha256(("\n".join(manifest_lines) + ("\n" if manifest_lines else "")).encode("utf-8")).hexdigest()

    success = build_outcome == "success" and build_present and bool(files)
    receipt = {
        "artifact_type": "admissibility_wiki_pages_build_receipt",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "workflow_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "job": os.environ.get("GITHUB_JOB"),
            "event_name": os.environ.get("GITHUB_EVENT_NAME"),
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "ref": os.environ.get("GITHUB_REF"),
            "sha": os.environ.get("GITHUB_SHA"),
        },
        "build": {
            "command": "npm run build",
            "step_outcome": build_outcome,
            "state": "PAGES_BUILD_COMPLETE" if success else "PAGES_BUILD_FAILED_OR_INCOMPLETE",
            "build_directory_present": build_present,
            "file_count": len(files),
            "total_size_bytes": sum(path.stat().st_size for path in files),
            "manifest_sha256": manifest_sha256,
        },
        "deployment_requested": False,
        "deployment_completed": False,
        "public_verification_completed": False,
        "release_authorized": False,
        "authority_boundary": {
            "pages_build_is_deployment_authority": False,
            "pages_build_is_public_verification": False,
            "pages_build_is_release_authority": False,
            "receipt_is_execution_authority": False,
        },
        "required_next_transition": (
            "upload_pages_artifact_then_allow_separate_deployment_job"
            if success
            else "repair_build_failure_and_rebuild_before_deployment"
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"PAGES BUILD RECEIPT: {receipt['build']['state']} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
