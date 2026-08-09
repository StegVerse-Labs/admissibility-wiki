#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "external-frameworks" / "source-receipts" / "nist-ai-rmf-1.0.source.json"
EXPECTED_SHA256 = "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1"
EXPECTED_SIZE = 1946127


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"NIST AI RMF SOURCE RECEIPT: FAIL - {message}")


def main() -> int:
    require(RECEIPT.exists(), "durable source receipt missing")
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))

    require(data.get("artifact_type") == "external_framework_official_source_receipt", "artifact_type mismatch")
    require(data.get("schema_version") == "0.1", "schema_version mismatch")
    require(data.get("framework_id") == "nist-ai-rmf", "framework_id mismatch")
    require(data.get("framework_version") == "NIST AI RMF 1.0", "framework_version mismatch")
    require(data.get("publication_identifier") == "NIST AI 100-1", "publication_identifier mismatch")
    require(data.get("publication_date") == "2023-01-26", "publication_date mismatch")
    require(data.get("capture_workflow_run") == 31290014846, "capture workflow run mismatch")
    require(data.get("capture_artifact_id") == 9031064931, "capture artifact id mismatch")
    require(data.get("overall_status") == "OFFICIAL_SOURCE_FETCHED_HASHED", "overall_status mismatch")

    content = data.get("content", {})
    require(content.get("sha256") == EXPECTED_SHA256, "official source SHA-256 mismatch")
    require(content.get("size_bytes") == EXPECTED_SIZE, "official source size mismatch")
    require(content.get("content_type") == "application/pdf", "content_type mismatch")
    require(content.get("pdf_magic_validated") is True, "PDF magic was not validated")

    retention = data.get("retention_boundary", {})
    require(retention.get("source_document_redistributed") is False, "source redistribution boundary violated")
    require(retention.get("receipt_retains_hash_and_metadata_only") is True, "receipt retention boundary mismatch")
    require(retention.get("source_remains_at_official_nist_url") is True, "official-source custody boundary mismatch")

    authority = data.get("authority_boundary", {})
    for key in (
        "source_hash_is_nist_endorsement",
        "source_hash_is_certification",
        "source_hash_grants_standing",
        "source_hash_grants_execution_authority",
    ):
        require(authority.get(key) is False, f"authority boundary must remain false: {key}")

    print(
        "NIST AI RMF SOURCE RECEIPT: PASS - "
        f"sha256={EXPECTED_SHA256} size={EXPECTED_SIZE} source_redistributed=false authority_effect=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
