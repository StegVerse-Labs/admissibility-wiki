#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "apply_pages_build_verification_status.py"
CANONICAL = ROOT / "static" / "status" / "pages-build-verification.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(binding: Path, promotion: Path, status: Path, output: Path, apply: bool) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(ENGINE), "--artifact-binding", str(binding), "--promotion-receipt", str(promotion), "--status", str(status), "--output", str(output)]
    if apply:
        cmd.append("--apply")
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def main() -> int:
    failures: list[str] = []
    for path in (ENGINE, CANONICAL):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    text = ENGINE.read_text(encoding="utf-8") if ENGINE.exists() else ""
    for marker in (
        "ALLOW_STATUS_PROMOTION_ONLY",
        "PAGES_ARTIFACT_PRESERVED",
        "APPLIED_PAGES_ARTIFACT_PRESERVED",
        "ALREADY_PAGES_ARTIFACT_PRESERVED",
        '"deployment_authorized": False',
        '"public_verification_complete": False',
        '"release_authorized": False',
        '"downstream_propagation_authorized": False',
        "status_application_may_mutate_other_files",
    ):
        if marker not in text:
            failures.append(f"engine missing marker: {marker}")

    if not failures:
        with tempfile.TemporaryDirectory(prefix="pages-status-application-") as td:
            d = Path(td)
            status = d / "status.json"
            binding = d / "binding.json"
            promotion = d / "promotion.json"
            dry_result = d / "dry.json"
            apply_result = d / "apply.json"
            repeat_result = d / "repeat.json"
            bad_result = d / "bad.json"

            status.write_text(CANONICAL.read_text(encoding="utf-8"), encoding="utf-8")
            candidate_hash = "a" * 64
            artifact_digest = "sha256:" + "b" * 64
            binding_payload = {
                "schema_version": "0.1",
                "receipt_type": "pages_artifact_binding_receipt",
                "repository": "StegVerse-Labs/admissibility-wiki",
                "target_commit": "c" * 40,
                "source_candidate": {
                    "path": "reports/pages-build-verification-candidate.json",
                    "sha256": candidate_hash,
                    "verification_state": "PAGES_BUILD_PASS_ARTIFACT_PENDING",
                    "build_manifest_sha256": "d" * 64,
                },
                "observed_workflow": {"run_id": 100, "job_id": 200, "run_attempt": 1},
                "artifact": {"name": "github-pages", "artifact_id": 300, "artifact_digest": artifact_digest, "preserved": True},
                "verification_state": "PAGES_ARTIFACT_PRESERVED",
                "canonical_status_mutation_applied": False,
                "deployment_authorized": False,
                "public_verification_complete": False,
                "release_authorized": False,
                "downstream_propagation_authorized": False,
                "required_next_transition": "apply_observed_pages_artifact_evidence_to_canonical_status_in_separate_governed_commit",
                "non_claims": ["a", "b", "c", "d", "e", "f"],
            }
            promotion_payload = {
                "schema_version": "0.1",
                "receipt_type": "pages_build_status_promotion_receipt",
                "repository": "StegVerse-Labs/admissibility-wiki",
                "source_candidate": {"path": "reports/pages-build-verification-candidate.json", "sha256": candidate_hash},
                "formalism_validator_evidence": {"status": "PASS", "evidence_ref": "fixture://formalism-pass"},
                "pages_artifact_evidence": {"status": "PASS", "run_id": 100, "job_id": 200, "artifact_id": 300, "artifact_digest": artifact_digest, "evidence_ref": "fixture://pages-artifact"},
                "decision": "ALLOW_STATUS_PROMOTION_ONLY",
                "canonical_status_mutation_allowed": True,
                "deployment_authorized": False,
                "public_verification_complete": False,
                "non_claims": ["a", "b", "c", "d", "e"],
            }
            binding.write_text(json.dumps(binding_payload, indent=2) + "\n", encoding="utf-8")
            promotion.write_text(json.dumps(promotion_payload, indent=2) + "\n", encoding="utf-8")

            before = status.read_bytes()
            dry = run(binding, promotion, status, dry_result, False)
            if dry.returncode != 0 or status.read_bytes() != before or load(dry_result).get("application_state") != "VALIDATED_DRY_RUN":
                failures.append("dry-run boundary failed")

            applied = run(binding, promotion, status, apply_result, True)
            if applied.returncode != 0:
                failures.append(f"apply failed: {applied.stdout.strip()}")
            else:
                updated = load(status)
                result = load(apply_result)
                if updated.get("verification_state") != "PAGES_ARTIFACT_PRESERVED":
                    failures.append("status did not advance to PAGES_ARTIFACT_PRESERVED")
                if updated.get("deployment_authorized") is not False or updated.get("public_verification_complete") is not False:
                    failures.append("status application changed authority boundaries")
                if result.get("application_state") != "APPLIED_PAGES_ARTIFACT_PRESERVED":
                    failures.append("apply result state mismatch")

            repeated = run(binding, promotion, status, repeat_result, True)
            if repeated.returncode != 0 or load(repeat_result).get("application_state") != "ALREADY_PAGES_ARTIFACT_PRESERVED":
                failures.append("idempotent repeat failed")

            promotion_payload["pages_artifact_evidence"]["artifact_id"] = 301
            promotion.write_text(json.dumps(promotion_payload, indent=2) + "\n", encoding="utf-8")
            bad = run(binding, promotion, status, bad_result, False)
            if bad.returncode == 0 or load(bad_result).get("application_state") != "BLOCKED":
                failures.append("mismatched artifact evidence did not fail closed")

    print("PAGES BUILD VERIFICATION STATUS APPLICATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
