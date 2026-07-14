#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "optimization-target-binding-publication-verification.json"
DOCTRINE = ROOT / "docs" / "formalisms" / "optimization-target-binding-at-commit.md"
FORMALISM = ROOT / "static" / "formalisms" / "optimization-target-binding-at-commit.v0.1.json"
SIDEBAR = ROOT / "sidebars.js"
CHECKER = ROOT / "scripts" / "check_optimization_target_binding_at_commit.py"
DEPLOYMENT_CHECK = ROOT / "scripts" / "check_governed_llm_deployment_status.py"
ACTIVATION_WRITER = ROOT / "scripts" / "write-public-activation-receipt.mjs"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"

EXPECTED_STATE = "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_AND_PUBLIC_ROUTE_VERIFICATION"
EXPECTED_ROUTES = {
    "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit",
    "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json",
    "https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json",
}
REQUIRED_EVIDENCE = {
    "canonical_workflow_pass",
    "docusaurus_build_pass",
    "doctrine_route_verified",
    "machine_readable_route_verified",
    "status_route_verified",
    "proof_fixture_receipt_attached",
}


def main() -> int:
    failures: list[str] = []
    for path in (
        STATUS,
        DOCTRINE,
        FORMALISM,
        SIDEBAR,
        CHECKER,
        DEPLOYMENT_CHECK,
        ACTIVATION_WRITER,
        WORKFLOW,
    ):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    formalism = json.loads(FORMALISM.read_text(encoding="utf-8"))
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    deployment_check = DEPLOYMENT_CHECK.read_text(encoding="utf-8")
    activation_writer = ACTIVATION_WRITER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    if status.get("schema") != "stegverse.optimization_target_binding_publication_verification.v0.1":
        failures.append("unexpected publication status schema")
    if status.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("unexpected repository")
    if status.get("state") != EXPECTED_STATE:
        failures.append("publication state must remain pending until external evidence is recorded")
    if set(status.get("expected_public_routes", [])) != EXPECTED_ROUTES:
        failures.append("expected public route set mismatch")

    evidence = status.get("evidence", {})
    if set(evidence) != REQUIRED_EVIDENCE:
        failures.append("publication evidence field set mismatch")
    if any(evidence.values()):
        failures.append("pending publication artifact must not claim unverified evidence")

    automation = status.get("automation", {})
    if automation.get("manual_route_verification_required") is not False:
        failures.append("manual route verification must remain eliminated")
    if automation.get("manual_receipt_creation_required") is not False:
        failures.append("manual receipt creation must remain eliminated")
    if automation.get("verification_job") != "verify-public-pages":
        failures.append("unexpected verification job")
    if automation.get("failure_behavior") != "FAIL_CLOSED":
        failures.append("publication automation must fail closed")

    authority = status.get("authority", {})
    for key in (
        "grants_execution_authority",
        "grants_cross_repository_mutation_authority",
        "grants_proof_authority",
    ):
        if authority.get(key) is not False:
            failures.append(f"{key} must be false")
    if authority.get("proof_owner") != "Data-Continuation/formalism-tests":
        failures.append("proof owner mismatch")

    if formalism.get("status") != "CONCEPTUAL_FORMALISM_INSTALLED":
        failures.append("formalism installation state mismatch")
    if formalism.get("authority", {}).get("grants_execution_authority") is not False:
        failures.append("formalism must not grant execution authority")
    if "FAIL_CLOSED" not in doctrine:
        failures.append("doctrine missing FAIL_CLOSED rule")
    if "formalisms/optimization-target-binding-at-commit" not in sidebar:
        failures.append("sidebar registration missing")

    for route in EXPECTED_ROUTES:
        if route not in deployment_check:
            failures.append(f"post-deployment verifier missing route: {route}")
    if "optimization-target-publication-verification-receipt.json" not in deployment_check:
        failures.append("post-deployment verifier must emit optimization-target receipt")
    if "optimization-target-publication-verification-receipt.json" not in activation_writer:
        failures.append("activation receipt writer must link optimization-target receipt")
    if "python scripts/check_governed_llm_deployment_status.py" not in workflow:
        failures.append("canonical workflow must invoke post-deployment verifier")
    if "node scripts/write-public-activation-receipt.mjs" not in workflow:
        failures.append("canonical workflow must write activation receipt")

    if failures:
        print("OPTIMIZATION TARGET BINDING PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OPTIMIZATION TARGET BINDING PUBLICATION: PASS")
    print(f"state={EXPECTED_STATE}")
    print("manual_route_verification_required=false")
    print("manual_receipt_creation_required=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
