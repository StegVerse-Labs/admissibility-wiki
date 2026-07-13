#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "static/status/external-chat-activation-evidence.json"
PROVENANCE = ROOT / "static/status/external-chat-activation-evidence.provenance.json"
OUTPUT = ROOT / "reports/external-chat-activation-observation-candidate.json"


def load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def canonical_evidence_hash(value: dict[str, Any]) -> str:
    material = dict(value)
    material.pop("evidence_sha256", None)
    return sha256(material)


def main() -> int:
    evidence = load(EVIDENCE)
    provenance = load(PROVENANCE)
    now = datetime.now(timezone.utc).isoformat()

    state = "PENDING_SOURCE_EVIDENCE"
    reason = "validated projection and provenance are not both present"
    source: dict[str, Any] = {
        "evidence_present": evidence is not None,
        "provenance_present": provenance is not None,
    }

    if evidence is not None and provenance is not None:
        claimed = evidence.get("evidence_sha256")
        calculated = canonical_evidence_hash(evidence)
        if claimed != calculated:
            state = "FAIL_CLOSED"
            reason = "projected evidence hash does not recompute"
        elif provenance.get("source_evidence_sha256") != claimed:
            state = "FAIL_CLOSED"
            reason = "provenance evidence hash does not match projection"
        elif provenance.get("source_commit_sha") != evidence.get("commit_sha"):
            state = "FAIL_CLOSED"
            reason = "provenance commit identity does not match projection"
        elif str(provenance.get("source_workflow_run_id")) != str(evidence.get("workflow_run_id")):
            state = "FAIL_CLOSED"
            reason = "provenance workflow run identity does not match projection"
        elif evidence.get("result") != "OBSERVED_NON_MUTATING_PUBLIC_PATHS":
            state = "PENDING_OBSERVED_NON_MUTATING_RESULT"
            reason = f"source result is {evidence.get('result')!r}"
        else:
            local = evidence.get("local_validation", {})
            live = evidence.get("post_deployment_live_verification", {})
            if not (
                local.get("passed") is True
                and local.get("status") == "PASSED"
                and local.get("authority_effect") == "NONE"
                and live.get("passed") is True
                and live.get("result") == "PASS"
                and live.get("mutation_required_disabled") is True
            ):
                state = "FAIL_CLOSED"
                reason = "observed result lacks required non-mutating predicates"
            else:
                state = "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE"
                reason = None

        source.update({
            "source_repository": evidence.get("repository"),
            "source_commit_sha": evidence.get("commit_sha"),
            "source_workflow_run_id": evidence.get("workflow_run_id"),
            "source_workflow_run_attempt": evidence.get("workflow_run_attempt"),
            "source_evidence_sha256": claimed,
            "source_result": evidence.get("result"),
            "mutation_required_disabled": evidence.get("post_deployment_live_verification", {}).get("mutation_required_disabled"),
            "provenance_imported_at": provenance.get("imported_at"),
            "provenance_source": provenance.get("source"),
        })

    candidate: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_type": "external_chat_activation_observation_candidate",
        "generated_at": now,
        "state": state,
        "reason": reason,
        "source": source,
        "candidate_effect": {
            "canonical_status_mutated": False,
            "deployment_authorized": False,
            "repository_mutation_authorized": False,
            "publication_authorized": False,
            "certification_created": False,
            "standing_created": False,
        },
        "required_next_transition": (
            "separately_authorized_canonical_status_promotion"
            if state == "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE"
            else "preserve_or_acquire_valid_source_evidence"
        ),
    }
    candidate["candidate_sha256"] = sha256(candidate)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print(f"EXTERNAL CHAT ACTIVATION OBSERVATION CANDIDATE: {state}")
    print(f"Candidate: {OUTPUT.relative_to(ROOT)}")
    return 1 if state == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
