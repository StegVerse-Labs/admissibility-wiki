---
title: REFUSE Example
---

# REFUSE Example

A `REFUSE` result means the evaluator declines to process the proposed transition as requested because the request is outside declared scope, violates a boundary, lacks required framing, or attempts to make a claim the evaluator is not authorized to decide.

`REFUSE` is different from `DENY`. A denial evaluates a transition and finds it inadmissible. A refusal may reject the request form, scope, or authority claim before full admissibility evaluation.

## Example Transition

```json
{
  "transition_id": "example.transition.refuse.001",
  "from_state": "unknown",
  "to_state": "enforced",
  "actor": "external_requester",
  "authority_class": "none_declared",
  "policy_ref": "policy.scope.v1",
  "evidence_posture": "missing",
  "review_posture": "not_applicable",
  "decision": "REFUSE",
  "commit_time_validity": false
}
```

## Example Receipt

```json
{
  "receipt_id": "receipt.example.refuse.001",
  "transition_id": "example.transition.refuse.001",
  "decision": "REFUSE",
  "authority_class": "none_declared",
  "policy_ref": "policy.scope.v1",
  "refusal_reason": "transition_request_outside_declared_scope",
  "evidence_hash": null,
  "context_hash": "sha256:example-context-hash",
  "commit_time_validity": false,
  "issued_at": "2026-06-17T00:00:00Z"
}
```

## Replay Command

```bash
python verify_transition.py \
  --transition examples/example.transition.refuse.001.json \
  --receipt examples/receipt.example.refuse.001.json \
  --policy policies/policy.scope.v1.json
```

## Expected Result

```text
REFUSE: request is outside declared governance scope and does not provide a valid transition basis.
```

## Interpretation

The evaluator refuses the request because it does not declare a valid governed transition, authority class, or evidence basis within the evaluator's scope.

The refusal protects the governance boundary. It avoids pretending that the evaluator has authority over a transition it cannot observe, authorize, enforce, or prove.

## Boundary

A refused request can be resubmitted with a valid transition frame, authority class, evidence posture, and policy reference. The new request must be evaluated independently at its own commit-time boundary.
