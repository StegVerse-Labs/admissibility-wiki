---
title: Governance-Chain Certification
sidebar_label: Governance-Chain Certification
---

# Governance-Chain Certification

## Canonical status

```text
status: CANONICAL_FORMAL_STANDARD
canonical_branch: main
origin_pull_request: 101
merge_commit: 956a787a1fd858efe30d0b909fd5cf2400151988
certification_authority_activated: false
public_certification_program_activated: false
```

StegVerse Governance-Chain Certification defines a property-scoped certification system for governance mechanisms and governance-adjacent mechanisms that materially participate in a consequential transition.

The certification target may sit immediately before governance, within governance, immediately after governance, or at a governed interlock between independently authoritative systems.

## Core proposition

StegVerse certification is evidence of demonstrated properties at a defined boundary under a defined test profile. It is not a generic endorsement.

```text
certification = demonstrated_property
              + defined_boundary
              + frozen_subject_version
              + declared_test_profile
              + retained_evidence
              + negative_controls
              + validity_window
```

A certification claim MUST NOT exceed what retained evidence establishes.

## Certification surfaces

### PRE — pre-governance

Examples include identity binding, intent capture, candidate construction, input normalization, policy resolution, evidence collection, provenance binding, state observation, and authority-source resolution.

A PRE certification asks whether governance-relevant inputs arrive with the claimed identity, provenance, freshness, completeness, and semantic boundaries intact.

### GOV — governance

Examples include admissibility, authority, policy applicability, evidence sufficiency, fail-closed behavior, commit-time decision binding, obligation handling, and review/hold behavior.

A GOV certification asks whether claimed governance properties are established before consequence attaches and whether negative and unresolved cases remain bounded.

### POST — post-governance

Examples include commit integrity, consequence execution, idempotency, receipt generation, custody, replay, reconstruction, rollback/recovery, proof publication, and continuity recording.

A POST certification asks whether the admitted transition is the transition that commits, whether evidence survives the consequence boundary, and whether later verification can reconstruct what occurred without silently re-executing it.

### INT — governed interlock

INT applies where two independently authoritative systems exchange governed evidence, requests, receipts, state assertions, or consequence candidates.

```text
system_A_authority != system_B_authority
interop != authority_transfer
successful_translation != execution_permission
receipt_exchange != shared_governance_authority
```

An interlock may be certified for bounded translation, evidence preservation, authority separation, fail-closed routing, replay/reconstruction correspondence, or continuing conformance.

## Property registry

The initial property families are:

```text
AUTHORITY_CURRENT
ADMISSIBILITY_COMMIT_BOUND
FAIL_CLOSED
EVIDENCE_PROVENANCE
STATE_CORRESPONDENCE
REPLAY_STABLE
RECONSTRUCTABLE
CONSEQUENCE_BOUND
IDEMPOTENT_TARGET
CUSTODY_DURABLE
INTERLOCK_AUTHORITY_SEPARATED
INTERLOCK_TRANSLATION_BOUNDED
CONTINUING_CONFORMANCE
```

Machine-readable definitions and minimum negative-control families are retained in `data/certification/property-registry.v0.1.json`.

## Minimum deterministic profiles

`data/certification/minimum-profiles.v0.1.json` defines minimum PRE/GOV/POST/INT profiles. Every profile requires explicit property coverage and negative controls. A positive path alone is insufficient.

Where a mechanism can materially allow or block consequence, relevant profiles exercise both successful and unsuccessful behavior, including `ALLOW`, `DENY`, `FAIL_CLOSED`, stale authority/evidence, policy/state drift, duplicate commit/replay, and boundary-translation failure where applicable.

## Evidence and lifecycle

Certification candidates, results, and evidence packets use machine-readable schemas under `schemas/`.

Evidence is version-bound and freshness-bounded. Lifecycle states include:

```text
CURRENT
EXPIRED
SUSPENDED
REVOKED
SUPERSEDED
```

Renewal requires re-evaluation. Prior evidence may be reused only when continued applicability is independently established. Missing or conflicting required evidence cannot become success.

## Public claims

Public certification language MUST state the exact component/version, certification surface, profile version, certified properties, evidence locator, and current lifecycle state.

Generic shorthand such as `StegVerse approved`, `safe`, `trusted`, or an unrestricted `governance certified` claim is not valid under this standard.

A badge is only a pointer to a machine-readable current certificate. It is not a substitute for evidence.

See `docs/certification/CERTIFICATION_OPERATIONAL_STANDARD.md`.

## Independence and commercial boundary

A party may pay for access to testing, evidence production, interlock connectivity, or bounded examination services. Payment MUST NOT purchase the disposition.

```text
fee -> access / testing / evidence / examination
fee != CERTIFIED
customer identity != decision input
commercial relationship != governance authority
```

A failed, limited, unresolved, expired, suspended, or revoked result remains valid even when the subject paid for access to the evaluation surface.

## SDK evidence adapter

The StegVerse SDK is the preferred evaluator-facing surface when the tested proposition is representable through published SDK capabilities. Submitted manifest hashes, governance decisions, route receipts, Master Records custody, replay, reconstruction, and result-binding hashes may become certification evidence.

An SDK `ALLOW` is not itself a certification. The selected profile, negative controls, evidence sufficiency, lifecycle requirements, and certificate validator must also pass.

## Fin-Co precedent

Fin-Co / Fin-Co-Lab provides an existing ecosystem precedent that implementation claims alone are insufficient, certification requires explicit suite/report evidence, and `ALLOW`, `DENY`, and `FAIL_CLOSED` behavior must be tested. Governance-Chain Certification generalizes those principles across PRE/GOV/POST/INT surfaces.

## First external process pilot

The first external process pilot applies the INT profile to the publicly documented ArquivoNulo protocol family.

```text
result: UNRESOLVED
certificate_issued: false
authority_effect: NONE
```

The pilot demonstrates that public architectural material can enter the certification process without being silently promoted to certification when live interlock traces, required negative controls, and request/return receipt evidence are absent.

Record: `data/certification/pilots/arquivonulo-int-pilot.v0.1.json`.

## Validation

Scoped validator:

```text
python scripts/check_governance_chain_certification.py
```

Retained scoped result:

```text
GOVERNANCE_CHAIN_CERTIFICATION: PASS
profiles=4
negative_fixtures=9
external_pilot=UNRESOLVED_NO_CERTIFICATE
authority_effect=NONE
```

See `validation/GOVERNANCE_CHAIN_CERTIFICATION_VALIDATION_2026-08-23.md` for validation class and limits.

## Non-claims

```text
certification != endorsement
certification != product quality guarantee
certification != legal approval
certification != permanent validity
certification != execution authority
certification != shared authority
certification != absence of undiscovered defects
passing one property != passing all properties
passing one version != passing later versions
payment != certification outcome
```

## Authority activation boundary

The formal standard is now canonical. That does **not** activate a public certification authority or certificate-issuance authority.

Activation is a separate future goal requiring an evidence-complete candidate, generation of a real machine-readable certificate, independent verification of that certificate and evidence packet, preservation of the negative-control/fail-closed guarantees, and an explicit activation decision.

Until that transition is completed:

```text
formal_standard: CANONICAL_COMPLETE
public_certification_authority: INACTIVE
certificate_issuance_authority: INACTIVE
```
