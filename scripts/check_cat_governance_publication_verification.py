#!/usr/bin/env python3
"""Validate the CAT Governance Stack publication evidence receipt."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static" / "status" / "cat-governance-publication-verification.v1.json"
DOC = ROOT / "docs" / "index.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"

EXPECTED_JOBS = {
    "build-pages": 91766690214,
    "deploy-pages": 91768371492,
    "verify-public-pages": 91769034746,
}
EXPECTED_ARTIFACTS = {
    "github-pages": (
        8865658459,
        "sha256:c37b91542eff9b8a0169811096950fe8d5c5cbce187b1be93a851330a9e71fdc",
    ),
    "pages-build-receipt": (
        8865657321,
        "sha256:4e76058b636b33a9974dfd0a13420c9846750b95bf4eb881c3cea468c39f49c3",
    ),
    "full-validation-chain-report": (
        8865473106,
        "sha256:94bf38a739fac7fe3602531cf3f1bb2a430874303b600538b4e45b119118a74a",
    ),
}
MARKERS = ("CAT Governance Stack", "ECAT and ICAT should not be reduced")


def fail(message: str) -> None:
    raise SystemExit(f"CAT GOVERNANCE PUBLICATION VERIFICATION: FAIL - {message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing receipt: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail("receipt root must be an object")
    return value


def main() -> int:
    receipt = load_json(RECEIPT)
    if receipt.get("schema") != "stegverse.cat-governance-publication-verification.v1":
        fail("schema mismatch")
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if receipt.get("source_page") != "docs/index.md":
        fail("source-page mismatch")
    if receipt.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        fail("workflow mismatch")
    if receipt.get("result") != "VERIFIED_DEPLOYED_ARTIFACT_AND_PUBLIC_ROUTE_JOB":
        fail("result is not verified")

    run = receipt.get("workflow_run")
    if not isinstance(run, dict):
        fail("workflow_run missing")
    if run.get("run_id") != 30837466398:
        fail("run ID mismatch")
    if run.get("head_sha") != "fd3523766e66d37c3e1b0e64905117103197e968":
        fail("head SHA mismatch")
    if run.get("overall_conclusion") != "failure_fail_closed_validation":
        fail("overall conclusion must preserve fail-closed repository validation")

    jobs = run.get("publication_jobs")
    if not isinstance(jobs, dict):
        fail("publication_jobs missing")
    for name, job_id in EXPECTED_JOBS.items():
        job = jobs.get(name)
        if not isinstance(job, dict):
            fail(f"missing job evidence: {name}")
        if job.get("job_id") != job_id or job.get("conclusion") != "success":
            fail(f"job evidence mismatch: {name}")

    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, dict):
        fail("artifacts missing")
    for name, (artifact_id, digest) in EXPECTED_ARTIFACTS.items():
        artifact = artifacts.get(name)
        if not isinstance(artifact, dict):
            fail(f"missing artifact evidence: {name}")
        if artifact.get("artifact_id") != artifact_id:
            fail(f"artifact ID mismatch: {name}")
        if artifact.get("digest") != digest:
            fail(f"artifact digest mismatch: {name}")

    inspection = receipt.get("inspection")
    if not isinstance(inspection, dict):
        fail("inspection missing")
    if inspection.get("root_index_present") is not True:
        fail("root index was not observed")
    if inspection.get("deployed_artifact_marker_result") != "PASS":
        fail("deployed artifact marker result is not PASS")
    if inspection.get("public_route_job_result") != "PASS":
        fail("public route job result is not PASS")
    if inspection.get("recurring_marker_verification_installed") is not True:
        fail("recurring marker verification is not installed")
    marker_results = inspection.get("required_markers")
    if not isinstance(marker_results, dict):
        fail("required marker results missing")
    for marker in MARKERS:
        if marker_results.get(marker) is not True:
            fail(f"marker not verified: {marker}")

    if not DOC.is_file() or not WORKFLOW.is_file():
        fail("source document or workflow missing")
    doc_text = DOC.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    for marker in MARKERS:
        if marker not in doc_text:
            fail(f"source document marker missing: {marker}")
        if marker not in workflow_text:
            fail(f"workflow verification marker missing: {marker}")
    if "Verify CAT governance stack publication" not in workflow_text:
        fail("named recurring verification step missing")

    non_claims = receipt.get("non_claims")
    if not isinstance(non_claims, dict) or not non_claims:
        fail("non_claims missing")
    if any(value is not False for value in non_claims.values()):
        fail("publication evidence must not grant authority or claim full validation")

    print(
        "CAT GOVERNANCE PUBLICATION VERIFICATION: PASS - "
        "build, deploy, public-route job, and deployed artifact markers are bound"
    )
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
