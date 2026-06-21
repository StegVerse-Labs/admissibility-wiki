---
title: Discovery Review Queue
---

# Discovery Review Queue

## Purpose

The Discovery Review Queue is the public-safe staging area for candidate relationships before they become accepted wiki relationship records.

## Queue Boundary

The queue contains candidates only.

A queued item does not mean the wiki has accepted synonymy, equivalence, dependency, consequence, or conflict.

## Candidate States

```text
review_required
accepted
reclassified
rejected
deferred
superseded
```

## Required Candidate Fields

```text
candidate_id
term_a
term_b
relationship_type
confidence
source_origin_a
source_origin_b
evidence_a
evidence_b
review_status
review_notes
created_at
updated_at
```

## Promotion Rule

A candidate relationship may be promoted only when:

```text
1. Both source origins are formal artifacts.
2. Evidence is linked to both terms or concepts.
3. The relationship type is reviewed.
4. The review decision is recorded.
5. The final record preserves both origins.
```

## Rejection Rule

A rejected relationship should remain reconstructable unless removal is required by privacy, safety, legal, or source-boundary constraints.

## Non-Claims

```text
The review queue does not define terms.
The review queue does not accept relationship candidates by default.
The review queue does not replace source authority.
The review queue does not expose private source content.
```
