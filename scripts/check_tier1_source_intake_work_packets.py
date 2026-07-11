#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "tier1-source-intake-work-packets.md"
DATA = ROOT / "docs" / "external-frameworks" / "tier1-source-intake-work-packets.json"
COVERAGE = ROOT / "docs" / "external-frameworks" / "framework-family-coverage.json"
INTAKE = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.json"

REQUIRED_FIELDS = {
    "canonical_source",
    "source_version_or_date",
    "published_scope",
    "published_non_claims",
    "artifact_type",
    "relationship_class",
    "benchmark_relevance",
    "authority_boundary",
    "evidence_posture",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [DOC, DATA, COVERAGE, INTAKE]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("TIER 1 SOURCE INTAKE WORK PACKETS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    data = load_json(DATA)
    coverage = load_json(COVERAGE)
    intake = load_json(INTAKE)

    if data.get("artifact_type") != "external_framework_source_intake_work_packets":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")

    for key, value in data.get("authority_boundary", {}).items():
        if value is not False:
            failures.append(f"authority boundary must be false: {key}")

    if set(data.get("required_capture_fields", [])) != REQUIRED_FIELDS:
        failures.append("required capture fields mismatch")

    tier1 = next((item for item in coverage.get("promotion_queue", []) if item.get("tier") == 1), None)
    expected_ids = set(tier1.get("candidate_ids", [])) if tier1 else set()
    packet_items = [item for item in data.get("packets", []) if isinstance(item, dict)]
    packet_ids = {item.get("candidate_id") for item in packet_items}

    if packet_ids != expected_ids:
        failures.append(f"packet ids do not match Tier 1 queue: packets={sorted(packet_ids)} expected={sorted(expected_ids)}")

    intake_by_id = {
        item.get("candidate_id"): item
        for item in intake.get("candidates", [])
        if isinstance(item, dict)
    }

    for packet in packet_items:
        candidate_id = packet.get("candidate_id")
        source = intake_by_id.get(candidate_id)
        if source is None:
            failures.append(f"packet missing intake candidate: {candidate_id}")
            continue
        if packet.get("name") != source.get("name"):
            failures.append(f"packet name mismatch: {candidate_id}")
        if packet.get("intake_class") != source.get("intake_class"):
            failures.append(f"packet intake class mismatch: {candidate_id}")
        if packet.get("priority_tier") != 1:
            failures.append(f"packet priority tier must be 1: {candidate_id}")
        if packet.get("target_state") != "sourced_intake":
            failures.append(f"packet target state mismatch: {candidate_id}")
        if packet.get("status") != "source_capture_required":
            failures.append(f"packet must remain source_capture_required: {candidate_id}")
        if packet.get("expected_relationship_class") not in {"synonymous", "adjacent", "new", "unresolved"}:
            failures.append(f"invalid expected relationship class: {candidate_id}")
        if not packet.get("capture_focus"):
            failures.append(f"packet missing capture focus: {candidate_id}")
        if not packet.get("expected_benchmark_dimensions"):
            failures.append(f"packet missing expected benchmark dimensions: {candidate_id}")

    for phrase in [
        "work packet != sourced intake",
        "A packet with missing fields remains `source_capture_required`.",
        "Packet completion only permits sourced-intake review.",
    ]:
        if phrase not in doc:
            failures.append(f"work packet doc missing phrase: {phrase}")

    print("TIER 1 SOURCE INTAKE WORK PACKETS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
