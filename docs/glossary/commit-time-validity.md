---
title: Commit-Time Validity
---

# Commit-Time Validity

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with commit-time validity, but are not treated as identical without review:

- execution-time validity;
- runtime validity;
- commit-time policy evaluation;
- just-in-time validation;
- freshness check.

## Adjacent Terms

The following terms are adjacent because they may support validity without fully defining the StegVerse concept:

- precondition check;
- invariant check;
- authorization check;
- conformance check;
- compliance review.

## Definition

Commit-time validity is the condition that a transition remains valid at the moment its result is allowed to bind.

It is not enough for a transition to have been valid at proposal time, approval time, or review time.

## Why It Matters

A transition can become invalid between proposal and execution.

Commit-time validity closes that gap by requiring the decision basis to remain current at the binding point.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may verify local validity without requiring the full authority, policy, evidence, review, context, continuity, and consequence posture required for admissibility.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Terms

- [Admissibility](./admissibility.md)
- [Commit-Time Authority](./commit-time-authority.md)
- [Drift](./drift.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
