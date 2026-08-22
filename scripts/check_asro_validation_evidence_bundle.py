#!/usr/bin/env python3
"""Emit a fail-closed machine-readable ASRO validation evidence bundle.

This runner intentionally covers the immutable-input and comparison-governance
layers without claiming hosted workflow, release, runtime, reciprocal execution,
or bilateral authority.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "asro-validation-evidence-bundle.json"
STATIC_RECEIPT = ROOT / "receipts" / "asro-static-input-integrity-observation-2026-08-22.json"
CHECKS = (
    ("immutable_input_bundle", ROOT / "scripts" / "check_asro_exact_head_input_bundle.py"),
    ("comparison_governance", ROOT / "scripts" / "check_asro_comparison_governance.py"),
    ("provenance_correction", ROOT / "scripts" / "check_asro_provenance_correction.py"),
)


def execute(label: str, path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "label": label,
            "path": str(path.relative_to(ROOT)),
            "status": "FAIL",
            "return_code": 127,
            "output": "missing validator",
        }
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "label": label,
        "path": str(path.relative_to(ROOT)),
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout.rstrip(),
    }


def main() -> int:
    results = [execute(label, path) for label, path in CHECKS]
    errors: list[str] = []

    static_integrity = None
    if not STATIC_RECEIPT.exists():
        errors.append("missing_static_integrity_receipt")
    else:
        try:
            static_integrity = json.loads(STATIC_RECEIPT.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid_static_integrity_receipt:{exc}")
        else:
            if static_integrity.get("static_integrity_result") != "PASS_STATIC_BLOB_CONSISTENCY":
                errors.append("static_integrity_not_pass")
            observed = static_integrity.get("observed_inputs") or {}
            if len(observed) != 8 or not all((item or {}).get("match") is True for item in observed.values()):
                errors.append("static_integrity_not_8_of_8")
            if static_integrity.get("canonical_workflow_result") != "UNOBSERVED":
                errors.append("static_receipt_must_not_claim_hosted_result")

    failed = [item for item in results if item["status"] != "PASS"]
    overall = "PASS_LOCAL_EVIDENCE_BUNDLE" if not failed and not errors else "FAIL_CLOSED"
    report = {
        "schema_version": "1.0.0",
        "artifact_type": "asro_validation_evidence_bundle",
        "goal_id": "ADMISSIBILITY-ASRO-REVIEW-DISPOSITION-001",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "executed_head": os.environ.get("GITHUB_SHA") or "LOCAL_OR_UNBOUND_EXECUTION",
        "checks": results,
        "static_integrity_receipt": str(STATIC_RECEIPT.relative_to(ROOT)),
        "static_integrity_result": None if static_integrity is None else static_integrity.get("static_integrity_result"),
        "static_integrity_input_count": 0 if static_integrity is None else len(static_integrity.get("observed_inputs") or {}),
        "errors": errors,
        "overall_status": overall,
        "hosted_canonical_workflow_result": "UNOBSERVED_BY_THIS_ARTIFACT",
        "authority": {
            "release": False,
            "deployment": False,
            "runtime": False,
            "activation": False,
            "reciprocal_execution": False,
            "bilateral_authorization": False,
        },
        "boundary": "A local evidence-bundle PASS proves only the checked repository invariants and pinned-byte consistency. It does not prove hosted canonical execution, repository-wide PASS, release, deployment, runtime, activation, reciprocal execution, reviewer standing, or bilateral authorization.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    for item in results:
        print(f"{item['label']}: {item['status']}")
        if item["output"]:
            print(item["output"])
    if errors:
        for error in errors:
            print(f"ERROR: {error}")

    if overall != "PASS_LOCAL_EVIDENCE_BUNDLE":
        print("ASRO VALIDATION EVIDENCE BUNDLE: FAIL_CLOSED")
        return 1
    print("ASRO VALIDATION EVIDENCE BUNDLE: PASS_LOCAL_EVIDENCE_BUNDLE")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
