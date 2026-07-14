---
title: Review Output Receipts and Supersession
---

# Review Output Receipts and Supersession

## Purpose

This page defines how specialist-review outputs become durable receipts and how a later promotion decision may supersede an earlier deferred decision without erasing history.

Review receipts preserve evidence, reviewer class, result, objections, missing evidence, and timing. Supersession occurs only after declared locator and review conditions are satisfied.

## Required Review Classes

```text
physics_foundations
mathematical_formalism
admissibility_governance
```

Each class must have exactly one current receipt for the active route.

## Receipt Results

| Result | Meaning |
|---|---|
| `SUPPORT` | The reviewer supports the proposed mapping within stated scope. |
| `OBJECT` | A material objection is recorded and must be resolved or carried forward. |
| `DEFER` | Review cannot complete until named evidence or conditions exist. |
| `INSUFFICIENT_EVIDENCE` | Available material cannot support a scoped conclusion. |
| `OUT_OF_SCOPE` | The assigned review class cannot evaluate the claim as framed. |

A placeholder receipt is not an issued specialist review. Placeholders exist only to preserve required routing and force a fail-closed outcome while review remains unavailable.

## Current Receipt Posture

All three Lai-route receipts are `placeholder_fail_closed` and return `DEFER`.

```text
review-receipt-lai-physics-foundations-v0-1
review-receipt-lai-mathematical-formalism-v0-1
review-receipt-lai-admissibility-governance-v0-1
```

## Supersession Rule

The current deferred decision may not be superseded until:

1. the source locator is `CONFIRMED` or `PARTIAL_WITH_STABLE_RETRIEVABLE_SOURCE`;
2. all required specialist receipts are issued;
3. no issued receipt remains `DEFER`, `INSUFFICIENT_EVIDENCE`, or `OUT_OF_SCOPE` for the promotion being considered;
4. source reconciliation and drift analysis are completed;
5. a new promotion decision is created; and
6. the new decision points to the prior decision as superseded rather than deleting it.

## Current Evaluation

```text
current_decision_id: decision-lai-intake-defer-v0-1
locator_verification: UNRESOLVED
issued_receipt_count: 0
placeholder_receipt_count: 3
evaluation_result: DEFER_NO_SUPERSESSION
```

The evaluator must remain fail-closed. Placeholder receipts can never produce acceptance or automatic promotion.

## Reconstruction Chain

```text
source evidence
-> bibliographic intake
-> translation records
-> locator intake
-> specialist route
-> review output receipts
-> drift analysis
-> promotion decision
-> supersession pointer
-> preserved prior decision
```

## Validation

```bash
python scripts/check_review_receipts_and_supersession.py
```

Expected current output:

```text
REVIEW RECEIPTS AND SUPERSESSION: PASS - 3 receipts; result=DEFER_NO_SUPERSESSION
```

## Workflow Boundary

No new standalone workflow is introduced by this checkpoint. The repository's canonical validation chain remains the integration surface for later registration of this validator.

## Non-Claims

Review receipts and supersession records govern wiki record posture only. They do not prove the external paper, create peer review, validate physics, establish equivalence with GCAT or BCAT, or grant execution authority.
