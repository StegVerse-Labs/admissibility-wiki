---
title: Canonical Formalism Catalog
---

# Canonical Formalism Catalog

## Purpose

This page defines the wiki’s formalism-catalog responsibility boundary.

The Admissibility Wiki does not originate canonical formalisms. It mirrors, relates, crosswalks, and discovers relationships around canonical formalisms defined by `Admissible-Existence`.

## Graph Index

The current public formalism graph can be inspected here:

[Canonical Formalism Graph Index](./formalism-graph-index.md)

## Source Chain

```text
Admissible-Existence defines canonical formalisms.
Publisher publishes papers and public exposition.
Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.
External frameworks are crosswalk targets only.
```

## Catalog Status

The catalog is incomplete until each canonical formalism has:

```text
canonical name
canonical source repository
public-safe definition
scope
purpose
related formalisms
mathematical candidates
proof candidates
validation candidates
publisher artifacts
reference implementations
wiki crosswalk targets
non-claims
```

## Initial Canonical Formalism Families

| Canonical Formalism | Source Repository | Wiki State | Public-Safe Definition State |
|---|---|---|---|
| [Commit-Time Admissibility](./commit-time-admissibility.md) | `Admissible-Existence/CTA` | mirrored | initial scaffold, tests, and handoff installed |
| [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md) | `Admissible-Existence/IICT` | mirrored | initial scaffold, tests, and handoff installed |
| [State Transition Continuity Model](./state-transition-continuity-model.md) | `Admissible-Existence/STCM` | watching | initial scaffold installed |
| [Runtime Transition Governance](./runtime-transition-governance.md) | `Admissible-Existence/RTG` | watching | initial scaffold installed |
| [Boundary Conditions](./boundary-conditions.md) | `Admissible-Existence/BC` | watching | initial scaffold installed |
| [Transition Table](./transition-table.md) | `Admissible-Existence/TT` | watching | initial scaffold installed |
| [Triad Governance Model](./triad-governance-model.md) | `Admissible-Existence/Triad` | watching | initial scaffold installed |
| [Continuity Handoff Formalism](./continuity-handoff-formalism.md) | `Admissible-Existence/CHF` | watching | initial scaffold installed |
| [Data Continuity](./data-continuity.md) | `Admissible-Existence/DaCo` | watching | initial scaffold installed |
| [Decision Continuity](./decision-continuity.md) | `Admissible-Existence/DC` | watching | initial scaffold installed |
| [Governance-Centered and Boundary-Centered Admissibility Testing](./governance-centered-boundary-centered-admissibility-testing.md) | `Admissible-Existence/GCAT-BCAT` | source_available | first complete publication family available through Publisher |
| [Core-Lite Admissibility Engine](./core-lite-admissibility-engine.md) | `Admissible-Existence/core-lite` | watching | initial scaffold installed |
| [Learning Transition Governance](./learning-transition-governance.md) | `Admissible-Existence/learning-transition-governance` | watching | initial scaffold installed |
| [Admissible-Existence Validation Factory](./admissible-existence-validation-factory.md) | `Admissible-Existence/ae-validation-factory` | watching | initial scaffold installed |

## Priority Rule

Canonical formalism pages should be built before external-framework crosswalk pages are promoted as major navigation targets.

External frameworks such as GLM and EVIDE may remain in intake, but their relationship claims should not be treated as mature until the canonical formalism graph is populated.

## Formalism Page Template

Each canonical formalism page should use this structure:

```text
Canonical Name
Canonical Source Repository
Definition
Scope
Purpose
Core Constructs
Related Formalisms
Mathematical Candidates
Proof Candidates
Validation Candidates
Publisher Artifacts
Reference Implementations
External Crosswalk Targets
Open Questions
Non-Claims
```

## Non-Claims

```text
The wiki catalog does not define the canonical formalism.
The wiki catalog does not prove or validate the formalism.
A listed relationship does not imply accepted equivalence.
External framework mapping does not replace canonical formalism definition.
```

## Next Safe Build Target

Continue source-confirmed mathematical, proof, validation, artifact, and implementation extraction across the canonical formalism graph.
