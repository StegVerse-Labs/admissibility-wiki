#!/usr/bin/env python3
"""Import Publisher's Ecosystem Chat activation projection for wiki display.

Projection-only consumer. A verified wiki projection requires Publisher's
hash-bound activation status and independently reconstructed terminal custody.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "status" / "ecosystem-chat-publisher-activation.json"
SOURCE_URL = os.getenv(
    "STEGVERSE_PUBLISHER_ECOSYSTEM_CHAT_STATUS_URL",
    "https://raw.githubusercontent.com/GCAT-BCAT-Engine/Publisher/main/data/ecosystem-chat-activation-status.json",
)
TIMEOUT = float(os.getenv("STEGVERSE_PUBLISHER_STATUS_FETCH_TIMEOUT_SECONDS", "20"))


def canonical_hash(payload: dict[str, Any]) -> str:
    material = dict(payload)
    material.pop("status_sha256", None)
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def fetch() -> tuple[dict[str, Any], str]:
    outbound = request.Request(
        SOURCE_URL,
        headers={"Accept": "application/json", "User-Agent": "StegVerse-Admissibility-Wiki-Activation-Importer/1.2"},
    )
    with request.urlopen(outbound, timeout=TIMEOUT) as response:
        raw = response.read()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("publisher_status_not_object")
    return value, hashlib.sha256(raw).hexdigest()


def validate(source: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if source.get("schema") != "stegverse.publisher.ecosystem_chat_activation_status.v1":
        failures.append("schema_mismatch")
    if not isinstance(source.get("status_sha256"), str):
        failures.append("status_digest_missing")
    elif source.get("status_sha256") != canonical_hash(source):
        failures.append("status_digest_mismatch")
    for key in ("publication_authorized", "release_authorized", "execution_authorized"):
        if source.get(key) is not False:
            failures.append(f"authority_boundary_invalid:{key}")
    if source.get("manual_user_action_required") is not False:
        failures.append("manual_action_boundary_invalid")
    if source.get("terminal_custody_verified") is not True:
        failures.append("terminal_custody_not_verified")
    if not isinstance(source.get("terminal_custody_sha256"), str) or len(source.get("terminal_custody_sha256", "")) != 64:
        failures.append("terminal_custody_digest_missing")
    if source.get("custody_repository") != "master-records/orchestration":
        failures.append("custody_repository_mismatch")
    return failures


def write(status: str, reason: str, source: dict[str, Any] | None = None, source_sha256: str | None = None) -> None:
    verified = bool(
        source
        and source.get("status") == "VERIFIED_ACTIVATION_IMPORTED"
        and source.get("activation_complete") is True
        and source.get("terminal_custody_verified") is True
    )
    payload = {
        "schema": "stegverse.admissibility_wiki.ecosystem_chat_activation_projection.v2",
        "status": status,
        "reason": reason,
        "source_repository": "GCAT-BCAT-Engine/Publisher",
        "source_url": SOURCE_URL,
        "source_sha256": source_sha256,
        "publisher_status_sha256": source.get("status_sha256") if source else None,
        "publisher_status": source.get("status") if source else None,
        "publisher_activation_complete": source.get("activation_complete") if source else False,
        "terminal_custody_sha256": source.get("terminal_custody_sha256") if source else None,
        "terminal_custody_verified": source.get("terminal_custody_verified") if source else False,
        "custody_repository": source.get("custody_repository") if source else None,
        "verified_activation_projection": verified and status == "VERIFIED_PUBLISHER_ACTIVATION_IMPORTED",
        "manual_user_action_required": False,
        "authority_boundary": {
            "projection_is_publication_authority": False,
            "projection_is_release_authority": False,
            "projection_is_custody": False,
            "projection_is_execution_authority": False,
            "projection_is_admissibility_determination": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    try:
        source, digest = fetch()
    except error.HTTPError as exc:
        write("PENDING_PUBLISHER_ACTIVATION", f"source_http_status_{exc.code}")
        return 0
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
        write("PENDING_PUBLISHER_ACTIVATION", f"source_unavailable:{type(exc).__name__}")
        return 0

    failures = validate(source)
    if failures:
        write("REJECTED_PUBLISHER_ACTIVATION", ";".join(sorted(failures)), source, digest)
        return 1
    if source.get("status") != "VERIFIED_ACTIVATION_IMPORTED" or source.get("activation_complete") is not True:
        write("PENDING_PUBLISHER_ACTIVATION", "publisher_activation_not_complete", source, digest)
        return 0
    write("VERIFIED_PUBLISHER_ACTIVATION_IMPORTED", "publisher_activation_and_terminal_custody_verified", source, digest)
    print("ADMISSIBILITY_WIKI_ECOSYSTEM_CHAT_ACTIVATION_IMPORT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())