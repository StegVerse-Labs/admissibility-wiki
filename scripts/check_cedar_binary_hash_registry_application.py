#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "apply_cedar_binary_hash_registry_promotion.py"
CANONICAL_REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TEST_HASH = "a" * 64


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_engine(receipt: Path, registry: Path, output: Path, apply: bool) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ENGINE), "--receipt", str(receipt), "--registry", str(registry), "--output", str(output)]
    if apply:
        command.append("--apply")
    return subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def main() -> int:
    failures: list[str] = []
    for path in (ENGINE, CANONICAL_REGISTRY):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("CEDAR BINARY HASH REGISTRY APPLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    engine_text = ENGINE.read_text(encoding="utf-8")
    required_markers = [
        "ALLOW_REGISTRY_PROMOTION_ONLY",
        "APPROVED_NOT_APPLIED",
        "APPLIED_HASH_ONLY",
        "ALREADY_APPLIED_HASH_ONLY",
        "frameworks[cedar-policy].selection.compiled_binary_sha256",
        '"runtime_execution_authorized": False',
        '"runtime_execution_requested": False',
        '"external_consequence_allowed": False',
        "hash_application_may_change_any_other_registry_field",
        "hash_application_may_dispatch_or_execute",
    ]
    for marker in required_markers:
        if marker not in engine_text:
            failures.append(f"engine missing marker: {marker}")
    for forbidden in ("cedar authorize", "subprocess.run([binary", '"execution_authorized"] = True'):
        if forbidden in engine_text:
            failures.append(f"engine contains forbidden execution marker: {forbidden}")

    if not failures:
        with tempfile.TemporaryDirectory(prefix="cedar-registry-application-") as directory:
            temp = Path(directory)
            registry_path = temp / "registry.json"
            receipt_path = temp / "promotion-receipt.json"
            dry_output = temp / "dry-run.json"
            apply_output = temp / "apply.json"
            repeat_output = temp / "repeat.json"

            registry = load(CANONICAL_REGISTRY)
            cedar = next(item for item in registry["frameworks"] if item.get("framework_id") == "cedar-policy")
            cedar["selection"]["compiled_binary_sha256"] = None
            cedar["execution_authorized"] = False
            registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

            receipt = {
                "schema_version": "0.1",
                "receipt_type": "cedar_binary_registry_promotion_receipt",
                "framework_id": "cedar-policy",
                "source_promotion_candidate": {
                    "path": "fixture://candidate",
                    "sha256": "b" * 64,
                    "candidate_state": "READY_FOR_REGISTRY_PROMOTION_REVIEW",
                    "binary_sha256": TEST_HASH,
                },
                "decision": "ALLOW_REGISTRY_PROMOTION_ONLY",
                "promotion_state": "APPROVED_NOT_APPLIED",
                "review": {
                    "status": "PASS",
                    "reviewer_identity": "fixture-reviewer",
                    "delegation_ref": "fixture://delegation/hash-only",
                    "reviewed_at_utc": "2026-07-12T00:00:00Z",
                    "evidence_refs": ["fixture://candidate"],
                },
                "registry_target": {
                    "path": str(registry_path),
                    "field": "frameworks[cedar-policy].selection.compiled_binary_sha256",
                    "expected_previous_value": None,
                    "proposed_value": TEST_HASH,
                },
                "registry_mutation_applied": False,
                "runtime_execution_authorized": False,
                "external_consequence_allowed": False,
                "required_next_transition": "apply_hash_only_registry_mutation_in_separate_governed_commit_then_revalidate_selection_registry",
                "non_claims": [
                    "promotion approval does not create execution authority",
                    "binary hash promotion does not establish compatibility",
                    "registry mutation does not authorize runtime execution",
                    "review completion does not establish standing",
                ],
            }
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            before = registry_path.read_bytes()
            dry = run_engine(receipt_path, registry_path, dry_output, False)
            if dry.returncode != 0:
                failures.append(f"dry-run failed: {dry.stdout.strip()}")
            elif registry_path.read_bytes() != before:
                failures.append("dry-run mutated registry")
            else:
                dry_result = load(dry_output)
                if dry_result.get("application_state") != "VALIDATED_DRY_RUN":
                    failures.append("dry-run state mismatch")
                if dry_result.get("registry_mutation_applied") is not False:
                    failures.append("dry-run claimed mutation")

            applied = run_engine(receipt_path, registry_path, apply_output, True)
            if applied.returncode != 0:
                failures.append(f"apply failed: {applied.stdout.strip()}")
            else:
                result = load(apply_output)
                updated = load(registry_path)
                updated_cedar = next(item for item in updated["frameworks"] if item.get("framework_id") == "cedar-policy")
                if result.get("application_state") != "APPLIED_HASH_ONLY":
                    failures.append("apply state mismatch")
                if updated_cedar.get("selection", {}).get("compiled_binary_sha256") != TEST_HASH:
                    failures.append("approved binary hash was not applied")
                if updated_cedar.get("execution_authorized") is not False:
                    failures.append("application changed execution authority")
                if not HEX64.fullmatch(str(result.get("registry", {}).get("updated_sha256", ""))):
                    failures.append("updated registry hash missing")

            repeated = run_engine(receipt_path, registry_path, repeat_output, True)
            if repeated.returncode != 0:
                failures.append(f"idempotent repeat failed: {repeated.stdout.strip()}")
            else:
                result = load(repeat_output)
                if result.get("application_state") != "ALREADY_APPLIED_HASH_ONLY":
                    failures.append("idempotent repeat state mismatch")
                if result.get("registry_mutation_applied") is not False:
                    failures.append("idempotent repeat claimed a second mutation")

    print("CEDAR BINARY HASH REGISTRY APPLICATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
