---
title: Terminology Convergence
---

# Terminology Convergence

## Purpose

This page defines how the Admissibility Wiki handles StegVerse terms, identical external terms, overlapping terms, adjacent terms, and StegVerse-specific terms.

The goal is to make the wiki a convergence layer for governance vocabulary rather than a closed glossary.

## Page Status

```text
active
```

## Page Posture

```text
governance policy
```

## Maturity Posture

```text
conceptual
```

## Authority Boundary

This page defines wiki editorial posture. It does not decide whether a system transition is admissible, generate receipts, authorize execution, or replace formalism-tests.

## Core Rule

When a StegVerse term has one or more materially identical terms in another domain, those terms should be listed directly under the StegVerse term before distinctions, examples, mappings, or sector-specific notes.

This prevents the wiki from presenting a StegVerse term as novel when the underlying idea is already named elsewhere.

## Term Relationship Classes

### Identical Definition

Use when an external term describes the same underlying concept with no material difference for the page's purpose.

Identically defined terms should appear directly under the StegVerse term in a section named:

```text
Equivalent Terms
```

### Overlapping Definition

Use when an external term partially describes the same concept but does not carry the full StegVerse meaning.

Overlapping terms should appear in a section named:

```text
Overlapping Terms
```

### Adjacent Definition

Use when an external term belongs to the same conceptual neighborhood but answers a different governance question.

Adjacent terms should appear in a section named:

```text
Adjacent Terms
```

### StegVerse-Specific

Use only after reasonable overlap search shows that no existing term carries the same meaning.

A StegVerse-specific term should explain why existing terms are insufficient.

## Required Glossary Placement

Glossary pages should use this order when relationship information exists:

1. StegVerse term.
2. Equivalent terms, if any.
3. Overlapping terms, if any.
4. Adjacent terms, if any.
5. StegVerse definition.
6. Distinction.
7. Why the StegVerse term is retained.
8. Minimal example.
9. Proposal, decision, replay, and reconstruction links when mature.

## Example Pattern

```md
# Standing at Execution

## Equivalent Terms

- Execution-time validity, when used to mean authority and evidence are valid at the moment consequence binds.

## Overlapping Terms

- Runtime authorization.
- Just-in-time authorization.
- Commit-time policy evaluation.

## StegVerse Definition

Standing at execution is the condition that authority, evidence, consent, policy, and continuity remain admissible at the binding moment of consequence.

## Why The StegVerse Term Is Retained

The StegVerse term is retained when the external term does not include continuity, consequence standing, or admissibility predicates.
```

## Research Requirement

Before labeling a term StegVerse-specific, contributors should search across relevant domains, including at minimum:

- AI governance;
- formal verification;
- distributed systems;
- policy-as-code;
- safety engineering;
- audit and assurance;
- legal and compliance terminology;
- high-consequence review systems when relevant.

The search does not need to prove that no equivalent exists anywhere. It must show reasonable care before asserting specificity.

## Submission Requirement

User-submitted terms, browser-originated proposals, and LLM-assisted proposals may include equivalence claims.

Those claims are not accepted as authority until reviewed and recorded through the proposal and decision process.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Limits

This page does not certify the accuracy of any individual equivalence claim.

It defines how such claims should be placed, reviewed, and distinguished.

## Related Pages

- [Page Template](./page-template.md)
- [Editorial Policy](./editorial-policy.md)
- [Current Task Sync](./current-task-sync.md)
