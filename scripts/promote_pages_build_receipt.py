#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "reports" / "pages-build-receipt.json"
DEFAULT_OUTPUT = ROOT / "reports" / "pages-build-verification-promotion-candidate.json"
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
    parser = argparse.ArgumentParser(description="Validate a durable Pages build receipt and emit a non-mutating verification promotion candidate.")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    failures: list[str] = []
    receipt: dict[str, Any] = {}
    try:
        receipt = load(args.receipt)
    except Exception as exc:
        failures.append(f"receipt invalid: {exc}")

    context = receipt.get("workflow_context", {}) if receipt else {}
    build = receipt.get("build", {}) if receipt else {}
    boundary = receipt.get("authority_boundary", {}) if receipt else {}

    required_context = ["run_id", "run_attempt", "workflow", "job", "repository", "ref", "sha"]
    if receipt:
        if receipt.get("artifact_type") != "admissibility_wiki_pages_build_receipt":
            failures.append("artifact_type mismatch")
        if receipt.get("schema_version") != "0.1":
            failures.append("schema_version mismatch")
        for field in required_context:
            if not context.get(field):
                failures.append(f"workflow_context.{field} missing")
        if context.get("repository") != "StegVerse-Labs/admissibility-wiki":
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
        "artifact_type": "pages_build_verification_promotion_candidate",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "source_build_receipt": {
            "path": str(args.receipt),
            "sha256": sha256(args.receipt) if args.receipt.exists() else None,
        },
        "candidate_state": "READY_FOR_PAGES_VERIFICATION_REVIEW" if valid else "BLOCKED_INVALID_BUILD_RECEIPT",
        "proposed_verification_state": "PAGES_BUILD_PASS_ARTIFACT_PENDING" if valid else "FAIL_CLOSED",
        "observed_workflow": {
            "run_id": context.get("run_id"),
            "run_attempt": context.get("run_attempt"),
            "job": context.get("job"),
            "commit": context.get("sha"),
        },
        "required_checks": {
            "formalism_publication_validator": {
                "status": "REVIEW_REQUIRED",
                "evidence_ref": None,
            },
            "docusaurus_production_build": {
                "status": "PASS" if valid else "FAIL",
                "evidence_ref": str(args.receipt) if valid else None,
                "manifest_sha256": build.get("manifest_sha256"),
                "file_count": build.get("file_count"),
                "total_size_bytes": build.get("total_size_bytes"),
            },
            "pages_artifact_upload": {
                "status": "PENDING",
                "evidence_ref": None,
            },
        },
        "status_mutation_performed": False,
        "deployment_authorized": False,
        "public_verification_complete": False,
        "release_authorized": False,
        "downstream_propagation_authorized": False,
        "failures": failures,
        "required_next_transition": (
            "attach_formalism_validator_and_pages_artifact_evidence_then_apply_status_in_separate_governed_commit"
            if valid
            else "repair_or_replace_build_receipt_before_verification_promotion"
        ),
        "authority_boundary": {
            "promotion_candidate_is_pages_artifact_evidence": False,
            "promotion_candidate_is_deployment_authority": False,
            "promotion_candidate_is_public_verification": False,
            "promotion_candidate_is_release_authority": False,
            "promotion_candidate_may_mutate_status": False,
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print(f"PAGES BUILD RECEIPT PROMOTION: {candidate['candidate_state']} -> {args.output}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
