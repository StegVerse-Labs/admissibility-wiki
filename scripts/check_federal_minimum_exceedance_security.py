#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "static" / "security" / "federal-minimum-exceedance-security-profile.json"
BASELINE = ROOT / "docs" / "security" / "federal-minimum-exceedance-security-baseline.md"
HANDOFF = ROOT / "docs" / "security" / "FEDERAL_MINIMUM_EXCEEDANCE_SECURITY_MIRROR_HANDOFF.md"

REQUIRED_FLOOR = {
    "NIST SP 800-53 Rev. 5",
    "NIST SP 800-53B",
    "NIST SP 800-218 SSDF",
    "FIPS 140-3",
    "FedRAMP Rev. 5",
}
REQUIRED_CONTROLS = {
    "authority_separation",
    "deny_by_default",
    "missing_evidence_fails_closed",
    "run_bound_identity",
    "sha256_input_output_binding",
    "deterministic_negative_path_tests",
    "single_canonical_workflow",
    "duplicate_execution_prevention",
    "expiring_or_release_conditioned_claims",
    "supply_chain_provenance",
    "cryptographic_agility",
    "post_quantum_migration_readiness",
    "operator_authority_degradation_testing",
    "recovery_and_reconstructability",
    "privacy_minimization_and_purpose_limitation",
    "continuous_repository_owned_observation",
    "security_downgrade_requires_governed_exception",
}
REQUIRED_STATES = {
    "COMPLETE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED",
    "CLAIMED", "SUPERSEDED", "MERGED", "FAIL_CLOSED",
}
FALSE_CLAIMS = {
    "fedramp_authorized",
    "fisma_authorized",
    "fips_validated",
    "federal_compliance_certified",
    "agency_approved",
    "penetration_resistance_verified",
    "runtime_activation_verified",
}
FALSE_INFERENCES = {
    "verification_implies_execution",
    "publication_implies_admissibility",
    "deployment_implies_release_authority",
    "federal_floor_implies_certification",
    "post_quantum_readiness_implies_validation",
    "missing_evidence_implies_success",
}


def main() -> int:
    failures: list[str] = []
    for path in (PROFILE, BASELINE, HANDOFF):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return report(failures)

    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    except Exception as exc:
        return report([f"profile unreadable: {exc}"])

    if profile.get("schema_version") != "stegverse.federal_minimum_exceedance_security_profile.v1":
        failures.append("schema_version mismatch")
    if profile.get("profile_id") != "SECURITY-FEDERAL-MINIMUM-EXCEEDANCE-001":
        failures.append("profile_id mismatch")
    if profile.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if profile.get("policy") != "FEDERAL_REQUIREMENTS_ARE_MINIMUM_STEGVERSE_MUST_EXCEED":
        failures.append("policy must preserve federal-floor exceedance requirement")

    floor_entries = profile.get("federal_floor", [])
    floor_refs = {item.get("reference") for item in floor_entries if isinstance(item, dict)}
    if floor_refs != REQUIRED_FLOOR:
        failures.append(f"federal floor mismatch: {sorted(floor_refs)}")
    for item in floor_entries:
        if not isinstance(item, dict):
            failures.append("federal floor entry must be an object")
            continue
        if item.get("reference") in {"NIST SP 800-53 Rev. 5", "NIST SP 800-53B", "NIST SP 800-218 SSDF"}:
            if item.get("required_as_floor") is not True:
                failures.append(f"{item.get('reference')} must be required as floor")
        if item.get("reference") == "FIPS 140-3":
            if item.get("required_when_applicable") is not True or item.get("validation_claimed") is not False:
                failures.append("FIPS 140-3 applicability or claim boundary invalid")
        if item.get("reference") == "FedRAMP Rev. 5":
            if item.get("required_when_applicable") is not True or item.get("authorization_claimed") is not False:
                failures.append("FedRAMP applicability or claim boundary invalid")
        if item.get("certification_claimed") is True:
            failures.append(f"unsupported certification claim for {item.get('reference')}")

    controls = profile.get("exceedance_controls", {})
    if set(controls) != REQUIRED_CONTROLS:
        failures.append("exceedance control set mismatch")
    for control in REQUIRED_CONTROLS:
        if controls.get(control) is not True:
            failures.append(f"exceedance control must remain true: {control}")

    if set(profile.get("required_states", [])) != REQUIRED_STATES:
        failures.append("required state set mismatch")

    inferences = profile.get("prohibited_inferences", {})
    if set(inferences) != FALSE_INFERENCES:
        failures.append("prohibited inference set mismatch")
    for field in FALSE_INFERENCES:
        if inferences.get(field) is not False:
            failures.append(f"prohibited inference must remain false: {field}")

    claims = profile.get("claims", {})
    if set(claims) != FALSE_CLAIMS:
        failures.append("claim set mismatch")
    for field in FALSE_CLAIMS:
        if claims.get(field) is not False:
            failures.append(f"unsupported security claim must remain false: {field}")

    owner = profile.get("owner", {})
    if owner.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("owner repository mismatch")
    if owner.get("workflow") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("canonical workflow binding mismatch")
    if owner.get("validator") != "scripts/check_federal_minimum_exceedance_security.py":
        failures.append("validator self-binding mismatch")

    if profile.get("manual_user_action_required") is not False:
        failures.append("manual user action must remain false")
    if profile.get("cross_repository_mutation_authority_granted") is not False:
        failures.append("cross-repository mutation authority must remain false")
    if profile.get("release_authority_granted") is not False:
        failures.append("release authority must remain false")

    baseline = BASELINE.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    markers = (
        "Federal security requirements are the minimum acceptable floor",
        "Security downgrade prevention",
        "Missing, malformed, stale, inconsistent, unverifiable, or inaccessible evidence",
        "This document is a control policy and engineering baseline. It is not a claim",
    )
    for marker in markers:
        if marker not in baseline:
            failures.append(f"baseline missing marker: {marker}")
    for marker in (
        "SECURITY-FEDERAL-MINIMUM-EXCEEDANCE-001",
        "MACHINE_OWNED",
        "do not create a second active workflow",
        "MERGED INTO: StegVerse-Labs/admissibility-wiki/docs/security/FEDERAL_MINIMUM_EXCEEDANCE_SECURITY_MIRROR_HANDOFF.md",
    ):
        if marker not in handoff:
            failures.append(f"handoff missing marker: {marker}")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("FEDERAL MINIMUM EXCEEDANCE SECURITY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("FEDERAL MINIMUM EXCEEDANCE SECURITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
