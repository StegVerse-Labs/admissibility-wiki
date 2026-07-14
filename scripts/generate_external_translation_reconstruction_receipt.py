#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "external-translation" / "reconstruction-receipt.json"

INPUTS = {
    "disciplinary_translation_records": ROOT / "static" / "translation-records" / "disciplinary-translation-records.v0.1.json",
    "mathematics_crosswalk": ROOT / "static" / "translation-records" / "mathematics-crosswalk.v0.1.json",
    "external_physics_records": ROOT / "static" / "translation-records" / "external-physics-translation-records.v0.1.json",
    "bibliographic_intake": ROOT / "static" / "translation-records" / "external-bibliographic-intake.v0.1.json",
    "promotion_governance": ROOT / "static" / "translation-records" / "external-record-promotion-governance.v0.1.json",
    "source_locator_intake": ROOT / "static" / "translation-records" / "source-locator-intake.v0.1.json",
    "specialist_routing": ROOT / "static" / "translation-records" / "specialist-review-routing.v0.1.json",
    "review_receipts": ROOT / "static" / "translation-records" / "specialist-review-output-receipts.v0.1.json",
    "supersession_state": ROOT / "static" / "translation-records" / "external-record-supersession-state.v0.1.json",
}


def canonical_sha256(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load(name: str) -> dict:
    path = INPUTS[name]
    if not path.exists():
        raise SystemExit(f"missing reconstruction input: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    data = {name: load(name) for name in INPUTS}

    locator_records = data["source_locator_intake"].get("records", [])
    routes = data["specialist_routing"].get("routes", [])
    decisions = data["promotion_governance"].get("decision_records", [])
    receipts = data["review_receipts"].get("receipts", [])
    supersession = data["supersession_state"]

    if len(locator_records) != 1 or len(routes) != 1 or len(decisions) < 1:
        raise SystemExit("expected one active locator, one active route, and at least one promotion decision")

    locator = locator_records[0]
    route = routes[0]
    current_decision_id = supersession.get("current_decision_id")
    current_decision = next((d for d in decisions if d.get("decision_id") == current_decision_id), None)
    if current_decision is None:
        raise SystemExit(f"current decision not found: {current_decision_id}")

    required_classes = set(route.get("required_review_classes", []))
    receipt_classes = {receipt.get("review_class") for receipt in receipts}
    cross_record_checks = {
        "source_id_consistent": len({
            locator.get("source_id"),
            route.get("source_id"),
            data["external_physics_records"].get("sources", [{}])[0].get("source_id"),
            supersession.get("source_id"),
        }) == 1,
        "route_id_consistent": route.get("route_id") == supersession.get("route_id") == data["review_receipts"].get("route_id"),
        "required_review_classes_covered": required_classes == receipt_classes,
        "current_decision_resolves": current_decision is not None,
        "locator_result_carried_forward": locator.get("verification_result") == supersession.get("observed_conditions", {}).get("locator_verification"),
        "supersession_fail_closed_when_incomplete": (
            supersession.get("evaluation_result") == "DEFER_NO_SUPERSESSION"
            if locator.get("verification_result") == "UNRESOLVED" or any(r.get("receipt_posture") != "issued" for r in receipts)
            else True
        ),
    }

    overall_status = "PASS" if all(cross_record_checks.values()) else "FAIL"
    receipt = {
        "schema": "admissibility_wiki.external_translation_reconstruction_receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "source_id": supersession.get("source_id"),
        "locator_intake_id": locator.get("locator_intake_id"),
        "locator_verification": locator.get("verification_result"),
        "route_id": route.get("route_id"),
        "required_review_classes": sorted(required_classes),
        "review_receipts": [
            {
                "receipt_id": r.get("receipt_id"),
                "review_class": r.get("review_class"),
                "review_result": r.get("review_result"),
                "receipt_posture": r.get("receipt_posture"),
            }
            for r in sorted(receipts, key=lambda item: str(item.get("review_class")))
        ],
        "current_decision": {
            "decision_id": current_decision.get("decision_id"),
            "result": current_decision.get("result"),
            "resulting_review_posture": current_decision.get("resulting_review_posture"),
        },
        "supersession": {
            "evaluation_result": supersession.get("evaluation_result"),
            "supersedes_decision_id": supersession.get("supersedes_decision_id"),
            "candidate_successor_decision_id": supersession.get("candidate_successor_decision_id"),
        },
        "cross_record_checks": cross_record_checks,
        "input_hashes": {
            name: {
                "path": str(path.relative_to(ROOT)),
                "canonical_json_sha256": canonical_sha256(path),
            }
            for name, path in INPUTS.items()
        },
        "continuation": {
            "owner": supersession.get("ownership"),
            "next_event": supersession.get("next_event"),
            "permitted_scope": "Re-evaluate the deferred external record only after locator and specialist-receipt conditions change; preserve prior decisions through explicit supersession pointers.",
        },
        "authority_boundary": "This receipt proves only that the declared locator, route, review receipts, promotion decision, and supersession state were jointly reconstructed and checked in one repository run. It does not validate physics, create peer review, establish equivalence, promote a record, or grant execution authority.",
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"EXTERNAL TRANSLATION RECONSTRUCTION RECEIPT: {overall_status}")
    print(f"Receipt: {REPORT.relative_to(ROOT)}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
