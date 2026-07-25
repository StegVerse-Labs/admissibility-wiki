#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "visibility-vs-authority.md"
STATUS = ROOT / "static" / "status" / "visibility-authority-status.json"

REQUIRED_DOC = (
    "Public accessibility and governance authority are independent state dimensions.",
    "`PUBLICLY_VISIBLE` is descriptive only.",
    "acknowledgement != endorsement",
    "reconstruction != authorization",
    "StegVerse-org/StegVerse-SDK",
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/Site",
    "master-records/orchestration",
)


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append("missing doctrine")
    else:
        text = DOC.read_text(encoding="utf-8")
        failures.extend(f"missing doctrine marker: {marker}" for marker in REQUIRED_DOC if marker not in text)

    if not STATUS.exists():
        failures.append("missing status")
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
        if data.get("goal_id") != "visibility-vs-authority":
            failures.append("invalid goal_id")
        invariants = data.get("invariants") or {}
        for key in (
            "public_visibility_is_authority",
            "acknowledgement_is_endorsement",
            "acknowledgement_is_attribution",
            "acknowledgement_is_public_association",
            "reconstruction_is_authorization",
        ):
            if invariants.get(key) is not False:
                failures.append(f"{key} must be false")
        if data.get("manual_user_action_required") is not False:
            failures.append("manual_user_action_required must be false")
        if data.get("authority_posture") != "DOCUMENTATION_ONLY_NO_DOWNSTREAM_MUTATION":
            failures.append("invalid authority_posture")

    print("VISIBILITY AUTHORITY DOCTRINE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
