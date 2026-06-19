---
title: Admissibility
---

# Admissibility

## Equivalent Terms

No materially identical external term is recorded for this page yet.

If a contributor claims that another field uses an identical term for the same concept, that claim should be submitted through the proposal lifecycle and reviewed before being listed here.

## Overlapping Terms

- Authorization, when used to describe whether an action is allowed.
- Policy compliance, when used to describe whether a proposed action satisfies a governing rule.
- Action admissibility, when used to describe whether a proposed action may proceed under stated constraints.

## Adjacent Terms

- Auditability.
- Explainability.
- Validity.
- Safety constraint.
- Governance control.

## Definition

Admissibility is the property of a proposed transition being allowed to proceed under the authority, policy, evidence, and context state that exists at the moment the transition binds.

A transition is admissible when the system can show that the transition had standing at commit time.

That standing may depend on:

- the authority class of the actor;
- the relevant policy reference;
- the evidence available at the moment of decision;
- the review posture;
- the current context state;
- the absence or acceptable handling of drift;
- the existence of a receipt that records the decision basis.

## Distinction

Admissibility is not the same as usefulness, technical possibility, approval, visibility, or continuity.

A system may be able to execute a transition while no longer being able to justify why that execution should bind.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because the page combines authority, policy, evidence, review, context, drift, receipt, and commit-time standing into one transition-governance concept.

Overlapping terms may describe part of that surface, but do not necessarily require consequence to have standing at the binding moment.

## Minimal Example

A proposed action may be technically executable and previously approved, but inadmissible if the policy changed before the action bound.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Terms

- [Transition](./transition.md)
- [Commit-Time Authority](./commit-time-authority.md)
- [Receipt-Bound Execution](./receipt-bound-execution.md)
- [Reconstructability](./reconstructability.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
