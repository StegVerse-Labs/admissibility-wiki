---
title: Discovery Relationship Types
---

# Discovery Relationship Types

## Purpose

This page defines the public vocabulary for candidate relationships produced by the Formalism Discovery Engine.

These labels are review vocabulary only. They do not assert final equivalence or authority.

## Candidate Relationship Types

| Relationship Type | Meaning |
|---|---|
| `equivalent_candidate` | Terms or concepts may express the same formal meaning. |
| `near_equivalent_candidate` | Terms or concepts strongly overlap but may not fully match. |
| `parent_candidate` | One concept may contain or generalize another. |
| `child_candidate` | One concept may specialize another. |
| `prerequisite_candidate` | One concept may be required before another can hold. |
| `consequence_candidate` | One concept may follow from another. |
| `conflict_candidate` | Two concepts may be incompatible or contradictory. |
| `adjacent_candidate` | Concepts are related but not clearly equivalent, hierarchical, or conflicting. |
| `unresolved_candidate` | Evidence indicates relation, but the relationship class is not yet clear. |

## Review Outcomes

| Review Outcome | Meaning |
|---|---|
| `accepted` | Reviewer confirms the relationship type. |
| `reclassified` | Reviewer accepts a relationship but changes its type. |
| `rejected` | Reviewer rejects the candidate relationship. |
| `deferred` | More source evidence is required. |
| `superseded` | A later candidate or source artifact replaces the candidate. |

## Required Evidence

Every candidate relationship should include:

```text
term_a
term_b
relationship_type
source_origin_a
source_origin_b
evidence_a
evidence_b
confidence
review_status
```

## Non-Claims

```text
A relationship type is not a final relationship claim.
A candidate relationship is not an equivalence decision.
A confidence score is not proof.
A source origin link is not endorsement.
```
