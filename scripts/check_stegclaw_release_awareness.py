#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "stegclaw-release-awareness.json"

def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")

def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "1.0.0", "schema_version")
    require(data.get("record_type") == "admissibility_wiki.stegclaw.release_awareness", "record_type")
    require(data.get("source_repository") == "Data-Continuation/StegClaw", "source_repository")
    src = data.get("source_release", {})
    require(src.get("state") == "RELEASED", "release state")
    require(src.get("version") == "1.0.0", "version")
    require(src.get("tag_name") == "v1.0.0", "tag")
    require(src.get("release_id") == 381434394, "release id")
    require(src.get("release_target") == "6b89a4bfb3d4c2fcc61e6cccaa4f292fb4d58cdb", "release target")
    require(src.get("validation_run") == 33650991623, "validation run")
    require(src.get("validation_artifact_id") == 9854745757, "validation artifact")
    effect = data.get("local_effect", {})
    require(effect.get("state") == "RELEASE_AWARENESS_ONLY", "local state")
    for key in ("external_framework_protocol_modified","framework_evaluation_promoted","admissibility_determined","standing_granted","proof_granted","release_authorized","execution_authorized","custody_recorded","runtime_activation_claimed"):
        require(effect.get(key) is False, key)
    collision = data.get("collision_control", {})
    for key in ("issue_50_lane_untouched","external_framework_36_lane_untouched","riverbraid_lane_untouched","hil_dependency_lane_untouched"):
        require(collision.get(key) is True, key)
    arch = data.get("validation_architecture", {})
    require(arch.get("canonical_single_workflow_preserved") is True, "single workflow preserved")
    require(arch.get("dedicated_workflow_created") is False, "dedicated workflow absent")
    require(arch.get("validator_registered_via_workflow_sprawl_migrated_checks") is True, "migrated check binding")
    require(data.get("authority_effect") == "NONE", "authority effect")
    require(data.get("manual_user_action_required") is False, "manual action")
    print("PASS: StegClaw v1.0.0 Admissibility Wiki release awareness validated")

if __name__ == "__main__":
    main()
