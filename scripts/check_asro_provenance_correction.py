#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVATIVE = ROOT / "static/data/framework-evaluations/asro/stegverse-generated-bounded-metadata-derivative.json"
ALIAS = ROOT / "static/data/framework-evaluations/asro/asro-author-provided-bounded-representative-object.json"
DOC = ROOT / "docs/external-frameworks/asro-provenance-correction-2026-07-26.md"


def load(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    try:
        derivative = load(DERIVATIVE)
        alias = load(ALIAS)
        if not DOC.exists():
            errors.append(f"missing:{DOC.relative_to(ROOT)}")

        expected_derivative = {
            "artifact_type": "stegverse_generated_bounded_metadata_derivative",
            "creator": "StegVerse Labs",
            "classification": "STEGVERSE_GENERATED_BOUNDED_DERIVATIVE",
            "canonical_status": "NON_CANONICAL",
            "released_asro_native_schema": False,
            "derivation_status": "TRANSFORMED_OR_REDUCED",
        }
        for key, value in expected_derivative.items():
            if derivative.get(key) != value:
                errors.append(f"derivative:{key}")

        source = derivative.get("source_example", {})
        if source.get("publicly_reproduced") is not False:
            errors.append("derivative:source_publicly_reproduced")
        if source.get("content_hash_recorded") is not False:
            errors.append("derivative:source_content_hash_recorded")
        if not str(source.get("source_linkage_status", "")).startswith("UNRESOLVED"):
            errors.append("derivative:source_linkage_status")

        if alias.get("status") != "DEPRECATED_MISCLASSIFIED_PUBLIC_ALIAS":
            errors.append("alias:status")
        if alias.get("replacement") != str(DERIVATIVE.relative_to(ROOT)):
            errors.append("alias:replacement")
        if alias.get("history_preservation", {}).get("prior_public_history_rewritten") is not False:
            errors.append("alias:history_rewrite")

        for field in ("asro_release", "jointly_issued", "certification", "endorsement", "admissibility", "execution"):
            if alias.get("authority_boundary", {}).get(field) is not False:
                errors.append(f"alias:authority:{field}")

        if DOC.exists():
            text = DOC.read_text(encoding="utf-8")
            for marker in (
                "Existing public packet: UNILATERAL_STEGVERSE_ANALYSIS",
                "Bilateral Seam Comparison Record: NOT_ISSUED",
                "External ASRO-native execution: NOT_TESTED",
                "Accountable reviewer or issuer: unresolved",
            ):
                if marker not in text:
                    errors.append(f"doc:{marker}")
    except (AssertionError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    if errors:
        print("ASRO PROVENANCE CORRECTION: FAIL - " + ", ".join(errors))
        return 1
    print("ASRO PROVENANCE CORRECTION: PASS")
    print("Source contribution and StegVerse-generated derivative remain separately classified; reciprocal execution remains deferred and non-authorizing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
