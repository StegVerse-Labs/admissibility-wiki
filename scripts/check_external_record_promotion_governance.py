#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMOTION = ROOT / "static" / "translation-records" / "external-record-promotion-governance.v0.1.json"
BIB = ROOT / "static" / "translation-records" / "external-bibliographic-intake.v0.1.json"
EXTERNAL = ROOT / "static" / "translation-records" / "external-physics-translation-records.v0.1.json"

ALLOWED_RESULTS = {"MAP", "ACCEPT", "DEFER", "DISPUTE", "ESCALATE", "REFUSE", "SUPERSEDE"}
REQUIRED_DECISION_FIELDS = {
    "decision_id", "target_type", "target_ids", "reviewer_authority_class",
    "policy_reference", "evidence_references", "evidence_posture", "result",
    "result_reason", "resulting_review_posture", "required_next_event",
    "ownership", "non_claims"
}


def fail(message: str) -> None:
    raise SystemExit(f"EXTERNAL RECORD PROMOTION GOVERNANCE: FAIL - {message}")


def main() -> None:
    for path in (PROMOTION, BIB, EXTERNAL):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    bib = json.loads(BIB.read_text(encoding="utf-8"))
    ext = json.loads(EXTERNAL.read_text(encoding="utf-8"))
    known_targets = {r["bibliographic_id"] for r in bib.get("records", [])}
    known_targets |= {r["external_record_id"] for r in ext.get("records", [])}

    data = json.loads(PROMOTION.read_text(encoding="utf-8"))
    if set(data.get("allowed_results", [])) != ALLOWED_RESULTS:
        fail("allowed_results must exactly match the governed result set")
    boundary = str(data.get("authority_boundary", ""))
    if not boundary or ("does not" not in boundary.lower() and "do not" not in boundary.lower()):
        fail("authority_boundary must contain an explicit non-claim")

    decisions = data.get("decision_records")
    if not isinstance(decisions, list) or not decisions:
        fail("decision_records must be a non-empty list")

    seen: set[str] = set()
    for decision in decisions:
        missing = REQUIRED_DECISION_FIELDS - set(decision)
        decision_id = str(decision.get("decision_id", "<missing>"))
        if missing:
            fail(f"decision {decision_id} missing fields: {sorted(missing)}")
        if decision_id in seen:
            fail(f"duplicate decision_id: {decision_id}")
        seen.add(decision_id)
        if decision["result"] not in ALLOWED_RESULTS:
            fail(f"decision {decision_id} has invalid result: {decision['result']}")
        targets = decision["target_ids"]
        if not isinstance(targets, list) or not targets:
            fail(f"decision {decision_id} target_ids must be non-empty")
        for target in targets:
            if target not in known_targets:
                fail(f"decision {decision_id} references unknown target: {target}")
        evidence = decision["evidence_references"]
        if not isinstance(evidence, list) or not evidence:
            fail(f"decision {decision_id} evidence_references must be non-empty")
        if "not" not in str(decision["non_claims"]).lower():
            fail(f"decision {decision_id} must include an explicit non-claim")

    print(f"EXTERNAL RECORD PROMOTION GOVERNANCE: PASS - {len(decisions)} decisions validated")


if __name__ == "__main__":
    main()
