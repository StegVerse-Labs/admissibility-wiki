#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "status" / "ecosystem-documentation-endpoints.json"
HEALTH = ROOT / "static" / "status" / "cross-wiki-health-status.json"
WRITER = ROOT / "scripts" / "write-public-activation-receipt.mjs"
WRITER_CHECK = ROOT / "scripts" / "check-public-activation-receipt-writer.mjs"
EXPECTED_ENDPOINTS = {
    "stegverse-site": ("StegVerse-Labs/Site", "https://stegverse-labs.github.io/Site/"),
    "admissibility-wiki": ("StegVerse-Labs/admissibility-wiki", "https://stegverse-labs.github.io/admissibility-wiki/"),
    "stegguardian-wiki": ("StegVerse-002/stegguardian-wiki", "https://stegverse-002.github.io/stegguardian-wiki/"),
    "stegtalk-wiki": ("StegVerse-Labs/stegtalk-wiki", "https://stegverse-labs.github.io/stegtalk-wiki/"),
}


def load_json(path: Path, failures: list[str], label: str) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing {label}: {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid {label} json: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    registry = load_json(REGISTRY, failures, "endpoint registry")
    health = load_json(HEALTH, failures, "cross-wiki health status")

    for path in (WRITER, WRITER_CHECK):
        if not path.exists():
            failures.append(f"missing automation surface: {path.relative_to(ROOT)}")

    if registry.get("record_type") != "stegverse_ecosystem_documentation_endpoints":
        failures.append("endpoint registry record type mismatch")
    endpoints = {item.get("id"): item for item in registry.get("endpoints", []) if isinstance(item, dict)}
    for endpoint_id, (repo, url) in EXPECTED_ENDPOINTS.items():
        item = endpoints.get(endpoint_id)
        if not item:
            failures.append(f"missing endpoint: {endpoint_id}")
            continue
        if item.get("repo") != repo:
            failures.append(f"endpoint repo mismatch: {endpoint_id}")
        if item.get("url") != url:
            failures.append(f"endpoint url mismatch: {endpoint_id}")
        if not item.get("role"):
            failures.append(f"endpoint role missing: {endpoint_id}")

    if health.get("record_type") != "admissibility_wiki_cross_wiki_health_status":
        failures.append("health record type mismatch")
    if health.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("health repo mismatch")
    if health.get("origin_public_url") != "https://stegverse-labs.github.io/admissibility-wiki/":
        failures.append("health origin url mismatch")
    if health.get("peer_registry") != "status/ecosystem-documentation-endpoints.json":
        failures.append("health peer registry mismatch")
    if health.get("status") != "pending_live_peer_checks":
        failures.append("health state must remain pending until run-bound live peer checks complete")

    checks = health.get("checks", {})
    if checks.get("peer_urls_declared") is not True:
        failures.append("peer urls declared must be true")
    if checks.get("origin_records_declared") is not True:
        failures.append("origin records declared must be true")
    for key in (
        "live_peer_http_confirmed",
        "peer_machine_records_confirmed",
        "cross_wiki_schema_consistency_confirmed",
    ):
        if checks.get(key) is not False:
            failures.append(f"{key} must remain false until verified by run-bound evidence")

    if health.get("manual_task_requirement") != "NONE":
        failures.append("manual task requirement must be NONE")
    if health.get("user_manual_action_required") is not False:
        failures.append("user manual action required must be false")
    if health.get("remaining_owner") != "CANONICAL_AUTOMATION_AND_SUCCESSOR_SCOPE":
        failures.append("remaining ownership must be canonical automation and successor scope")

    automation = health.get("automation")
    if not isinstance(automation, dict):
        failures.append("automation must be an object")
    else:
        expected = {
            "receipt_writer": "scripts/write-public-activation-receipt.mjs",
            "receipt_validator": "scripts/check-public-activation-receipt-writer.mjs",
            "receipt_artifact": "public-activation-receipt",
            "closure_key": "activation_closures.documentation_mesh",
            "closure_schema": "documentation_mesh_observation_closure.v1",
            "peer_root_checks_automatic": True,
            "peer_registry_checks_automatic": True,
            "peer_health_checks_automatic": True,
            "source_blocked_result_fail_closed": True,
            "handoff_reconciliation_required_for_continuation": False,
        }
        for key, value in expected.items():
            if automation.get(key) != value:
                failures.append(f"automation {key} mismatch")

    non_claims = health.get("non_claims", {})
    for key in (
        "cross_repo_authority_granted",
        "standing_conferred",
        "execution_authority",
        "downstream_mutation_authority_granted",
    ):
        if non_claims.get(key) is not False:
            failures.append(f"non-claim boundary must remain false: {key}")

    writer_text = WRITER.read_text(encoding="utf-8") if WRITER.exists() else ""
    for marker in (
        "documentation_mesh_observation_closure.v1",
        "SOURCE_BLOCKED_FAIL_CLOSED",
        "activation_closures",
        "documentation_mesh",
    ):
        if marker not in writer_text:
            failures.append(f"receipt writer missing documentation mesh marker: {marker}")

    print("ADMISSIBILITY DOCUMENTATION MESH:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
