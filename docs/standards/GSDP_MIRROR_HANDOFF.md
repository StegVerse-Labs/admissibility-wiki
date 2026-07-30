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
State: LOCAL_REFERENCE_VALIDATOR_AND_BOUNDARY_FIXTURES_INSTALLED_CANONICAL_BINDING_PENDING
Authority posture: public draft standard and self-description only
Certification authority: false
External adoption: not established
Independent conformance: not run
Registry authority: not established
Execution authority: false
Canonical workflow observation: not observed
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
```

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
- bind scripts/check_gsdp_reference.py into canonical repository validation
- observe canonical workflow execution
- retain first PASS or first-failure evidence without rewriting history
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

The initial activation goal is complete only when the normative draft, schema, reference declaration, validator, status receipt, negative fixtures, canonical validation binding, and observed canonical execution are installed without converting self-validation into external conformance.

## Archive posture

This handoff preserves the complete continuation state. The complete thread may be archived without retaining additional chat context.
