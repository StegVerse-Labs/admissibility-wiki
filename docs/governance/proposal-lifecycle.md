---
title: Proposal Lifecycle
---

# Proposal Lifecycle

## Purpose

This page defines how user-submitted, maintainer-submitted, browser-originated, and LLM-assisted proposals enter review for the Admissibility Wiki.

The proposal lifecycle exists so the wiki can accept broad terminology input without treating submission as authority.

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

This page governs wiki proposal handling. It does not authorize execution, decide runtime admissibility, or replace formalism-tests.

## Definition

A proposal is a recorded request to create, update, deprecate, supersede, map, dispute, or delete wiki content.

A proposal may contain useful information, but the proposal itself has no acceptance authority until a decision record gives it standing.

## Proposal Classes

```text
term_proposal
term_revision
equivalence_claim
overlap_claim
adjacency_claim
implementation_mapping
external_reference
counterexample
dispute
proof_path_example
page_deprecation
page_supersession
```

## Proposer Classes

```text
maintainer
contributor
external
user_submitted
browser_originated
llm_assisted
ai_entity_suggested
```

## Lifecycle States

```text
submitted
triaged
under_review
needs_evidence
accepted
accepted_experimental
accepted_external_view
rejected
deferred
superseded
withdrawn
```

## Required Proposal Fields

```json
{
  "proposal_id": "proposal.example.001",
  "proposal_class": "term_proposal",
  "target_page": "docs/glossary/example.md",
  "proposer_class": "user_submitted",
  "summary": "Short proposal summary.",
  "claimed_relationships": [
    {
      "relationship": "equivalent | overlapping | adjacent | broader_than | narrower_than | contradicts",
      "external_term": "Example external term",
      "external_domain": "Example domain",
      "notes": "Why the relationship is claimed."
    }
  ],
  "evidence_posture": "none | partial | present | sufficient",
  "policy_ref": "policy.wiki.page-review.v1",
  "status": "submitted"
}
```

## Submission Rule

A proposal may originate from a user interface, issue, pull request, browser flow, LLM-assisted draft, AI Entity suggestion, or maintainer edit.

Regardless of origin, the proposal must be judged by the same review posture before it becomes accepted wiki content.

## Equivalence Rule

If a proposal claims that another field already uses an identical term for the same concept, that claim should be recorded directly in the proposal under `claimed_relationships`.

If accepted, the identical term should be listed directly under the StegVerse term on the target page in an `Equivalent Terms` section.

## Decision Dependency

A proposal does not create page standing by itself.

Standing requires a decision record that identifies:

- the proposal being decided;
- the authority class;
- the policy reference;
- the evidence posture;
- the review posture;
- the decision outcome;
- the commit-time validity posture.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Limits

This page does not determine whether any individual term is correct.

It defines the lifecycle by which proposed wiki information is reviewed.

## Related Pages

- [Terminology Convergence](./terminology-convergence.md)
- [Page Template](./page-template.md)
- [Admissibility-Wiki AI Entity](./admissibility-wiki-ai-entity.md)
- [Current Task Sync](./current-task-sync.md)
