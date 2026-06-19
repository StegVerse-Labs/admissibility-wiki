---
title: Policy Reference
---

# Policy Reference

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with policy reference, but are not treated as identical without review:

- policy identifier;
- rule reference;
- control reference;
- standard reference;
- requirement reference;
- policy-as-code, when used to represent or evaluate policy logic as code or structured policy language. This overlaps with Policy Reference when the policy artifact supplies the rule basis for a transition, but it is not equivalent unless the specific policy artifact and version are cited as the commit-time rule basis.

## Adjacent Terms

The following terms are adjacent because they may describe policy content or evidence without identifying the exact rule basis used at commit time:

- policy document;
- compliance framework;
- control catalog;
- governance rule;
- decision table.

## Definition

A policy reference is the specific rule, policy, standard, or governance artifact used to evaluate a proposed transition.

It identifies the rule basis for the decision.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may identify policy material without requiring a stable commit-time rule basis that can be reconstructed from a receipt or decision record.

## Reference Requirements

A policy reference should be stable enough that a reviewer can determine which policy was applied at commit time.

It may point to:

- a repository policy file;
- a governance rule;
- a versioned standard;
- a workflow rule;
- a decision table;
- a formalism artifact.

## Why It Matters

Without a policy reference, a transition receipt may record that a decision happened without showing the rule basis for that decision.

Admissibility requires more than a result.

It requires the ability to identify the governing basis for that result.

## Governance Links

```yaml
governance:
  proposal_link: "../../static/governance/proposals/proposal.example.006.json"
  decision_link: "../../static/governance/decisions/decision.example.006.json"
  replay_link: "../../static/governance/replay/decision.example.006.txt"
  reconstruction_link: "../../static/governance/evidence/decision.example.006/README.md"
```

## Related Terms

- [Admissibility](./admissibility.md)
- [Authority Class](./authority-class.md)
- [Receipt-Bound Execution](./receipt-bound-execution.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
- [Terminology Overlap Research Notes](../research/terminology-overlap-research-notes.md)
