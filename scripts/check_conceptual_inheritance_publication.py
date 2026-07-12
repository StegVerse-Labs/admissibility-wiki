#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "static" / "status" / "conceptual-inheritance-publication-verification.json"
ALLOWED_STATES = {
    "PENDING_LIVE_DEPLOYMENT_VERIFICATION",
    "VERIFIED",
    "FAILED_CLOSED",
}
TARGET_STATES = {"PENDING", "VERIFIED", "FAILED"}


def main() -> int:
    failures: list[str] = []

    if not RECORD.exists():
        print("CONCEPTUAL INHERITANCE PUBLICATION: FAIL")
        print(f"- missing {RECORD.relative_to(ROOT)}")
        return 1

    try:
        data = json.loads(RECORD.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("CONCEPTUAL INHERITANCE PUBLICATION: FAIL")
        print(f"- unreadable publication record: {exc}")
        return 1

    if data.get("goal_id") != "conceptual-inheritance-provenance-standing":
        failures.append("unexpected goal_id")
    if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("unexpected repository")
    if data.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("canonical workflow path mismatch")
    if data.get("verification_state") not in ALLOWED_STATES:
        failures.append("invalid verification_state")
    if data.get("manual_task_required") is not False:
        failures.append("manual_task_required must be false")

    local_artifacts = data.get("local_artifacts")
    if not isinstance(local_artifacts, dict) or not local_artifacts:
        failures.append("local_artifacts must be a non-empty object")
    else:
        for label, rel_path in local_artifacts.items():
            if not isinstance(rel_path, str) or not rel_path:
                failures.append(f"invalid local artifact path: {label}")
                continue
            if not (ROOT / rel_path).exists():
                failures.append(f"missing local artifact: {rel_path}")

    targets = data.get("public_targets")
    if not isinstance(targets, list) or len(targets) < 2:
        failures.append("at least two public targets are required")
        targets = []

    seen_kinds: set[str] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            failures.append(f"public target {index} must be an object")
            continue
        kind = target.get("kind")
        if not isinstance(kind, str) or not kind:
            failures.append(f"public target {index} missing kind")
        elif kind in seen_kinds:
            failures.append(f"duplicate public target kind: {kind}")
        else:
            seen_kinds.add(kind)
        url = target.get("url")
        if not isinstance(url, str) or not url.startswith("https://stegverse-labs.github.io/admissibility-wiki/"):
            failures.append(f"public target {index} has invalid URL")
        state = target.get("state")
        if state not in TARGET_STATES:
            failures.append(f"public target {index} has invalid state")

        if state == "VERIFIED":
            status = target.get("http_status")
            if not isinstance(status, int) or not 200 <= status < 400:
                failures.append(f"verified target {index} lacks successful http_status")
            if target.get("content_marker_verified") is not True:
                failures.append(f"verified target {index} lacks content marker verification")
            if not target.get("verified_at"):
                failures.append(f"verified target {index} lacks verified_at")

    markers = data.get("required_content_markers")
    required_markers = {
        "Conceptual Inheritance and Provenance Standing",
        "architectural integrity",
        "provenance continuity",
        "origin-claim standing",
    }
    if not isinstance(markers, list) or not required_markers.issubset(set(markers)):
        failures.append("required content markers are incomplete")

    non_claims = data.get("non_claims")
    if not isinstance(non_claims, list):
        failures.append("non_claims must be a list")
    else:
        joined = " ".join(str(item) for item in non_claims).lower()
        for marker in ("pending deployment", "public visibility", "authorship"):
            if marker not in joined:
                failures.append(f"missing non-claim marker: {marker}")

    overall = data.get("verification_state")
    verified_count = sum(1 for target in targets if isinstance(target, dict) and target.get("state") == "VERIFIED")
    failed_count = sum(1 for target in targets if isinstance(target, dict) and target.get("state") == "FAILED")
    if overall == "VERIFIED" and verified_count != len(targets):
        failures.append("overall VERIFIED requires every target to be VERIFIED")
    if overall == "FAILED_CLOSED" and failed_count == 0:
        failures.append("FAILED_CLOSED requires at least one failed target")
    if overall == "PENDING_LIVE_DEPLOYMENT_VERIFICATION" and verified_count == len(targets) and targets:
        failures.append("all targets are verified but overall state remains pending")

    if failures:
        print("CONCEPTUAL INHERITANCE PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONCEPTUAL INHERITANCE PUBLICATION: PASS")
    print(f"- verification_state: {overall}")
    print(f"- public_targets: {len(targets)}")
    print(f"- verified_targets: {verified_count}")
    print("- pending state remains fail-closed and is not treated as deployment success")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
