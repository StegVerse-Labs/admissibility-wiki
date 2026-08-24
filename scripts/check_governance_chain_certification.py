#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "doctrine": ROOT / "docs/certification/GOVERNANCE_CHAIN_CERTIFICATION.md",
    "operational": ROOT / "docs/certification/CERTIFICATION_OPERATIONAL_STANDARD.md",
    "handoff": ROOT / "docs/certification/GOVERNANCE_CHAIN_CERTIFICATION_MIRROR_HANDOFF.md",
    "candidate_schema": ROOT / "schemas/governance-chain-certification-candidate.schema.json",
    "result_schema": ROOT / "schemas/governance-chain-certification-result.schema.json",
    "evidence_schema": ROOT / "schemas/governance-chain-certification-evidence.schema.json",
    "properties": ROOT / "data/certification/property-registry.v0.1.json",
    "profiles": ROOT / "data/certification/minimum-profiles.v0.1.json",
    "negative_fixtures": ROOT / "data/certification/negative-fixtures.v0.1.json",
    "pilot": ROOT / "data/certification/pilots/arquivonulo-int-pilot.v0.1.json",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for label, path in REQUIRED.items():
        if not path.exists():
            fail(f"missing required artifact: {label}: {path}")

    profiles = load_json(REQUIRED["profiles"])
    if set(profiles["surfaces"]) != {"PRE", "GOV", "POST", "INT"}:
        fail("minimum profiles must define exactly PRE/GOV/POST/INT")
    for surface, profile in profiles["surfaces"].items():
        if not profile.get("required_properties"):
            fail(f"{surface} missing required properties")
        if not profile.get("required_negative_controls"):
            fail(f"{surface} missing negative controls")

    props = load_json(REQUIRED["properties"])
    serialized_props = json.dumps(props)
    for required_property in [
        "FAIL_CLOSED", "EVIDENCE_PROVENANCE", "REPLAY_STABLE", "RECONSTRUCTABLE",
        "INTERLOCK_AUTHORITY_SEPARATED", "INTERLOCK_TRANSLATION_BOUNDED"
    ]:
        if required_property not in serialized_props:
            fail(f"property registry missing {required_property}")

    fixtures = load_json(REQUIRED["negative_fixtures"])["fixtures"]
    fixture_ids = {f["id"] for f in fixtures}
    required_fixtures = {
        "missing-evidence", "stale-certificate", "failed-negative-control",
        "authority-injection", "semantic-expansion", "payment-bias",
        "generic-badge-overclaim", "replay-reexecution", "proof-after-effect"
    }
    if not required_fixtures.issubset(fixture_ids):
        fail("negative fixture coverage incomplete")
    for fixture in fixtures:
        if fixture.get("must_not") in {None, ""}:
            fail(f"fixture lacks prohibited false-positive state: {fixture['id']}")

    evidence_schema = load_json(REQUIRED["evidence_schema"])
    lifecycle = json.dumps(evidence_schema)
    for marker in ["fresh_until", "EXPIRED", "SUSPENDED", "REVOKED", "SUPERSEDED", "renewal_requires_retest"]:
        if marker not in lifecycle:
            fail(f"evidence lifecycle contract missing {marker}")

    operational = REQUIRED["operational"].read_text(encoding="utf-8")
    for marker in [
        "Payment does not buy a disposition",
        "CURRENT -> EXPIRED",
        "Fin-Co certification model",
        "SDK evidence adapter",
        "Interlock certification",
        "badge MUST resolve to a machine-readable current certificate",
    ]:
        if marker not in operational:
            fail(f"operational standard missing marker: {marker}")

    pilot = load_json(REQUIRED["pilot"])
    if pilot.get("result") != "UNRESOLVED" or pilot.get("certificate_issued") is not False:
        fail("external pilot must preserve missing-evidence fail-closed outcome")
    if pilot.get("authority_effect") != "NONE":
        fail("pilot may not grant authority")

    print("GOVERNANCE_CHAIN_CERTIFICATION: PASS")
    print(f"profiles={len(profiles['surfaces'])}")
    print(f"negative_fixtures={len(fixtures)}")
    print("external_pilot=UNRESOLVED_NO_CERTIFICATE")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"GOVERNANCE_CHAIN_CERTIFICATION: FAIL: {exc}", file=sys.stderr)
        raise
