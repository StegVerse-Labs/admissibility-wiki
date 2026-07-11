#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BLOCKERS = ROOT / "docs" / "external-frameworks" / "goal5-external-blockers.json"
CLASSIFICATION = ROOT / "docs" / "external-frameworks" / "admissible-existence-seed-cycle-classification.json"
SEED_PAGE = ROOT / "docs" / "external-frameworks" / "admissible-existence-seed-cycle.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_BLOCKER_IDS = {
    "morrison-raw-audit-payload",
    "morrison-replay-captures",
    "source-versioned-example-payloads",
    "workflow-result-capture",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [BLOCKERS, CLASSIFICATION, SEED_PAGE, HANDOFF]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("GOAL 5 EXTERNAL BLOCKERS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    blockers = load_json(BLOCKERS)
    classification = load_json(CLASSIFICATION)
    seed_page = SEED_PAGE.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    if blockers.get("artifact_type") != "goal5_external_dependency_blocker_registry":
        failures.append("blocker registry artifact type mismatch")
    if blockers.get("schema_version") != "0.1":
        failures.append("blocker registry schema version mismatch")

    blocker_items = blockers.get("blockers", [])
    blocker_ids = {item.get("blocker_id") for item in blocker_items if isinstance(item, dict)}
    for blocker_id in sorted(REQUIRED_BLOCKER_IDS):
        if blocker_id not in blocker_ids:
            failures.append(f"missing required blocker: {blocker_id}")

    for item in blocker_items:
        if not isinstance(item, dict):
            failures.append("blocker must be object")
            continue
        blocker_id = item.get("blocker_id")
        for key in [
            "dependency_type",
            "required_artifact",
            "current_state",
            "owner_boundary",
            "fallback_posture",
            "next_action",
        ]:
            if not item.get(key):
                failures.append(f"blocker missing {key}: {blocker_id}")
        if item.get("blocks_structure_completion") is not False:
            failures.append(f"blocker must not block structure completion: {blocker_id}")
        if item.get("blocks_validation_release_readiness") is not True:
            failures.append(f"blocker must block validation release readiness: {blocker_id}")

    authority = blockers.get("authority_boundary", {})
    for key, value in authority.items():
        if value is not False:
            failures.append(f"blocker authority boundary must be false: {key}")

    if classification.get("artifact_type") != "external_framework_scope_classification":
        failures.append("seed-cycle classification artifact type mismatch")
    if classification.get("schema_version") != "0.1":
        failures.append("seed-cycle classification schema version mismatch")
    if classification.get("classification") != "mirror_only_internal_ecosystem_status":
        failures.append("seed-cycle classification must remain mirror-only")
    if classification.get("benchmark_mapping_required") is not False:
        failures.append("seed-cycle benchmark mapping must not be required")

    classification_authority = classification.get("authority_boundary", {})
    for key, value in classification_authority.items():
        if value is not False:
            failures.append(f"seed-cycle authority boundary must be false: {key}")

    for phrase in [
        "ecosystem seed-cycle status mirror",
        "not as an external-framework validation claim",
        "The seed-cycle mirror does not create execution authority.",
    ]:
        if phrase not in seed_page:
            failures.append(f"seed-cycle page missing phrase: {phrase}")

    for phrase in [
        "goal5-external-blockers.json",
        "admissible-existence-seed-cycle-classification.json",
    ]:
        if phrase not in handoff:
            failures.append(f"handoff missing reference: {phrase}")

    print("GOAL 5 EXTERNAL BLOCKERS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
