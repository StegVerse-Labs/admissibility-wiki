#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVATION = ROOT / "static" / "status" / "repo-standards-downstream-mirror-activation.json"
REPORT = ROOT / "static" / "status" / "repo-standards-downstream-activation-validation-report.json"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"

REQUIRED_TARGETS = {
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-002/stegguardian-wiki",
    "StegVerse-002/StegGuardian",
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"DOWNSTREAM ACTIVATION: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    raw = read_text(path)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"DOWNSTREAM ACTIVATION: FAIL - invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("DOWNSTREAM ACTIVATION: FAIL - JSON root must be an object")
    return data


def expect(data: dict, expected: dict, label: str) -> None:
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f"DOWNSTREAM ACTIVATION: FAIL - {label} {key} expected {value!r}, got {data.get(key)!r}")


def main() -> int:
    data = read_json(ACTIVATION)
    expect(data, {
        "activation_id": "repo-standards-downstream-mirror-activation",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-and-installation-bundle-pending-release",
        "status": "PENDING_UPSTREAM_TAG_RELEASE_AND_LOCAL_VALIDATION",
    }, "activation")

    targets = {item.get("target") for item in data.get("downstream_targets", []) if isinstance(item, dict)}
    missing = sorted(REQUIRED_TARGETS - targets)
    if missing:
        raise SystemExit(f"DOWNSTREAM ACTIVATION: FAIL - missing targets: {', '.join(missing)}")

    report = read_json(REPORT)
    expect(report, {
        "report_id": "repo-standards-downstream-activation-validation-report",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-and-installation-bundle-pending-release",
        "result": "PENDING_LOCAL_VALIDATION",
        "validator": "scripts/check_repo_standards_downstream_activation.py",
    }, "report")

    handoff = read_text(HANDOFF)
    if "repo-standards-downstream-mirror-activation.json" not in handoff:
        raise SystemExit("DOWNSTREAM ACTIVATION: FAIL - handoff does not reference downstream activation artifact")

    print("DOWNSTREAM ACTIVATION: PASS - downstream mirror activation queue and report present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
