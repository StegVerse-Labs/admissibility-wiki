#!/usr/bin/env python3
"""Verify governed LLM public pages, contracts, and validation are present."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "docs/governance/governed-llm-reconstructive-search.md",
    "docs/governance/governed-llm-activation-map.md",
    "docs/governance/governed-llm-site-verification.md",
    "docs/governance/governed-llm-deployment-status.md",
    "docs/governance/governed-llm-archive-handoff.md",
    "docs/governance/llm-consciousness-model-system-boundary.md",
    "docs/governance/SYSTEM_BOUNDARY_MIRROR_HANDOFF.md",
    "static/governance/system-boundary-declaration.schema.v0.1.json",
    "static/governance/system-boundary-declaration.example.v0.1.json",
    "static/governance/fixtures/system-boundary-declaration-cases.v0.1.json",
    "scripts/check_system_boundary_declaration.py",
    "docs/governance/governed-relationship-transitions.md",
    "docs/governance/GOVERNED_RELATIONSHIP_TRANSITIONS_MIRROR_HANDOFF.md",
    "static/governance/governed-relationship-transition.schema.v0.1.json",
    "static/governance/governed-relationship-transition.example.v0.1.json",
    "static/governance/fixtures/governed-relationship-publication-observation-cases.v0.1.json",
    "scripts/check_governed_relationship_transitions.py",
    "static/status/governed-relationship-transition-publication-candidate.json",
    "scripts/check_governed_relationship_publication_candidate.py",
    "scripts/observe_governed_relationship_publication.py",
    "static/schemas/governed-relationship-transition-publication-observation.schema.json",
    "scripts/check_governed_relationship_publication_observation_schema.py",
    "scripts/check_governed_relationship_publication_custody_binding.py",
    "static/status/admissible-resolution-ingestion-receipt.json",
    "scripts/check_admissible_resolution_ingestion_receipt.py",
)
REQUIRED_REFERENCES = {
    "sidebars.js": (
        "governance/governed-llm-reconstructive-search",
        "governance/governed-llm-activation-map",
        "governance/governed-llm-site-verification",
        "governance/governed-llm-deployment-status",
        "governance/governed-llm-archive-handoff",
        "governance/governed-relationship-transitions",
    ),
    "docusaurus.config.js": (
        "/governance/governed-llm-activation-map",
        "Governed LLM",
    ),
    "README.md": (
        "docs/governance/governed-llm-reconstructive-search.md",
        "docs/governance/governed-llm-activation-map.md",
        "docs/governance/governed-relationship-transitions.md",
    ),
    "docs/governance/llm-consciousness-model-system-boundary.md": (
        "system-boundary-declaration.schema.v0.1.json",
        "system-boundary-declaration.example.v0.1.json",
        "check_system_boundary_declaration.py",
    ),
    "docs/governance/governed-relationship-transitions.md": (
        "governed-relationship-transition.schema.v0.1.json",
        "governed-relationship-transition.example.v0.1.json",
        "check_governed_relationship_transitions.py",
    ),
    "docs/governance/GOVERNED_RELATIONSHIP_TRANSITIONS_MIRROR_HANDOFF.md": (
        "observe_governed_relationship_publication.py",
        "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
    ),
}


def run_checker(relative_path: str, failure_label: str) -> int:
    checker = ROOT / relative_path
    result = subprocess.run(
        [sys.executable, str(checker)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        print(f"GOVERNED LLM PAGES: FAIL - {failure_label}")
    return result.returncode


def main() -> int:
    missing: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            missing.append("missing file: {}".format(relative_path))

    for relative_path, needles in REQUIRED_REFERENCES.items():
        path = ROOT / relative_path
        if not path.exists():
            missing.append("missing reference file: {}".format(relative_path))
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                missing.append("missing reference in {}: {}".format(relative_path, needle))

    if missing:
        for item in missing:
            print("GOVERNED LLM PAGES: FAIL - {}".format(item))
        return 1

    checks = (
        ("scripts/check_system_boundary_declaration.py", "system-boundary contract validation failed"),
        ("scripts/check_governed_relationship_transitions.py", "relationship-transition validation failed"),
        (
            "scripts/check_governed_relationship_publication_candidate.py",
            "relationship-transition publication candidate validation failed",
        ),
        (
            "scripts/check_governed_relationship_publication_observation_schema.py",
            "relationship-transition publication observation schema validation failed",
        ),
        (
            "scripts/check_governed_relationship_publication_custody_binding.py",
            "relationship-transition publication custody binding validation failed",
        ),
        (
            "scripts/check_admissible_resolution_ingestion_receipt.py",
            "Admissible Resolution ingestion receipt validation failed",
        ),
    )
    for relative_path, failure_label in checks:
        return_code = run_checker(relative_path, failure_label)
        if return_code != 0:
            return return_code

    print(
        "GOVERNED LLM PAGES: PASS - docs, contracts, fixtures, publication candidates, "
        "observation schemas, observation surfaces, custody bindings, bounded Admissible "
        "Resolution ingestion, and references present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
