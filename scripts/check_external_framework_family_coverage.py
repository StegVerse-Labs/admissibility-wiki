#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "framework-family-coverage.md"
DATA = ROOT / "docs" / "external-frameworks" / "framework-family-coverage.json"
INTAKE = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.json"
INDEX = ROOT / "docs" / "external-frameworks" / "index.md"
SIDEBAR = ROOT / "sidebars.js"

REQUIRED_CLASSES = {
    "runtime_governance",
    "policy_as_code",
    "provenance_and_trace",
    "identity_and_authority",
    "risk_and_assurance",
    "threat_and_security",
    "privacy_and_data_governance",
    "model_eval_and_monitoring",
    "regulatory_and_standards",
    "agent_protocols",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [DOC, DATA, INTAKE, INDEX, SIDEBAR]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK FAMILY COVERAGE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    data = load_json(DATA)
    intake = load_json(INTAKE)
    index = INDEX.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    if data.get("artifact_type") != "external_framework_family_coverage":
        failures.append("coverage artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("coverage schema version mismatch")

    posture = data.get("posture", {})
    for key, value in posture.items():
        if value is not False:
            failures.append(f"coverage posture must be false: {key}")

    candidates = [item for item in intake.get("candidates", []) if isinstance(item, dict)]
    actual_counts = Counter(item.get("intake_class") for item in candidates)
    declared_counts = {
        item.get("intake_class"): item.get("candidate_count")
        for item in data.get("families", [])
        if isinstance(item, dict)
    }

    if set(declared_counts) != REQUIRED_CLASSES:
        failures.append("coverage families must match all required intake classes")
    for intake_class in sorted(REQUIRED_CLASSES):
        if declared_counts.get(intake_class) != actual_counts.get(intake_class):
            failures.append(
                f"candidate count mismatch for {intake_class}: "
                f"declared={declared_counts.get(intake_class)} actual={actual_counts.get(intake_class)}"
            )

    if data.get("candidate_total") != len(candidates):
        failures.append("candidate total mismatch")

    candidate_ids = {item.get("candidate_id") for item in candidates}
    queued_ids: list[str] = []
    tiers = data.get("promotion_queue", [])
    if len(tiers) != 3:
        failures.append("promotion queue must contain three tiers")
    for tier in tiers:
        if not isinstance(tier, dict):
            failures.append("promotion tier must be object")
            continue
        if tier.get("tier") not in {1, 2, 3}:
            failures.append(f"invalid promotion tier: {tier.get('tier')}")
        ids = tier.get("candidate_ids", [])
        if not ids:
            failures.append(f"promotion tier has no candidates: {tier.get('tier')}")
        for candidate_id in ids:
            if candidate_id not in candidate_ids:
                failures.append(f"promotion queue candidate missing from intake: {candidate_id}")
            queued_ids.append(candidate_id)

    duplicates = [candidate_id for candidate_id, count in Counter(queued_ids).items() if count > 1]
    for candidate_id in duplicates:
        failures.append(f"candidate appears in multiple promotion tiers: {candidate_id}")

    if len(data.get("future_gap_families", [])) < 8:
        failures.append("future gap family coverage is too narrow")

    for phrase in [
        "family coverage != validation",
        "promotion priority != endorsement",
        "Current total: **42 source-required candidates across 10 intake classes**.",
        "Standing must be reconstructed",
    ]:
        if phrase not in doc:
            failures.append(f"coverage doc missing phrase: {phrase}")

    if "External Framework Family Coverage" not in index:
        failures.append("external frameworks index missing coverage reference")
    if "external-frameworks/framework-family-coverage" not in sidebar:
        failures.append("sidebar missing coverage page")

    print("EXTERNAL FRAMEWORK FAMILY COVERAGE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
