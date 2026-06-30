#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "external-frameworks" / "generated-page-validation-summary.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"

VALIDATORS = [
    "scripts/check_external_framework_page_analysis_boundary.py",
    "scripts/check_external_framework_page_candidates.py",
    "scripts/check_external_framework_page_surfaces.py",
    "scripts/check_generated_page_surfaces_handoff.py",
    "scripts/check_generated_page_surfaces_root_addendum.py",
    "scripts/check_generated_page_workflow_entrypoint_migration.py",
    "scripts/check_generated_page_entrypoint_closeout_propagation.py",
    "scripts/check_generated_page_release_evidence_bundle.py",
    "scripts/check_generated_page_ci_evidence_surface.py",
    "scripts/check_generated_page_ci_evidence_surface_handoff.py",
    "scripts/check_generated_page_closeout_state_generation.py",
]


def main() -> int:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    data = {
        "artifact_type": "generated_page_validation_summary",
        "schema_version": "0.2",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "validated_through": "scripts/check_external_framework_page_status.py",
        "surface_inventory": "docs/external-frameworks/generated-page-surfaces.json",
        "surface_handoff": "docs/external-frameworks/GENERATED_PAGE_SURFACES_HANDOFF.md",
        "root_addendum": "docs/GENERATED_PAGE_SURFACES_ROOT_ADDENDUM.md",
        "validators_called_by_page_status": VALIDATORS,
        "manual_tasks_removed": [
            "generated_surface_discovery",
            "generated_surface_handoff_discovery",
            "generated_surface_root_handoff_discovery",
            "generated_closeout_state_reconstruction"
        ],
        "boundary": {
            "validation_summary_is_authority": False,
            "single_workflow_policy_preserved": True,
            "manual_generated_surface_discovery_required": False
        }
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
