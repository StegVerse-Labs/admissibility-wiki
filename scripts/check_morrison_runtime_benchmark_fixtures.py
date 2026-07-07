#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "docs" / "external-frameworks" / "fixtures" / "morrison-runtime-benchmark-observations.v0.1.json"
CC = ROOT / "docs" / "external-frameworks" / "morrison-runtime-commitment-candidate.json"
REPORT = ROOT / "docs" / "external-frameworks" / "reports" / "morrison-runtime.compatibility.json"
BOUNDARY = ROOT / "docs" / "external-frameworks" / "morrison-runtime-boundary-observation.md"

REQUIRED_OBSERVATION_IDS = {
    "mrg-rg-003-prepare-allow-001": "ALLOW",
    "mrg-rg-002-transfer-block-001": "BLOCK",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [OBS, CC, REPORT, BOUNDARY]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("MORRISON RUNTIME BENCHMARK FIXTURES: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    obs = load_json(OBS)
    cc = load_json(CC)
    report = load_json(REPORT)
    boundary = BOUNDARY.read_text(encoding="utf-8")

    if obs.get("artifact_type") != "external_framework_runtime_benchmark_observation_fixture":
        failures.append("observation fixture artifact type mismatch")
    if cc.get("artifact_type") != "external_framework_commitment_candidate_fixture":
        failures.append("commitment candidate artifact type mismatch")
    if obs.get("framework_id") != "morrison-runtime" or cc.get("framework_id") != "morrison-runtime":
        failures.append("framework id mismatch")

    observation_map = {
        item.get("observation_id"): item
        for item in obs.get("observations", [])
        if isinstance(item, dict)
    }
    for observation_id, expected_result in REQUIRED_OBSERVATION_IDS.items():
        item = observation_map.get(observation_id)
        if not item:
            failures.append(f"missing observation: {observation_id}")
            continue
        if item.get("observed_result") != expected_result:
            failures.append(f"observation {observation_id} result mismatch")
        if not item.get("exact_input"):
            failures.append(f"observation {observation_id} missing exact input")
        if not item.get("evaluated_steps"):
            failures.append(f"observation {observation_id} missing evaluated steps")
        if item.get("parser_status") != "parsed_two_steps":
            failures.append(f"observation {observation_id} parser status mismatch")
        if "raw_audit_payload" not in item.get("missing_fields", []):
            failures.append(f"observation {observation_id} must preserve raw audit missing field")

    replay = obs.get("replay_plan", {})
    if replay.get("minimum_runs_per_case") != 3:
        failures.append("replay plan minimum run count mismatch")
    if replay.get("fail_closed_on_mismatch") is not True:
        failures.append("replay plan must fail closed on mismatch")

    authority = obs.get("authority_boundary", {})
    for key in [
        "fixture_is_authority",
        "runtime_allow_is_stegverse_allow",
        "runtime_block_is_stegverse_certification",
        "captured_observation_is_general_validation",
    ]:
        if authority.get(key) is not False:
            failures.append(f"observation authority boundary mismatch: {key}")

    cc_authority = cc.get("authority_boundary", {})
    for key in [
        "commitment_candidate_is_authority",
        "morrison_runtime_allow_is_authority",
        "morrison_runtime_block_is_certification",
        "external_framework_inclusion_is_certification",
        "external_framework_inclusion_is_execution_authority",
    ]:
        if cc_authority.get(key) is not False:
            failures.append(f"commitment candidate boundary mismatch: {key}")

    observed_inputs = cc.get("observed_inputs", [])
    if len(observed_inputs) < 2:
        failures.append("commitment candidate must include both preparation and execution observations")
    if cc.get("expected_spe_result", {}).get("default") != "FAIL-CLOSED":
        failures.append("commitment candidate default SPE result must fail closed")

    report_observations = report.get("runtime_governance_benchmark_observations", [])
    if len(report_observations) < 2:
        failures.append("compatibility report missing benchmark observations")

    for phrase in [
        "Observed Case A: Preparation Permitted",
        "Observed Case B: Execution-Capable Transfer Blocked",
        "This page does not claim Morrison Runtime is defective.",
    ]:
        if phrase not in boundary:
            failures.append(f"boundary page missing phrase: {phrase}")

    print("MORRISON RUNTIME BENCHMARK FIXTURES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
