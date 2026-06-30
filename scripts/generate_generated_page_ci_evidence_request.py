#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "external-frameworks" / "generated-page-ci-evidence-request.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"


def main() -> int:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    ci = model["ci"]
    data = {
        "artifact_type": "generated_page_ci_evidence_request",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "requested_evidence": ci["requested_evidence"],
        "current_state": ci["current_state"],
        "release_gate": ci["release_gate"],
        "manual_tasks_removed": ci["manual_tasks_removed"],
        "boundary": {
            "ci_request_is_authority": False,
            "missing_ci_fails_closed": True,
            "single_workflow_policy_preserved": True
        }
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
