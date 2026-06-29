#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_MD = ROOT / "docs" / "external-frameworks" / "index.md"
INDEX_JSON = ROOT / "docs" / "external-frameworks" / "index.json"
AE_MD = ROOT / "docs" / "external-frameworks" / "admissible-existence-seed-cycle.md"
AE_JSON = ROOT / "docs" / "external-frameworks" / "admissible-existence-seed-cycle.json"


def main():
    missing = [str(path.relative_to(ROOT)) for path in [INDEX_MD, INDEX_JSON, AE_MD, AE_JSON] if not path.exists()]
    if missing:
        print(json.dumps({"result": "FAIL", "missing": missing}, indent=2))
        return 1
    md = INDEX_MD.read_text(encoding="utf-8")
    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    names = [entry.get("name") for entry in data.get("entries", [])]
    ok = "Admissible Existence Seed Cycle" in md and "Admissible Existence Seed Cycle" in names
    print(json.dumps({"result": "PASS" if ok else "FAIL", "checked": "Admissible Existence Seed Cycle"}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
