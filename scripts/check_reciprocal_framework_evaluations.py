#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static" / "data" / "framework-evaluations"


def main() -> int:
    failures: list[str] = []
    registry = json.loads((BASE / "index.json").read_text(encoding="utf-8"))
    for entry in registry.get("frameworks", []):
        path = BASE / entry["record_path"]
        if not path.exists():
            failures.append(f"missing framework record: {path.relative_to(ROOT)}")
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("framework", {}).get("framework_id") != entry.get("framework_id"):
            failures.append(f"registry/record framework_id mismatch: {entry.get('framework_id')}")
        if record.get("publication", {}).get("projection_authority") != "NONE":
            failures.append(f"projection authority must remain NONE: {entry.get('framework_id')}")
    if failures:
        print("RECIPROCAL FRAMEWORK EVALUATIONS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("RECIPROCAL FRAMEWORK EVALUATIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
