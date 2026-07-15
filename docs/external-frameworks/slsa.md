---
title: SLSA
---
# SLSA

## Status

```text
Relationship type: external framework crosswalk
Evidence class: SOURCE_REVIEWED
Page completeness: COMPLETE_WITH_EXTERNAL_GATES
Runtime observation: none attached
Independent reproduction: false
Comparative testing claim allowed: false
Execution authority claim allowed: false
Maintenance owner: admissibility-wiki External Frameworks audit
```

## Official Source

- Specification: https://slsa.dev/spec/v1.2/
- Source posture: SLSA v1.2 captured; no pinned build system, provenance bundle, or verifier run is attached.

## Framework-Native Scope

SLSA defines software supply-chain security tracks, provenance expectations, build requirements, and assurance levels. It provides a vocabulary for describing how artifacts were produced and what controls or evidence support trust in that production process.

## Evidence Provenance

| Evidence class | Current evidence | Status | Missing fields |
|---|---|---|---|
| Official framework source | SLSA v1.2 specification | present | immutable snapshot hash |
| Implementation source | No selected implementation attached | missing | builder, verifier, release, commit |
| Observed behavior | No provenance verification run | missing | provenance bundle, verifier output, timestamp |
| Reproduced behavior | No independent rerun | missing | replay command, runtime, independent result |
| StegVerse analysis | Bounded crosswalk | present | common test fixture |

## Relationship to Admissibility

```text
SLSA asks: What supply-chain guarantees and provenance support confidence in how an artifact was produced?
StegVerse Admissibility asks: May this actor perform this action against this target now and bind consequence?
```

SLSA evidence may strengthen source, build, and artifact standing. It does not determine current delegation, action-level authority, runtime policy, or commit-time validity.

## Execution Authority Boundary

```text
SLSA level != runtime permission
provenance verification != current standing
trusted builder != authorized deployer
artifact assurance != execution authority
```

## Observation Boundary

```text
Selected builder: none
Pinned verifier: none
Provenance bundle: none
Raw verification output: none
Runtime configuration: none
Independent reproduction: none
```

No benchmark or implementation result is claimed.

## StegVerse Analysis

| Criterion | Current result |
|---|---|
| Identity | Builder and producer identity may be evidenced, but the current actor is separate. |
| Authority | Build authority does not become deployment or execution authority. |
| Policy | SLSA requirements may inform policy evidence but do not replace live policy evaluation. |
| Delegation | Builder delegation and runtime delegation are distinct. |
| Evidence | Provenance can strengthen reconstructability when signed, complete, and retained. |
| Replayability | Requires pinned builder/verifier, provenance, inputs, commands, and environment. |
| Reconstructability | Strong only to the extent the provenance chain and referenced materials remain available. |
| Commit-time validity | Must be evaluated separately at the requested transition. |
| Failure behavior | Missing or unverifiable provenance must not be treated as a pass. |

## Commit-Time Interoperability Contract

```text
transition_id
artifact_digest
slsa_version
provenance_digest
builder_identity
build_type
source_repository
source_revision
verification_result
verification_timestamp
verifier_version
policy_reference
delegation_reference
target_action
execution_context
validity_window
```

## Failure Classes

| Failure class | Applies | Notes |
|---|---:|---|
| Semantic equivalence divergence | yes | Supply-chain assurance may be mistaken for runtime safety. |
| Authority drift | yes | A trusted build does not prove a current actor may deploy it. |
| Stale evidence | yes | Source, dependencies, builder state, and revocation posture may change. |
| Replay divergence | yes | Unpinned tooling can produce different verification outcomes. |
| Recoverability loss | yes | Missing provenance or source material prevents reconstruction. |
| Source-claim mismatch | yes | Claimed SLSA posture may exceed the evidence actually attached. |

## Machine-Readable Companions

- Manifest: `docs/external-frameworks/slsa.json`
- Compatibility report: `docs/external-frameworks/reports/slsa.compatibility.json`
- Registry: `docs/external-frameworks/index.json`
- Canonical inventory: `static/external-frameworks/canonical-union-inventory.v1.json`

## Validation Completion Criteria

```text
select and pin one SLSA-compatible provenance producer and verifier
publish provenance and artifact digests
capture raw verifier output and timestamp
publish expected outcome and replay commands
complete an independent rerun
route the bounded result into a Commitment Candidate fixture
```

## Non-Claims

SLSA is not a StegVerse canonical formalism. Build assurance is not runtime admissibility, current delegation, execution authority, certification, or a general compatibility result.

## Challenge Path

A challenge must identify the specification version, claimed level or track, evidence field, supporting artifact, and requested correction. A challenge changes standing only after the evidence record is updated and re-evaluated.

## Next Safe Build Target

Publish one pinned provenance-verification fixture with raw output, immutable hashes, replay instructions, and an independent rerun.

This page reflects a bounded admissibility packet. Publication does not create standing.