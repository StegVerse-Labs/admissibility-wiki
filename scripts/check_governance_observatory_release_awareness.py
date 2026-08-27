#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "governance-observatory-release-awareness.json"

def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")

def main():
    data = json.loads(PATH.read_text())
    require(data.get("schema_version") == "1.0.0", "schema_version")
    require(data.get("record_type") == "admissibility_wiki.governance_observatory.release_awareness", "record_type")
    require(data.get("repository") == "StegVerse-Labs/admissibility-wiki", "repository")
    require(data.get("source_repository") == "StegVerse-Labs/governance-observatory", "source_repository")
    src = data.get("source_release", {})
    require(src.get("state") == "RELEASED", "release state")
    require(src.get("version") == "0.1.0", "version")
    require(src.get("tag_name") == "v0.1.0", "tag")
    require(src.get("release_id") == 377486341, "release id")
    require(src.get("release_state_head") == "31afc11745507e4764c2c9f44be1e5143e920ef1", "release head")
    require(src.get("release_workflow_run") == 33025454602, "release workflow")
    effect = data.get("local_effect", {})
    require(effect.get("state") == "RELEASE_AWARENESS_ONLY", "local state")
    for key in (
        "external_framework_protocol_modified","framework_evaluation_promoted",
        "admissibility_determined","standing_granted","proof_granted",
        "release_authorized","execution_authorized","custody_recorded",
    ):
        require(effect.get(key) is False, key)
    collision = data.get("collision_control", {})
    for key in (
        "external_framework_second_page_lane_untouched",
        "issue_50_canonical_validation_lane_untouched",
        "riverbraid_lane_untouched",
    ):
        require(collision.get(key) is True, key)
    arch = data.get("validation_architecture", {})
    require(arch.get("canonical_single_workflow_preserved") is True, "single workflow preserved")
    require(arch.get("dedicated_workflow_created") is False, "dedicated workflow absent")
    require(arch.get("validator_registered_via_workflow_sprawl_migrated_checks") is True, "migrated validation binding")
    aegis = data.get("aegisai_boundary", {})
    require(aegis.get("source_only") is True, "AEGISAI source-only")
    require(aegis.get("runtime_validated") is False, "AEGISAI runtime boundary")
    require(aegis.get("framework_promoted") is False, "AEGISAI framework boundary")
    require(data.get("manual_user_action_required") is False, "manual user action")
    print("PASS: Governance Observatory v0.1.0 Admissibility Wiki release awareness validated")

if __name__ == "__main__":
    main()
