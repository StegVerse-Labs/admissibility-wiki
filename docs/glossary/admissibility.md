---
title: Admissibility
---

# Admissibility

Admissibility is the property of a proposed transition being allowed to proceed under the authority, policy, evidence, and context state that exists at the moment the transition binds.

Admissibility is not the same as usefulness, technical possibility, approval, visibility, or continuity.

## Definition

A transition is admissible when the system can show that the transition had standing at commit time.

That standing may depend on:

- the authority class of the actor;
- the relevant policy reference;
- the evidence available at the moment of decision;
- the review posture;
- the current context state;
- the absence or acceptable handling of drift;
- the existence of a receipt that records the decision basis.

## Why It Matters

A system may be able to execute a transition while no longer being able to justify why that execution should bind.

Admissibility focuses on that gap.

It asks whether the consequence of a transition still has standing when the transition is committed.

## Related Terms

- [Transition](./transition.md)
- [Commit-Time Authority](./commit-time-authority.md)
- [Receipt-Bound Execution](./receipt-bound-execution.md)
- [Reconstructability](./reconstructability.md)
