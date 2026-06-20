---
title: Governance-Centered and Boundary-Centered Admissibility Testing
---

# Governance-Centered and Boundary-Centered Admissibility Testing

## Status

```text
Canonical source organization: Admissible-Existence
Canonical source repository: Admissible-Existence/GCAT-BCAT
Wiki state: source_available
Publication family: GCAT-BCAT-Engine/Publisher/papers/GCAT-BCAT
Detail status: initial public-safe canonical detail page
```

## Definition

Governance-Centered and Boundary-Centered Admissibility Testing is a canonical formalism family for evaluating whether governance conditions and boundary conditions are satisfied before a transition, execution, publication, or consequence is treated as admissible.

## Source Boundary

```text
Admissible-Existence defines the formalism.
Publisher publishes papers and public exposition.
Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.
```

The wiki is not the source authority for this formalism.

## Scope

This formalism family applies where a system must distinguish between:

```text
visibility and governance
approval and execution
review artifact and commit-time authority
stored evidence and admissible consequence
boundary declaration and boundary satisfaction
```

## Purpose

The purpose of this formalism family is to support tests that ask whether a proposed or attempted transition has enough governance standing and boundary satisfaction to proceed, deny, escalate, defer, refuse, or fail closed.

## Core Constructs

| Construct | Role |
|---|---|
| Governance-centered admissibility testing | Tests whether policy, authority, review, and consequence-standing conditions are satisfied. |
| Boundary-centered admissibility testing | Tests whether the transition is inside the required boundary before consequence binds. |
| Authority class | Identifies the kind of standing being claimed by the actor or process. |
| Policy reference | Identifies the governing rule or policy basis. |
| Evidence posture | Identifies whether the supporting evidence is present, sufficient, stale, conflicting, or missing. |
| Review posture | Identifies whether review has occurred and what kind of review standing exists. |
| Commit-time validity | Identifies whether standing still exists when consequence would bind. |
| Receipt | Preserves enough evidence to reconstruct the decision path. |

## Related Canonical Formalisms

| Related Formalism | Relationship |
|---|---|
| Transition Table | Provides the classification surface for transition posture. |
| Boundary Conditions | Provides boundary satisfaction requirements. |
| Runtime Transition Governance | Applies governance at runtime or execution boundary. |
| State Transition Continuity Model | Supports continuity and standing analysis across state changes. |
| Decision Continuity | Supports persistence and reconstructability of decision standing. |
| Data Continuity | Supports persistence and reconstructability of data evidence. |
| Continuity Handoff Formalism | Supports transfer of task and evidence context across sessions or systems. |

## Mathematical Candidates

```text
Status: pending source-confirmed extraction from canonical source or publication artifacts.
```

Mathematical candidates should be linked here only after their source artifact is identified and public-safe.

## Proof Candidates

```text
Status: pending source-confirmed extraction from canonical source or publication artifacts.
```

Proof candidates should identify the exact artifact, source repository or paper path, replay path if present, and what the proof does and does not establish.

## Validation Candidates

```text
Status: pending source-confirmed extraction from canonical source or publication artifacts.
```

Validation candidates should identify executable tests, formalism tests, sample traces, receipts, or deterministic examples.

## Publication Artifacts

Current known publication family:

```text
https://github.com/GCAT-BCAT-Engine/Publisher/tree/main/papers/GCAT-BCAT
```

Durable machine-readable inventory:

```text
static/formalisms/gcat-bcat-publication-artifacts.v0.1.json
```

Inventory update path:

```text
scripts/enumerate-gcat-bcat-publisher-artifacts.mjs
scripts/apply-gcat-bcat-publisher-artifacts.mjs
github/workflows/enumerate-gcat-bcat-publisher-artifacts.yml
github/workflows/apply-gcat-bcat-publisher-artifacts.yml
```

Paths shown above without leading dot for iOS readability where applicable. The actual workflow paths use the leading dot directory.

This path is treated as a publication/exposition family, not as the canonical formalism authority.

## Reference Implementations

```text
Status: pending source-confirmed extraction.
```

Reference implementations should be listed only when the repository and implementation role are known.

## External Crosswalk Targets

| External Framework | Relationship |
|---|---|
| GLM | Possible pre-event boundary declaration and claim/non-claim framing. |
| EVIDE | Possible post-event evidence and reconstructability framing. |

These are crosswalk targets only. They do not replace canonical formalism definition.

## Open Questions

```text
Which exact Publisher paper files should be linked as first-order public explanation artifacts?
Which mathematical candidates are public-safe and source-confirmed?
Which proof candidates are public-safe and source-confirmed?
Which validation candidates are executable and source-confirmed?
Which related formalism links should be accepted by decision record rather than listed as intake relationships?
```

## Non-Claims

```text
This wiki page does not define the formalism.
This wiki page does not prove or validate the formalism.
Publisher papers are publication artifacts, not canonical source authority.
External framework mappings are crosswalk candidates, not equivalence decisions.
A listed relationship does not imply accepted formal equivalence.
```
