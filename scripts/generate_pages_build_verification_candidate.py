#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILD_RECEIPT = ROOT / "reports" / "pages-build-receipt.json"
OUTPUT = ROOT / "reports" / "pages-build-verification-candidate.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Pages build receipt must contain a JSON object")
    return payload


def main() -> int:
    failures: list[str] = []
    receipt: dict[str, Any] = {}
    try:
        receipt = load(BUILD_RECEIPT)
    except Exception as exc:
        failures.append(f"receipt invalid: {exc}")

    workflow = receipt.get("workflow_context", {}) if receipt else {}
    build = receipt.get("build", {}) if receipt else {}
    boundary = receipt.get("authority_boundary", {}) if receipt else {}

    if receipt:
        if receipt.get("artifact_type") != "admissibility_wiki_pages_build_receipt":
            failures.append("artifact_type mismatch")
        if receipt.get("schema_version") != "0.1":
            failures.append("schema_version mismatch")
        for field in ("run_id", "run_attempt", "workflow", "job", "repository", "ref", "sha"):
            if not workflow.get(field):
                failures.append(f"workflow_context.{field} missing")
        if workflow.get("repository") != "StegVerse-Labs/admissibility-wiki":
            failures.append("workflow repository mismatch")
        if build.get("command") != "npm run build":
            failures.append("build command mismatch")
        if build.get("step_outcome") != "success":
            failures.append("build step did not succeed")
        if build.get("state") != "PAGES_BUILD_COMPLETE":
            failures.append("build state is not PAGES_BUILD_COMPLETE")
        if build.get("build_directory_present") is not True:
            failures.append("build directory was not preserved")
        if not isinstance(build.get("file_count"), int) or build.get("file_count", 0) <= 0:
            failures.append("build file count missing or invalid")
        if not isinstance(build.get("total_size_bytes"), int) or build.get("total_size_bytes", 0) <= 0:
            failures.append("build byte count missing or invalid")
        if not HEX64.fullmatch(str(build.get("manifest_sha256", ""))):
            failures.append("build manifest sha256 missing or malformed")
        for key in ("deployment_requested", "deployment_completed", "public_verification_completed", "release_authorized"):
            if receipt.get(key) is not False:
                failures.append(f"{key} must remain false")
        for key in (
            "pages_build_is_deployment_authority",
            "pages_build_is_public_verification",
            "pages_build_is_release_authority",
            "receipt_is_execution_authority",
        ):
            if boundary.get(key) is not False:
                failures.append(f"authority_boundary.{key} must remain false")

    valid = not failures
    candidate = {
        "artifact_type": "pages_build_verification_candidate",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "target_commit": workflow.get("sha"),
        "source_build_receipt": {
            "path": "reports/pages-build-receipt.json",
            "sha256": sha256(BUILD_RECEIPT) if BUILD_RECEIPT.exists() else None,
        },
        "verification_state": "PAGES_BUILD_PASS_ARTIFACT_PENDING" if valid else "FAIL_CLOSED",
        "required_checks": {
            "formalism_publication_validator": {
                "status": "REVIEW_REQUIRED" if valid else "UNVERIFIED",
                "evidence_ref": None,
            },
            "docusaurus_production_build": {
                "status": "PASS" if valid else "FAIL",
                "evidence_ref": "reports/pages-build-receipt.json" if valid else None,
            },
            "pages_artifact_upload": {
                "status": "PENDING" if valid else "BLOCKED",
                "evidence_ref": None,
            },
        },
        "observed_workflow": {
            "run_id": workflow.get("run_id"),
            "job": workflow.get("job"),
            "run_attempt": workflow.get("run_attempt"),
        },
        "build_evidence": {
            "manifest_sha256": build.get("manifest_sha256"),
            "file_count": build.get("file_count"),
            "total_size_bytes": build.get("total_size_bytes"),
            "step_outcome": build.get("step_outcome"),
        },
        "candidate_only": True,
        "status_mutation_performed": False,
        "deployment_authorized": False,
        "public_verification_complete": False,
        "release_authorized": False,
        "downstream_propagation_authorized": False,
        "failures": failures,
        "required_next_transition": (
            "attach_formalism_validator_and_pages_artifact_evidence_then_apply_status_in_separate_governed_commit"
            if valid
            else "repair_build_failure_and_repeat_canonical_build"
        ),
        "non_claims": [
            "candidate generation does not mutate canonical status",
            "build receipt does not prove formalism validator success",
            "build receipt does not prove Pages artifact upload",
            "Pages build success is not deployment authority",
            "Pages artifact upload is not public verification",
            "candidate validation does not authorize release or downstream propagation",
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print(f"PAGES BUILD VERIFICATION CANDIDATE: {candidate['verification_state']} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
