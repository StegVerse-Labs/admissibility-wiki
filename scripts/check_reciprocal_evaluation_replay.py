#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static" / "data" / "framework-evaluations"
TEST = BASE / "test-cases" / "asro-declared-reference-membership-v1.json"
RUN = BASE / "runs" / "asro-declared-reference-membership-v1-stegverse-run-001.jsonl"


def main() -> int:
    failures: list[str] = []
    test = json.loads(TEST.read_text(encoding="utf-8"))
    events = [json.loads(line) for line in RUN.read_text(encoding="utf-8").splitlines() if line.strip()]

    if test.get("status") != "FROZEN":
        failures.append("test case is not frozen")
    if test.get("replay", {}).get("deterministic") is not True:
        failures.append("test case is not deterministic")
    indexes = [event.get("event_index") for event in events]
    if indexes != list(range(1, len(events) + 1)):
        failures.append("event indexes are not contiguous and ordered")
    if any(event.get("test_case_id") != test.get("test_case_id") for event in events):
        failures.append("run contains mismatched test_case_id")
    if any(event.get("run_id") != "asro-declared-reference-membership-v1-stegverse-run-001" for event in events):
        failures.append("run contains mismatched run_id")
    if not events or events[-1].get("event_type") != "RUN_COMPLETED":
        failures.append("run does not terminate with RUN_COMPLETED")
    else:
        final = events[-1]
        if final.get("result") != "PASS":
            failures.append("final result is not PASS")
        if final.get("replay_status") != "PASS":
            failures.append("replay status is not PASS")
        if final.get("reconstruction_status") != "PASS":
            failures.append("reconstruction status is not PASS")
        if final.get("admissibility") != "NOT_EVALUATED":
            failures.append("replay improperly establishes admissibility")
        if final.get("authority") != "NONE" or final.get("execution") != "NONE":
            failures.append("replay improperly grants authority or execution")

    if failures:
        print("RECIPROCAL EVALUATION REPLAY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("RECIPROCAL EVALUATION REPLAY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
