---
title: Reconstructability
---

# Reconstructability

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with reconstructability, but are not treated as identical without review:

- auditability;
- traceability;
- explainability;
- observability;
- provenance.

## Adjacent Terms

The following terms are adjacent because they may support reconstruction without necessarily explaining why consequence had standing:

- event history;
- log retention;
- forensic record;
- post-event review;
- incident analysis.

## Definition

Reconstructability is the ability to recover enough information after an event to understand what happened and why a decision appeared to have standing.

It is related to auditability, but it is not identical to auditability.

## Admissibility-Relevant Reconstruction

For admissibility, reconstruction must address more than event history.

It must help recover:

- the authority posture;
- the evidence posture;
- the policy reference;
- the review state;
- the decision result;
- the commit-time context.

## Important Distinction

A system may reconstruct what happened without reconstructing why consequence had standing.

That distinction is central to transition governance.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may preserve evidence, traces, or explanations without requiring reconstruction of admissibility, standing, and binding consequence.

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
- [Receipt-Bound Execution](./receipt-bound-execution.md)
- [Auditability vs Admissibility](../comparisons/auditability-vs-admissibility.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
