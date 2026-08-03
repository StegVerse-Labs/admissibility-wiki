#!/usr/bin/env python3
"""Validate the reconstructable singularity schema example and threshold semantics."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "static/formalisms/reconstructable-singularity.v0.1.schema.json"
EXAMPLE = ROOT / "static/formalisms/reconstructable-singularity.v0.1.example.json"
DOC = ROOT / "docs/formalisms/reconstructable-singularity.md"


def fail(message: str) -> int:
    print(f"RECONSTRUCTABLE SINGULARITY: FAIL - {message}")
    return 1


def main() -> int:
    for path in (SCHEMA, EXAMPLE, DOC):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    record = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    required = set(schema["required"])
    missing = required.difference(record)
    if missing:
        return fail(f"example missing required fields: {sorted(missing)}")

    candidates = set(record["candidate_histories"])
    observers = {item["observer_id"]: item for item in record["observers"]}
    selected = record["selected_observer_ids"]
    if len(selected) != record["threshold"]["minimum_perspective_count"]:
        return fail("selected observer count does not equal declared minimum")
    if any(observer_id not in observers for observer_id in selected):
        return fail("selected observer is undefined")

    surviving = set(candidates)
    for observer_id in selected:
        observation = observers[observer_id]
        affirmed = set(observation["affirmed_history_ids"])
        excluded = set(observation["excluded_history_ids"])
        if not affirmed.issubset(candidates) or not excluded.issubset(candidates):
            return fail(f"observer {observer_id} references unknown histories")
        if affirmed.intersection(excluded):
            return fail(f"observer {observer_id} both affirms and excludes a history")
        surviving.intersection_update(affirmed)
        surviving.difference_update(excluded)

    declared = set(record["surviving_history_ids"])
    if surviving != declared:
        return fail(f"computed survivors {sorted(surviving)} != declared {sorted(declared)}")
    if len(surviving) != 1:
        return fail("selected perspectives do not produce a singleton reconstruction")

    # Prove minimality for this record: removing any selected observer must destroy uniqueness.
    for removed in selected:
        reduced = set(candidates)
        for observer_id in selected:
            if observer_id == removed:
                continue
            observation = observers[observer_id]
            reduced.intersection_update(observation["affirmed_history_ids"])
            reduced.difference_update(observation["excluded_history_ids"])
        if len(reduced) == 1:
            return fail(f"declared set is not minimal; {removed} is redundant")

    doc = DOC.read_text(encoding="utf-8")
    for needle in ("k_{\\Gamma}^{*}", "|\\mathcal C_A(I)|=1", "exclusionary"):
        if needle not in doc:
            return fail(f"formal document missing required expression: {needle}")

    print("RECONSTRUCTABLE SINGULARITY: PASS - schema assets present, singleton reconstruction computed, and selected perspective set is minimal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
