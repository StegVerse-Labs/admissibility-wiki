# Governed System Description Protocol Mirror Handoff

## Source of truth

This file is the active goal-specific handoff for the Governed System Description Protocol (`GSDP`) work in `StegVerse-Labs/admissibility-wiki`.

The repository-wide source of truth remains:

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
```

## Goal

Define a public, machine-readable standard by which governed AI systems describe their identity, composition, operators, capabilities, authority, non-authority, policies, admissibility rules, evidence, status, dependencies, historical versions, and reconstruction surfaces.

StegVerse is the first bounded reference implementation, not proof that the standard is complete, independently adopted, certified, or externally recognized.

## Current state

```text
Goal id: gsdp-public-governed-system-description-standard
State: FIRST_CANONICAL_FAILURE_RETAINED_REPAIR_VALIDATION_PENDING
Authority posture: public draft standard and self-description only
Certification authority: false
External adoption: not established
Independent conformance: not run
Registry authority: not established
Execution authority: false
Canonical validation binding: installed
Canonical workflow observation: FAIL_CLOSED_OBSERVED
First observed run: 30568611934 / run 3630
First GSDP result: FAIL — GSDP_STATUS_CONTRACT_DRIFT
```

## Constitutional rules

```text
capability != authority
identity != standing
publication != truth
machine-readable != correct
schema-valid != substantively valid
self-declaration != independent verification
current declaration != historical state at time T
component ownership != system-wide authority
operator control != certification authority
conformance claim != conformance proof
discoverability != interoperability
interoperability != execution authority
failed observation != erased history
repaired validation != retroactive PASS
```

## Installed initial artifacts

```text
docs/standards/governed-system-description-protocol.md
static/schemas/gsdp/governed-system-description.schema.json
static/data/standards/gsdp/examples/stegverse.pending.v0.1.json
scripts/check_gsdp_reference.py
static/status/gsdp-reference-status.json
static/data/standards/gsdp/fixtures/authority-non-inheritance.invalid.v0.1.json
static/data/standards/gsdp/fixtures/historical-supersession.valid.v0.1.json
static/data/standards/gsdp/fixtures/schema-minimum.invalid.v0.1.json
scripts/check_admissibility_automation_handoff.py
static/data/standards/gsdp/observations/canonical-workflow-observation.30568611934.v0.1.json
```

## Canonical binding and first observation

```text
Validator: scripts/check_gsdp_reference.py
Canonical aggregate: scripts/check_admissibility_automation_handoff.py
Repository entrypoint: npm run validate
Canonical workflow: .github/workflows/validate-chain-continuation.yml
Binding commit: 7db29a1e154f7b6e5f318a3d79bd968996a5d28e
Binding state: INSTALLED
First observed workflow run: 30568611934
First observed workflow conclusion: failure
Canonical pre-scan: PASS (11/11)
Full validation chain: FAIL (49 passed, 6 failed, 1 skipped)
GSDP-specific failure: validator expected a superseded pre-binding status value
Failure classification: GSDP_STATUS_CONTRACT_DRIFT
Failure history: RETAINED, NOT REWRITTEN
Authority effect: NONE
```

The first canonical run is preserved as fail-closed evidence. The GSDP defect was a status-contract mismatch introduced when the status receipt advanced after canonical binding while the validator retained its prior literal state requirement. The repair allows explicitly governed lifecycle states and binds the first observation receipt. A successor run may demonstrate the repair, but it must not replace or rewrite the first failure.

Other aggregate failures observed in run 30568611934 remain owned by their respective goals and are not classified as GSDP defects.

## Validator coverage

```text
required declaration-layer presence
GSDP draft-version binding
unique operator and component identifiers
operator-to-component reference resolution
component-to-operator reference resolution
component-to-dependency reference resolution
positive-authority / explicit-non-authority contradiction rejection
prohibited authority assertion rejection
pending-reference conformance non-claim preservation
canonical optional declaration-hash syntax
explicit independent/certification/execution/external-adoption non-claims
authority non-inheritance negative fixture
historical supersession continuity fixture
minimum declaration rejection fixture
bounded status-receipt validation
first canonical observation receipt validation
lifecycle-state transition validation
```

The validator proves only deterministic local structure and boundary behavior. It does not establish external adoption, independent conformance, certification, operational readiness, or execution authority.

## Minimum declaration layers

```text
identity
composition
operators
capabilities
authority and explicit non-authority
governance and admissibility
evidence and reconstruction
status and maturity
dependencies and external authorities
historical continuity and supersession
claims and explicit non-claims
```

## First conformance classes

```text
GSDP-DISCOVERABLE
GSDP-GOVERNED
GSDP-EVIDENCED
GSDP-RECONSTRUCTABLE
GSDP-INTEROPERABLE
GSDP-CERTIFIABLE
```

Each higher class is additive. No class may be claimed solely from schema validation.

## Public discovery target

```text
/.well-known/governed-system.json
```

Publication to `StegVerse-Labs/Site` requires the current `docs/SITE_MIRROR_HANDOFF.md` authority and orchestration sequence. This repository may define the standard and fixtures, but it does not independently activate the Site route.

## Remaining work and destinations

```text
StegVerse-Labs/admissibility-wiki:
- observe the repaired GSDP validator in a successor canonical workflow run
- retain the successor result separately from the first failure
- close initial reference activation when GSDP validation is observed executing under the canonical workflow
- expand the StegVerse reference declaration only from verified component records
- add complete conformance-class semantic checks
- add external declaration examples after accountable source receipt

StegVerse-Labs/Site:
- public .well-known route after Site handoff admission
- human-readable standard page
- current StegVerse declaration projection

GCAT-BCAT-Engine/Publisher:
- versioned publication package and publication receipt after Publisher handoff admission

StegVerse-002/stegguardian-wiki:
- challenge, correction, appeal, conflict, and reviewer-standing projection
```

## Completion boundary

The initial activation goal is complete when the normative draft, schema, reference declaration, validator, status receipt, negative fixtures, canonical validation binding, and canonical execution observation are installed without converting self-validation into external conformance. The retained first failure satisfies the observation requirement historically; the current repair must still be observed so the active GSDP validator is shown executing rather than merely installed.

## Archive posture

This handoff preserves the complete continuation state. The complete thread may be archived without retaining additional chat context.
