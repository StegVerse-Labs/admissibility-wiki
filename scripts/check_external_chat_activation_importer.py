#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORTER = ROOT / "scripts/import_external_chat_activation_evidence.py"

REQUIRED = [
    "STEGVERSE_EXTERNAL_CHAT_ACTIVATION_EVIDENCE_SOURCE",
    "external_chat_activation_evidence",
    "StegVerse-Labs/Site",
    "evidence_sha256",
    "canonical_hash",
    "OBSERVED_NON_MUTATING_PUBLIC_PATHS",
    "mutation_required_disabled",
    "static/status/external-chat-activation-evidence.json",
    "external_chat_activation_evidence_import_provenance",
    "import_is_deployment_authority",
    "import_is_repository_mutation_authority",
    "import_is_publication_authority",
    "import_is_certification",
    "import_creates_standing",
]


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION IMPORTER: FAIL - {message}")
    return 1


def main() -> int:
    if not IMPORTER.exists():
        return fail("importer missing")
    text = IMPORTER.read_text(encoding="utf-8")
    for marker in REQUIRED:
        if marker not in text:
            return fail(f"missing marker: {marker}")
    if 'return 0\n\n    try:' not in text:
        return fail("no-source skip boundary missing")
    if 'tmp.replace(OUTPUT)' not in text:
        return fail("atomic projection replacement missing")
    if 'claimed != calculated' not in text:
        return fail("content hash comparison missing")
    if 'mutation_required_disabled") is True' not in text:
        return fail("observed result mutation-disabled predicate missing")
    print("EXTERNAL CHAT ACTIVATION IMPORTER: PASS (source identity, hash, predicates, atomic projection, non-authority boundary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
