#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "release-readiness.v1.json"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"


def fail(message: str) -> None:
    raise SystemExit(f"RELEASE READINESS: FAIL - {message}")


def main() -> int:
    for path in (STATUS, WORKFLOW):
        if not path.exists():
            fail(f"missing required path: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("schema") != "admissibility_wiki_release_readiness.v1":
        fail("unexpected schema")
    if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")

    observed = data.get("observed_evidence", {})
    if observed.get("validate_chain_continuation") != "PASS_OBSERVED":
        fail("canonical validation pass must remain recorded")
    if observed.get("build_pages") not in {"PASS_OBSERVED", "FAIL_CLOSED_OBSERVED"}:
        fail("build-pages observation state is invalid")
    if observed.get("deploy_pages") not in {"PASS_OBSERVED", "NOT_RUN", "FAIL_CLOSED_OBSERVED"}:
        fail("deploy-pages observation state is invalid")
    if observed.get("verify_public_pages") not in {"PASS_OBSERVED", "NOT_RUN", "FAIL_CLOSED_OBSERVED"}:
        fail("verify-public-pages observation state is invalid")

    gates = data.get("release_gates", {})
    if gates.get("canonical_validation_pass_observed") is not True:
        fail("canonical validation gate mismatch")
    if gates.get("tag_or_release_authority_granted") is not False:
        fail("tag or release authority must remain false")
    for key in (
        "authority_granted",
        "release_authority_granted",
        "deployment_authority_granted",
        "downstream_mutation_authority_granted",
    ):
        if data.get(key) is not False:
            fail(f"{key} must be false")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("release readiness violates no-manual boundary")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "validate-chain-continuation:",
        "build-pages:",
        "deploy-pages:",
        "verify-public-pages:",
    ):
        if marker not in workflow:
            fail(f"canonical workflow missing marker: {marker}")

    propagation = data.get("propagation_posture", {})
    if not propagation:
        fail("propagation posture is missing")
    if any(value != "QUEUED_NO_MUTATION_AUTHORITY" for value in propagation.values()):
        fail("downstream propagation must remain queued without mutation authority")

    print(
        "RELEASE READINESS: PASS - "
        f"classification={data.get('classification')} validation=observed build={observed.get('build_pages')} "
        "release_authority=false manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
