#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/external-frameworks/examples/external-chat-cooperative-review-package.example.json"
CORRECTION = ROOT / "docs/external-frameworks/examples/external-chat-correction-receipt.example.json"
DELEGATION = ROOT / "docs/external-frameworks/examples/external-chat-reviewer-delegation.example.json"
PUBLICATION = ROOT / "docs/external-frameworks/examples/external-chat-publication-transition.example.json"
SCHEMAS = [
    ROOT / "docs/external-frameworks/schemas/external-chat-cooperative-review-package.schema.json",
    ROOT / "docs/external-frameworks/schemas/external-chat-correction-receipt.schema.json",
    ROOT / "docs/external-frameworks/schemas/external-chat-reviewer-delegation.schema.json",
    ROOT / "docs/external-frameworks/schemas/external-chat-publication-transition.schema.json",
]
RECEIPT_RE = re.compile(r"^external-compatibility-receipt:sha256:[a-f0-9]{64}$")
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
SCOPE_RE = re.compile(r"^(field:[A-Za-z0-9_.:-]+|package:read|publication_review|\*)$")


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT REVIEW PACKETS: FAIL - {message}")
    return 1


def main() -> int:
    for path in [REVIEW, CORRECTION, DELEGATION, PUBLICATION, *SCHEMAS]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
        json.loads(path.read_text(encoding="utf-8"))

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    delegation = json.loads(DELEGATION.read_text(encoding="utf-8"))
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))

    if review.get("packet_type") != "external_framework_cooperative_review_package":
        return fail("review packet type mismatch")
    if review.get("submitter_opt_in") is not True or review.get("raw_submission_included") is not False:
        return fail("review packet opt-in/raw-submission boundary invalid")
    if not RECEIPT_RE.match(review.get("compatibility_receipt_id", "")):
        return fail("review packet receipt ID invalid")
    if not HASH_RE.match(review.get("submission_sha256", "")):
        return fail("review packet submission hash invalid")
    if any(value is not False for value in review.get("boundary", {}).values()):
        return fail("review packet boundary must remain false")

    if correction.get("receipt_type") != "external_framework_correction_receipt":
        return fail("correction receipt type mismatch")
    if correction.get("review_decision") not in {"UPHOLD", "CORRECT", "PARTIAL_CORRECTION", "INSUFFICIENT_EVIDENCE"}:
        return fail("correction review decision invalid")
    if not RECEIPT_RE.match(correction.get("challenged_receipt_id", "")):
        return fail("challenged receipt ID invalid")
    if not HASH_RE.match(correction.get("challenged_submission_sha256", "")):
        return fail("challenged submission hash invalid")
    decision = correction["review_decision"]
    replacement_result = correction.get("replacement_result")
    replacement_receipt = correction.get("replacement_receipt_id")
    if decision in {"CORRECT", "PARTIAL_CORRECTION"} and (not replacement_result or not replacement_receipt):
        return fail("correction decisions require replacement result and receipt")
    if decision in {"UPHOLD", "INSUFFICIENT_EVIDENCE"} and (replacement_result is not None or replacement_receipt is not None):
        return fail("non-correction decisions must not invent replacement result or receipt")
    if any(value is not False for value in correction.get("boundary", {}).values()):
        return fail("correction receipt boundary must remain false")

    if delegation.get("record_type") != "external_chat_reviewer_delegation":
        return fail("reviewer delegation record_type mismatch")
    if not HASH_RE.match(delegation.get("token_sha256", "")):
        return fail("reviewer token hash invalid")
    if not delegation.get("delegation_ref") or not delegation.get("reviewer_ref"):
        return fail("reviewer/delegation reference missing")
    scopes = delegation.get("scopes")
    if not isinstance(scopes, list) or not scopes or len(scopes) != len(set(scopes)):
        return fail("reviewer scopes must be unique and non-empty")
    if any(not SCOPE_RE.match(scope) for scope in scopes):
        return fail("reviewer scope invalid")
    valid_from = datetime.fromisoformat(delegation["valid_from"].replace("Z", "+00:00"))
    valid_until = datetime.fromisoformat(delegation["valid_until"].replace("Z", "+00:00"))
    if valid_until <= valid_from:
        return fail("reviewer delegation validity window invalid")
    if any(value is not False for value in delegation.get("authority_boundary", {}).values()):
        return fail("reviewer delegation authority boundary must remain false")

    if publication.get("transition_type") != "external_framework_wiki_publication_transition":
        return fail("publication transition type mismatch")
    if publication.get("publication_executed") is not False:
        return fail("publication transition must not execute publication")
    if not publication.get("correction_receipt_id") or not publication.get("publisher_ref"):
        return fail("publication transition identity references missing")
    if not publication.get("target_path", "").startswith("docs/external-frameworks/"):
        return fail("publication target path outside external-framework scope")
    required_boundary = {
        "transition_is_not_repository_write": True,
        "transition_is_not_certification": True,
        "transition_creates_no_standing": True,
        "separate_repository_mutation_required": True,
    }
    if publication.get("boundary") != required_boundary:
        return fail("publication transition boundary mismatch")

    print("EXTERNAL CHAT REVIEW PACKETS: PASS (package, correction, reviewer delegation, publication transition)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
