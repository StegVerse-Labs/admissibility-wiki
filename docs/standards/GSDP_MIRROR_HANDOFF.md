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
State: CANONICAL_VALIDATION_BOUND_WORKFLOW_OBSERVATION_PENDING
Authority posture: public draft standard and self-description only
Certification authority: false
External adoption: not established
Independent conformance: not run
Registry authority: not established
Execution authority: false
Canonical validation binding: installed
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
scripts/check_admissibility_automation_handoff.py
```

## Canonical binding

```text
Validator: scripts/check_gsdp_reference.py
Canonical aggregate: scripts/check_admissibility_automation_handoff.py
Repository entrypoint: npm run validate
Canonical workflow: .github/workflows/validate-chain-continuation.yml
Binding commit: 7db29a1e154f7b6e5f318a3d79bd968996a5d28e
Binding state: INSTALLED
Observed execution state: NOT_OBSERVED
```

The GSDP validator is now executed by the admissibility automation aggregate already called by `npm run validate`. This establishes repository-level canonical binding. It does not establish that the workflow has run successfully, that the reference declaration conforms externally, or that any conformance class may be claimed.

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
- observe canonical workflow execution
- retain first PASS or first-failure evidence without rewriting history
- update the GSDP status receipt only from canonical workflow evidence
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

## 2026-08-26 validator-state reconciliation

Hosted canonical validation exposed a stale checker constant: the status and this handoff already record `CANONICAL_VALIDATION_BOUND_WORKFLOW_OBSERVATION_PENDING`, while the checker still required the predecessor `LOCAL_REFERENCE_VALIDATION_INSTALLED_WORKFLOW_OBSERVATION_PENDING` state.

Commit `09f5d280b15998d1cd0c6d65256b21b325d02a49` aligns the checker to the current canonical-bound state. No workflow PASS, external conformance, certification, registry authority, or execution authority is inferred; workflow observation remains pending.

## Completion boundary

The initial activation goal is complete only when the normative draft, schema, reference declaration, validator, status receipt, negative fixtures, canonical validation binding, and observed canonical execution are installed without converting self-validation into external conformance.

## Archive posture

This handoff preserves the complete continuation state. The complete thread may be archived without retaining additional chat context.

## Execution ownership and collision partition

Standard: `StegVerse-Labs/Continuity/docs/REPOSITORY_HANDOFF_STANDARD.md` / `stegverse.handoff-execution-ownership/v1`.

### MANUAL / SESSION-STARTABLE

```yaml
- task_id: ADMISSIBILITY-GSDP-HANDOFF-ADOPTION-115
  execution_owner: repo-standards #37 integration lane + admissibility-wiki repository owner
  claim_state: CLAIMED_FOR_INTEGRATION
  worker_registry_ref: StegVerse-Labs/repo-standards#37 + StegVerse-Labs/admissibility-wiki#115
  manual_execution_allowed: true
  manual_allowed_role: integration
  collision_scope: execution-ownership metadata in this GSDP handoff only; excludes GSDP implementation, validator/status mutation, canonical workflow observation, Site/Publisher/Guardian propagation, credentials, claims/fences/leases, and authority-bearing work
  release_condition: this textual migration is merged and issue #115 is reconciled
  next_executable_action: merge ownership metadata only while preserving current GSDP worker/authority boundaries
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: GSDP-REMAINING-WORK-AGGREGATE
  execution_owner: current repository-native GSDP/canonical-validation owner recorded by issue #50, orchestration state, scoped task registries, and newest applicable handoff
  claim_state: MACHINE_OWNED
  worker_registry_ref: issue #50 + data/admissibility-wiki-orchestration-state.json + scripts/check_admissibility_automation_handoff.py + current scoped GSDP records
  manual_execution_allowed: false
  manual_allowed_role: observation
  collision_scope: canonical workflow observation, GSDP status-receipt mutation, reference-declaration expansion, conformance-class semantic checks, external declaration intake, and repository-native validation execution
  release_condition: newest valid task/registry/claim/handoff explicitly releases or supersedes the exact scope
  next_executable_action: preserve machine-owned continuation and observe canonical evidence without competing
```

### ESCALATED / AUTHORITY-OWNED

```yaml
- task_id: GSDP-AUTHORITY-BOUNDARY
  execution_owner: applicable Site/Publisher/certification/registry/admissibility authority -> ecosystem governance
  claim_state: ESCALATED
  worker_registry_ref: this handoff + destination handoffs + repository authority records
  manual_execution_allowed: false
  manual_allowed_role: reconciliation
  collision_scope: external conformance, certification, registry authority, public Site route activation, Publisher publication authority, admissibility determination, release, custody, execution, Guardian enforcement, credentials, or cross-repository mutation authority
  release_condition: explicit canonical authority grant for the exact bounded scope
  next_executable_action: fail closed; schema validity, self-declaration, canonical binding, publication, or migration metadata are not external authority
```

### COMPLETED / SUPERSEDED

- The normative draft/schema/reference/validator/binding artifacts already installed remain historical implementation evidence and are not reopened by this migration.
- Any prior implication that `pending`, `not observed`, or remaining GSDP work is manually startable is superseded by the machine-owned aggregate above.
- Any inference that GSDP schema validation or publication establishes external conformance, certification, registry, admissibility, or execution authority is superseded/prohibited.
