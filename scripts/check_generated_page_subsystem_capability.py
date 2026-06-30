#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "docs" / "external-frameworks" / "generated-page-subsystem-capability.json"
STATE_MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"

REQUIRED_CAPABILITIES = [
    "framework_report_generation",
    "framework_results_page_generation",
    "page_metadata_generation",
    "page_mapping_generation",
    "page_status_validation",
    "closeout_state_generation",
    "validation_summary_generation",
    "ci_evidence_request_generation",
]


def main() -> int:
    failures: list[str] = []
    if not CAPABILITY.exists():
        print("GENERATED PAGE SUBSYSTEM CAPABILITY: FAIL")
        print("- capability artifact missing")
        return 1
    if not STATE_MODEL.exists():
        print("GENERATED PAGE SUBSYSTEM CAPABILITY: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(CAPABILITY.read_text(encoding="utf-8"))
    model = json.loads(STATE_MODEL.read_text(encoding="utf-8"))

    if data.get("artifact_type") != "generated_page_subsystem_capability":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("status") != "validated_fail_closed_before_release_authorization":
        failures.append("status mismatch")
    if data.get("validated_by") != "validate-chain-continuation.yml":
        failures.append("validated-by mismatch")
    if data.get("state_model") != "docs/external-frameworks/generated-page-state-model.json":
        failures.append("state model path mismatch")

    capabilities = {item.get("capability_id"): item for item in data.get("capabilities", [])}
    for capability_id in REQUIRED_CAPABILITIES:
        item = capabilities.get(capability_id)
        if not item:
            failures.append(f"missing capability: {capability_id}")
            continue
        for key in ["generator", "validator", "output_family"]:
            if not item.get(key):
                failures.append(f"capability field missing: {capability_id}.{key}")
        for key in ["generator", "validator"]:
            path = item.get(key)
            if isinstance(path, str) and not (ROOT / path).exists():
                failures.append(f"capability referenced file missing: {path}")

    evidence = data.get("evidence_artifacts", [])
    generated_outputs = model.get("generated_outputs", [])
    for output in generated_outputs:
        if output not in evidence:
            failures.append(f"state output missing from capability evidence: {output}")
    for artifact in evidence:
        if not isinstance(artifact, str) or not (ROOT / artifact).exists():
            failures.append(f"capability evidence missing: {artifact}")

    for blocker in model.get("tag", {}).get("blocked_by", []):
        if blocker not in data.get("blocked_until", []):
            failures.append(f"tag blocker missing from capability boundary: {blocker}")

    boundary = data.get("boundary", {})
    if boundary.get("capability_artifact_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("release_without_authorization_allowed") is not False:
        failures.append("release boundary mismatch")
    if boundary.get("downstream_install_before_tag_allowed") is not False:
        failures.append("downstream boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

    print("GENERATED PAGE SUBSYSTEM CAPABILITY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
