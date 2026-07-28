#!/usr/bin/env python3
"""Validate the TA-14 continuous actor-standing public documentation chain."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "ta-14.md"
ASSESSMENT = ROOT / "docs" / "external-frameworks" / "ta-14-registry-public-record-assessment.md"
REFERENCE_DOCKET_PAGE = ROOT / "docs" / "external-frameworks" / "ta-14-public-review-docket.md"
REFERENCE_DOCKET_RECORD = ROOT / "static" / "data" / "governed-framework-reviews" / "ta-14.reference-docket.v1.json"
REFERENCE_DOCKET_SCHEMA = ROOT / "static" / "schemas" / "governed-framework-review.schema.json"
REFERENCE_DOCKET_CHECK = ROOT / "scripts" / "check_governed_framework_review_reference.py"
PUBLIC_ROUTE_CHECK = ROOT / "scripts" / "check_ta14_public_routes.py"
STATUS = ROOT / "static" / "status" / "ta-14-standing-reconstruction-status.json"
EVALUATION = ROOT / "static" / "data" / "framework-evaluations" / "ta-14.json"
FIXTURE = ROOT / "static" / "data" / "framework-evaluations" / "test-cases" / "ta14-continuous-standing-revalidation-v1.json"
OUTPUT_TEMPLATE = ROOT / "static" / "data" / "framework-evaluations" / "test-cases" / "ta14-continuous-standing-revalidation-output-template-v1.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TA-14 STANDING RECONSTRUCTION: FAIL - {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    doc = read(DOC)
    assessment = read(ASSESSMENT)
    reference_docket_page = read(REFERENCE_DOCKET_PAGE)
    public_route_check = read(PUBLIC_ROUTE_CHECK)
    sidebar = read(SIDEBAR)
    handoff = read(HANDOFF)

    status = json.loads(read(STATUS))
    evaluation = json.loads(read(EVALUATION))
    fixture = json.loads(read(FIXTURE))
    output_template = json.loads(read(OUTPUT_TEMPLATE))
    reference_docket_record = json.loads(read(REFERENCE_DOCKET_RECORD))
    reference_docket_schema = json.loads(read(REFERENCE_DOCKET_SCHEMA))

    for token in (
        "route admissibility != actor standing",
        "proof preserved != state revalidated",
        "PUBLICLY_UNRESOLVED != disproven",
        "Does TA-14 independently recompute",
    ):
        require(token in doc, f"primary doctrine missing token: {token}")

    for token in (
        "record preservation != current-state reconstruction",
        "Independent current actor-standing reconstruction: PUBLICLY_UNRESOLVED",
        "authoritative external source",
        "This assessment does not claim intentional evasion",
    ):
        require(token in assessment, f"registry assessment missing token: {token}")

    for token in (
        "review-ta14-reference-docket-2026-07-27",
        "Public Reconstruction Procedure",
        "PUBLICLY_UNRESOLVED",
        "Publication creates no execution authority",
    ):
        require(token in reference_docket_page, f"reference docket page missing token: {token}")

    for token in (
        "reports/ta14-public-route-observation.json",
        "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE",
        "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "Publication does not establish that TA-14 independently reconstructs current actor standing.",
    ):
        require(token in public_route_check, f"public route checker missing token: {token}")

    require(
        "external-frameworks/ta-14-registry-public-record-assessment" in sidebar,
        "registry assessment is not exposed in the sidebar",
    )
    require(
        "external-frameworks/ta-14-public-review-docket" in sidebar,
        "reference docket is not exposed in the sidebar",
    )
    require(
        "TA-14: standing PUBLICLY_UNRESOLVED" in handoff,
        "mirror handoff does not preserve the TA-14 standing boundary",
    )
    require(
        "Manifest id: public-anchor-three-docket-freeze-2026-07-27" in handoff,
        "mirror handoff does not bind TA-14 into the frozen three-docket manifest",
    )

    require(status.get("continuous_actor_standing_reconstruction") == "PUBLICLY_UNRESOLVED", "status must remain PUBLICLY_UNRESOLVED")
    require(status.get("standing_revocation_fixture") == "FROZEN_PROPOSED_NOT_RUN", "fixture must remain frozen and unrun")
    require(status.get("validation", {}).get("public_route_observation") == "PENDING", "public route observation must remain pending until workflow evidence exists")
    require(status.get("authority_boundary", {}).get("activation_authority_granted") is False, "status must deny activation authority")
    require(status.get("authority_boundary", {}).get("adverse_capability_conclusion") is False, "status must not infer adverse capability")

    determinations = evaluation.get("determinations", [])
    require(determinations, "machine-readable evaluation has no determination")
    require(
        any(item.get("continuous_actor_standing_reconstruction") == "PUBLICLY_UNRESOLVED" for item in determinations),
        "machine-readable evaluation does not preserve PUBLICLY_UNRESOLVED",
    )

    tests = evaluation.get("test_runs", [])
    require(
        any(item.get("test_id") == "ta14-continuous-standing-revalidation-001" and item.get("status") == "PROPOSED_NOT_RUN" for item in tests),
        "machine-readable evaluation is missing the proposed standing-revalidation test",
    )

    require(fixture.get("test_case_id") == "ta14-continuous-standing-revalidation-v1", "fixture id mismatch")
    require(fixture.get("status") == "FROZEN_PROPOSED_NOT_RUN", "fixture must remain frozen and unrun")
    require(fixture.get("preserved_route_record", {}).get("mutation_allowed") is False, "fixture must prohibit route mutation")
    require(fixture.get("external_state_mutation", {}).get("preserved_route_modified") is False, "external revocation must not mutate the preserved route")
    require(
        set(fixture.get("expected_discriminating_outcome", {}).get("acceptable_decisions", [])) == {"HOLD", "DENY", "ESCALATE"},
        "fixture acceptable decisions must be HOLD, DENY, or ESCALATE",
    )
    require(fixture.get("expected_discriminating_outcome", {}).get("must_occur_before_consequence") is True, "decision must occur before consequence")
    require(fixture.get("authority_boundary", {}).get("test_fixture_establishes_framework_failure") is False, "fixture must not infer framework failure")
    require(fixture.get("authority_boundary", {}).get("test_fixture_establishes_framework_capability") is False, "fixture must not infer framework capability")

    require(output_template.get("test_case_id") == fixture.get("test_case_id"), "output template does not bind to the frozen fixture")
    require(output_template.get("determination", {}).get("continuous_actor_standing_reconstruction") == "UNDETERMINED_UNTIL_RUN", "output template must remain undetermined")
    require(
        set(output_template.get("determination", {}).get("allowed_values", [])) == {
            "SUPPORTED_BY_THIS_TEST",
            "NOT_SUPPORTED_BY_THIS_TEST",
            "PUBLICLY_UNRESOLVED",
        },
        "output template determination values are incomplete",
    )
    require(output_template.get("authority_boundary", {}).get("certification_granted") is False, "output template must deny certification")
    require(output_template.get("authority_boundary", {}).get("execution_authority_granted") is False, "output template must deny execution authority")

    require(reference_docket_schema.get("title") == "Governed Framework Review Record", "reference docket schema title mismatch")
    require(reference_docket_record.get("schema_version") == "governed-framework-review.v1", "reference docket schema version mismatch")
    require(reference_docket_record.get("review_id") == "review-ta14-reference-docket-2026-07-27", "reference docket review id mismatch")
    require(reference_docket_record.get("current_standing") == "PUBLICLY_UNRESOLVED", "reference docket must remain PUBLICLY_UNRESOLVED")
    require(reference_docket_record.get("reconstruction_status") == "PARTIAL", "reference docket reconstruction status must remain PARTIAL")
    require(reference_docket_record.get("verified_capabilities") == [], "reference docket must not claim verified capabilities before a live result")
    require(
        any(item.get("test_id") == "ta14-continuous-standing-revalidation-001" and item.get("result") == "NOT_RUN" for item in reference_docket_record.get("test_results", [])),
        "reference docket must preserve the standing test as NOT_RUN",
    )

    result = subprocess.run(
        [sys.executable, str(REFERENCE_DOCKET_CHECK)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout.rstrip())
    require(result.returncode == 0, "reference docket validator failed")

    required_routes = {
        "/external-frameworks/ta-14",
        "/external-frameworks/ta-14-registry-public-record-assessment",
        "/status/ta-14-standing-reconstruction-status.json",
        "/data/framework-evaluations/test-cases/ta14-continuous-standing-revalidation-v1.json",
        "/data/framework-evaluations/test-cases/ta14-continuous-standing-revalidation-output-template-v1.json",
    }
    require(required_routes.issubset(set(status.get("public_routes", []))), "status record is missing one or more public routes")

    print("TA-14 STANDING RECONSTRUCTION: PASS - doctrine, assessment, reference docket, schema, status, evaluation, frozen fixture, output template, public route checker, navigation, and handoff agree")


if __name__ == "__main__":
    main()
