---
title: Commit-Time Authority
---

# Commit-Time Authority

## Canonical coordinate relationship

StegVerse governance is located at:

```text
G = (Authority, Time)
```

Commit-time authority is the applicable **Authority** resolved at the governing **Time** at which a transition would bind. This term therefore expresses the Authority × Time model rather than creating a separate governance primitive.

State, policy, identity, delegation, evidence, review posture, continuity, scope, and recoverability are evaluated context at that coordinate.

Elapsed time alone does not create, revoke, transfer, or renew Authority:

```text
Delta-time -/-> Delta-authority
```

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with commit-time authority, but are not treated as identical without review:

- runtime authorization;
- just-in-time authorization;
- commit-time policy evaluation;
- execution-time authorization;
- policy enforcement;
- policy decision, when used to describe a policy-engine result produced from supplied input, policies, and data. This overlaps with Commit-Time Authority when the decision contributes to resolving Authority at the binding Time, but it is not equivalent unless the decision also preserves the authority class, evidence posture, review posture, continuity posture, and consequence boundary required for admissibility.

## Adjacent Terms

The following terms are adjacent because they may occur near the same system boundary but do not necessarily answer the same governance question:

- access control;
- approval workflow;
- policy-as-code;
- audit logging;
- attestation.

## Definition

Commit-time authority is the Authority basis that applies at the Time a transition binds.

It is not enough that an actor was previously approved, previously trusted, or previously authorized.

## Core Distinction

Approval is not continuity.

Execution is not admissibility.

Commit-time authority asks what Authority applies at the governing Time when the system is about to commit consequence.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may describe authorization, enforcement, or policy evaluation without necessarily requiring consequence standing, continuity posture, evidence posture, and admissibility at the binding moment.

## Examples

The Authority resolved at a later governing Time may differ because evaluated context changed, including:

- policy;
- identity records;
- delegation or revocation state;
- evidence posture;
- review status;
- required observer availability;
- action scope or authority class.

Those contextual changes can alter the Authority determination at the later Time. Passage of time by itself is not the cause.

## Governance Links

```yaml
governance:
  proposal_link: "../../static/governance/proposals/proposal.example.008.json"
  decision_link: "../../static/governance/decisions/decision.example.008.json"
  replay_link: "../../static/governance/replay/decision.example.008.txt"
  reconstruction_link: "../../static/governance/evidence/decision.example.008/README.md"
```

## Related Terms

- [Authority × Time Governance Coordinate](../governance/authority-time-governance-coordinate.md)
- [Admissibility](./admissibility.md)
- [Governance Boundary](./governance-boundary.md)
- [Reconstructability](./reconstructability.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
- [Terminology Overlap Research Notes](../research/terminology-overlap-research-notes.md)
