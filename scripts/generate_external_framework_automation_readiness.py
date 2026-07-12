#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def main() -> int:
    payload = json.loads(GATES.read_text(encoding="utf-8"))
    frameworks: list[dict[str, Any]] = []
    ready_count = 0

    for record in payload.get("frameworks", []):
        selection = record.get("selection") if isinstance(record.get("selection"), dict) else {}
        required_fields = list(record.get("required_fields", []))
        framework_specific = list(record.get("framework_specific_requirements", []))
        missing_required = [field for field in required_fields if not nonempty(selection.get(field))]

        supplied_specific = selection.get("framework_specific_context")
        specific_complete = (
            isinstance(supplied_specific, dict)
            and all(nonempty(supplied_specific.get(field)) for field in framework_specific)
        )
        hashes_present = any(
            "hash" in field.lower() and nonempty(selection.get(field)) for field in required_fields
        )
        version_present = any(
            ("version" in field.lower() or "commit" in field.lower()) and nonempty(selection.get(field))
            for field in required_fields
        )
        command_present = any(
            "command" in field.lower() and nonempty(selection.get(field)) for field in required_fields
        )

        selection_complete = (
            not missing_required
            and specific_complete
            and hashes_present
            and version_present
            and command_present
            and record.get("selection_state") == "implementation_selected_hash_bound"
        )
        execution_job_allowed = bool(
            selection_complete
            and record.get("execution_authorized") is True
            and payload.get("gate", {}).get("execution_jobs_may_be_added") is True
        )
        if execution_job_allowed:
            ready_count += 1

        frameworks.append(
            {
                "framework_id": record.get("framework_id"),
                "selection_state": record.get("selection_state"),
                "missing_required_fields": missing_required,
                "framework_specific_context_complete": specific_complete,
                "hash_evidence_present": hashes_present,
                "version_evidence_present": version_present,
                "command_evidence_present": command_present,
                "selection_complete": selection_complete,
                "execution_authorized_in_registry": record.get("execution_authorized") is True,
                "execution_job_allowed": execution_job_allowed,
                "automation_state": "ready_for_execution_job_review" if execution_job_allowed else "blocked_selection_required",
            }
        )

    result = {
        "artifact_type": "external_framework_automation_readiness_matrix",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_registry": {
            "path": str(GATES.relative_to(ROOT)),
            "sha256": sha256(GATES),
        },
        "github_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "sha": os.environ.get("GITHUB_SHA"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
        },
        "summary": {
            "framework_count": len(frameworks),
            "ready_for_execution_job_review": ready_count,
            "blocked_selection_required": len(frameworks) - ready_count,
            "execution_jobs_may_be_added": ready_count > 0,
        },
        "frameworks": frameworks,
        "authority_boundary": {
            "automation_readiness_is_execution_authority": False,
            "selection_completion_is_certification": False,
            "selection_completion_is_compatibility": False,
            "selection_completion_creates_standing": False,
            "readiness_matrix_may_cause_external_consequence": False,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        "IMPLEMENTATION AUTOMATION READINESS: "
        f"{ready_count}/{len(frameworks)} ready; "
        f"{len(frameworks) - ready_count} blocked -> {OUTPUT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
