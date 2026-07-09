#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "goal5-release-readiness.md"
DATA = ROOT / "docs" / "external-frameworks" / "goal5-release-readiness.json"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_STRUCTURE_TRUE = {
    "benchmark_suite_installed",
    "mapping_companions_installed",
    "fixture_artifacts_installed",
    "expanded_intake_installed",
    "promotion_criteria_installed",
    "release_readiness_gate_installed",
}

REQUIRED_EVIDENCE_KEYS = {
    "source_versioned_examples_attached",
    "morrison_raw_audit_payloads_attached",
    "morrison_replay_captures_attached",
    "candidate_promotions_sourced",
    "build_verification_passed",
}

REQUIRED_TARGETS = {
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-Labs/stegguardian-wiki",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [DOC, DATA, HANDOFF]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")
    if failures:
        print("GOAL 5 RELEASE READINESS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    data = load_json(DATA)

    if data.get("artifact_type") != "goal5_external_framework_release_readiness":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("release_readiness") != "not_ready_for_tag":
        failures.append("release readiness must remain not_ready_for_tag until evidence gates complete")

    structure = data.get("structure_status", {})
    for key in sorted(REQUIRED_STRUCTURE_TRUE):
        if structure.get(key) is not True:
            failures.append(f"structure gate must be true: {key}")

    evidence = data.get("evidence_status", {})
    for key in sorted(REQUIRED_EVIDENCE_KEYS):
        if key not in evidence:
            failures.append(f"missing evidence gate: {key}")
        elif evidence[key] is not False:
            failures.append(f"evidence gate should remain false until completed: {key}")

    disallowed = data.get("disallowed_claims", {})
    for key, value in disallowed.items():
        if value is not False:
            failures.append(f"disallowed claim must be false: {key}")

    targets = set(data.get("cross_repo_update_targets", []))
    for target in sorted(REQUIRED_TARGETS):
        if target not in targets:
            failures.append(f"missing cross repo update target: {target}")

    for phrase in [
        "release_readiness: not_ready_for_tag",
        "Goal 5 does not certify external frameworks.",
        "When this goal reaches tag/release readiness",
        "Release readiness is not certification.",
    ]:
        if phrase not in doc:
            failures.append(f"release doc missing phrase: {phrase}")

    if "goal5-release-readiness" not in handoff:
        failures.append("handoff missing release readiness reference")

    print("GOAL 5 RELEASE READINESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
