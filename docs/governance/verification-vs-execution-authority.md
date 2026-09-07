---
title: Verification, Evidence, and the Authority × Time Governance Coordinate
---

# Verification, Evidence, and the Authority × Time Governance Coordinate

## Governance signal

Virginia's 2026 SB 384 / HB 797 directs the Joint Commission on Technology and Science to evaluate a framework for Independent Verification Organizations (IVOs). The supplied public announcement describes independent, expert-led bodies that verify whether AI systems meet outcome-based safety goals.

Source observed:

```text
https://www.prnewswire.com/news-releases/fathom-applauds-governor-spanbergers-signing-of-landmark-ai-governance-legislation-302739994.html
Published: 2026-04-13
Source class: organization-issued public announcement distributed by PR Newswire
```

This source is evidence of a policy direction and of the announced study mandate. It is not, by itself, the enacted bill text, an operational IVO standard, proof of implementation, or evidence that an IVO holds live authority over individual executions.

## Canonical governance coordinate

StegVerse governance is located at:

```text
G = (Authority, Time)
```

Authority and Time are the coordinates of governance.

Verification, evidence, state, policy, delegation, scope, identity, recoverability, context, and review posture are evaluated at that coordinate. They are not additional governance coordinates and they do not replace either coordinate.

Verification therefore does not sit on a separate authority plane. It supplies evidence about propositions evaluated at `(Authority, Time)`.

## The verification distinction

Independent verification can answer questions such as:

- whether a system was assessed against stated criteria;
- whether documentation and evidence were available to reviewers;
- whether an external expert body found the system consistent with a safety target;
- whether a product earned a verification status or seal.

Those functions matter. They do not resolve the governance coordinate for a consequential transition.

The narrower commit-time question is:

> What Authority applies at the Time this specific consequential decision would bind?

Verification evaluates a system, artifact, process, event, or claim. Its result may become evidence used when evaluating a proposed transition at the applicable Authority × Time coordinate.

## Required live control point

For a high-risk action, governance remains incomplete unless the workflow preserves a point at which the applicable Authority can still produce a non-admitting disposition before consequence attaches.

```text
verified system
  != resolved Authority at governing Time

review completed
  != current delegation

impact assessment
  != commit-time admissibility

explainable result
  != permission to execute
```

A governed execution boundary should bind:

```text
governance_coordinate:
  authority
  time

evaluated_context:
  proposed action and target
  actor or requesting entity
  institution or governing relation
  policy reference
  delegation / authority basis evidence
  evidence and review posture
  execution context
  scope
  recoverability / rollback profile
  resulting disposition
  receipt / reconstruction evidence
```

The evaluated-context fields inform or evidence the decision at the coordinate. They are not governance coordinates themselves.

## Institutional test

The decisive institutional question is not only whether the model or system was reviewed. It is whether the applicable Authority remained resolvable and consequential at the governing Time.

A useful public test remains:

> Show where the workflow can still say "NO."

That refusal point is evidence that an Authority relation remains causally consequential before commitment. It does not mean refusal itself creates Authority.

## Relationship to the StegVerse triad

| Layer | Question | Verification relevance |
|---|---|---|
| Transition governance | What transition is being considered at `(Authority, Time)`? | Verification may supply evidence and review posture. |
| Admissibility governance | Is that transition admissible at the applicable governance coordinate? | Requires resolution of Authority at Time plus evaluation of applicable context. |
| Continuity governance | Can the coordinate, inputs, decision path, and consequence be reconstructed later? | Requires receipts/evidence for assessment, authority resolution, execution, or denial. |

The IVO concept can strengthen evidence quality and independent review. It enters the governed transition path as evidence/review context rather than as a replacement governance coordinate.

## Boundary statement

```text
Governance = Authority × Time
verification != Authority
verification != Time
certification != governance coordinate
system approval != action-level admissibility
post-event explanation != pre-consequence refusal
Delta-time -/-> Delta-authority
```

The next governance phase is therefore not limited to "show your work." It must preserve the Authority × Time coordinate, the evidence used there, and the ability to reconstruct what was admitted or refused and why.

## Related

- [Authority × Time Governance Coordinate](./authority-time-governance-coordinate.md)
- [Commit-Time Authority](../glossary/commit-time-authority.md)
- [Relational Transition Geometry](../formalisms/runtime-transition-governance.md)
