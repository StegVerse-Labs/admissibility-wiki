#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "correctability-projection.json"
EXPECTED_DIGEST = "sha256:030f22b998a6f9c382db5463a4cc55f6d70132d5dd20d880778b5efda9844536"
EXPECTED_INTERVENTIONS = [
    "pause", "deny", "revoke", "quarantine", "rollback",
    "redirect", "supersede", "compensate", "escalate",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main():
    data = json.loads(PATH.read_text())
    require(data.get("record_type") == "stegverse.correctability.admissibility_projection", "record_type")
    require(data.get("source_repository") == "StegVerse-Labs/StegCore", "source_repository")
    require(data.get("source_goal") == "CORRECTABILITY-LAYER-001", "source_goal")

    src = data.get("source_validation", {})
    require(src.get("workflow_run_id") == 30774680694, "workflow_run_id")
    require(src.get("job_id") == 91567818006, "job_id")
    require(src.get("fixture_count") == 10 and src.get("passed_count") == 10, "source validation counts")
    require(src.get("artifact_id") == 8841612361, "artifact_id")
    require(src.get("artifact_digest") == EXPECTED_DIGEST, "artifact_digest")

    interpretation = data.get("interpretation", {})
    for key in (
        "correctability_is_distinct_from_admissibility",
        "reconstructability_is_not_timely_correction",
        "late_request_is_not_timely_correction",
        "post_irreversibility_compensation_is_not_prevention",
        "successful_execution_is_not_authority",
    ):
        require(interpretation.get(key) is True, key)
    require(interpretation.get("allowed_interventions") == EXPECTED_INTERVENTIONS, "allowed_interventions")

    effect = data.get("admissibility_effect", {})
    require(effect.get("state") == "VERIFIED_SOURCE_SEMANTICS_INGESTED", "state")
    for key in (
        "admissibility_determined", "execution_authorized", "publication_authorized",
        "release_authorized", "custody_recorded", "guardian_authority",
    ):
        require(effect.get(key) is False, key)
    require(data.get("manual_user_action_required") is False, "manual_user_action_required")
    print("PASS: bounded correctability admissibility projection validated")


if __name__ == "__main__":
    main()
