#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "reports" / "discovery-governance-handoff-proof-receipt.json"
DOWNLOADED_PROOF = ROOT / "discovery-governance-handoff-proof-receipt.json"
PUBLICATION = ROOT / "reports" / "discovery-governance-publication-receipt.json"
PUBLIC_ACTIVATION = ROOT / "reports" / "public-activation-receipt.json"
OUT = ROOT / "reports" / "discovery-governance-activation-evidence-receipt.json"
REQUIRED_ROUTES = {
    "discovery_governance_doctrine", "discovery_governance_schema",
    "discovery_governance_status", "discovery_governance_example",
    "discovery_governance_publication_receipt_schema",
}
FALSE_FIELDS = (
    "implementation_equivalence_established", "interoperability_verified",
    "consent_granted", "standing_granted", "authority_granted",
    "admissibility_granted", "commitment_granted",
    "execution_permission_granted", "certification_granted",
    "endorsement_granted", "downstream_mutation_authority_granted",
)


def load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(str(path.relative_to(ROOT)))
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    proof = publication = public_activation = None
    if not PROOF.exists() and DOWNLOADED_PROOF.exists():
        PROOF.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DOWNLOADED_PROOF, PROOF)
    try:
        proof = load(PROOF)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        failures.append(f"proof receipt unavailable: {exc}")
    try:
        publication = load(PUBLICATION)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        failures.append(f"publication receipt unavailable: {exc}")
    try:
        public_activation = load(PUBLIC_ACTIVATION)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        failures.append(f"public activation receipt unavailable: {exc}")
    dependencies = os.getenv("DISCOVERY_WORKFLOW_DEPENDENCIES_SATISFIED") == "true"
    if not dependencies:
        failures.append("canonical validation/build/deploy dependency chain not asserted by workflow")
    proof_pass = False
    four_outcomes_preserved = False
    fixture_sha256 = None
    if proof is not None:
        if proof.get("schema") != "discovery_governance_handoff_proof_receipt.v1":
            failures.append("proof receipt schema mismatch")
        results = proof.get("results", [])
        observed = {item.get("actual") for item in results if item.get("matched") is True}
        required = {"HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED"}
        four_outcomes_preserved = required.issubset(observed)
        proof_pass = proof.get("overall_result") == "PASS" and four_outcomes_preserved
        fixture_sha256 = proof.get("fixture_sha256")
        if proof.get("overall_result") != "PASS":
            failures.append("proof receipt is not PASS")
        if not four_outcomes_preserved:
            failures.append("proof receipt does not preserve all four deterministic outcomes")
        if not isinstance(fixture_sha256, str) or len(fixture_sha256) != 64:
            failures.append("proof receipt fixture_sha256 missing or invalid")
    route_pass = publication_state_complete = pages_deployment_observed = authority_boundary_preserved = False
    if publication is not None:
        if publication.get("schema") != "discovery_governance_publication_receipt.v1":
            failures.append("publication receipt schema mismatch")
        routes = publication.get("routes", {})
        if set(routes) != REQUIRED_ROUTES:
            failures.append("publication receipt route set mismatch")
        route_pass = all(item.get("reachable") is True and isinstance(item.get("http_status"), int) and 200 <= item["http_status"] < 400 for item in routes.values()) if set(routes) == REQUIRED_ROUTES else False
        if publication.get("all_required_public_routes_verified") is not route_pass:
            failures.append("publication route aggregate mismatch")
        publication_state_complete = publication.get("state") == "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE"
        pages_deployment_observed = publication.get("pages_deployment_observed") is True
        authority_boundary_preserved = all(publication.get(field) is False for field in FALSE_FIELDS)
        if not publication_state_complete:
            failures.append("publication receipt is not workflow-observed complete")
        if not pages_deployment_observed:
            failures.append("Pages deployment was not observed")
        for field in FALSE_FIELDS:
            if publication.get(field) is not False:
                failures.append(f"publication receipt must preserve {field}=false")
    exact_closure_match = linked_receipt_bound = public_publication_complete = False
    if public_activation is not None:
        embedded = public_activation.get("activation_closures", {}).get("discovery_governance")
        if embedded is None:
            failures.append("public activation receipt lacks discovery closure")
        exact_closure_match = publication is not None and embedded == publication
        if publication is not None and not exact_closure_match:
            failures.append("standalone publication receipt differs from embedded closure")
        linked_receipt_bound = public_activation.get("linked_receipts", {}).get("discovery_governance_publication_receipt") == "reports/discovery-governance-publication-receipt.json"
        if not linked_receipt_bound:
            failures.append("linked publication receipt path mismatch")
        public_publication_complete = public_activation.get("publication_complete") is True
        if not public_publication_complete:
            failures.append("public activation receipt is not publication_complete")
    identities = [(payload.get("repository"), payload.get("commit"), payload.get("run_id"), payload.get("run_attempt")) for payload in (proof, publication, public_activation) if payload is not None]
    identity_match = len(identities) == 3 and len(set(identities)) == 1
    if identities and not identity_match:
        failures.append("receipt repository/run identity mismatch")
    input_digests_present = PROOF.exists() and PUBLICATION.exists() and PUBLIC_ACTIVATION.exists()
    completion_criteria = {
        "canonical_dependency_chain_observed": dependencies,
        "proof_receipt_pass": proof_pass,
        "four_outcomes_preserved": four_outcomes_preserved,
        "all_five_public_routes_verified": route_pass,
        "publication_state_complete": publication_state_complete,
        "pages_deployment_observed": pages_deployment_observed,
        "standalone_embedded_closure_exact_match": exact_closure_match,
        "linked_publication_receipt_bound": linked_receipt_bound,
        "public_activation_publication_complete": public_publication_complete,
        "receipt_run_identity_match": identity_match,
        "input_sha256_digests_present": input_digests_present,
        "authority_boundary_preserved": authority_boundary_preserved,
    }
    goal_completion_observed = not failures and all(completion_criteria.values())
    receipt = {
        "schema": "discovery_governance_activation_evidence_receipt.v1",
        "goal_id": "discovery-governance-minimum-handoff",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"), "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "state": "ACTIVATION_EVIDENCE_COMPLETE" if goal_completion_observed else "ACTIVATION_EVIDENCE_FAIL_CLOSED",
        "goal_completion_observed": goal_completion_observed,
        "completion_criteria": completion_criteria,
        "canonical_dependency_chain_observed": dependencies,
        "proof_receipt": {
            "path": str(PROOF.relative_to(ROOT)),
            "sha256": sha256(PROOF) if PROOF.exists() else None,
            "fixture_sha256": fixture_sha256,
            "overall_result": proof.get("overall_result") if proof else None,
        },
        "publication_receipt": {
            "path": str(PUBLICATION.relative_to(ROOT)),
            "sha256": sha256(PUBLICATION) if PUBLICATION.exists() else None,
            "state": publication.get("state") if publication else None,
            "all_required_public_routes_verified": publication.get("all_required_public_routes_verified") if publication else False,
        },
        "public_activation_receipt": {
            "path": str(PUBLIC_ACTIVATION.relative_to(ROOT)),
            "sha256": sha256(PUBLIC_ACTIVATION) if PUBLIC_ACTIVATION.exists() else None,
            "publication_complete": public_activation.get("publication_complete") if public_activation else False,
            "embedded_closure_exact_match": exact_closure_match,
        },
        "failures": failures,
        "consent_granted": False, "standing_granted": False,
        "authority_granted": False, "admissibility_granted": False,
        "commitment_granted": False, "execution_permission_granted": False,
        "certification_granted": False, "endorsement_granted": False,
        "interoperability_verified": False, "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "manual_task_requirement": "NONE", "user_manual_action_required": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {receipt['state']}")
    for criterion, passed in completion_criteria.items():
        print(f"- {criterion}: {'PASS' if passed else 'FAIL'}")
    for failure in failures:
        print(f"- {failure}")
    return 0 if goal_completion_observed else 1


if __name__ == "__main__":
    raise SystemExit(main())
