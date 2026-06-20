---
title: Canonical Formalism Catalog
---

# Canonical Formalism Catalog

## Purpose

This page defines the wiki’s formalism-catalog responsibility boundary.

The Admissibility Wiki does not originate canonical formalisms. It mirrors, relates, crosswalks, and discovers relationships around canonical formalisms defined by `Admissible-Existence`.

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
| [State Transition Continuity Model](./state-transition-continuity-model.md) | `Admissible-Existence/STCM` | watching | initial scaffold installed |
| [Runtime Transition Governance](./runtime-transition-governance.md) | `Admissible-Existence/RTG` | watching | initial scaffold installed |
| Boundary Conditions | `Admissible-Existence/BC` | watching | pending public-safe source availability |
| [Transition Table](./transition-table.md) | `Admissible-Existence/TT` | watching | initial scaffold installed |
| Triad Governance Model | `Admissible-Existence/Triad` | watching | pending public-safe source availability |
| Continuity Handoff Formalism | `Admissible-Existence/CHF` | watching | pending public-safe source availability |
| Data Continuity | `Admissible-Existence/DaCo` | watching | pending public-safe source availability |
| [Decision Continuity](./decision-continuity.md) | `Admissible-Existence/DC` | watching | initial scaffold installed |
| [Governance-Centered and Boundary-Centered Admissibility Testing](./governance-centered-boundary-centered-admissibility-testing.md) | `Admissible-Existence/GCAT-BCAT` | source_available | first complete publication family available through Publisher |
| Core-Lite Admissibility Engine | `Admissible-Existence/core-lite` | watching | pending public-safe source availability |
| Learning Transition Governance | `Admissible-Existence/learning-transition-governance` | watching | pending source-confirmed extraction |
| Admissible-Existence Validation Factory | `Admissible-Existence/ae-validation-factory` | watching | pending public-safe source availability |

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

Register Decision Continuity in the machine-readable formalism registry, then continue source-confirmed mathematical, proof, and validation candidate extraction.
