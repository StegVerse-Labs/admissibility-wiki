---
title: Drift
---

# Drift

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with drift, but are not treated as identical without review:

- state drift;
- configuration drift;
- policy drift;
- context drift;
- evidence staleness.

## Adjacent Terms

The following terms are adjacent because they may describe change without necessarily changing admissibility standing:

- update;
- version change;
- environmental change;
- data change;
- status change.

## Definition

Drift is a relevant change in identity, authority, policy, evidence, review, context, or system state that may affect whether a proposed transition remains admissible.

Drift is not automatically failure.

It becomes governance-relevant when it changes the basis on which a transition would be allowed to bind.

Drift is a change between the expected decision basis and the current decision basis.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may describe change without requiring an admissibility check at the binding moment.

## Examples

Examples include:

- policy drift;
- evidence drift;
- identity drift;
- authority drift;
- context drift;
- review drift.

## Why It Matters

A transition that was valid earlier may become inadmissible after drift.

Commit-time governance should detect or account for drift before allowing consequence to bind.

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
- [Evidence Posture](./evidence-posture.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
