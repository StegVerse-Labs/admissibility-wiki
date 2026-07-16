#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
ADDENDUM = ROOT / "docs" / "MIRROR_HANDOFF_GUARD_ADDENDUM.md"
STATUS = "static/status/guardian-destination-resolution-status.json"
PUBLIC_REPO = "StegVerse-002/stegguardian-wiki"
IMPLEMENTATION_REPO = "StegVerse-002/StegGuardian"
OLD_UNRESOLVED = "stegguardian-wiki:\n  - downstream summary after wiki validation"


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("handoff missing")
    if not ADDENDUM.exists():
        failures.append("handoff addendum missing")

    handoff_text = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""
    addendum_text = ADDENDUM.read_text(encoding="utf-8") if ADDENDUM.exists() else ""
    continuity_text = handoff_text + "\n" + addendum_text

    for required in [STATUS, PUBLIC_REPO, IMPLEMENTATION_REPO]:
        if required not in continuity_text:
            failures.append(f"missing continuity content: {required}")

    if "downstream public Guardian summary after wiki validation" not in continuity_text:
        failures.append("missing public destination summary")
    if "standing-boundary awareness after wiki validation" not in continuity_text:
        failures.append("missing implementation destination summary")
    if OLD_UNRESOLVED in handoff_text:
        failures.append("old unresolved Guardian destination remains in root handoff")
    if not (ROOT / STATUS).exists():
        failures.append("Guardian destination status artifact missing")

    for boundary in [
        "destination mutation authority: none granted",
        "activation authority: none granted",
    ]:
        if boundary not in continuity_text:
            failures.append(f"missing non-authority boundary: {boundary}")

    print("ADMISSIBILITY WIKI MIRROR HANDOFF GUARDIAN DESTINATIONS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
