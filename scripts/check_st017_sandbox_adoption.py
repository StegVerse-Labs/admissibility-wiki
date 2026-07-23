#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates/sandbox-first/admissibility-wiki.sandbox-profile.json"
RUNNER = ROOT / "scripts/run_sandbox_validation.py"
FULL_CHAIN = ROOT / "scripts/check_full_validation_chain.py"
WORKFLOW = ROOT / ".github/workflows/validate-chain-continuation.yml"
IOS_WORKFLOW = ROOT / "iosnoperiod/github/workflows/validate-chain-continuation.yml"
IOS_PATCH = ROOT / "iosnoperiod/github/workflows/validate-chain-continuation.patch.md"
ADOPTION = ROOT / "docs/external-frameworks/ST017_SANDBOX_ADOPTION.md"
HANDOFF = ROOT / "docs/external-frameworks/EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md"
REPORT = ROOT / "reports/sandbox-first-validation.report.json"

REQUIRED_COMMAND_IDS = [
    "compile-python",
    "generate-external-framework-reports",
    "generate-external-framework-results",
    "generate-page-metadata",
    "generate-page-mapping",
    "generate-page-status",
    "generate-automation-readiness",
    "validate-goal5-aggregate",
    "install-node-dependencies",
    "build-docusaurus-site",
    "validate-st017-adoption",
]


def mirror_delta_is_controlled() -> bool:
    if not (WORKFLOW.exists() and IOS_WORKFLOW.exists()):
        return False
    if WORKFLOW.read_text(encoding="utf-8") == IOS_WORKFLOW.read_text(encoding="utf-8"):
        return True
    return IOS_PATCH.exists() and "not activation evidence" in IOS_PATCH.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--structural-only", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    for path in [PROFILE, RUNNER, FULL_CHAIN, WORKFLOW, IOS_WORKFLOW, ADOPTION, HANDOFF]:
        if not path.exists():
            errors.append(f"missing:{path.relative_to(ROOT)}")

    if PROFILE.exists():
        data = json.loads(PROFILE.read_text(encoding="utf-8"))
        if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
            errors.append("profile_repository_mismatch")
        command_ids = [item.get("id") for item in data.get("commands", [])]
        for command_id in REQUIRED_COMMAND_IDS:
            if command_id not in command_ids:
                errors.append(f"profile_missing:{command_id}")
        if "validate-governance-artifacts" in command_ids:
            errors.append("profile_contains_duplicate_repository_drift_gate")

    if WORKFLOW.exists() and IOS_WORKFLOW.exists():
        if not mirror_delta_is_controlled():
            errors.append("ios_workflow_mirror_mismatch_without_controlled_patch")
        workflow_text = WORKFLOW.read_text(encoding="utf-8")
        for marker in [
            "python scripts/check_full_validation_chain.py",
            "full-validation-chain-report",
            "reports/full_validation_chain_report.json",
        ]:
            if marker not in workflow_text:
                errors.append(f"workflow_missing:{marker}")

    if FULL_CHAIN.exists():
        text = FULL_CHAIN.read_text(encoding="utf-8")
        for marker in [
            "scripts/run_sandbox_validation.py",
            "sandbox-first-validation.report.json",
            '"st017_sandbox"',
            "sandbox_status",
        ]:
            if marker not in text:
                errors.append(f"full_chain_missing:{marker}")

    if ADOPTION.exists():
        text = ADOPTION.read_text(encoding="utf-8")
        for marker in [
            "SANDBOX: NOT_RUN",
            "GITHUB_ACTIONS: NOT_OBSERVED",
            "PUBLIC_OUTPUT: NOT_VERIFIED",
            "No release tag is authorized.",
        ]:
            if marker not in text:
                errors.append(f"adoption_missing:{marker}")

    if not args.structural_only:
        if not REPORT.exists():
            errors.append("sandbox_report_missing")
        else:
            report = json.loads(REPORT.read_text(encoding="utf-8"))
            if report.get("sandbox_status") != "PASS":
                errors.append("sandbox_status_not_pass")
            if report.get("github_actions_status") != "NOT_OBSERVED":
                errors.append("sandbox_report_infers_github_actions")
            authority = report.get("authority", {})
            if any(authority.values()):
                errors.append("sandbox_report_grants_authority")

    if errors:
        print("ADMISSIBILITY-WIKI ST-017 ADOPTION: FAIL")
        for error in errors:
            print(error)
        return 1
    print("ADMISSIBILITY-WIKI ST-017 ADOPTION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
