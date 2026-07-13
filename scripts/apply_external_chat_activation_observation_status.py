#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "reports/external-chat-activation-observation-candidate.json"
DEFAULT_STATUS = ROOT / "static/status/external-chat-activation-observation.json"
DEFAULT_RESULT = ROOT / "reports/external-chat-activation-status-application.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_hash(value: dict[str, Any], field: str) -> str:
    material = dict(value)
    material.pop(field, None)
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def blocked(output: Path, reason: str) -> int:
    write(output, {
        "schema_version": "1.0.0",
        "record_type": "external_chat_activation_status_application",
        "application_state": "BLOCKED",
        "reason": reason,
        "canonical_status_mutated": False,
        "authority_boundary": {
            "application_is_deployment_authority": False,
            "application_is_repository_mutation_authority": False,
            "application_is_publication_authority": False,
            "application_is_certification": False,
            "application_creates_standing": False,
        },
    })
    print(f"EXTERNAL CHAT ACTIVATION STATUS APPLICATION: BLOCKED - {reason}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--promotion-receipt", type=Path, required=True)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        candidate = load(args.candidate)
        promotion = load(args.promotion_receipt)
        status = load(args.status)
    except Exception as exc:
        return blocked(args.output, f"input load failed: {exc}")

    candidate_hash = canonical_hash(candidate, "candidate_sha256")
    if candidate.get("candidate_sha256") != candidate_hash:
        return blocked(args.output, "candidate hash does not recompute")
    if candidate.get("state") != "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE":
        return blocked(args.output, "candidate is not observed non-mutating public paths")
    if promotion.get("receipt_type") != "external_chat_activation_status_promotion_receipt":
        return blocked(args.output, "promotion receipt type mismatch")
    if promotion.get("decision") != "ALLOW_CANONICAL_STATUS_PROMOTION_ONLY":
        return blocked(args.output, "promotion decision does not allow canonical status promotion")
    if promotion.get("canonical_status_mutation_allowed") is not True:
        return blocked(args.output, "canonical status mutation not allowed")
    if promotion.get("target_path") != "static/status/external-chat-activation-observation.json":
        return blocked(args.output, "promotion target path mismatch")

    source_candidate = promotion.get("source_candidate", {})
    source_evidence = promotion.get("source_evidence", {})
    source = candidate.get("source", {})
    if source_candidate.get("sha256") != candidate_hash:
        return blocked(args.output, "promotion candidate hash drift")
    if source_candidate.get("candidate_state") != candidate.get("state"):
        return blocked(args.output, "promotion candidate state drift")
    comparisons = {
        "repository": source.get("source_repository"),
        "commit_sha": source.get("source_commit_sha"),
        "workflow_run_id": str(source.get("source_workflow_run_id")),
        "workflow_run_attempt": str(source.get("source_workflow_run_attempt")),
        "evidence_sha256": source.get("source_evidence_sha256"),
        "mutation_required_disabled": source.get("mutation_required_disabled"),
    }
    for key, expected in comparisons.items():
        if source_evidence.get(key) != expected:
            return blocked(args.output, f"promotion source evidence drift: {key}")
    if source_evidence.get("mutation_required_disabled") is not True:
        return blocked(args.output, "mutation-disabled predicate missing")

    if status.get("status_type") != "external_chat_activation_observation":
        return blocked(args.output, "canonical status type mismatch")
    already = (
        status.get("observation_state") == "OBSERVED_NON_MUTATING_PUBLIC_PATHS"
        and status.get("source_candidate_sha256") == candidate_hash
        and status.get("source_evidence_sha256") == source_evidence.get("evidence_sha256")
    )
    application_state = "ALREADY_OBSERVED_NON_MUTATING_PUBLIC_PATHS" if already else "VALIDATED_DRY_RUN"

    if args.apply and not already:
        updated = {
            "schema_version": "1.0.0",
            "status_type": "external_chat_activation_observation",
            "observation_state": "OBSERVED_NON_MUTATING_PUBLIC_PATHS",
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "source_repository": source_evidence["repository"],
            "source_commit_sha": source_evidence["commit_sha"],
            "source_workflow_run_id": source_evidence["workflow_run_id"],
            "source_workflow_run_attempt": source_evidence["workflow_run_attempt"],
            "source_evidence_sha256": source_evidence["evidence_sha256"],
            "source_candidate_sha256": candidate_hash,
            "mutation_required_disabled": True,
            "canonical_status_mutation_applied": True,
            "deployment_authorized": False,
            "repository_mutation_authorized": False,
            "publication_authorized": False,
            "certification_created": False,
            "standing_created": False,
            "required_next_transition": "separately_authorized_disposable_staging_mutation_or_continued_non_mutating_observation",
            "authority_boundary": "This status records an observed non-mutating public-path state only and does not create deployment, repository mutation, publication, certification, compatibility standing, or consequence authority.",
        }
        write(args.status, updated)
        application_state = "APPLIED_OBSERVED_NON_MUTATING_PUBLIC_PATHS"

    result = {
        "schema_version": "1.0.0",
        "record_type": "external_chat_activation_status_application",
        "application_state": application_state,
        "canonical_status_mutated": application_state == "APPLIED_OBSERVED_NON_MUTATING_PUBLIC_PATHS",
        "source_candidate_sha256": candidate_hash,
        "source_evidence_sha256": source_evidence.get("evidence_sha256"),
        "target_path": "static/status/external-chat-activation-observation.json",
        "authority_boundary": {
            "application_is_deployment_authority": False,
            "application_is_repository_mutation_authority": False,
            "application_is_publication_authority": False,
            "application_is_certification": False,
            "application_creates_standing": False,
        },
    }
    write(args.output, result)
    print(f"EXTERNAL CHAT ACTIVATION STATUS APPLICATION: {application_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
