#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_RECEIPT = ROOT / "reports" / "pages-build-receipt.json"
OUTPUT = ROOT / "reports" / "pages-build-verification-candidate.json"


def main() -> int:
    if not BUILD_RECEIPT.exists():
        print(f"PAGES BUILD VERIFICATION CANDIDATE: BLOCKED — missing {BUILD_RECEIPT.relative_to(ROOT)}", file=sys.stderr)
        return 2

    receipt = json.loads(BUILD_RECEIPT.read_text(encoding="utf-8"))
    workflow = receipt.get("workflow_context", {})
    build = receipt.get("build", {})
    success = build.get("state") == "PAGES_BUILD_COMPLETE"

    candidate = {
        "artifact_type": "pages_build_verification_candidate",
        "schema_version": "0.1",
        "repository": workflow.get("repository"),
        "target_commit": workflow.get("sha"),
        "verification_state": "PAGES_BUILD_PASS_ARTIFACT_PENDING" if success else "FAIL_CLOSED",
        "required_checks": {
            "formalism_publication_validator": {
                "status": "PASS" if success else "UNVERIFIED",
                "evidence_ref": "canonical npm validation chain completed before site build" if success else None,
            },
            "docusaurus_production_build": {
                "status": "PASS" if success else "FAIL",
                "evidence_ref": "reports/pages-build-receipt.json" if success else None,
            },
            "pages_artifact_upload": {
                "status": "PENDING" if success else "BLOCKED",
                "evidence_ref": None,
            },
        },
        "observed_workflow": {
            "run_id": workflow.get("run_id"),
            "job": workflow.get("job"),
            "run_attempt": workflow.get("run_attempt"),
        },
        "build_evidence": {
            "manifest_sha256": build.get("manifest_sha256"),
            "file_count": build.get("file_count"),
            "total_size_bytes": build.get("total_size_bytes"),
            "step_outcome": build.get("step_outcome"),
        },
        "candidate_only": True,
        "deployment_authorized": False,
        "public_verification_complete": False,
        "required_next_transition": (
            "observe_pages_artifact_upload_and_bind_artifact_id_and_digest"
            if success
            else "repair_build_failure_and_repeat_canonical_build"
        ),
        "non_claims": [
            "candidate generation does not mutate canonical status",
            "build receipt does not prove Pages artifact upload",
            "Pages build success is not deployment authority",
            "Pages artifact upload is not public verification",
            "candidate validation does not authorize release or downstream propagation",
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print(f"PAGES BUILD VERIFICATION CANDIDATE: {candidate['verification_state']} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
