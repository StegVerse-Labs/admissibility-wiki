#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.md"
DATA = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.json"
INDEX = ROOT / "docs" / "external-frameworks" / "index.md"

REQUIRED_CLASSES = {
    "runtime_governance",
    "policy_as_code",
    "provenance_and_trace",
    "identity_and_authority",
    "risk_and_assurance",
    "threat_and_security",
    "privacy_and_data_governance",
    "model_eval_and_monitoring",
    "regulatory_and_standards",
    "agent_protocols",
}

REQUIRED_CANDIDATES = {
    "opa",
    "cedar-policy",
    "spiffe-spire",
    "in-toto",
    "slsa",
    "sigstore",
    "openlineage",
    "nist-csf",
    "nist-sp-800-53",
    "oscal",
    "gdpr",
    "model-cards",
    "datasheets-for-datasets",
    "guardrails-ai",
    "llama-guard",
    "neMo-guardrails",
    "mcp",
    "openapi",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [DOC, DATA, INDEX]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")
    if failures:
        print("EXPANDED EXTERNAL FRAMEWORK INTAKE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    data = load_json(DATA)
    index = INDEX.read_text(encoding="utf-8")

    if data.get("artifact_type") != "expanded_external_framework_intake_registry":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")

    posture = data.get("posture", {})
    for key in [
        "candidate_is_certification",
        "candidate_is_endorsement",
        "candidate_is_execution_authority",
        "candidate_is_stegverse_standing",
        "unsourced_candidate_is_evidence",
    ]:
        if posture.get(key) is not False:
            failures.append(f"posture boundary must be false: {key}")

    classes = set(data.get("intake_classes", []))
    for cls in sorted(REQUIRED_CLASSES):
        if cls not in classes:
            failures.append(f"missing intake class: {cls}")

    candidates = data.get("candidates", [])
    if len(candidates) < 40:
        failures.append("expected at least 40 expanded framework candidates")
    candidate_ids = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            failures.append("candidate must be object")
            continue
        candidate_id = candidate.get("candidate_id")
        if candidate_id in candidate_ids:
            failures.append(f"duplicate candidate id: {candidate_id}")
        candidate_ids.add(candidate_id)
        for key in ["candidate_id", "name", "intake_class", "status", "reason"]:
            if not candidate.get(key):
                failures.append(f"candidate missing {key}: {candidate_id}")
        if candidate.get("intake_class") not in classes:
            failures.append(f"candidate intake class invalid: {candidate_id}")
        if candidate.get("status") != "source_required":
            failures.append(f"new intake candidates should remain source_required: {candidate_id}")

    for candidate_id in sorted(REQUIRED_CANDIDATES):
        if candidate_id not in candidate_ids:
            failures.append(f"missing required candidate: {candidate_id}")

    for phrase in [
        "candidate != sourced page",
        "candidate != execution authority",
        "This intake page does not certify external frameworks.",
        "Standing must be reconstructed",
    ]:
        if phrase not in doc:
            failures.append(f"intake doc missing phrase: {phrase}")

    if "Expanded External Framework Intake" not in index:
        failures.append("index missing expanded intake reference")

    print("EXPANDED EXTERNAL FRAMEWORK INTAKE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
