---
title: Decision Record
---

# Decision Record

## Purpose

This page defines the wiki decision record used to accept, reject, defer, escalate, or refuse proposed wiki changes.

Decision records make the wiki review process reconstructable instead of relying on undocumented editorial judgment.

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

This page defines decision-record vocabulary for wiki governance. It does not authorize execution, prove runtime admissibility, or replace formalism-tests.

## Definition

A decision record is a structured record explaining how a proposal was resolved, what authority class reviewed it, what evidence posture was available, and whether the page change had standing at the binding wiki commit moment.

## Decision Outcomes

```text
ALLOW
DENY
ESCALATE
REFUSE
DEFER
SUPERSEDE
```

## Required Decision Fields

```json
{
  "decision_id": "decision.example.001",
  "proposal_id": "proposal.example.001",
  "target_page": "docs/glossary/example.md",
  "decision": "ALLOW",
  "authority_class": "wiki_maintainer",
  "policy_ref": "policy.wiki.page-review.v1",
  "evidence_posture": "sufficient",
  "review_posture": "maintainer_reviewed",
  "commit_time_validity": true,
  "relationship_disposition": [
    {
      "external_term": "Example external term",
      "relationship": "equivalent",
      "disposition": "accepted | rejected | deferred",
      "notes": "Reason for disposition."
    }
  ],
  "issued_at": "2026-06-19T00:00:00Z"
}
```

## Relationship Disposition

When a proposal claims that an external term is equivalent, overlapping, adjacent, broader, narrower, or contradictory, the decision record should explicitly dispose of that claim.

Accepted equivalence claims should be placed directly under the StegVerse term on the target page.

Rejected or deferred equivalence claims should remain reconstructable through the proposal and decision records.

## Replay Requirement

A mature decision should link to a replay note or artifact explaining how a reviewer can reconstruct the decision path from the proposal, policy reference, evidence posture, and target page state.

If executable replay does not yet exist, the replay link may be marked `not_applicable`, but the reason should be stated.

## Reconstruction Requirement

A mature decision should identify the evidence folder or record needed to reconstruct why the decision appeared to have standing.

Evidence may include:

- proposal text;
- claimed equivalent or overlapping terms;
- external references;
- review notes;
- ontology diffs;
- page diffs;
- policy references.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Limits

A decision record explains wiki standing. It does not prove that the underlying governance concept is correct in every external domain.

## Related Pages

- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Terminology Convergence](./terminology-convergence.md)
- [Page Template](./page-template.md)
- [Current Task Sync](./current-task-sync.md)
