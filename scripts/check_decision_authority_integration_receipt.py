#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "external-frameworks" / "decision-authority-integration-receipt.json"
PAGE = ROOT / "docs" / "external-frameworks" / "decision-authority.md"
MANIFEST = ROOT / "docs" / "external-frameworks" / "decision-authority.json"
REPORT = ROOT / "docs" / "external-frameworks" / "reports" / "decision-authority.compatibility.json"
INDEX = ROOT / "docs" / "external-frameworks" / "index.md"

REQUIRED_SURFACES = {
    "docs/external-frameworks/decision-authority.md",
    "docs/external-frameworks/decision-authority.json",
    "docs/external-frameworks/reports/decision-authority.compatibility.json",
    "docs/external-frameworks/index.json",
    "docs/external-frameworks/index.md",
    "docs/external-frameworks/evidence-provenance-rollout.json",
    "docs/external-frameworks/evaluation-results.md",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [RECEIPT, PAGE, MANIFEST, REPORT, INDEX]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("DECISION AUTHORITY INTEGRATION RECEIPT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    receipt = load_json(RECEIPT)
    index = INDEX.read_text(encoding="utf-8")

    if receipt.get("artifact_type") != "external_framework_merge_integration_receipt":
        failures.append("receipt artifact type mismatch")
    if receipt.get("schema_version") != "0.1":
        failures.append("receipt schema version mismatch")
    if receipt.get("framework_id") != "decision-authority":
        failures.append("framework id mismatch")

    pr = receipt.get("pull_request", {})
    if pr.get("number") != 10:
        failures.append("pull request number mismatch")
    if pr.get("merged") is not True or pr.get("state") != "merged":
        failures.append("pull request must be recorded as merged")
    for key in ["head_sha", "merge_commit_sha", "merged_at"]:
        if not pr.get(key):
            failures.append(f"pull request missing {key}")

    validation = receipt.get("validation", {})
    if validation.get("pre_merge_conclusion") != "success":
        failures.append("pre-merge validation must be successful")
    for key in [
        "complete_validation_report_uploaded",
        "goal5_validation_report_uploaded",
        "enforcement_step_passed",
    ]:
        if validation.get(key) is not True:
            failures.append(f"validation evidence must be true: {key}")
    for key in ["main_branch_build_verified", "public_deployment_verified"]:
        if validation.get(key) is not False:
            failures.append(f"pending deployment evidence must remain false: {key}")

    installed = set(receipt.get("installed_surfaces", []))
    for surface in sorted(REQUIRED_SURFACES):
        if surface not in installed:
            failures.append(f"missing installed surface: {surface}")

    authority = receipt.get("authority_boundary", {})
    for key, value in authority.items():
        if value is not False:
            failures.append(f"authority boundary must be false: {key}")

    if receipt.get("status") != "MERGED_PREMERGE_VALIDATED_MAIN_DEPLOYMENT_PENDING":
        failures.append("receipt status mismatch")
    if "Decision Authority" not in index:
        failures.append("external frameworks index missing Decision Authority")

    print("DECISION AUTHORITY INTEGRATION RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
