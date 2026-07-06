#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "external-frameworks"
REGISTRY = DOCS / "index.json"
ROLLOUT = DOCS / "evidence-provenance-rollout.json"

REQUIRED_STANDARD_FILES = [
    DOCS / "evaluation-standard.md",
    DOCS / "failure-class-catalog.md",
    DOCS / "external-framework-template.md",
    DOCS / "EXPANSION_POLICY.json",
    DOCS / "evidence-provenance-rollout.md",
    ROLLOUT,
]

REQUIRED_INDEX_LINKS = [
    "./evaluation-standard.md",
    "./failure-class-catalog.md",
    "./external-framework-template.md",
    "./evidence-provenance-rollout.md",
]

REQUIRED_STANDARD_TERMS = [
    "Evidence Provenance",
    "Claim Traceability Rule",
    "Comparative Fairness Rule",
    "Observed Behavior Rule",
    "Required Runtime Result Artifact Set",
    "Machine-Readable Companion Requirement",
]

REQUIRED_FAILURE_CLASSES = [
    "FC-001",
    "Semantic Equivalence Divergence",
    "FC-007",
    "Fail-Open Runtime Error",
    "FC-012",
    "Evidence Class Confusion",
]

REQUIRED_TEMPLATE_SECTIONS = [
    "## Evidence Provenance",
    "## Parameterized Test Cases",
    "## StegVerse Analysis",
    "## Failure Classes",
    "## Non-Claims",
]

BATCH1_PAGE_REQUIREMENTS = {
    "glm": {
        "path": DOCS / "glm.md",
        "terms": [
            "## Evidence Provenance",
            "Official Framework Sources",
            "Official Implementation Sources",
            "Observed Behavior",
            "Reproduced Behavior",
            "StegVerse Analysis",
            "Interoperability Assessment",
            "Standing",
            "F1:",
            "S1:",
            "S2:",
        ],
    },
    "evide": {
        "path": DOCS / "evide.md",
        "terms": [
            "## Evidence Provenance",
            "Official Framework Sources",
            "Official Implementation Sources",
            "Observed Behavior",
            "Reproduced Behavior",
            "StegVerse Analysis",
            "Interoperability Assessment",
            "Standing",
            "F1:",
            "S1:",
            "S2:",
        ],
    },
    "morrison-runtime": {
        "path": DOCS / "morrison-runtime.md",
        "terms": [
            "Evidence Provenance",
            "Parameterized Boundary Case",
            "Semantic Value Movement Versus Tool Label",
            "FC-001",
            "raw audit payload",
            "timestamp",
        ],
    },
}

REQUIRED_ROLLOUT_ENTRY_FIELDS = [
    "framework_id",
    "name",
    "page",
    "source_status",
    "official_framework_sources",
    "official_implementation_sources",
    "observed_behavior",
    "reproduced_behavior",
    "stegverse_analysis",
    "interoperability_assessment",
    "standing",
    "next_action",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def main() -> int:
    failures: list[str] = []

    for path in REQUIRED_STANDARD_FILES + [REGISTRY]:
        if not path.exists():
            failures.append(f"missing standard file: {path.relative_to(ROOT)}")

    for framework_id, requirement in BATCH1_PAGE_REQUIREMENTS.items():
        path = requirement["path"]
        if not path.exists():
            failures.append(f"missing Batch 1 page: {framework_id}: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    index = read(DOCS / "index.md")
    standard = read(DOCS / "evaluation-standard.md")
    catalog = read(DOCS / "failure-class-catalog.md")
    template = read(DOCS / "external-framework-template.md")
    rollout_page = read(DOCS / "evidence-provenance-rollout.md")
    rollout = load_json(ROLLOUT)
    registry = load_json(REGISTRY)

    for link in REQUIRED_INDEX_LINKS:
        if link not in index:
            failures.append(f"index missing link: {link}")

    for term in REQUIRED_STANDARD_TERMS:
        if term not in standard:
            failures.append(f"evaluation standard missing term: {term}")

    for term in REQUIRED_FAILURE_CLASSES:
        if term not in catalog:
            failures.append(f"failure catalog missing term: {term}")

    for section in REQUIRED_TEMPLATE_SECTIONS:
        if section not in template:
            failures.append(f"template missing section: {section}")

    for framework_id, requirement in BATCH1_PAGE_REQUIREMENTS.items():
        content = read(requirement["path"])
        for term in requirement["terms"]:
            if term not in content:
                failures.append(f"Batch 1 page {framework_id} missing term: {term}")

    for term in ["First-Pass Rollout Matrix", "Batch 1", "Batch 5"]:
        if term not in rollout_page:
            failures.append(f"rollout page missing term: {term}")

    if rollout.get("artifact_type") != "external_framework_evidence_provenance_rollout":
        failures.append("rollout artifact_type mismatch")
    if rollout.get("schema_version") != "0.1":
        failures.append("rollout schema_version mismatch")

    registry_ids = [entry.get("framework_id") for entry in registry.get("entries", [])]
    rollout_ids = [entry.get("framework_id") for entry in rollout.get("entries", [])]

    if len(rollout_ids) != len(set(rollout_ids)):
        failures.append("rollout contains duplicate framework_id entries")

    missing_from_rollout = sorted(set(registry_ids) - set(rollout_ids))
    extra_in_rollout = sorted(set(rollout_ids) - set(registry_ids))
    for framework_id in missing_from_rollout:
        failures.append(f"registry framework missing from rollout: {framework_id}")
    for framework_id in extra_in_rollout:
        failures.append(f"rollout framework not found in registry: {framework_id}")

    for entry in rollout.get("entries", []):
        framework_id = entry.get("framework_id", "UNKNOWN")
        for field in REQUIRED_ROLLOUT_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"rollout entry {framework_id} missing field: {field}")
        page = entry.get("page")
        if isinstance(page, str) and page.startswith("docs/external-frameworks/"):
            page_path = ROOT / page
            if not page_path.exists():
                failures.append(f"rollout entry {framework_id} page does not exist: {page}")

    batch1_status = rollout.get("batch_status", {}).get("batch_1")
    if batch1_status != "PAGE_PROVENANCE_SECTIONS_INSTALLED":
        failures.append("rollout batch_1 status must be PAGE_PROVENANCE_SECTIONS_INSTALLED")

    boundary = rollout.get("global_boundary", {})
    for key in [
        "rollout_is_certification",
        "rollout_is_endorsement",
        "rollout_is_execution_authority",
        "compatibility_is_certification",
        "observed_behavior_generalized_beyond_captured_evidence",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"rollout boundary must be false: {key}")

    banned_morrison_fragments = [
        "| 1 | ALLOW | BLOCK | False allow",
        "| Test | Observed Result | StegVerse Expected Result | Validation Meaning |",
    ]
    morrison = read(DOCS / "morrison-runtime.md")
    for fragment in banned_morrison_fragments:
        if fragment in morrison:
            failures.append("Morrison page still contains unsupported historical public result table")

    print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
