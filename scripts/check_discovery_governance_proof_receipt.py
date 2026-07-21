#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_discovery_governance_handoff.py"
FIXTURES = ROOT / "tests" / "fixtures" / "discovery-governance-handoff-cases.json"
SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-handoff-proof-receipt.schema.json"
RECEIPT = ROOT / "reports" / "discovery-governance-handoff-proof-receipt.json"
OUTCOMES = {"HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED"}
FALSE_FIELDS = (
    "consent_granted", "standing_granted", "authority_granted",
    "admissibility_granted", "commitment_granted",
    "execution_permission_granted", "certification_granted",
    "endorsement_granted", "interoperability_verified",
    "downstream_mutation_authority_granted",
)


def main() -> int:
    failures: list[str] = []
    for path in (CHECKER, FIXTURES, SCHEMA):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("DISCOVERY GOVERNANCE PROOF RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    result = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    print(result.stdout.rstrip())
    if result.returncode != 0:
        failures.append("handoff checker failed")
    if not RECEIPT.exists():
        failures.append("proof receipt was not generated")
    else:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        fixture_digest = hashlib.sha256(FIXTURES.read_bytes()).hexdigest()
        if receipt.get("schema") != "discovery_governance_handoff_proof_receipt.v1":
            failures.append("proof receipt schema mismatch")
        if receipt.get("goal_id") != "discovery-governance-minimum-handoff":
            failures.append("proof receipt goal_id mismatch")
        if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
            failures.append("proof receipt repository mismatch")
        if receipt.get("fixture_sha256") != fixture_digest:
            failures.append("proof receipt fixture digest mismatch")
        results = receipt.get("results", [])
        if len(results) < 4:
            failures.append("proof receipt does not contain all deterministic cases")
        observed = {item.get("actual") for item in results}
        if not OUTCOMES.issubset(observed):
            failures.append("proof receipt lacks complete deterministic outcome coverage")
        if any(item.get("matched") is not True for item in results):
            failures.append("proof receipt contains an unmatched result")
        if receipt.get("overall_result") != "PASS":
            failures.append("proof receipt overall_result is not PASS")
        for field in FALSE_FIELDS:
            if receipt.get(field) is not False:
                failures.append(f"proof receipt must force {field}=false")

    if failures:
        print("DISCOVERY GOVERNANCE PROOF RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE PROOF RECEIPT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
