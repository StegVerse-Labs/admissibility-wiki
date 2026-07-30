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
Initial reference activation: COMPLETE
Current phase: VERIFIED_ECOSYSTEM_INVENTORY_AND_SEMANTIC_CONFORMANCE
Current phase state: PARTIAL_PROVENANCE_BOUND_INVENTORY_INSTALLED_CANONICAL_OBSERVATION_PENDING
Authority posture: public draft standard and self-description only
Certification authority: false
External adoption: not established
Independent conformance: not run
Registry authority: not established
Execution authority: false
Claimed conformance classes: none
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
component inventory entry != verified component truth
source-record presence != operational deployment
inventory completeness != conformance
```

## Initial activation evidence

```text
Run 30568611934 / workflow run 3630
- workflow conclusion: failure
- GSDP result: FAIL
- classification: GSDP_STATUS_CONTRACT_DRIFT
- history: retained, not rewritten

Run 30569337389 / workflow run 3634
- workflow conclusion: failure
- GSDP result: PASS
- repair verified: true
- aggregate failure owned by GSDP: false
- history: retained separately from first failure
```

The repaired reference validator executed successfully inside the canonical workflow. Initial GSDP reference activation is complete only at the bounded standard-reference layer. No repository-wide PASS, release, deployment, certification, conformance, registry, publication, or execution authority is inferred.

## Installed initial reference artifacts

```text
docs/standards/governed-system-description-protocol.md
static/schemas/gsdp/governed-system-description.schema.json
static/data/standards/gsdp/examples/stegverse.pending.v0.1.json
scripts/check_gsdp_reference.py
static/status/gsdp-reference-status.json
static/data/standards/gsdp/fixtures/authority-non-inheritance.invalid.v0.1.json
static/data/standards/gsdp/fixtures/historical-supersession.valid.v0.1.json
static/data/standards/gsdp/fixtures/schema-minimum.invalid.v0.1.json
static/data/standards/gsdp/observations/canonical-workflow-observation.30568611934.v0.1.json
static/data/standards/gsdp/observations/canonical-workflow-observation.30569337389.v0.1.json
```

## Installed inventory-phase artifacts

```text
static/data/standards/gsdp/inventory/stegverse-ecosystem.inventory.pending.v0.1.json
scripts/check_gsdp_inventory.py
static/status/gsdp-inventory-status.json
scripts/check_admissibility_automation_handoff.py
```

The inventory seed is derived only from the current governed ecosystem index and its status record. It contains:

```text
organizations recorded: 6
source-bound components recorded: 11
unresolved coordinates recorded: 2
deprecated components recorded: 0
inventory completeness: PARTIAL
semantic conformance evaluation: NOT_RUN
claimed conformance classes: none
```

A component marked `record_status=verified` means that the coordinate is explicitly named by the cited repository source. It does not mean the component is deployed, operational, admissible, independently verified, certified, or authorized to execute.

## Inventory validation coverage

```text
source index and status presence
bounded inventory lifecycle state
allowed verified/pending/deprecated/unresolved vocabulary
unique organization and component identifiers
organization-reference resolution
mandatory provenance and last-verified fields
explicit authority-inference prohibition
partial-inventory preservation
zero conformance-class claims
semantic evaluation NOT_RUN preservation
bounded inventory status receipt
```

The inventory validator is bound into `scripts/check_admissibility_automation_handoff.py`, which is already called by the canonical repository validation chain.

## Public discovery target

```text
/.well-known/governed-system.json
```

Publication to `StegVerse-Labs/Site` requires the current `docs/SITE_MIRROR_HANDOFF.md` authority and orchestration sequence. This repository may define the standard, inventory, fixtures, and conformance logic, but it does not independently activate the Site route.

## Current phase remaining work

```text
StegVerse-Labs/admissibility-wiki:
- observe the inventory validator in the canonical workflow
- retain the first inventory PASS or first failure without rewriting history
- expand inventory only from verified repository records
- resolve RTG/STCM canonical repository coordinates
- resolve the external-executor coordinate or preserve it unresolved
- identify deprecated and superseded components from accountable records
- implement additive GSDP-DISCOVERABLE through GSDP-CERTIFIABLE predicates
- retain zero claimed conformance classes until each predicate is satisfied
- add contradiction, stale-record, unresolved-reference, and authority-inheritance fixtures
- add external declarations only after accountable source receipt

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

The inventory and semantic-conformance phase is complete only when the ecosystem inventory is provenance-bound, stale and unresolved records are governed, additive conformance predicates are implemented, canonical execution is observed, and any claimed class is supported by its complete predicate set. Schema validity or inventory presence alone can never establish conformance.

The broader GSDP standard is not complete until public discovery publication, independent assessment support, correction governance, versioned publication, and external implementation evidence exist.

## Archive posture

This handoff preserves the complete continuation state. The complete thread may be archived without retaining additional chat context.
