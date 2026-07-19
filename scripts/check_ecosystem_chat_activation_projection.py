#!/usr/bin/env python3
"""Refresh and validate the fail-closed Ecosystem Chat downstream projection."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/status/ecosystem-chat-activation-status.json"
STATE_URL = "https://raw.githubusercontent.com/StegVerse-Labs/Site/main/data/ecosystem-chat-activation-state.json"
PACKET_URL = "https://raw.githubusercontent.com/StegVerse-Labs/Site/main/data/ecosystem-chat-activation-propagation.json"
REPOSITORY = "StegVerse-Labs/admissibility-wiki"


def canonical_sha(value: dict, field: str) -> str:
    material = dict(value)
    material.pop(field, None)
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def fetch(url: str, attempts: int = 4) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "StegVerse-Admissibility-Ecosystem-Chat-Projection/2.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                value = json.loads(response.read().decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError("source_not_object")
            return value
        except Exception as exc:  # network/source failures remain fail-closed
            last_error = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise RuntimeError(f"source_fetch_failed:{type(last_error).__name__}") from last_error


def ensure_false_flags(value: dict, keys: tuple[str, ...], label: str) -> None:
    boundary = value.get("authority_boundary") or {}
    if any(boundary.get(key) is not False for key in keys):
        raise ValueError(f"{label}_authority_escalation")


def validate_projection(value: dict) -> None:
    if value.get("schema") != "stegverse.ecosystem_chat.downstream_projection.v2":
        raise ValueError("projection_schema_mismatch")
    if value.get("repository") != REPOSITORY:
        raise ValueError("projection_repository_mismatch")
    if value.get("manual_user_action_required") is not False:
        raise ValueError("manual_action_must_remain_false")
    if value.get("destination_declared") is not True:
        raise ValueError("destination_declaration_missing")
    if not isinstance(value.get("blockers"), list):
        raise ValueError("projection_blockers_missing")
    ensure_false_flags(
        value,
        (
            "projection_is_activation_authority",
            "projection_is_release_authority",
            "projection_is_publication_authority",
            "projection_is_custody",
            "projection_is_admissibility_authority",
            "projection_is_execution_authority",
        ),
        "projection",
    )
    if value.get("state") == "VERIFIED_INGESTION_READY":
        if value.get("destination_ingestion_ready") is not True or value.get("blockers"):
            raise ValueError("verified_projection_not_ready")
    elif value.get("state") != "ACTIVATION_EVIDENCE_PENDING":
        raise ValueError("projection_state_invalid")
    if canonical_sha(value, "projection_sha256") != value.get("projection_sha256"):
        raise ValueError("projection_hash_mismatch")


def refresh() -> dict:
    state = fetch(STATE_URL)
    packet = fetch(PACKET_URL)
    if canonical_sha(state, "state_sha256") != state.get("state_sha256"):
        raise ValueError("source_state_hash_mismatch")
    if canonical_sha(packet, "packet_sha256") != packet.get("packet_sha256"):
        raise ValueError("source_packet_hash_mismatch")
    if packet.get("source_state_sha256") != state.get("state_sha256"):
        raise ValueError("source_binding_mismatch")
    ensure_false_flags(
        state,
        (
            "state_grants_deployment_authority",
            "state_grants_mutation_authority",
            "state_grants_custody_authority",
            "state_grants_release_authority",
        ),
        "source_state",
    )
    ensure_false_flags(
        packet,
        (
            "propagation_is_activation_authority",
            "propagation_is_release_authority",
            "propagation_is_publication_authority",
            "propagation_is_custody",
        ),
        "source_packet",
    )

    destinations = {
        item.get("repository"): item
        for item in packet.get("destinations", [])
        if isinstance(item, dict)
    }
    destination = destinations.get(REPOSITORY)
    if not destination:
        raise ValueError("destination_not_declared")
    if destination.get("manual_user_action_required") is not False:
        raise ValueError("destination_manual_action_escalation")

    ready = (
        state.get("state") == "ACTIVATION_COMPLETE"
        and packet.get("state") == "READY_FOR_DOWNSTREAM_INGESTION"
        and destination.get("ingestion_ready") is True
    )
    blockers: list[str] = []
    if state.get("state") != "ACTIVATION_COMPLETE":
        blockers.append("site_activation_not_complete")
    if packet.get("state") != "READY_FOR_DOWNSTREAM_INGESTION":
        blockers.append("site_propagation_not_ready")
    if destination.get("ingestion_ready") is not True:
        blockers.append("destination_ingestion_not_ready")

    projection = {
        "schema": "stegverse.ecosystem_chat.downstream_projection.v2",
        "repository": REPOSITORY,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": "VERIFIED_INGESTION_READY" if ready else "ACTIVATION_EVIDENCE_PENDING",
        "source_repository": "StegVerse-Labs/Site",
        "source_state": state.get("state"),
        "source_propagation_state": packet.get("state"),
        "source_state_sha256": state.get("state_sha256"),
        "source_packet_sha256": packet.get("packet_sha256"),
        "destination_declared": True,
        "destination_ingestion_ready": destination.get("ingestion_ready") is True,
        "required_action": destination.get("required_action"),
        "blockers": blockers,
        "manual_user_action_required": False,
        "authority_boundary": {
            "projection_is_activation_authority": False,
            "projection_is_release_authority": False,
            "projection_is_publication_authority": False,
            "projection_is_custody": False,
            "projection_is_admissibility_authority": False,
            "projection_is_execution_authority": False,
        },
    }
    projection["projection_sha256"] = canonical_sha(projection, "projection_sha256")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(projection, indent=2) + "\n", encoding="utf-8")
    return projection


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checked-in-only", action="store_true")
    args = parser.parse_args()
    if args.checked_in_only:
        value = json.loads(OUTPUT.read_text(encoding="utf-8"))
    else:
        try:
            value = refresh()
        except Exception as exc:
            value = json.loads(OUTPUT.read_text(encoding="utf-8"))
            print(f"ECOSYSTEM CHAT ACTIVATION PROJECTION: SOURCE_PENDING ({type(exc).__name__})")
    validate_projection(value)
    print(
        "ECOSYSTEM CHAT ACTIVATION PROJECTION: PASS "
        f"({value['state']}; blockers={','.join(value['blockers']) or 'none'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
