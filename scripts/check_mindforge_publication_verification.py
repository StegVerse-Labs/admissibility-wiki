#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs/external-frameworks/evidence/mindforge-publication-verification.template.json"
STATUS = ROOT / "static/status/mindforge-boundary-review-status.json"
AUTH = ROOT / "static/status/mindforge-publication-attribution-authorization.json"
HANDOFF = ROOT / "docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md"

EXPECTED_ROUTES = {
    "/external-frameworks/mindforge",
    "/external-frameworks/commit-time-interoperability-contract",
    "/schemas/standing-determination-receipt.schema.json",
    "/status/mindforge-boundary-review-status.json",
}


def main() -> int:
    failures: list[str] = []
    for path in (TEMPLATE, STATUS, AUTH, HANDOFF):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("MINDFORGE PUBLICATION VERIFICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    auth = json.loads(AUTH.read_text(encoding="utf-8"))
    handoff = HANDOFF.read_text(encoding="utf-8")

    if template.get("schema_version") != "mindforge_publication_verification.v1":
        failures.append("publication template schema mismatch")
    if template.get("goal_id") != "mindforge-commit-time-boundary-activation":
        failures.append("publication template goal mismatch")

    routes = template.get("routes")
    if not isinstance(routes, list):
        failures.append("routes must be a list")
        routes = []
    observed_routes = {item.get("route") for item in routes if isinstance(item, dict)}
    if observed_routes != EXPECTED_ROUTES:
        failures.append(f"route set mismatch: {sorted(observed_routes)}")

    authority = template.get("authority_boundary")
    if not isinstance(authority, dict):
        failures.append("missing authority boundary")
    else:
        for field in (
            "publication_creates_framework_standing",
            "publication_creates_execution_authority",
            "publication_is_official_mindforge_specification",
            "publication_is_compatibility_certification",
        ):
            if authority.get(field) is not False:
                failures.append(f"{field} must remain false")

    auth_state = auth.get("authorization_state")
    if template.get("attribution_authorization_state") != auth_state:
        failures.append("publication template authorization state drift")

    pending = auth_state == "PENDING_REVIEWER_RESPONSE"
    if pending and template.get("reviewer_attribution_published") is not False:
        failures.append("pending reviewer authorization cannot publish attribution")

    state = template.get("state")
    if state == "VERIFIED":
        if template.get("workflow_conclusion") != "success":
            failures.append("verified publication requires successful workflow")
        if template.get("build_pages_conclusion") != "success":
            failures.append("verified publication requires successful build-pages")
        if template.get("deploy_pages_conclusion") != "success":
            failures.append("verified publication requires successful deploy-pages")
        for item in routes:
            if item.get("reachable") is not True or item.get("content_verified") is not True:
                failures.append(f"verified state lacks route evidence: {item.get('route')}")
    elif state != "TEMPLATE_NOT_OBSERVED":
        failures.append(f"unsupported publication state: {state}")

    if status.get("publication_verification_template") != str(TEMPLATE.relative_to(ROOT)):
        failures.append("status does not bind publication verification template")
    for marker in (
        "mindforge-publication-verification.template.json",
        "public route verification",
        "publication activation",
    ):
        if marker not in handoff:
            failures.append(f"handoff missing publication marker: {marker}")

    if failures:
        print("MINDFORGE PUBLICATION VERIFICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "MINDFORGE PUBLICATION VERIFICATION: PASS "
        f"(state={state}; routes={len(routes)}; attribution={auth_state}; activation_closed=" 
        f"{template.get('activation_receipt_closed')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
