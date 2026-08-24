# External Certification Intake Mirror Handoff

## Scope

```text
goal_id: GOVERNANCE-CHAIN-EXTERNAL-INTAKE-001
repository: StegVerse-Labs/admissibility-wiki
branch: dev/external-certification-intake
role: DEVELOPMENT_LANE
state: ACTIVE_IMPLEMENTATION
public_certification_authority: INACTIVE
external_certificate_issuance_authority: INACTIVE
reference_issuance_authority: ACTIVE
credential_authority: TV/TVC
GitHub runtime authority: NONE
```

## Goal

Implement the evidence-intake gate required before any external governance or governance-adjacent system can enter the canonical certificate issuance path.

The intake gate must distinguish a candidate that is ready for testing from one that is merely documented, marketed, or partially inspectable.

## Required outputs

```text
1. external candidate intake contract
2. machine-readable submission schema
3. intake-state schema/result classes
4. fail-closed intake validator
5. ArquivoNulo intake record using currently observed evidence
6. explicit evidence-gap request packet for ArquivoNulo
7. scoped validation record
8. canonical merge
```

## Intake states

```text
READY_FOR_CERTIFICATION_TEST
READY_WITH_DECLARED_LIMITS
EVIDENCE_REQUESTED
SOURCE_ONLY_NOT_TESTABLE
INDETERMINATE
REJECTED_SCOPE
```

Intake readiness is not certification and does not grant execution, governance, custody, endorsement, or public-claim authority.

## Required evidence families

A candidate must identify, as applicable:

```text
immutable subject/version binding
claimed certification surface: PRE | GOV | POST | INT
claimed properties
test profile
executable or observable interface
positive fixture route
negative-control route
effect/commit observation point
request and return receipts
replay/reconstruction material
current authority/policy/environment inputs where claimed
retained evidence destination
known limits
```

## External candidate policy

A public specification alone may support `SOURCE_ONLY_NOT_TESTABLE` or `EVIDENCE_REQUESTED`, but it MUST NOT become `READY_FOR_CERTIFICATION_TEST` unless the required test and observation surfaces are actually available.

## Current first intake candidate

```text
candidate: ArquivoNulo public protocol family
proposed_surface: INT
current_state: EVIDENCE_REQUESTED
certificate_issued: false
authority_effect: NONE
```

The existing public-source pilot remains unresolved because live interlock traces, negative controls, and request/return receipt evidence are not currently available in the retained record.
