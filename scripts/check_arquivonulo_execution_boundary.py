#!/usr/bin/env python3
"""Validate the bounded ArquivoNulo execution-boundary evaluation chain."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "arquivonulo.md"
EVALUATION = ROOT / "static" / "data" / "framework-evaluations" / "arquivonulo.json"
INDEX = ROOT / "static" / "data" / "framework-evaluations" / "index.json"
STATUS = ROOT / "static" / "status" / "arquivonulo-execution-boundary-status.json"
FIXTURE = ROOT / "docs" / "external-frameworks" / "fixtures" / "arquivonulo-continuing-admissibility-test.v0.1.json"
PUBLICATION_TEMPLATE = ROOT / "docs" / "external-frameworks" / "evidence" / "arquivonulo-publication-verification.template.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ARQUIVONULO_MIRROR_HANDOFF.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ARQUIVONULO EXECUTION BOUNDARY: FAIL - {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    doc = read(DOC)
    sidebar = read(SIDEBAR)
    handoff = read(HANDOFF)
    evaluation = json.loads(read(EVALUATION))
    index = json.loads(read(INDEX))
    status = json.loads(read(STATUS))
    fixture = json.loads(read(FIXTURE))
    publication = json.loads(read(PUBLICATION_TEMPLATE))

    for token in (
        "valid proof != continuing admissibility",
        "interdiction != pre-consequence prevention",
        "anchored state != current reality",
        "S5 Execution",
        "S7 Proof Verification",
        "PUBLICLY_UNRESOLVED",
    ):
        require(token in doc, f"doctrine missing token: {token}")

    require("external-frameworks/arquivonulo" in sidebar, "ArquivoNulo route is not exposed in the sidebar")
    for token in (
        "arquivonulo-execution-boundary-evaluation",
        "static/status/arquivonulo-execution-boundary-status.json",
        "arquivonulo-continuing-admissibility-test.v0.1.json",
        "arquivonulo-publication-verification.template.json",
    ):
        require(token in handoff, f"goal-specific handoff missing token: {token}")

    require(evaluation.get("framework_id") == "arquivonulo", "framework_id must be arquivonulo")
    source = evaluation.get("source_posture", {})
    require(source.get("owner_controlled_public_sources_observed") is True, "public-source observation must be recorded")
    require(source.get("owner_confirmed_frozen_declaration") is False, "owner-confirmed declaration must remain false")
    require(source.get("live_test_run") is False, "live test must remain false")

    boundary = evaluation.get("execution_boundary", {})
    require(boundary.get("status") == "PUBLICLY_UNRESOLVED", "execution boundary must remain PUBLICLY_UNRESOLVED")
    require(boundary.get("commit_bound_prevention_demonstrated") is False, "commit-bound prevention must not be claimed")
    require(boundary.get("post_execution_verification_possible_from_published_sequence") is True, "published sequence ambiguity must be preserved")

    continuing = evaluation.get("continuing_admissibility", {})
    require(continuing.get("status") == "PUBLICLY_UNRESOLVED", "continuing admissibility must remain PUBLICLY_UNRESOLVED")
    required_proxies = {
        "current_authority",
        "applicable_policy",
        "admissible_evidence",
        "environmental_correspondence",
        "recoverability",
        "intervention_capacity",
    }
    require(required_proxies.issubset(set(continuing.get("integrity_proof_is_not_proxy_for", []))), "continuing-admissibility proxy exclusions are incomplete")

    authority = evaluation.get("authority", {})
    for key in ("comparison", "certification", "endorsement", "execution", "custody", "integration"):
        require(authority.get(key) is False, f"authority.{key} must remain false")

    registry_entry = next((item for item in index.get("frameworks", []) if item.get("framework_id") == "arquivonulo"), None)
    require(registry_entry is not None, "framework registry is missing ArquivoNulo")
    require(registry_entry.get("record_path") == "arquivonulo.json", "registry record_path is incorrect")
    require(registry_entry.get("live_test_status") == "NOT_TESTED", "registry live_test_status must remain NOT_TESTED")

    require(status.get("goal_id") == "arquivonulo-execution-boundary-evaluation", "status goal_id is incorrect")
    require(status.get("state") == "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_AND_PUBLICATION_OBSERVATION", "status state is incorrect")
    require(status.get("test_posture", {}).get("fixture_status") == "PROPOSED_NOT_RUN", "status fixture must remain PROPOSED_NOT_RUN")
    observation = status.get("workflow_observation", {})
    require(observation.get("canonical_validation_observed") is False, "canonical validation may not be claimed without evidence")
    require(observation.get("public_deployment_observed") is False, "public deployment may not be claimed without evidence")
    require(observation.get("activation_receipt_closed") is False, "activation receipt may not be closed without evidence")

    require(fixture.get("test_id") == "arquivonulo-continuing-admissibility-001", "fixture test_id is incorrect")
    require(fixture.get("status") == "PROPOSED_NOT_RUN", "fixture must remain PROPOSED_NOT_RUN")
    require(fixture.get("source_posture") == "STEGVERSE_PROPOSED_NEUTRAL_FIXTURE_NOT_OWNER_CONFIRMED", "fixture source posture is incorrect")
    require(fixture.get("mutation", {}).get("change_exactly_one") is True, "fixture must change exactly one governing condition")
    required_results = {"ALLOW", "HOLD", "DENY", "INTERDICT", "EFFECT_ALREADY_BOUND", "INSUFFICIENT_EVIDENCE"}
    require(required_results.issubset(set(fixture.get("allowed_results", []))), "fixture allowed results are incomplete")
    required_points = {
        "before_S5_external_effect",
        "at_S5_execution_or_transmission",
        "at_S6_validation_and_proof_generation",
        "at_S7_proof_verification",
        "after_interdiction_or_success",
    }
    require(required_points.issubset(set(fixture.get("attempt", {}).get("required_observation_points", []))), "fixture observation points are incomplete")
    for key in ("certification", "endorsement", "execution", "custody", "adverse_capability_conclusion"):
        require(fixture.get("authority", {}).get(key) is False, f"fixture authority.{key} must remain false")

    require(publication.get("evidence_id") == "arquivonulo-publication-verification", "publication template evidence_id is incorrect")
    require(publication.get("status") == "TEMPLATE_NOT_OBSERVED", "publication template must remain unobserved until populated from evidence")
    require(publication.get("commit_sha") is None, "publication template commit_sha must remain null before observation")
    routes = publication.get("routes", [])
    require(len(routes) == 3, "publication template must contain three public routes")
    urls = {item.get("url") for item in routes}
    required_urls = {
        "https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/arquivonulo",
        "https://stegverse-labs.github.io/admissibility-wiki/data/framework-evaluations/arquivonulo.json",
        "https://stegverse-labs.github.io/admissibility-wiki/status/arquivonulo-execution-boundary-status.json",
    }
    require(required_urls == urls, "publication template routes are incomplete or unexpected")
    closure = publication.get("closure", {})
    for key in ("canonical_validation_observed", "public_deployment_observed", "activation_receipt_closed"):
        require(closure.get(key) is False, f"publication closure.{key} must remain false before evidence")
    publication_authority = publication.get("authority_boundary", {})
    for key in ("publication_evidence_is_execution_authority", "certification_granted", "endorsement_granted", "custody_granted", "integration_claimed"):
        require(publication_authority.get(key) is False, f"publication authority_boundary.{key} must remain false")

    print("ARQUIVONULO EXECUTION BOUNDARY: PASS - doctrine, evaluation, registry, status, fixture, publication template, navigation, and handoff agree")


if __name__ == "__main__":
    main()
