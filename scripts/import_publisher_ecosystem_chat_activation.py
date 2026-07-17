#!/usr/bin/env python3
"""Import Publisher's Ecosystem Chat activation projection for wiki display.

This consumer is projection-only. It validates the Publisher status contract and
preserves a source digest, but it grants no publication, release, custody,
execution, deployment, or admissibility authority.
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


def fetch() -> tuple[dict[str, Any], str]:
    outbound = request.Request(
        SOURCE_URL,
        headers={"Accept": "application/json", "User-Agent": "StegVerse-Admissibility-Wiki-Activation-Importer/1.0"},
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
    for key in ("publication_authorized", "release_authorized", "custody_recorded", "execution_authorized"):
        if source.get(key) is not False:
            failures.append(f"authority_boundary_invalid:{key}")
    if source.get("manual_user_action_required") is not False:
        failures.append("manual_action_boundary_invalid")
    return failures


def write(status: str, reason: str, source: dict[str, Any] | None = None, source_sha256: str | None = None) -> None:
    verified = bool(
        source
        and source.get("status") == "VERIFIED_ACTIVATION_IMPORTED"
        and source.get("activation_complete") is True
    )
    payload = {
        "schema": "stegverse.admissibility_wiki.ecosystem_chat_activation_projection.v1",
        "status": status,
        "reason": reason,
        "source_repository": "GCAT-BCAT-Engine/Publisher",
        "source_url": SOURCE_URL,
        "source_sha256": source_sha256,
        "publisher_status": source.get("status") if source else None,
        "publisher_activation_complete": source.get("activation_complete") if source else False,
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
    write("VERIFIED_PUBLISHER_ACTIVATION_IMPORTED", "publisher_projection_verified", source, digest)
    print("ADMISSIBILITY_WIKI_ECOSYSTEM_CHAT_ACTIVATION_IMPORT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
