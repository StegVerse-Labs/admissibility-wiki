---
title: Page Template
---

# Page Template

Use this structure when adding or updating a public vocabulary, governance, proof-path, comparison, implementation-map, or ontology page.

The template exists to make page posture, authority boundary, proposal history, decision history, replayability, and reconstructability explicit.

## Purpose

State what this page defines or explains.

## Page Status

```text
draft | active | superseded | deprecated | historical | external-reference
```

## Page Posture

```text
concept | implementation map | comparison | proof path | runbook | ontology guide | essay | external comparison | governance policy
```

## Maturity Posture

```text
conceptual | implemented | experimental | proposed | external
```

## Authority Boundary

State what authority this page has and what authority it does not have.

Example:

```text
This page defines vocabulary. It does not generate receipts, authorize execution, or replace formalism-tests.
```

## Definition

Give a concise definition.

## Distinction

State what the concept is not.

## Minimal Example

Provide one small example that can be understood without private context.

## StegVerse Mapping

Name the relevant StegVerse repo, component, artifact, or proof path if applicable.

## Governance Links

Every mature page should identify the governance records that explain how the page entered or changed state.

Use `not_applicable` only when the page is a seed page that predates the governance-link system.

```yaml
governance:
  proposal_link: "not_applicable | proposals/<proposal-id>.json | issue-or-pr-url"
  decision_link: "not_applicable | decisions/<decision-id>.json | issue-or-pr-url"
  replay_link: "not_applicable | replay/<decision-id>.txt | command-or-artifact-url"
  reconstruction_link: "not_applicable | evidence/<decision-id>/README.md | evidence-url"
```

## Proposal Record

When a page is created or materially changed, the proposal record should identify:

```json
{
  "proposal_id": "proposal.example.001",
  "target_page": "docs/path/example.md",
  "proposal_type": "create | update | deprecate | supersede | delete",
  "proposer_class": "maintainer | contributor | external | llm_assisted | browser_originated",
  "claimed_page_posture": "concept",
  "claimed_maturity_posture": "conceptual",
  "authority_class": "wiki_maintainer | vocabulary_editor | external_contributor | contributor_suggest",
  "policy_ref": "policy.wiki.page-review.v1",
  "evidence_posture": "present"
}
```

## Page Decision Record

When a page change is accepted, denied, escalated, or refused, the decision record should identify:

```json
{
  "decision_id": "decision.example.001",
  "proposal_id": "proposal.example.001",
  "target_page": "docs/path/example.md",
  "decision": "ALLOW | DENY | ESCALATE | REFUSE",
  "authority_class": "wiki_maintainer",
  "policy_ref": "policy.wiki.page-review.v1",
  "evidence_posture": "sufficient",
  "review_posture": "entity_reviewed | maintainer_reviewed | quorum_reviewed | external_reference",
  "commit_time_validity": true,
  "issued_at": "2026-06-17T00:00:00Z"
}
```

## Replay Link

Provide the command, artifact, or record that can re-check the page decision when applicable.

If no executable replay exists yet, mark the link as `not_applicable` and explain why.

## Reconstruction Link

Provide the evidence location needed to reconstruct why the page decision appeared to have standing.

This may include proposal text, review notes, policy references, related proof-path examples, ontology diffs, or formalism-test artifacts.

## Limits

State what this page does not prove or claim.

## Related Pages

- Link to related glossary pages.
- Link to implementation pages.
- Link to proof-path pages when relevant.
- Link to governance pages when relevant.

## Ontology Update Required

If the page defines or changes a core term, update:

```text
static/ontology/admissibility-vocabulary.v0.1.json
```

## Validation Checklist

Before publishing or accepting a mature page, verify:

- page status is declared;
- page posture is declared;
- maturity posture is declared;
- authority boundary is explicit;
- proposal link is present or explicitly marked `not_applicable`;
- decision link is present or explicitly marked `not_applicable`;
- replay link is present or explicitly marked `not_applicable`;
- reconstruction link is present or explicitly marked `not_applicable`;
- ontology update requirement is satisfied or explicitly not required;
- the page does not claim proof authority unless it links to the actual proof authority artifact.
