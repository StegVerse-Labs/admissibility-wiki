#!/usr/bin/env python3
"""Validate bounded adjudication of TA-14 StegVerse gap-review v2 findings."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADJUDICATION = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.adjudication.json"
EXPECTED = [f"G-{i:02d}" for i in range(1, 19)]
ALLOWED_DISPOSITIONS = {"AGREE", "PARTIAL", "DISAGREE", "DEFER"}
ALLOWED_STATES = {"BOUNDED", "EVIDENCE_MAPPING", "DEFERRED_BOUNDED", "ADJUDICATED_BOUNDED"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TA-14 GAP REVIEW V2 ADJUDICATION: FAIL - {message}")


def main() -> None:
    require(ADJUDICATION.is_file(), "adjudication record missing")
    data = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "external-review-adjudication.v1", "schema mismatch")
    require(set(data.get("disposition_vocabulary", [])) == ALLOWED_DISPOSITIONS, "disposition vocabulary drift")

    rules = data.get("rules", {})
    require(rules.get("no_disposition_without_evidence_path") is True, "evidence-path rule missing")
    require(rules.get("missing_public_proof_is_not_nonexistence") is True, "missing-proof boundary missing")
    require(rules.get("architecture_disagreement_is_not_implementation_failure") is True, "architecture/runtime boundary missing")
    require(rules.get("self_authored_validation_is_not_independent_reconstruction") is True, "independence boundary missing")
    require(rules.get("unresolved_finding_does_not_halt_other_findings") is True, "non-halting rule missing")

    findings = data.get("findings")
    require(isinstance(findings, list) and len(findings) == 18, "exactly eighteen findings required")
    ids = [item.get("finding_id") for item in findings if isinstance(item, dict)]
    require(ids == EXPECTED, "finding order or coverage mismatch")

    disposition_counts = {value: 0 for value in ALLOWED_DISPOSITIONS}
    for finding in findings:
        require(isinstance(finding, dict), "finding must be an object")
        finding_id = finding.get("finding_id")
        disposition = finding.get("disposition")
        require(disposition in ALLOWED_DISPOSITIONS, f"invalid disposition for {finding_id}")
        disposition_counts[disposition] += 1
        require(finding.get("state") in ALLOWED_STATES, f"invalid state for {finding_id}")
        work_path = finding.get("work_path")
        require(isinstance(work_path, str) and work_path, f"missing work_path for {finding_id}")
        require(not work_path.startswith(("http://", "https://")), f"external work path prohibited for {finding_id}")
        require((ROOT / work_path).exists(), f"work_path does not exist for {finding_id}: {work_path}")
        evidence_targets = finding.get("evidence_targets")
        require(isinstance(evidence_targets, list) and evidence_targets, f"evidence targets missing for {finding_id}")

    require(data.get("standing_effect") == "NONE_PENDING_REVIEW", "adjudication must not silently alter standing")
    boundary = data.get("authority_boundary", {})
    for key in (
        "certification_granted",
        "execution_authority_granted",
        "government_recognition_established",
        "independent_reconstruction_established",
    ):
        require(boundary.get(key) is False, f"authority boundary drift: {key}")

    print(
        "TA-14 GAP REVIEW V2 ADJUDICATION: PASS - "
        f"18/18 findings bounded; AGREE={disposition_counts['AGREE']}, "
        f"PARTIAL={disposition_counts['PARTIAL']}, DISAGREE={disposition_counts['DISAGREE']}, "
        f"DEFER={disposition_counts['DEFER']}; unresolved evidence remains nonblocking"
    )


if __name__ == "__main__":
    main()
