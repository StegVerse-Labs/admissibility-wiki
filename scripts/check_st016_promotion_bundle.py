#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "exports" / "repo-standards" / "st016" / "promotion-bundle.json"
SCHEMA = ROOT / "exports" / "repo-standards" / "st016" / "documentation-mesh-observation-closure.schema.json"
DESTINATION_HANDOFF_MARKER = "RSTD-SANDBOX-FIRST-001"

REQUIRED_ARTIFACTS = {
    "exports/repo-standards/st016/documentation-mesh-observation-closure.schema.json",
    "scripts/write-public-activation-receipt.mjs",
    "scripts/check-public-activation-receipt-writer.mjs",
    "scripts/check_documentation_mesh_status.py",
    "static/status/ecosystem-documentation-endpoints.json",
    "static/status/cross-wiki-health-status.json",
}


def main() -> int:
    failures: list[str] = []
    for path in (BUNDLE, SCHEMA):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    expected = {
        "bundle_type": "repo_standards_promotion_bundle",
        "standard": "ST-016",
        "source_repository": "StegVerse-Labs/admissibility-wiki",
        "destination_repository": "StegVerse-Labs/repo-standards",
        "promotion_posture": "QUEUED_NON_COLLIDING_NO_DESTINATION_MUTATION",
    }
    for key, value in expected.items():
        if bundle.get(key) != value:
            failures.append(f"bundle {key} mismatch")

    if bundle.get("destination_active_goal_observed") != DESTINATION_HANDOFF_MARKER:
        failures.append("destination active-goal marker mismatch")

    artifacts = set(bundle.get("artifacts", []))
    missing = REQUIRED_ARTIFACTS - artifacts
    if missing:
        failures.append(f"bundle artifact list missing: {sorted(missing)}")
    for artifact in REQUIRED_ARTIFACTS:
        if not (ROOT / artifact).exists():
            failures.append(f"declared artifact missing: {artifact}")

    acceptance = bundle.get("acceptance", {})
    required_acceptance = {
        "existing_workflow_only": True,
        "new_workflow_required": False,
        "destination_mutation_authority_granted": False,
        "manual_copy_required": False,
        "user_manual_action_required": False,
    }
    for key, value in required_acceptance.items():
        if acceptance.get(key) is not value:
            failures.append(f"acceptance {key} mismatch")

    non_claims = bundle.get("non_claims", {})
    for key in (
        "destination_installed",
        "destination_validated",
        "release_authority_granted",
        "cross_repo_authority_granted",
        "standing_conferred",
        "execution_authority",
    ):
        if non_claims.get(key) is not False:
            failures.append(f"non-claim {key} must be false")

    if schema.get("title") != "ST-016 Documentation Mesh Observation Closure":
        failures.append("closure schema title mismatch")
    if schema.get("properties", {}).get("schema", {}).get("const") != "documentation_mesh_observation_closure.v1":
        failures.append("closure schema identifier mismatch")

    print("ST-016 PROMOTION BUNDLE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
