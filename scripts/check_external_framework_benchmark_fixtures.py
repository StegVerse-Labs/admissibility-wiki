#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "docs" / "external-frameworks" / "fixtures"
MAPPING_DIR = ROOT / "docs" / "external-frameworks" / "benchmark-mappings"
ROLLOUT = ROOT / "docs" / "external-frameworks" / "benchmark-mapping-rollout.json"
EXAMPLES = FIXTURE_DIR / "source-versioned-examples.v0.1.json"

REQUIRED_FRAMEWORK_FIXTURES = {
    "glm",
    "evide",
    "decisionassure",
    "mindforge",
    "morrison-runtime",
    "asro",
    "care-runtime",
    "aar",
    "mitre-atlas",
    "owasp-top-10-llm",
    "agent-governance-playbook",
    "killswitch-md",
    "nist-ai-rmf",
    "iso-iec-42001",
    "eu-ai-act",
    "policy-cards",
    "runtime-governance-policies-on-paths",
}

REQUIRED_AUTHORITY_FALSE_KEYS = {
    "fixture_is_authority",
    "external_framework_inclusion_is_execution_authority",
}

REQUIRED_EXAMPLE_FIELDS = {
    "example_id",
    "framework_id",
    "source_reference",
    "source_version_or_date",
    "fixture_reference",
    "benchmark_dimensions",
    "example_input",
    "expected_stegverse_posture",
    "non_claims",
    "missing_fields",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [FIXTURE_DIR, MAPPING_DIR, ROLLOUT, EXAMPLES]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK BENCHMARK FIXTURES: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    rollout = load_json(ROLLOUT)
    examples = load_json(EXAMPLES)
    rollout_ids = {entry.get("framework_id") for entry in rollout.get("entries", []) if isinstance(entry, dict)}
    mapping_ids = {load_json(path).get("framework_id") for path in MAPPING_DIR.glob("*.mapping.json")}

    fixture_ids: set[str] = set()
    fixture_paths = sorted(FIXTURE_DIR.glob("*-benchmark-fixture.v0.1.json"))
    fixture_paths += sorted(FIXTURE_DIR.glob("*-benchmark-observations.v0.1.json"))

    if not fixture_paths:
        failures.append("no benchmark fixture files found")

    for fixture_path in fixture_paths:
        fixture = load_json(fixture_path)
        framework_id = fixture.get("framework_id")
        fixture_ids.add(framework_id)
        artifact_type = fixture.get("artifact_type")

        if artifact_type not in {"external_framework_benchmark_fixture", "external_framework_runtime_benchmark_observation_fixture"}:
            failures.append(f"fixture artifact type mismatch: {fixture_path.relative_to(ROOT)}")
        if fixture.get("schema_version") != "0.1":
            failures.append(f"fixture schema mismatch: {fixture_path.relative_to(ROOT)}")
        if framework_id not in rollout_ids:
            failures.append(f"fixture framework not in rollout: {framework_id}")
        if framework_id not in mapping_ids:
            failures.append(f"fixture framework missing mapping companion: {framework_id}")

        if artifact_type == "external_framework_benchmark_fixture":
            cases = fixture.get("fixture_cases", [])
            if not isinstance(cases, list) or not cases:
                failures.append(f"fixture missing cases: {framework_id}")
            for case in cases:
                if not isinstance(case, dict):
                    failures.append(f"fixture case not object: {framework_id}")
                    continue
                for key in ["fixture_id", "benchmark_dimensions", "stegverse_expected_posture", "default_spe_result"]:
                    if key not in case:
                        failures.append(f"fixture case missing {key}: {framework_id}")
                if case.get("default_spe_result") != "FAIL-CLOSED":
                    failures.append(f"fixture case must default fail closed: {framework_id}:{case.get('fixture_id')}")
                if not case.get("missing_fields_fail_closed"):
                    failures.append(f"fixture case missing fail-closed fields: {framework_id}:{case.get('fixture_id')}")

        authority = fixture.get("authority_boundary", {})
        for required_key in REQUIRED_AUTHORITY_FALSE_KEYS:
            if authority.get(required_key) is not False:
                failures.append(f"fixture authority boundary missing false {required_key}: {framework_id}")
        for key, value in authority.items():
            if value is not False:
                failures.append(f"fixture authority boundary must be false: {framework_id}:{key}")

    for framework_id in sorted(REQUIRED_FRAMEWORK_FIXTURES):
        if framework_id not in fixture_ids:
            failures.append(f"missing required fixture framework: {framework_id}")

    if examples.get("artifact_type") != "external_framework_source_versioned_example_registry":
        failures.append("example registry artifact type mismatch")
    if examples.get("schema_version") != "0.1":
        failures.append("example registry schema mismatch")
    boundaries = examples.get("default_boundaries", {})
    for key in ["example_is_authority", "example_is_certification", "example_is_public_validation", "example_is_execution_authority"]:
        if boundaries.get(key) is not False:
            failures.append(f"example boundary must be false: {key}")
    for key in ["missing_source_fails_closed", "missing_timestamp_fails_closed", "missing_raw_payload_fails_closed"]:
        if boundaries.get(key) is not True:
            failures.append(f"example fail-closed boundary must be true: {key}")

    example_items = examples.get("examples", [])
    if not isinstance(example_items, list) or len(example_items) < 5:
        failures.append("example registry must include at least five examples")
    for item in example_items:
        if not isinstance(item, dict):
            failures.append("example item must be object")
            continue
        for field in REQUIRED_EXAMPLE_FIELDS:
            if field not in item:
                failures.append(f"example missing field {field}: {item.get('example_id')}")
        if item.get("framework_id") not in fixture_ids:
            failures.append(f"example framework missing fixture: {item.get('framework_id')}")
        for key, value in item.get("non_claims", {}).items():
            if value is not False:
                failures.append(f"example non-claim must be false: {item.get('example_id')}:{key}")
        if not item.get("missing_fields"):
            failures.append(f"example must preserve missing fields: {item.get('example_id')}")

    print("EXTERNAL FRAMEWORK BENCHMARK FIXTURES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
