---
title: Authority Class
---

# Authority Class

## Equivalent Terms

No accepted equivalent terms are recorded yet.

Equivalent-term claims should be submitted through the proposal lifecycle and accepted only through a decision record.

## Overlapping Terms

The following terms may overlap with authority class, but are not treated as identical without review:

- role;
- permission class;
- access level;
- authorization scope;
- privilege level.

## Adjacent Terms

The following terms are adjacent because they may identify or constrain an actor without defining the transition authority category:

- identity;
- credential;
- capability;
- delegation;
- trust level.

## Definition

An authority class is a declared category of permission or standing that an actor, agent, service, repository, or governed component may hold for a proposed transition.

Authority class is not the same as identity.

Identity says who or what is acting.

Authority class says what kind of governed action that actor may claim standing to perform.

## Why The StegVerse Term Is Retained

The StegVerse term is retained because overlapping terms may describe access, role, or privilege without requiring a transition-specific standing category evaluated at commit time.

## Examples

Examples may include:

- maintainer publish;
- reviewer approve;
- ingestion engine submit;
- validator attest;
- governance engine decide;
- observer record.

## Why It Matters

Admissibility depends on matching the proposed transition to the correct authority class.

A valid identity may still lack the required authority class for a specific transition.

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
- [Policy Reference](./policy-reference.md)
- [Terminology Convergence](../governance/terminology-convergence.md)
