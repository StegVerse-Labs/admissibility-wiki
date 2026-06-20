---
title: Data Continuity
---

# Data Continuity

## Status

Canonical source repository: `Admissible-Existence/DaCo`

Wiki state: watching

Detail status: initial public-safe canonical detail page

## Definition

Data Continuity is a canonical formalism for evaluating whether evidence, records, hashes, receipts, references, and data context remain connected across state changes, handoffs, reviews, publications, or execution attempts.

It supports inspection of whether later decisions can still rely on prior data, or whether the data basis must be re-collected, re-bound, superseded, quarantined, or rejected.

## Source Boundary

Admissible-Existence defines the formalism. Publisher publishes papers and public exposition. The Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.

The wiki is not the source authority for this formalism.

## Scope

Data Continuity applies where a transition depends on evidence or data that must remain reconstructable, current, admissible, and bound to the correct source and destination context.

## Purpose

The purpose of Data Continuity is to prevent systems from treating stored data as still usable when its source, freshness, custody, hash chain, evidence posture, or destination standing has changed.

## Core Constructs

| Construct | Role |
|---|---|
| Data record | A data artifact, reference, hash, receipt, or evidence item. |
| Data standing | Whether the data can support the transition or decision. |
| Data continuity | Whether the data remains connected across transition boundaries. |
| Custody | The state of data holding, transfer, quarantine, supersession, or installation. |
| Source reference | The origin from which data or evidence was derived. |
| Destination reference | The target context where data is used or installed. |
| Receipt | Record supporting reconstruction of data standing. |

## Related Canonical Formalisms

| Related Formalism | Relationship |
|---|---|
| State Transition Continuity Model | Evaluates state continuity around data records. |
| Decision Continuity | Uses data continuity to preserve decision standing. |
| Runtime Transition Governance | Applies data standing at runtime or publication time. |
| Transition Table | Classifies data-bearing transition posture. |
| Boundary Conditions | Determines whether the data remains inside the required boundary. |
| Continuity Handoff Formalism | Preserves data context across handoffs. |

## Mathematical Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

## Proof Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

## Validation Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

Validation candidates should include stale data, broken hash chain, superseded data, failed installation, quarantined data, and destination-return remediation cases when public-safe source artifacts are available.

## Publication Artifacts

Status: pending source-confirmed extraction.

## Reference Implementations

Status: pending source-confirmed extraction.

## External Crosswalk Targets

| External Framework | Relationship |
|---|---|
| GLM | May help declare the data-use claims, non-claims, and composition frame before review. |
| EVIDE | May help preserve post-event evidence needed to reconstruct data standing. |

These are crosswalk targets only. They do not replace canonical formalism definition.

## Open Questions

```text
Which exact Admissible-Existence source file defines Data Continuity?
Which custody states are canonical versus explanatory?
Which tests validate stale, superseded, quarantined, and destination-return cases?
Which receipt fields are required for reconstructing data standing?
```

## Non-Claims

This wiki page does not define, prove, or validate the formalism. External framework mappings are crosswalk candidates, not equivalence decisions. A listed relationship does not imply accepted formal equivalence.
