#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts/apply_external_chat_activation_observation_status.py"
CANONICAL = ROOT / "static/status/external-chat-activation-observation.json"


def sha(value: dict) -> str:
    material = dict(value)
    material.pop("candidate_sha256", None)
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(candidate: Path, promotion: Path, status: Path, output: Path, apply: bool) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(ENGINE), "--candidate", str(candidate), "--promotion-receipt", str(promotion), "--status", str(status), "--output", str(output)]
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
        "ALLOW_CANONICAL_STATUS_PROMOTION_ONLY",
        "VALIDATED_DRY_RUN",
        "APPLIED_OBSERVED_NON_MUTATING_PUBLIC_PATHS",
        "ALREADY_OBSERVED_NON_MUTATING_PUBLIC_PATHS",
        '"deployment_authorized": False',
        '"repository_mutation_authorized": False',
        '"publication_authorized": False',
        '"certification_created": False',
        '"standing_created": False',
    ):
        if marker not in text:
            failures.append(f"engine missing marker: {marker}")

    if not failures:
        with tempfile.TemporaryDirectory(prefix="external-chat-status-") as td:
            d = Path(td)
            candidate_path = d / "candidate.json"
            promotion_path = d / "promotion.json"
            status_path = d / "status.json"
            dry_path = d / "dry.json"
            apply_path = d / "apply.json"
            repeat_path = d / "repeat.json"
            bad_path = d / "bad.json"

            source = {
                "source_repository": "StegVerse-Labs/Site",
                "source_commit_sha": "a" * 40,
                "source_workflow_run_id": "100",
                "source_workflow_run_attempt": "2",
                "source_evidence_sha256": "b" * 64,
                "mutation_required_disabled": True,
            }
            candidate = {
                "schema_version": "1.0.0",
                "record_type": "external_chat_activation_observation_candidate",
                "generated_at": "2026-07-13T00:00:00+00:00",
                "state": "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE",
                "reason": None,
                "source": source,
                "candidate_effect": {
                    "canonical_status_mutated": False,
                    "deployment_authorized": False,
                    "repository_mutation_authorized": False,
                    "publication_authorized": False,
                    "certification_created": False,
                    "standing_created": False,
                },
                "required_next_transition": "separately_authorized_canonical_status_promotion",
            }
            candidate["candidate_sha256"] = sha(candidate)
            promotion = {
                "schema_version": "1.0.0",
                "receipt_type": "external_chat_activation_status_promotion_receipt",
                "repository": "StegVerse-Labs/admissibility-wiki",
                "source_candidate": {
                    "path": "reports/external-chat-activation-observation-candidate.json",
                    "sha256": candidate["candidate_sha256"],
                    "candidate_state": candidate["state"],
                },
                "source_evidence": {
                    "repository": source["source_repository"],
                    "commit_sha": source["source_commit_sha"],
                    "workflow_run_id": source["source_workflow_run_id"],
                    "workflow_run_attempt": source["source_workflow_run_attempt"],
                    "evidence_sha256": source["source_evidence_sha256"],
                    "mutation_required_disabled": True,
                },
                "decision": "ALLOW_CANONICAL_STATUS_PROMOTION_ONLY",
                "canonical_status_mutation_allowed": True,
                "target_path": "static/status/external-chat-activation-observation.json",
                "authority_boundary": {
                    "promotion_is_deployment_authority": False,
                    "promotion_is_repository_mutation_authority": False,
                    "promotion_is_publication_authority": False,
                    "promotion_is_certification": False,
                    "promotion_creates_standing": False,
                    "mutation_remains_separately_authorized": True,
                },
            }
            candidate_path.write_text(json.dumps(candidate, indent=2) + "\n")
            promotion_path.write_text(json.dumps(promotion, indent=2) + "\n")
            status_path.write_text(CANONICAL.read_text(encoding="utf-8"))

            before = status_path.read_bytes()
            dry = run(candidate_path, promotion_path, status_path, dry_path, False)
            if dry.returncode != 0 or status_path.read_bytes() != before or load(dry_path).get("application_state") != "VALIDATED_DRY_RUN":
                failures.append("dry-run boundary failed")

            applied = run(candidate_path, promotion_path, status_path, apply_path, True)
            if applied.returncode != 0:
                failures.append(f"apply failed: {applied.stdout.strip()}")
            else:
                status = load(status_path)
                result = load(apply_path)
                if status.get("observation_state") != "OBSERVED_NON_MUTATING_PUBLIC_PATHS":
                    failures.append("canonical status did not advance")
                if any(status.get(key) is not False for key in ("deployment_authorized", "repository_mutation_authorized", "publication_authorized", "certification_created", "standing_created")):
                    failures.append("application changed authority boundaries")
                if result.get("application_state") != "APPLIED_OBSERVED_NON_MUTATING_PUBLIC_PATHS":
                    failures.append("application result mismatch")

            repeated = run(candidate_path, promotion_path, status_path, repeat_path, True)
            if repeated.returncode != 0 or load(repeat_path).get("application_state") != "ALREADY_OBSERVED_NON_MUTATING_PUBLIC_PATHS":
                failures.append("idempotent repeat failed")

            promotion["source_evidence"]["workflow_run_attempt"] = "3"
            promotion_path.write_text(json.dumps(promotion, indent=2) + "\n")
            bad = run(candidate_path, promotion_path, status_path, bad_path, False)
            if bad.returncode == 0 or load(bad_path).get("application_state") != "BLOCKED":
                failures.append("run-attempt drift did not fail closed")

    print("EXTERNAL CHAT ACTIVATION STATUS APPLICATION:", "FAIL" if failures else "PASS")
    for item in failures:
        print(f"- {item}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
