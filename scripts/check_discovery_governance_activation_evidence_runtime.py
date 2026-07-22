#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_discovery_governance_activation_evidence.py"
PROOF = ROOT / "reports" / "discovery-governance-handoff-proof-receipt.json"
PUBLICATION = ROOT / "reports" / "discovery-governance-publication-receipt.json"
PUBLIC_ACTIVATION = ROOT / "reports" / "public-activation-receipt.json"
OUT = ROOT / "reports" / "discovery-governance-activation-evidence-receipt.json"

IDENTITY = {
    "repository": "StegVerse-Labs/admissibility-wiki",
    "commit": "runtime-validator-sha",
    "run_id": "runtime-validator-run",
    "run_attempt": "1",
}
ROUTES = (
    "discovery_governance_doctrine",
    "discovery_governance_schema",
    "discovery_governance_status",
    "discovery_governance_example",
    "discovery_governance_publication_receipt_schema",
)
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


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def proof_receipt() -> dict:
    outcomes = ("HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED")
    return {
        "schema": "discovery_governance_handoff_proof_receipt.v1",
        "goal_id": "discovery-governance-minimum-handoff",
        **IDENTITY,
        "fixture_sha256": "0" * 64,
        "results": [
            {"case_id": f"runtime-{outcome.lower()}", "expected": outcome, "actual": outcome, "matched": True}
            for outcome in outcomes
        ],
        "overall_result": "PASS",
    }


def publication_receipt(route_failure: str | None = None) -> dict:
    routes = {
        name: {
            "url": f"https://stegverse-labs.github.io/admissibility-wiki/runtime/{name}",
            "reachable": name != route_failure,
            "http_status": 503 if name == route_failure else 200,
            "verifier": "deterministic activation-evidence runtime validation",
        }
        for name in ROUTES
    }
    complete = route_failure is None
    payload = {
        "schema": "discovery_governance_publication_receipt.v1",
        "goal_id": "discovery-governance-minimum-handoff",
        **IDENTITY,
        "state": "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE" if complete else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "routes": routes,
        "all_required_public_routes_verified": complete,
        "pages_deployment_observed": complete,
        "architectural_alignment_classification": "DOCUMENTED_ARCHITECTURAL_ALIGNMENT",
        "manual_task_requirement": "NONE",
        "user_manual_action_required": False,
    }
    payload.update({field: False for field in FALSE_FIELDS})
    return payload


def public_activation_receipt(publication: dict) -> dict:
    return {
        "schema": "admissibility_wiki_public_activation_receipt.v7",
        **IDENTITY,
        "activation_closures": {"discovery_governance": publication},
        "linked_receipts": {
            "discovery_governance_publication_receipt": "reports/discovery-governance-publication-receipt.json"
        },
        "publication_complete": publication["all_required_public_routes_verified"],
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
    }


def run_writer() -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "GITHUB_SHA": IDENTITY["commit"],
        "GITHUB_RUN_ID": IDENTITY["run_id"],
        "GITHUB_RUN_ATTEMPT": IDENTITY["run_attempt"],
        "DISCOVERY_WORKFLOW_DEPENDENCIES_SATISFIED": "true",
    }
    return subprocess.run(
        [sys.executable, str(WRITER)],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def snapshot(paths: tuple[Path, ...]) -> dict[Path, bytes | None]:
    return {path: path.read_bytes() if path.exists() else None for path in paths}


def restore(saved: dict[Path, bytes | None]) -> None:
    for path, content in saved.items():
        if content is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)


def main() -> int:
    failures: list[str] = []
    paths = (PROOF, PUBLICATION, PUBLIC_ACTIVATION, OUT)
    saved = snapshot(paths)
    try:
        valid_publication = publication_receipt()
        write_json(PROOF, proof_receipt())
        write_json(PUBLICATION, valid_publication)
        write_json(PUBLIC_ACTIVATION, public_activation_receipt(valid_publication))
        success = run_writer()
        if success.returncode != 0:
            failures.append("valid evidence set did not produce a successful writer result")
            failures.append(success.stdout.strip())
        elif not OUT.exists():
            failures.append("valid evidence set did not produce an activation evidence receipt")
        else:
            receipt = json.loads(OUT.read_text(encoding="utf-8"))
            if receipt.get("state") != "ACTIVATION_EVIDENCE_COMPLETE":
                failures.append("valid evidence set did not reach ACTIVATION_EVIDENCE_COMPLETE")
            if receipt.get("goal_completion_observed") is not True:
                failures.append("valid evidence set did not observe goal completion")
            criteria = receipt.get("completion_criteria", {})
            if not criteria or not all(criteria.values()):
                failures.append("valid evidence set did not pass every completion criterion")
            for field in (
                "consent_granted", "standing_granted", "authority_granted",
                "admissibility_granted", "commitment_granted",
                "execution_permission_granted", "certification_granted",
                "endorsement_granted", "interoperability_verified",
                "release_authority_granted", "downstream_mutation_authority_granted",
            ):
                if receipt.get(field) is not False:
                    failures.append(f"valid receipt must preserve {field}=false")

        failed_publication = publication_receipt("discovery_governance_status")
        write_json(PUBLICATION, failed_publication)
        write_json(PUBLIC_ACTIVATION, public_activation_receipt(failed_publication))
        failure = run_writer()
        if failure.returncode == 0:
            failures.append("failed route evidence incorrectly produced a successful writer result")
        elif not OUT.exists():
            failures.append("failed route evidence did not preserve a fail-closed receipt")
        else:
            receipt = json.loads(OUT.read_text(encoding="utf-8"))
            if receipt.get("state") != "ACTIVATION_EVIDENCE_FAIL_CLOSED":
                failures.append("failed route evidence did not produce ACTIVATION_EVIDENCE_FAIL_CLOSED")
            if receipt.get("goal_completion_observed") is not False:
                failures.append("failed route evidence incorrectly observed goal completion")
            criteria = receipt.get("completion_criteria", {})
            for field in (
                "all_five_public_routes_verified",
                "publication_state_complete",
                "pages_deployment_observed",
                "public_activation_publication_complete",
            ):
                if criteria.get(field) is not False:
                    failures.append(f"failed route evidence must set {field}=false")
    finally:
        restore(saved)

    if failures:
        print("DISCOVERY GOVERNANCE ACTIVATION EVIDENCE RUNTIME: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE ACTIVATION EVIDENCE RUNTIME: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
