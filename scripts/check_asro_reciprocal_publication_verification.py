#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "asro-reciprocal-publication-verification.json"
CHECKER = ROOT / "scripts" / "check_governed_llm_deployment_status.py"

REQUIRED_ROUTE_KEYS = (
    "asro_external_framework_page",
    "asro_reciprocal_status",
    "asro_framework_record",
    "asro_test_case",
    "asro_stegverse_run",
)


def main() -> int:
    failures: list[str] = []
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    checker = CHECKER.read_text(encoding="utf-8")

    if status.get("state") != "AUTOMATED_PUBLIC_ROUTE_OBSERVATION_PENDING_NEXT_CANONICAL_WORKFLOW":
        failures.append("unexpected publication-verification state")
    observation = status.get("workflow_observation", {})
    if observation.get("checker") != "scripts/check_governed_llm_deployment_status.py":
        failures.append("public checker binding missing")
    if observation.get("report") != "reports/asro-reciprocal-public-route-observation.json":
        failures.append("ASRO public observation report path missing")
    if observation.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("canonical workflow binding missing")
    if observation.get("job") != "verify-public-pages":
        failures.append("public verification job binding missing")
    if observation.get("user_manual_action_required") is not False:
        failures.append("publication observation must not create a user task")

    bounded = status.get("bounded_result", {})
    expected = {
        "stegverse_bounded_run": "PASS",
        "correspondence": "ESTABLISHED",
        "replay": "PASS",
        "reconstruction": "PASS",
        "external_asro_native_execution": "NOT_TESTED",
        "reviewer_issuer": "unresolved",
    }
    for key, value in expected.items():
        if bounded.get(key) != value:
            failures.append(f"bounded result mismatch: {key}")

    for key, value in status.get("authority", {}).items():
        if value is not False:
            failures.append(f"authority escalation: {key}")

    for route_key in REQUIRED_ROUTE_KEYS:
        if f'"{route_key}"' not in checker:
            failures.append(f"public checker missing route: {route_key}")
    for marker in (
        'ASRO_RECEIPT = Path("reports/asro-reciprocal-public-route-observation.json")',
        '"external_asro_native_execution": "NOT_TESTED"',
        '"reviewer_issuer": "unresolved"',
        '"downstream_mutation_authority_granted": False',
        '"interoperability_verified": False',
    ):
        if marker not in checker:
            failures.append(f"public checker missing marker: {marker}")

    if failures:
        print("ASRO RECIPROCAL PUBLICATION VERIFICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO RECIPROCAL PUBLICATION VERIFICATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
