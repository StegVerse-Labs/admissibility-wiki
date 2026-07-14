#!/usr/bin/env python3
"""Mirror the canonical SDK system-boundary status without manual copying."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping

SOURCE = "https://raw.githubusercontent.com/StegVerse-org/StegVerse-SDK/main/evidence/system-boundary-downstream-status.v0.1.json"
OUTPUT = Path(__file__).resolve().parents[1] / "static/status/system-boundary-status.v0.1.json"
TARGET = "StegVerse-Labs/admissibility-wiki"
REQUIRED_FALSE = (
    "production_binding_enabled",
    "release_authorized",
    "execution_authority_granted",
    "custody_transferred",
    "admissibility_determined",
)


def validate_packet(packet: Mapping[str, Any]) -> None:
    if packet.get("schema_version") != "stegverse.system_boundary.downstream_status.v0.1":
        raise ValueError("unsupported schema")
    if packet.get("status_only") is not True or TARGET not in packet.get("targets", []):
        raise ValueError("packet is not an authorized status-only mirror")
    for key in REQUIRED_FALSE:
        if packet.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    verified = packet.get("activation_state") == "VERIFIED"
    if verified != (packet.get("verified") is True and packet.get("downstream_propagation_allowed") is True):
        raise ValueError("activation and propagation flags are inconsistent")


def main() -> int:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "admissibility-wiki-status-sync"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            packet = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"Status retrieval deferred; prior validated state retained: {exc}", file=sys.stderr)
        return 0
    validate_packet(packet)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print("System-boundary status updated.")
    else:
        print("System-boundary status unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
