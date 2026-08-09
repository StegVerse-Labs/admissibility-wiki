#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "external-frameworks" / "nist-ai-rmf" / "nist-ai-rmf-1.0-source-receipt.json"
SOURCE_URL = "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"
PUBLICATION_URL = "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10"
DOI = "https://doi.org/10.6028/NIST.AI.100-1"


def main() -> int:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "StegVerse-admissibility-wiki-source-capture/1.0"},
    )
    captured_at = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type")
            etag = response.headers.get("ETag")
            last_modified = response.headers.get("Last-Modified")
    except Exception as exc:
        print(f"NIST AI RMF SOURCE CAPTURE: FAILED_CLOSED - {type(exc).__name__}: {exc}")
        return 1

    if not body.startswith(b"%PDF-"):
        print("NIST AI RMF SOURCE CAPTURE: FAILED_CLOSED - fetched content is not a PDF")
        return 1

    receipt = {
        "artifact_type": "external_framework_official_source_receipt",
        "schema_version": "0.1",
        "framework_id": "nist-ai-rmf",
        "framework_version": "NIST AI RMF 1.0",
        "publication_identifier": "NIST AI 100-1",
        "publication_date": "2023-01-26",
        "publication_url": PUBLICATION_URL,
        "doi": DOI,
        "source_url": SOURCE_URL,
        "resolved_source_url": final_url,
        "captured_at_utc": captured_at,
        "content": {
            "sha256": hashlib.sha256(body).hexdigest(),
            "size_bytes": len(body),
            "content_type": content_type,
            "pdf_magic_validated": True,
            "etag": etag,
            "last_modified": last_modified,
        },
        "retention_boundary": {
            "source_document_redistributed": False,
            "receipt_retains_hash_and_metadata_only": True,
            "source_remains_at_official_nist_url": True,
        },
        "authority_boundary": {
            "source_hash_is_nist_endorsement": False,
            "source_hash_is_certification": False,
            "source_hash_grants_standing": False,
            "source_hash_grants_execution_authority": False,
        },
        "overall_status": "OFFICIAL_SOURCE_FETCHED_HASHED",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        "NIST AI RMF SOURCE CAPTURE: OFFICIAL_SOURCE_FETCHED_HASHED "
        f"sha256={receipt['content']['sha256']} size={receipt['content']['size_bytes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
