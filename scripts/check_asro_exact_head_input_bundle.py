#!/usr/bin/env python3
"""Validate the immutable ASRO input bundle captured for exact-head continuation."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "static" / "data" / "framework-evaluations" / "asro" / "exact-head-validation-inputs-2026-08-22.json"
TRIGGER = ROOT / "receipts" / "asro-exact-head-validation-trigger-2026-08-22.json"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    errors: list[str] = []
    if not BUNDLE.exists():
        print("ASRO EXACT-HEAD INPUT BUNDLE: FAIL - missing bundle")
        return 1

    try:
        bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ASRO EXACT-HEAD INPUT BUNDLE: FAIL - invalid JSON: {exc}")
        return 1

    if bundle.get("schema_version") != "1.0.0":
        errors.append("schema_version")
    if bundle.get("artifact_type") != "asro_exact_head_validation_inputs":
        errors.append("artifact_type")
    if bundle.get("goal_id") != "ADMISSIBILITY-ASRO-REVIEW-DISPOSITION-001":
        errors.append("goal_id")
    if bundle.get("source_head") != "99fde15049f4c86d7056d9501d6c52733b5e5d0e":
        errors.append("source_head")

    inputs = bundle.get("inputs") or {}
    required = {
        "owner_declaration",
        "contributor_protocol",
        "companion_declaration",
        "historical_public_source_pin",
        "accountable_party_declaration",
        "contribution_ledger",
        "comparison_governance_validator",
        "validation_trigger_receipt",
    }
    if set(inputs) != required:
        errors.append("input_set")

    for name, record in inputs.items():
        if not isinstance(record, dict):
            errors.append(f"input_record:{name}")
            continue
        rel = record.get("path")
        expected = record.get("git_blob_sha1")
        if not isinstance(rel, str) or not rel:
            errors.append(f"input_path:{name}")
            continue
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{40}", expected) is None:
            errors.append(f"input_blob_format:{name}")
            continue
        target = ROOT / rel
        if not target.exists():
            errors.append(f"missing_input:{name}:{rel}")
            continue
        actual = git_blob_sha1(target)
        if actual != expected:
            errors.append(f"blob_mismatch:{name}:{expected}:{actual}")

    boundaries = bundle.get("preserved_boundaries") or {}
    expected_boundaries = {
        "exact_historical_source_path": "UNRESOLVED",
        "independent_reviewer_issuer": "UNRESOLVED",
        "external_asro_native_execution": "NOT_TESTED",
        "reciprocal_execution": "DEFERRED",
        "bilateral_seam_comparison_record": "NOT_ISSUED_OR_AUTHORIZED",
        "repository_release": "NOT_AUTHORIZED",
        "runtime": "NOT_PROVEN",
        "activation": "NOT_COMPLETE",
    }
    for key, value in expected_boundaries.items():
        if boundaries.get(key) != value:
            errors.append(f"boundary:{key}")

    authority = bundle.get("authority") or {}
    for key in ("release", "deployment", "runtime", "activation", "reciprocal_execution", "bilateral_authorization"):
        if authority.get(key) is not False:
            errors.append(f"authority:{key}")

    if not TRIGGER.exists():
        errors.append("missing_trigger_receipt")
    else:
        try:
            trigger = json.loads(TRIGGER.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"trigger_invalid_json:{exc}")
        else:
            if trigger.get("receipt_type") != "asro_exact_head_validation_trigger":
                errors.append("trigger_type")
            if trigger.get("goal_id") != bundle.get("goal_id"):
                errors.append("trigger_goal_binding")
            if trigger.get("pre_trigger_head") != "dbf654bd69dc2cd4d488cb699dcd72c3d536612e":
                errors.append("trigger_pre_head")
            trigger_authority = trigger.get("authority") or {}
            for key in ("release", "deployment", "runtime", "activation", "reciprocal_execution", "bilateral_authorization"):
                if trigger_authority.get(key) is not False:
                    errors.append(f"trigger_authority:{key}")

    if errors:
        print("ASRO EXACT-HEAD INPUT BUNDLE: FAIL - " + ", ".join(errors))
        return 1

    print("ASRO EXACT-HEAD INPUT BUNDLE: PASS")
    print("Pinned artifact bytes, governance-validator identity, trigger binding, unresolved evidence states, and non-authority boundaries are preserved without moving-main substitution.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
