---
title: Relational Transition Geometry
---

# Relational Transition Geometry

## Status

Canonical source repository: `Admissible-Existence/RTG`

Wiki state: watching

Detail status: corrected public-safe canonical detail page / Authority × Time bound

## Governance-coordinate boundary

Relational Transition Geometry describes the geometry and context of a transition. It does not define a replacement governance coordinate system.

Canonical StegVerse governance coordinate:

```text
G = (Authority, Time)
```

RTG variables are evaluated at that coordinate. State, actor, target, boundary, evidence, context, recoverability, inference window, coherency horizon, and point of irreversibility are transition/context variables, not additional governance coordinates.

## Definition

Relational Transition Geometry is the foundational RTG formalism for describing the geometry of a transition before it is reduced into table cells, proof paths, runtime checks, or commit-time outcomes.

It models the relationships among actor, target, authority basis/relationship, boundary, context, evidence, recoverability, inference window, coherency horizon, and point of irreversibility while preserving `(Authority, Time)` as the governance location at which those relationships are evaluated.

## Source Boundary

Admissible-Existence defines the formalism. Publisher publishes papers and public exposition. The Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.

The wiki is not the source authority for this formalism.

## Correction Note

Earlier public-safe wiki language used RTG as Runtime Transition Governance. That language is narrowed.

RTG means Relational Transition Geometry at the foundation layer. Runtime governance remains a later execution-facing application of the transition geometry at an Authority × Time governance coordinate; it is not the primary RTG expansion.

## Scope

Relational Transition Geometry applies where a proposed or observed transition must be examined as a relationship rather than as a single approval, execution, state change, or result label.

## Purpose

The purpose of Relational Transition Geometry is to prevent transition evaluation from collapsing into one-dimensional labels such as approved, visible, executed, reviewed, or continuous.

It preserves the structural question first: what relationship is changing, across which boundary, with what evidence and recoverability, and at what distance from irreversible consequence? Governance then evaluates that transition context at the applicable `(Authority, Time)` coordinate.

## Core Constructs

| Construct | Role |
|---|---|
| Actor | Entity or process attempting, proposing, reviewing, or carrying a transition. |
| Target | Entity, state, artifact, boundary, or system affected by the transition. |
| Relationship | The transition relation among actor, target, authority basis, evidence, context, and consequence. |
| Transition vector | Direction and class of proposed state movement. |
| Authority relation | Evidence/context describing standing or authority basis relative to the target and requested transition; the applicable Authority coordinate is resolved separately at governing Time. |
| Boundary relation | Whether the transition remains inside the required scope, recoverability, consent, or other governed boundary. |
| Evidence relation | Whether evidence is sufficient, fresh, relevant, and reconstructable for the attempted transition. |
| Coherency horizon | The information boundary beyond which no additional information can be obtained from within a stabilized coherent state, even though existence may continue inside that boundary. |
| Inference window | The region in which authority-basis evidence, policy, context, delegation, and memory remain usable for standing determination. |
| Point of irreversibility | The point after which the transition cannot be fully recalled, reversed, re-bound, or restored without a new recovery or remediation process. |
| Recoverability profile | Whether the transition can be paused, reversed, reconstructed, remediated, or fail-closed. |

## Relationship to the Transition Table

The Transition Table is the operational bridge from Relational Transition Geometry into discrete transition classifications.

Relational Transition Geometry defines the shape. The Transition Table classifies that shape into reviewable and testable transition postures. Commit-Time Admissibility then evaluates whether the classified transition has standing at the applicable Authority × Time coordinate when consequence would bind.

```text
Relational Transition Geometry
  -> Transition Table
  -> Commit-Time Admissibility @ (Authority, Time)
  -> Runtime governance
```

## Relationship to Runtime Governance

Runtime governance is the execution-facing application of the geometry. It evaluates the current transition posture at the applicable Authority × Time coordinate at or near the moment an action, publication, denial, escalation, refusal, deferral, or fail-closed result would occur.

Runtime governance must not inherit Authority merely because a prior geometric, table, review, verification, or receipt record exists.

Time is not Authority, and elapsed time alone does not create or revoke Authority:

```text
Delta-time -/-> Delta-authority
```

That temporal non-causality rule does not remove Time from governance.

## Related Canonical Formalisms

| Related Formalism | Relationship |
|---|---|
| Authority × Time Governance Coordinate | Defines the governance location at which RTG context is evaluated. |
| Coherency Horizon | Defines the knowability boundary inside the transition geometry. |
| Transition Table | Operationalizes relational geometry as discrete transition cells. |
| Commit-Time Admissibility | Determines whether the proposed transition has standing at commitment at the applicable coordinate. |
| Governance-Centered and Boundary-Centered Admissibility Testing | Supplies governance and boundary tests over the relational geometry. |
| Boundary Conditions | Defines required boundary satisfaction inside the geometry. |
| State Transition Continuity Model | Supports continuity analysis across state changes and preserves coordinate-related evidence in receipts. |
| Decision Continuity | Supports persistence or loss of decision standing without manufacturing Authority. |
| Continuity Handoff Formalism | Preserves context when a transition crosses sessions, systems, or actors. |

## Mathematical Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

Potential variables should describe relationships and transition context, including actor-target relation, authority-basis distance, boundary distance, evidence sufficiency, inference distance, irreversibility distance, recoverability, and coherency horizon. These candidates do not add governance coordinates beyond Authority and Time.

## Proof Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

Proof candidates should show that the Transition Table is a discretized operational representation of Relational Transition Geometry, not an independent origin for the geometry or for the governance coordinate system.

## Validation Candidates

Status: pending source-confirmed extraction from canonical source or publication artifacts.

Validation candidates should include changed-Authority, changed-Time, changed-target, boundary-drift, stale-evidence, horizon-loss, non-recoverable-transition, point-of-irreversibility, and elapsed-time-without-authority-change cases when public-safe source artifacts are available.

## Publication Artifacts

Status: pending source-confirmed extraction.

## Reference Implementations

Status: pending source-confirmed extraction.

## External Crosswalk Targets

| External Framework | Relationship |
|---|---|
| GLM | May help declare pre-transition claims, non-claims, and boundary frame. |
| EVIDE | May help preserve post-transition evidence for reconstruction. |

These are crosswalk targets only. They do not replace canonical formalism definition or the Authority × Time governance coordinate.

## Open Questions

```text
Which exact Admissible-Existence source file defines each RTG variable?
Which variables are canonical versus explanatory?
Which artifacts establish the earliest preserved transition-geometry discussion?
Which proof path shows the Transition Table as the operational form of the geometry?
Which tests validate loss beyond the coherency horizon?
```

## Non-Claims

This wiki page does not define, prove, or validate the formalism. External framework mappings are crosswalk candidates, not equivalence decisions. A listed relationship does not imply accepted formal equivalence. Runtime governance remains a related execution layer evaluated at `(Authority, Time)`, not the corrected foundation meaning of RTG.

## Related

- [Authority × Time Governance Coordinate](../governance/authority-time-governance-coordinate.md)
- [Commit-Time Authority](../glossary/commit-time-authority.md)
