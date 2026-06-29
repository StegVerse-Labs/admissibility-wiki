---
title: Translation Records
---

# Translation Records

## Status

Record set: `static/translation-records/disciplinary-translation-records.v0.1.json`

Record state: intake

Authority boundary: translation records are interoperability artifacts only.

## Purpose

Translation records convert the Disciplinary Translation Groundwork into reviewable entries.

Each record identifies a source discipline term, preserves the source-safe native meaning, maps the term into a Transition Table role, declares a boundary condition, identifies a constraint reference, states an admissibility question, and records evidence and review posture.

The records do not prove source-discipline claims. They do not establish equivalence between disciplines. They do not create commit-time authority.

## Current Record Classes

| Class | Current use |
|---|---|
| physics | Maps state, interaction, horizon, measurement, entropy, and related physical terms into transition roles without claiming a new physical theory. |
| governed autonomy | Maps GCAT admissibility and capacity terms into transition roles. |
| boundary admissibility | Maps BCAT boundary terms into transition roles. |
| AI/runtime systems | Maps manifest, receipt, policy gate, and fail-closed runtime language into transition roles. |

## Current Intake Records

| Translation ID | Source discipline | Native term | Transition role | Review posture |
|---|---|---|---|---|
| `dtg-physics-state-v0-1` | physics | state | prior state or resulting state | proposed |
| `dtg-physics-interaction-v0-1` | physics | interaction | candidate transition or transition driver | proposed |
| `dtg-physics-horizon-v0-1` | physics | horizon | boundary condition or reconstruction limit | proposed |
| `dtg-gcat-capacity-margin-v0-1` | governed autonomy | admissibility margin | admissibility question | mapped |
| `dtg-bcat-boundary-v0-1` | boundary admissibility | boundary condition | boundary condition | mapped |
| `dtg-runtime-fail-closed-v0-1` | AI/runtime systems | fail-closed path | decision result | mapped |

## Required Record Fields

```text
translation_id
source_discipline
source_reference
native_term
native_meaning
transition_role
boundary_condition
constraint_reference
admissibility_question
evidence_posture
review_posture
non_claims
receipt_reference
```

## Review States

| State | Meaning |
|---|---|
| proposed | A candidate mapping exists, but specialist or source review has not accepted it. |
| mapped | A public-safe mapping exists and is suitable for crosswalk use, but it is not proof authority. |
| disputed | A mapping has a known objection or unresolved conflict. |
| accepted | A mapping has a decision record granting it wiki standing. |
| deferred | A mapping is intentionally held until stronger source evidence exists. |
| escalated | A mapping requires specialist review before further use. |

## Next Build Target

The next build target is validation tooling that checks every translation record contains the required fields, uses allowed review states, and preserves a non-claim boundary.

## Non-Claims

A translation record is not source proof, peer review, execution authority, admissibility proof, or evidence that the mapped disciplines are equivalent.
