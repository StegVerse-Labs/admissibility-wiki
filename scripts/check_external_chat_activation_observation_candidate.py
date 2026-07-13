#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/generate_external_chat_activation_observation_candidate.py"
OUTPUT = ROOT / "reports/external-chat-activation-observation-candidate.json"

ALLOWED_STATES = {
    "PENDING_SOURCE_EVIDENCE",
    "PENDING_OBSERVED_NON_MUTATING_RESULT",
    "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE",
    "FAIL_CLOSED",
}


def sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION OBSERVATION CANDIDATE: FAIL - {message}")
    return 1


def main() -> int:
    if not GENERATOR.exists():
        return fail("generator missing")
    completed = subprocess.run([sys.executable, str(GENERATOR)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if completed.returncode not in {0, 1}:
        return fail(f"generator exited unexpectedly: {completed.returncode}\n{completed.stdout}")
    if not OUTPUT.exists():
        return fail("candidate output missing")

    candidate = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if not isinstance(candidate, dict):
        return fail("candidate must be a JSON object")
    if candidate.get("schema_version") != "1.0.0":
        return fail("schema version mismatch")
    if candidate.get("record_type") != "external_chat_activation_observation_candidate":
        return fail("record type mismatch")
    if candidate.get("state") not in ALLOWED_STATES:
        return fail("invalid candidate state")

    claimed = candidate.get("candidate_sha256")
    material = dict(candidate)
    material.pop("candidate_sha256", None)
    calculated = sha256(material)
    if claimed != calculated:
        return fail("candidate SHA-256 mismatch")

    effect = candidate.get("candidate_effect")
    required_effect = {
        "canonical_status_mutated": False,
        "deployment_authorized": False,
        "repository_mutation_authorized": False,
        "publication_authorized": False,
        "certification_created": False,
        "standing_created": False,
    }
    if effect != required_effect:
        return fail("candidate authority boundary mismatch")

    state = candidate["state"]
    source = candidate.get("source", {})
    if state == "OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE":
        required = {
            "source_repository": "StegVerse-Labs/Site",
            "source_result": "OBSERVED_NON_MUTATING_PUBLIC_PATHS",
            "mutation_required_disabled": True,
        }
        for key, value in required.items():
            if source.get(key) != value:
                return fail(f"observed candidate source mismatch for {key}")
        if not isinstance(source.get("source_commit_sha"), str) or len(source["source_commit_sha"]) != 40:
            return fail("observed candidate source commit is invalid")
        if not source.get("source_workflow_run_id"):
            return fail("observed candidate source workflow run is missing")
        if not isinstance(source.get("source_evidence_sha256"), str) or len(source["source_evidence_sha256"]) != 64:
            return fail("observed candidate source evidence hash is invalid")
        if candidate.get("reason") is not None:
            return fail("observed candidate must not carry a failure reason")
        if candidate.get("required_next_transition") != "separately_authorized_canonical_status_promotion":
            return fail("observed candidate next transition mismatch")
    else:
        if candidate.get("required_next_transition") != "preserve_or_acquire_valid_source_evidence":
            return fail("pending or fail-closed candidate next transition mismatch")

    print(f"EXTERNAL CHAT ACTIVATION OBSERVATION CANDIDATE: PASS ({state})")
    return 0 if state != "FAIL_CLOSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
