#!/usr/bin/env python3
"""Run a deterministic synthetic smoke test of the Conectrr ITC evidence path.

This test proves only that the local Wiki machinery can exercise source-package
receipt, immutable hashing, reconstruction dispositions, drift coverage, replay,
and authority non-inheritance. It does not represent Conectrr-provided evidence.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.synthetic-capability-test.v1.json"
EXPECTED_DISPOSITIONS = {"AGREE", "DISAGREE", "DEFER"}
EXPECTED_DRIFT = {
    "EXPIRED_DELEGATION",
    "CHANGED_TARGET_SCOPE",
    "STALE_EVIDENCE",
    "CHANGED_POLICY_VERSION",
    "DEGRADED_RECOVERABILITY",
    "ACTOR_SUBSTITUTION",
    "TARGET_SUBSTITUTION",
    "SUPERSEDED_RECOMMENDATION",
    "CHANGED_DEPENDENCY_STATE",
    "INVALIDATED_SOURCE_REFERENCE",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def require_false_authority(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        fail(f"{label} authority object required")
    for field in ("certification", "execution", "custody", "endorsement"):
        if value.get(field) is not False:
            fail(f"{label} authority.{field} must remain false")


def main() -> int:
    if not FIXTURE.is_file():
        fail(f"missing fixture: {FIXTURE.relative_to(ROOT)}")
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if doc.get("schema") != "conectrr_itc_synthetic_capability_test.v1":
        fail("unexpected synthetic capability schema")
    if doc.get("external_validation_claimed") is not False:
        fail("synthetic test cannot claim external validation")
    require_false_authority(doc.get("authority"), "synthetic test")

    package = doc.get("source_package")
    if not isinstance(package, dict):
        fail("synthetic source_package object required")
    for key in ("specification", "canonical_itc", "validation_report"):
        item = package.get(key)
        if not isinstance(item, dict) or not item.get("media_type") or "content" not in item:
            fail(f"incomplete synthetic source artifact: {key}")
    if package["canonical_itc"].get("immutable") is not True:
        fail("synthetic canonical ITC must be immutable")

    canonical_itc = package["canonical_itc"]["content"]
    before = sha256(canonical_itc)
    reconstructed = json.loads(canonical_bytes(canonical_itc).decode("utf-8"))
    after = sha256(canonical_itc)
    replay = sha256(reconstructed)
    if before != after or before != replay:
        fail("synthetic immutable-source or replay hash mismatch")

    dispositions = {
        item.get("disposition")
        for item in doc.get("disposition_cases", [])
        if isinstance(item, dict) and item.get("expected") == "PASS"
    }
    if dispositions != EXPECTED_DISPOSITIONS:
        fail(f"synthetic disposition coverage mismatch: {sorted(dispositions)}")

    drift = set(doc.get("drift_cases", []))
    if drift != EXPECTED_DRIFT:
        fail(f"synthetic drift coverage mismatch: {sorted(drift)}")

    prohibited = set(package["specification"]["content"].get("prohibited_semantics", []))
    required_prohibited = {"consent", "authority", "admissibility", "governance", "commitment", "execution", "outcome_state"}
    if prohibited != required_prohibited:
        fail("synthetic specification prohibited-semantics set mismatch")
    for field in ("authority", "consent", "admissibility", "execution"):
        if canonical_itc.get(field) is not None:
            fail(f"synthetic ITC improperly asserts {field}")

    non_claims = "\n".join(str(item) for item in doc.get("non_claims", []))
    for marker in (
        "not Conectrr interoperability",
        "not external validation",
        "AGREE is not permission",
        "DISAGREE does not invalidate",
        "DEFER is not failure",
        "bounded source immutability only",
    ):
        if marker not in non_claims:
            fail(f"synthetic capability fixture missing non-claim marker: {marker}")

    print(f"OK: {FIXTURE.relative_to(ROOT)}")
    print(f"synthetic_source_hash_before={before}")
    print(f"synthetic_source_hash_after={after}")
    print("synthetic_replay=PASS")
    print("synthetic_dispositions=AGREE,DISAGREE,DEFER")
    print("synthetic_drift_cases=10")
    print("synthetic_authority_effect=NONE")
    print("external_validation_claimed=false")
    print("conectrr_itc_synthetic_capability=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
