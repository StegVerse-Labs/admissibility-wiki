#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/external-frameworks/schemas/external-chat-activation-evidence.schema.json"
EXAMPLE = ROOT / "docs/external-frameworks/examples/external-chat-activation-evidence.example.json"
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
RESULTS = {
    "OBSERVED_NON_MUTATING_PUBLIC_PATHS",
    "LOCAL_VALIDATION_NOT_CONFIRMED",
    "LIVE_EVIDENCE_NOT_AVAILABLE",
    "LIVE_EVIDENCE_NOT_CONFIRMED",
}
BOUNDARY = {
    "evidence_is_deployment_authority": False,
    "evidence_is_repository_mutation_authority": False,
    "evidence_is_publication_authority": False,
    "evidence_is_certification": False,
    "evidence_creates_standing": False,
    "mutation_remains_separately_authorized": True,
}


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION EVIDENCE: FAIL - {message}")
    return 1


def canonical_hash(payload: dict) -> str:
    material = dict(payload)
    material.pop("evidence_sha256", None)
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    for path in (SCHEMA, EXAMPLE):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        if not isinstance(value, dict):
            return fail(f"{path.relative_to(ROOT)} must contain an object")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    evidence = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    if schema.get("title") != "External Chat activation evidence":
        return fail("schema title mismatch")
    if evidence.get("schema_version") != "1.0.0" or evidence.get("record_type") != "external_chat_activation_evidence":
        return fail("identity fields invalid")
    if evidence.get("result") not in RESULTS:
        return fail("result class invalid")
    if evidence.get("repository") != "StegVerse-Labs/Site":
        return fail("source repository mismatch")
    commit_sha = evidence.get("commit_sha")
    if commit_sha is not None and not COMMIT_RE.match(commit_sha):
        return fail("commit SHA invalid")
    if evidence.get("authority_boundary") != BOUNDARY:
        return fail("authority boundary mismatch")

    local = evidence.get("local_validation")
    live = evidence.get("post_deployment_live_verification")
    if not isinstance(local, dict) or not isinstance(live, dict):
        return fail("local/live evidence objects missing")
    for label, value in (("local receipt", local.get("receipt_sha256")), ("live receipt", live.get("receipt_sha256"))):
        if value is not None and not HASH_RE.match(value):
            return fail(f"{label} SHA-256 invalid")

    observed = evidence["result"] == "OBSERVED_NON_MUTATING_PUBLIC_PATHS"
    predicates = (
        local.get("present") is True,
        local.get("passed") is True,
        local.get("status") == "PASSED",
        local.get("authority_effect") == "NONE",
        live.get("present") is True,
        live.get("passed") is True,
        live.get("result") == "PASS",
        live.get("mutation_required_disabled") is True,
    )
    if observed and not all(predicates):
        return fail("observed result lacks required predicates")
    if observed and evidence.get("failure_class") is not None:
        return fail("observed result may not retain failure_class")

    claimed_hash = evidence.get("evidence_sha256", "")
    if not HASH_RE.match(claimed_hash):
        return fail("evidence SHA-256 invalid")
    calculated = canonical_hash(evidence)
    if claimed_hash != calculated:
        return fail(f"evidence SHA-256 mismatch: expected {calculated}")

    print("EXTERNAL CHAT ACTIVATION EVIDENCE: PASS (schema, result predicates, hash, non-authority boundary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
