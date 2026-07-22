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
    "discovery_governance_doctrine",
    "discovery_governance_schema",
    "discovery_governance_status",
    "discovery_governance_example",
    "discovery_governance_publication_receipt_schema",
}
FALSE_FIELDS = (
    "implementation_equivalence_established",
    "interoperability_verified",
    "consent_granted",
    "standing_granted",
    "authority_granted",
    "admissibility_granted",
    "commitment_granted",
    "execution_permission_granted",
    "certification_granted",
    "endorsement_granted",
    "downstream_mutation_authority_granted",
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

    if proof is not None:
        if proof.get("schema") != "discovery_governance_handoff_proof_receipt.v1":
            failures.append("proof receipt schema mismatch")
        if proof.get("overall_result") != "PASS":
            failures.append("proof receipt is not PASS")
        results = proof.get("results", [])
        observed = {item.get("actual") for item in results if item.get("matched") is True}
        required = {"HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED"}
        if not required.issubset(observed):
            failures.append("proof receipt does not preserve all four deterministic outcomes")

    if publication is not None:
        if publication.get("schema") != "discovery_governance_publication_receipt.v1":
            failures.append("publication receipt schema mismatch")
        routes = publication.get("routes", {})
        if set(routes) != REQUIRED_ROUTES:
            failures.append("publication receipt route set mismatch")
        route_pass = all(
            item.get("reachable") is True
            and isinstance(item.get("http_status"), int)
            and 200 <= item["http_status"] < 400
            for item in routes.values()
        ) if set(routes) == REQUIRED_ROUTES else False
        if publication.get("all_required_public_routes_verified") is not route_pass:
            failures.append("publication route aggregate mismatch")
        if publication.get("state") != "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE":
            failures.append("publication receipt is not workflow-observed complete")
        if publication.get("pages_deployment_observed") is not True:
            failures.append("Pages deployment was not observed")
        for field in FALSE_FIELDS:
            if publication.get(field) is not False:
                failures.append(f"publication receipt must preserve {field}=false")

    embedded = None
    if public_activation is not None:
        embedded = public_activation.get("activation_closures", {}).get("discovery_governance")
        if embedded is None:
            failures.append("public activation receipt lacks discovery closure")
        if publication is not None and embedded != publication:
            failures.append("standalone publication receipt differs from embedded closure")
        if public_activation.get("linked_receipts", {}).get("discovery_governance_publication_receipt") != "reports/discovery-governance-publication-receipt.json":
            failures.append("linked publication receipt path mismatch")
        if public_activation.get("publication_complete") is not True:
            failures.append("public activation receipt is not publication_complete")

    identities = []
    for payload in (proof, publication, public_activation):
        if payload is not None:
            identities.append((payload.get("repository"), payload.get("commit"), payload.get("run_id"), payload.get("run_attempt")))
    if identities and len(set(identities)) != 1:
        failures.append("receipt repository/run identity mismatch")

    receipt = {
        "schema": "discovery_governance_activation_evidence_receipt.v1",
        "goal_id": "discovery-governance-minimum-handoff",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "state": "ACTIVATION_EVIDENCE_COMPLETE" if not failures else "ACTIVATION_EVIDENCE_FAIL_CLOSED",
        "canonical_dependency_chain_observed": dependencies,
        "proof_receipt": {
            "path": str(PROOF.relative_to(ROOT)),
            "sha256": sha256(PROOF) if PROOF.exists() else None,
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
            "embedded_closure_exact_match": publication is not None and embedded == publication,
        },
        "failures": failures,
        "consent_granted": False,
        "standing_granted": False,
        "authority_granted": False,
        "admissibility_granted": False,
        "commitment_granted": False,
        "execution_permission_granted": False,
        "certification_granted": False,
        "endorsement_granted": False,
        "interoperability_verified": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "manual_task_requirement": "NONE",
        "user_manual_action_required": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {receipt['state']}")
    for failure in failures:
        print(f"- {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
