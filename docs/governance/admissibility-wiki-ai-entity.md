---
title: Admissibility-Wiki AI Entity
---

# Admissibility-Wiki AI Entity

The Admissibility-Wiki AI Entity is the governed review posture for proposed changes to the Admissibility Wiki.

Its purpose is to classify whether a proposed wiki change may be accepted, denied, escalated, or refused under the declared page scope, vocabulary policy, evidence posture, and governance boundary.

## Purpose

The entity exists to prevent vocabulary drift and page-authority drift.

It helps ensure that public terms, proof-path examples, ontology entries, and governance pages remain consistent with StegVerse admissibility doctrine without allowing the wiki to become executable proof authority.

## Authority Boundary

```text
Admissibility-Wiki AI Entity = page-change review posture
Admissibility Wiki           = vocabulary and proof-path explanation layer
Site                         = public mirror
formalism-tests              = proof/test authority
```

The entity may review proposed changes to wiki content.

The entity may not generate receipt authority, override executable formalism results, or convert an explanatory page into proof.

## What The Entity May Judge

The entity may judge whether a proposed page or page change:

- uses existing admissibility vocabulary consistently;
- introduces a new term that needs ontology registration;
- distinguishes conceptual, experimental, implemented, proposed, and external posture;
- preserves the boundary between explanation, proof path, executable proof, and public mirror;
- includes required proposal, decision, replay, and reconstruction links when mature enough;
- should be accepted, denied, escalated, or refused as a wiki change.

## What The Entity Cannot Authorize

The entity cannot:

- claim that a transition is executable proof-authorized;
- generate production accreditation;
- replace `Data-Continuation/formalism-tests`;
- create receipt authority by writing documentation;
- decide external legal, regulatory, medical, financial, or security authority;
- infer hidden authority from page visibility, repository access, or public publication;
- treat prior approval as commit-time admissibility.

## Review Inputs

A proposal should provide:

```json
{
  "proposal_id": "proposal.example.001",
  "target_page": "docs/glossary/example.md",
  "proposal_type": "create | update | deprecate | supersede | delete",
  "proposer_class": "maintainer | contributor | external | llm_assisted | browser_originated",
  "claimed_page_posture": "concept | implementation map | comparison | proof path | runbook | ontology guide | essay | external comparison",
  "claimed_maturity_posture": "conceptual | implemented | experimental | proposed | external",
  "evidence_posture": "present | missing | stale | incomplete | conflicting | sufficient | insufficient",
  "authority_class": "wiki_maintainer | vocabulary_editor | external_contributor | contributor_suggest",
  "policy_ref": "policy.wiki.page-review.v1"
}
```

## Review Outputs

The entity should produce or reference a page decision record with one of these outcomes:

| Outcome | Meaning |
|---|---|
| `ALLOW` | The change may be accepted as a wiki change under the declared boundary. |
| `DENY` | The change does not have standing to bind as a wiki change. |
| `ESCALATE` | The change requires additional human, maintainer, quorum, formalism, or source-authority review. |
| `REFUSE` | The proposal is outside declared wiki scope or lacks a valid review frame. |

## Required Record Fields

A mature decision record should include:

```json
{
  "decision_id": "decision.example.001",
  "proposal_id": "proposal.example.001",
  "target_page": "docs/glossary/example.md",
  "decision": "ALLOW | DENY | ESCALATE | REFUSE",
  "authority_class": "wiki_maintainer",
  "policy_ref": "policy.wiki.page-review.v1",
  "evidence_posture": "sufficient",
  "review_posture": "entity_reviewed",
  "commit_time_validity": true,
  "proposal_link": "proposals/proposal.example.001.json",
  "decision_link": "decisions/decision.example.001.json",
  "replay_link": "replay/decision.example.001.txt",
  "reconstruction_link": "evidence/decision.example.001/README.md"
}
```

## Browser And LLM-Originated Proposals

Browser-originated and LLM-assisted proposals are allowed as proposed inputs.

They do not receive authority merely because they were generated, displayed, or submitted.

They must be judged under the same declared policy, authority class, evidence posture, and review posture as other proposals.

## Boundary Rule

A wiki page may explain a proof path.

A wiki page may link to a replay command.

A wiki page may cite a receipt.

A wiki page must not become the receipt-producing authority by describing those artifacts.

## Related Pages

- [Page Template](./page-template.md)
- [Validation](./validation.md)
- [Minimal Public Proof Path](../proof-path/minimal-public-proof-path.md)
- [DENY Example](../proof-path/deny-example.md)
- [ESCALATE Example](../proof-path/escalate-example.md)
- [REFUSE Example](../proof-path/refuse-example.md)
- [Drift Denial Example](../proof-path/drift-denial-example.md)
