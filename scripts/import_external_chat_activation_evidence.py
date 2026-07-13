#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/status/external-chat-activation-evidence.json"
PROVENANCE = ROOT / "static/status/external-chat-activation-evidence.provenance.json"


def canonical_hash(payload: dict[str, Any]) -> str:
    material = dict(payload)
    material.pop("evidence_sha256", None)
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_source(source: str) -> tuple[dict[str, Any], str]:
    if source.startswith(("https://", "http://")):
        request = urllib.request.Request(source, headers={"User-Agent": "StegVerse-External-Chat-Evidence-Importer"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            raise RuntimeError(f"source fetch failed: {exc}") from exc
        origin = source
    else:
        path = Path(source).expanduser().resolve()
        raw = path.read_text(encoding="utf-8")
        origin = str(path)
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("activation evidence source must contain a JSON object")
    return value, origin


def validate(payload: dict[str, Any]) -> None:
    if payload.get("schema_version") != "1.0.0" or payload.get("record_type") != "external_chat_activation_evidence":
        raise ValueError("activation evidence identity mismatch")
    if payload.get("repository") != "StegVerse-Labs/Site":
        raise ValueError("activation evidence source repository mismatch")
    boundary = payload.get("authority_boundary")
    required = {
        "evidence_is_deployment_authority": False,
        "evidence_is_repository_mutation_authority": False,
        "evidence_is_publication_authority": False,
        "evidence_is_certification": False,
        "evidence_creates_standing": False,
        "mutation_remains_separately_authorized": True,
    }
    if boundary != required:
        raise ValueError("activation evidence authority boundary mismatch")
    claimed = payload.get("evidence_sha256")
    calculated = canonical_hash(payload)
    if claimed != calculated:
        raise ValueError(f"activation evidence SHA-256 mismatch: expected {calculated}")
    if payload.get("result") == "OBSERVED_NON_MUTATING_PUBLIC_PATHS":
        local = payload.get("local_validation", {})
        live = payload.get("post_deployment_live_verification", {})
        if not (
            local.get("passed") is True
            and local.get("status") == "PASSED"
            and local.get("authority_effect") == "NONE"
            and live.get("passed") is True
            and live.get("result") == "PASS"
            and live.get("mutation_required_disabled") is True
        ):
            raise ValueError("observed result lacks required non-mutating predicates")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import an exact Site External Chat activation-evidence artifact.")
    parser.add_argument("source", nargs="?", default=os.getenv("STEGVERSE_EXTERNAL_CHAT_ACTIVATION_EVIDENCE_SOURCE"))
    args = parser.parse_args()
    if not args.source:
        print("EXTERNAL CHAT ACTIVATION IMPORT: SKIP - no source configured")
        return 0

    try:
        payload, origin = load_source(args.source)
        validate(payload)
    except Exception as exc:
        print(f"EXTERNAL CHAT ACTIVATION IMPORT: FAIL - {exc}")
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUTPUT)

    provenance = {
        "schema_version": "1.0.0",
        "record_type": "external_chat_activation_evidence_import_provenance",
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source": origin,
        "source_repository": payload.get("repository"),
        "source_commit_sha": payload.get("commit_sha"),
        "source_workflow_run_id": payload.get("workflow_run_id"),
        "source_evidence_sha256": payload.get("evidence_sha256"),
        "projected_path": str(OUTPUT.relative_to(ROOT)),
        "observed_result": payload.get("result"),
        "mutation_required_disabled": payload.get("post_deployment_live_verification", {}).get("mutation_required_disabled"),
        "authority_boundary": {
            "import_is_deployment_authority": False,
            "import_is_repository_mutation_authority": False,
            "import_is_publication_authority": False,
            "import_is_certification": False,
            "import_creates_standing": False,
        },
    }
    PROVENANCE.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"EXTERNAL CHAT ACTIVATION IMPORT: PASS - {payload.get('result')}")
    print(f"Projection: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
