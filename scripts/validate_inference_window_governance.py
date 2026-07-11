#!/usr/bin/env python3
"""Validate inference-window governance worked cases.

The validator uses only the Python standard library so it can run in the
repository's canonical workflow without adding a dependency.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ALLOWED_DISPOSITIONS = {"ALLOW", "DENY", "DEFER", "ESCALATE"}
RECOVERY_PATHS = {"rollback", "repair", "compensate", "contain", "appeal", "learn"}
EPSILON = 1e-12


class ValidationError(ValueError):
    """Raised when a governance record is structurally or logically invalid."""


@dataclass(frozen=True)
class Evaluation:
    case_id: str
    freshness: float
    evidence_sufficiency: float
    threshold: float
    standing: float
    stale_material_evidence: tuple[str, ...]
    hard_failures: tuple[str, ...]
    calculated_disposition: str


def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError("timestamp must be a string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValidationError(f"invalid ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"timestamp must include a timezone: {value}")
    return parsed.astimezone(timezone.utc)


def score(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{field} must be numeric")
    numeric = float(value)
    if not 0.0 <= numeric <= 1.0:
        raise ValidationError(f"{field} must be within [0, 1]")
    return numeric


def positive(value: Any, field: str, *, allow_zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{field} must be numeric")
    numeric = float(value)
    if allow_zero and numeric < 0:
        raise ValidationError(f"{field} must be non-negative")
    if not allow_zero and numeric <= 0:
        raise ValidationError(f"{field} must be positive")
    return numeric


def require_keys(record: dict[str, Any], keys: Iterable[str], context: str) -> None:
    missing = [key for key in keys if key not in record]
    if missing:
        raise ValidationError(f"{context} missing required keys: {', '.join(missing)}")


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def evaluate_case(case: dict[str, Any]) -> Evaluation:
    require_keys(
        case,
        (
            "id",
            "title",
            "commit_time",
            "evidence",
            "standing",
            "consequence",
            "threshold_coefficients",
            "independent_review_required",
            "expected_disposition",
        ),
        "case",
    )

    case_id = case["id"]
    if not isinstance(case_id, str) or not case_id:
        raise ValidationError("case.id must be a non-empty string")
    if case["expected_disposition"] not in ALLOWED_DISPOSITIONS:
        raise ValidationError(f"{case_id}: unsupported expected disposition")

    commit_time = parse_time(case["commit_time"])
    evidence = case["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ValidationError(f"{case_id}: evidence must be a non-empty list")

    weighted_freshness = 0.0
    weighted_sufficiency = 0.0
    total_weight = 0.0
    stale_material: list[str] = []

    for item in evidence:
        if not isinstance(item, dict):
            raise ValidationError(f"{case_id}: evidence items must be objects")
        require_keys(
            item,
            (
                "id",
                "observed_at",
                "max_age_seconds",
                "decay_rate_per_second",
                "weight",
                "material",
                "sufficiency",
            ),
            f"{case_id} evidence item",
        )
        observed_at = parse_time(item["observed_at"])
        age_seconds = (commit_time - observed_at).total_seconds()
        if age_seconds < 0:
            raise ValidationError(f"{case_id}/{item['id']}: evidence is observed after commit time")
        max_age = positive(item["max_age_seconds"], f"{case_id}/{item['id']}.max_age_seconds")
        decay = positive(
            item["decay_rate_per_second"],
            f"{case_id}/{item['id']}.decay_rate_per_second",
            allow_zero=True,
        )
        weight = positive(item["weight"], f"{case_id}/{item['id']}.weight")
        sufficiency = score(item["sufficiency"], f"{case_id}/{item['id']}.sufficiency")
        freshness = math.exp(-decay * age_seconds)
        weighted_freshness += weight * freshness
        weighted_sufficiency += weight * sufficiency
        total_weight += weight
        if bool(item["material"]) and age_seconds > max_age:
            stale_material.append(str(item["id"]))

    freshness = weighted_freshness / total_weight
    evidence_sufficiency = weighted_sufficiency / total_weight

    standing_record = case["standing"]
    if not isinstance(standing_record, dict):
        raise ValidationError(f"{case_id}: standing must be an object")
    require_keys(standing_record, ("authority", "policy", "context", "consent", "scope"), f"{case_id}.standing")
    authority = score(standing_record["authority"], f"{case_id}.standing.authority")
    policy = score(standing_record["policy"], f"{case_id}.standing.policy")
    context = score(standing_record["context"], f"{case_id}.standing.context")
    if not isinstance(standing_record["consent"], bool) or not isinstance(standing_record["scope"], bool):
        raise ValidationError(f"{case_id}: consent and scope must be booleans")

    consequence = case["consequence"]
    if not isinstance(consequence, dict):
        raise ValidationError(f"{case_id}: consequence must be an object")
    require_keys(
        consequence,
        ("irreversibility", "harm", "uncertainty", "recoverability", "recovery_paths"),
        f"{case_id}.consequence",
    )
    irreversibility = score(consequence["irreversibility"], f"{case_id}.consequence.irreversibility")
    harm = score(consequence["harm"], f"{case_id}.consequence.harm")
    uncertainty = score(consequence["uncertainty"], f"{case_id}.consequence.uncertainty")
    recoverability = score(consequence["recoverability"], f"{case_id}.consequence.recoverability")
    paths = consequence["recovery_paths"]
    if not isinstance(paths, list) or any(path not in RECOVERY_PATHS for path in paths):
        raise ValidationError(f"{case_id}: recovery_paths contains an unsupported value")

    coefficients = case["threshold_coefficients"]
    if not isinstance(coefficients, dict):
        raise ValidationError(f"{case_id}: threshold_coefficients must be an object")
    require_keys(
        coefficients,
        ("base", "irreversibility", "harm", "uncertainty", "unrecoverability"),
        f"{case_id}.threshold_coefficients",
    )
    base = score(coefficients["base"], f"{case_id}.threshold_coefficients.base")
    alpha = score(coefficients["irreversibility"], f"{case_id}.threshold_coefficients.irreversibility")
    beta = score(coefficients["harm"], f"{case_id}.threshold_coefficients.harm")
    gamma = score(coefficients["uncertainty"], f"{case_id}.threshold_coefficients.uncertainty")
    delta = score(coefficients["unrecoverability"], f"{case_id}.threshold_coefficients.unrecoverability")

    threshold = clamp(
        base
        + alpha * irreversibility
        + beta * harm
        + gamma * uncertainty
        + delta * (1.0 - recoverability)
    )
    standing = (
        0.25 * evidence_sufficiency
        + 0.20 * freshness
        + 0.20 * authority
        + 0.15 * policy
        + 0.20 * context
    )

    hard_failures: list[str] = []
    if authority <= EPSILON:
        hard_failures.append("authority_invalid")
    if policy <= EPSILON:
        hard_failures.append("policy_invalid")
    if not standing_record["consent"]:
        hard_failures.append("consent_absent")
    if not standing_record["scope"]:
        hard_failures.append("scope_exceeded")

    high_consequence = max(irreversibility, harm) >= 0.75 or recoverability <= 0.25
    review_required = case["independent_review_required"]
    if not isinstance(review_required, bool):
        raise ValidationError(f"{case_id}: independent_review_required must be boolean")

    if hard_failures:
        disposition = "DENY"
    elif stale_material:
        disposition = "DEFER"
    elif review_required or (standing + EPSILON < threshold and high_consequence):
        disposition = "ESCALATE"
    elif standing + EPSILON < threshold:
        disposition = "DENY"
    else:
        disposition = "ALLOW"

    return Evaluation(
        case_id=case_id,
        freshness=freshness,
        evidence_sufficiency=evidence_sufficiency,
        threshold=threshold,
        standing=standing,
        stale_material_evidence=tuple(stale_material),
        hard_failures=tuple(hard_failures),
        calculated_disposition=disposition,
    )


def validate_document(document: dict[str, Any]) -> list[Evaluation]:
    if not isinstance(document, dict):
        raise ValidationError("root must be an object")
    require_keys(document, ("schema_version", "cases"), "root")
    if document["schema_version"] != "1.0.0":
        raise ValidationError("unsupported schema_version")
    if not isinstance(document["cases"], list) or not document["cases"]:
        raise ValidationError("cases must be a non-empty list")

    evaluations: list[Evaluation] = []
    seen: set[str] = set()
    for case in document["cases"]:
        evaluation = evaluate_case(case)
        if evaluation.case_id in seen:
            raise ValidationError(f"duplicate case id: {evaluation.case_id}")
        seen.add(evaluation.case_id)
        expected = case["expected_disposition"]
        if evaluation.calculated_disposition != expected:
            raise ValidationError(
                f"{evaluation.case_id}: expected {expected}, calculated {evaluation.calculated_disposition}"
            )
        evaluations.append(evaluation)
    return evaluations


def load_document(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default="static/examples/inference-window-governance.worked-cases.json",
        type=Path,
    )
    args = parser.parse_args(argv)

    try:
        evaluations = validate_document(load_document(args.path))
    except ValidationError as exc:
        print(f"INFERENCE WINDOW GOVERNANCE: FAIL - {exc}", file=sys.stderr)
        return 1

    for item in evaluations:
        print(
            f"{item.case_id}: {item.calculated_disposition} "
            f"standing={item.standing:.4f} threshold={item.threshold:.4f} "
            f"freshness={item.freshness:.4f}"
        )
    print(f"INFERENCE WINDOW GOVERNANCE: PASS - {len(evaluations)} cases validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
