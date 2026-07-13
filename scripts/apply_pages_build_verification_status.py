#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATUS = ROOT / "static" / "status" / "pages-build-verification.json"
DEFAULT_OUTPUT = ROOT / "reports" / "pages-build-status-application-result.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    p = argparse.ArgumentParser(description="Apply only an evidence-authorized Pages verification status mutation.")
    p.add_argument("--artifact-binding", required=True, type=Path)
    p.add_argument("--promotion-receipt", required=True, type=Path)
    p.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    failures: list[str] = []
    try:
        binding = load(args.artifact_binding)
        promotion = load(args.promotion_receipt)
        status = load(args.status)
    except Exception as exc:
        binding, promotion, status = {}, {}, {}
        failures.append(str(exc))

    source = binding.get("source_candidate", {})
    artifact = binding.get("artifact", {})
    observed = binding.get("observed_workflow", {})
    promo_source = promotion.get("source_candidate", {})
    promo_artifact = promotion.get("pages_artifact_evidence", {})

    checks = {
        "binding_type": binding.get("receipt_type") == "pages_artifact_binding_receipt",
        "binding_state": binding.get("verification_state") == "PAGES_ARTIFACT_PRESERVED",
        "binding_not_applied": binding.get("canonical_status_mutation_applied") is False,
        "candidate_hash": bool(HEX64.fullmatch(str(source.get("sha256", "")))),
        "manifest_hash": bool(HEX64.fullmatch(str(source.get("build_manifest_sha256", "")))),
        "artifact_preserved": artifact.get("preserved") is True,
        "artifact_digest": bool(DIGEST.fullmatch(str(artifact.get("artifact_digest", "")))),
        "promotion_type": promotion.get("receipt_type") == "pages_build_status_promotion_receipt",
        "promotion_decision": promotion.get("decision") == "ALLOW_STATUS_PROMOTION_ONLY",
        "promotion_allows_status_only": promotion.get("canonical_status_mutation_allowed") is True,
        "formalism_pass": promotion.get("formalism_validator_evidence", {}).get("status") == "PASS" and bool(promotion.get("formalism_validator_evidence", {}).get("evidence_ref")),
        "pages_pass": promo_artifact.get("status") == "PASS" and bool(promo_artifact.get("evidence_ref")),
        "candidate_match": promo_source.get("sha256") == source.get("sha256"),
        "run_match": promo_artifact.get("run_id") == observed.get("run_id"),
        "job_match": promo_artifact.get("job_id") == observed.get("job_id"),
        "artifact_id_match": promo_artifact.get("artifact_id") == artifact.get("artifact_id"),
        "artifact_digest_match": promo_artifact.get("artifact_digest") == artifact.get("artifact_digest"),
        "deployment_false": promotion.get("deployment_authorized") is False and binding.get("deployment_authorized") is False,
        "public_verification_false": promotion.get("public_verification_complete") is False and binding.get("public_verification_complete") is False,
        "release_false": binding.get("release_authorized") is False,
        "propagation_false": binding.get("downstream_propagation_authorized") is False,
    }
    for name, ok in checks.items():
        if not ok:
            failures.append(f"predicate failed: {name}")

    previous_state = status.get("verification_state")
    applied = False
    idempotent = False
    updated_sha = None
    if not failures:
        expected_previous = {"PENDING_CANONICAL_RUN", "VALIDATOR_PASS_BUILD_PENDING", "PAGES_BUILD_PASS_ARTIFACT_PENDING", "PAGES_ARTIFACT_PRESERVED"}
        if previous_state not in expected_previous:
            failures.append("canonical status is not promotable")
        elif previous_state == "PAGES_ARTIFACT_PRESERVED":
            idempotent = True
        elif args.apply:
            updated = deepcopy(status)
            updated["target_commit"] = binding.get("target_commit")
            updated["verification_state"] = "PAGES_ARTIFACT_PRESERVED"
            updated["required_checks"] = {
                "formalism_publication_validator": {
                    "status": "PASS",
                    "evidence_ref": promotion["formalism_validator_evidence"]["evidence_ref"],
                },
                "docusaurus_production_build": {
                    "status": "PASS",
                    "evidence_ref": source.get("path"),
                },
                "pages_artifact_upload": {
                    "status": "PASS",
                    "evidence_ref": promo_artifact.get("evidence_ref"),
                },
            }
            updated["observed_workflow"] = {
                "run_id": observed.get("run_id"),
                "job_id": observed.get("job_id"),
                "artifact_id": artifact.get("artifact_id"),
                "artifact_digest": artifact.get("artifact_digest"),
            }
            updated["deployment_authorized"] = False
            updated["public_verification_complete"] = False
            args.status.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
            applied = True
            updated_sha = sha256(args.status)

    state = "BLOCKED"
    if not failures:
        state = "APPLIED_PAGES_ARTIFACT_PRESERVED" if applied else ("ALREADY_PAGES_ARTIFACT_PRESERVED" if idempotent else "VALIDATED_DRY_RUN")

    result = {
        "artifact_type": "pages_build_verification_status_application_result",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "application_state": state,
        "source_artifact_binding": {"path": str(args.artifact_binding), "sha256": sha256(args.artifact_binding) if args.artifact_binding.exists() else None},
        "source_promotion_receipt": {"path": str(args.promotion_receipt), "sha256": sha256(args.promotion_receipt) if args.promotion_receipt.exists() else None},
        "canonical_status": {"path": str(args.status), "previous_state": previous_state, "updated_sha256": updated_sha},
        "apply_requested": args.apply,
        "canonical_status_mutation_applied": applied,
        "deployment_authorized": False,
        "public_verification_complete": False,
        "release_authorized": False,
        "downstream_propagation_authorized": False,
        "failures": failures,
        "required_next_transition": "separate_deployment_observation_and_public_verification" if state in {"APPLIED_PAGES_ARTIFACT_PRESERVED", "ALREADY_PAGES_ARTIFACT_PRESERVED"} else "obtain_valid_artifact_binding_and_status_promotion_receipts",
        "authority_boundary": {
            "status_application_is_deployment_authority": False,
            "status_application_is_public_verification": False,
            "status_application_is_release_authority": False,
            "status_application_may_mutate_other_files": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PAGES STATUS APPLICATION: {state} -> {args.output}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
