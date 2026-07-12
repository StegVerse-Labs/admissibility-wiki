#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "external-frameworks" / "observed-evidence-capture-protocol.md"
QUEUE = ROOT / "docs" / "external-frameworks" / "observed-evidence-capture-queue.v0.1.json"
MAPPING_DIR = ROOT / "docs" / "external-frameworks" / "benchmark-mappings"
FIXTURE_DIR = ROOT / "docs" / "external-frameworks" / "fixtures"
HANDOFF = ROOT / "docs" / "external-frameworks" / "EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md"

PRIORITY_IDS = {"opa", "cedar-policy", "mcp", "a2a", "guardrails-ai", "llama-guard", "nemo-guardrails"}
ALLOWED_STATES = {
    "awaiting_capture",
    "captured_unverified",
    "observed_partial",
    "replay_ready",
    "replay_confirmed",
    "interoperability_candidate",
}
REQUIRED_CAPTURE_FIELDS = {
    "observation_id",
    "framework_id",
    "fixture_reference",
    "source_reference",
    "source_version_or_commit",
    "capture_timestamp_utc",
    "execution_environment",
    "exact_input",
    "exact_output",
    "exit_status_or_protocol_state",
    "policy_or_configuration_reference",
    "authority_context",
    "freshness_context",
    "trace_or_trajectory_reference",
    "artifact_hashes",
    "replay_instructions",
    "capture_limitations",
    "stegverse_expected_posture",
    "non_claims",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [PROTOCOL, QUEUE, MAPPING_DIR, FIXTURE_DIR, HANDOFF]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("OBSERVED EVIDENCE CAPTURE QUEUE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    protocol = PROTOCOL.read_text(encoding="utf-8")
    queue = load_json(QUEUE)
    handoff = HANDOFF.read_text(encoding="utf-8")

    if queue.get("artifact_type") != "external_framework_observed_evidence_capture_queue":
        failures.append("queue artifact type mismatch")
    if queue.get("schema_version") != "0.1":
        failures.append("queue schema version mismatch")
    if queue.get("status") != "AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE":
        failures.append("queue must remain explicitly non-observational before captures exist")

    declared_fields = set(queue.get("required_capture_fields", []))
    if declared_fields != REQUIRED_CAPTURE_FIELDS:
        failures.append("required capture fields do not match protocol contract")

    allowed_states = set(queue.get("allowed_states", []))
    if allowed_states != ALLOWED_STATES:
        failures.append("allowed evidence states mismatch")

    entries = [item for item in queue.get("entries", []) if isinstance(item, dict)]
    entry_ids = {item.get("framework_id") for item in entries}
    if entry_ids != PRIORITY_IDS:
        failures.append(f"priority framework set mismatch: {sorted(entry_ids)}")

    for item in entries:
        framework_id = item.get("framework_id")
        for key in ["framework_name", "fixture_reference", "capture_state", "capture_targets", "required_runtime", "next_action"]:
            if not item.get(key):
                failures.append(f"queue entry missing {key}: {framework_id}")
        if item.get("capture_state") != "awaiting_capture":
            failures.append(f"entry must remain awaiting_capture until exact evidence is attached: {framework_id}")
        if len(item.get("capture_targets", [])) < 3:
            failures.append(f"entry needs at least three capture targets: {framework_id}")

        mapping_path = MAPPING_DIR / f"{framework_id}.mapping.json"
        if not mapping_path.exists():
            failures.append(f"missing mapping companion: {framework_id}")

        fixture_path = ROOT / str(item.get("fixture_reference", ""))
        if not fixture_path.exists():
            failures.append(f"missing fixture reference: {framework_id}")

    authority = queue.get("authority_boundary", {})
    for key, value in authority.items():
        if value is not False:
            failures.append(f"queue authority boundary must be false: {key}")

    for phrase in [
        "fixture definition != observed output",
        "single run != replayability",
        "Missing source version, exact input, exact output, timestamp",
        "policy allow != StegVerse standing",
    ]:
        if phrase not in protocol:
            failures.append(f"protocol missing phrase: {phrase}")

    for phrase in [
        "observed-evidence-capture-protocol.md",
        "observed-evidence-capture-queue.v0.1.json",
    ]:
        if phrase not in handoff:
            failures.append(f"handoff missing reference: {phrase}")

    print("OBSERVED EVIDENCE CAPTURE QUEUE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
