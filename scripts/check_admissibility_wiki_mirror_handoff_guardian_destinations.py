#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
STATUS = "static/status/guardian-destination-resolution-status.json"
PUBLIC_REPO = "StegVerse-002/stegguardian-wiki"
IMPLEMENTATION_REPO = "StegVerse-002/StegGuardian"
OLD_UNRESOLVED = "stegguardian-wiki:\n  - downstream summary after wiki validation"


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        print("ADMISSIBILITY WIKI MIRROR HANDOFF GUARDIAN DESTINATIONS: FAIL")
        print("- handoff missing")
        return 1

    text = HANDOFF.read_text(encoding="utf-8")
    for required in [STATUS, PUBLIC_REPO, IMPLEMENTATION_REPO]:
        if required not in text:
            failures.append(f"missing handoff content: {required}")

    if "downstream public Guardian summary after wiki validation" not in text:
        failures.append("missing public destination summary")
    if "standing-boundary awareness after wiki validation" not in text:
        failures.append("missing implementation destination summary")
    if OLD_UNRESOLVED in text:
        failures.append("old unresolved Guardian destination remains in handoff")
    if not (ROOT / STATUS).exists():
        failures.append("Guardian destination status artifact missing")

    print("ADMISSIBILITY WIKI MIRROR HANDOFF GUARDIAN DESTINATIONS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
