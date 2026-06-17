---
title: ESCALATE Example
---

# ESCALATE Example

An `ESCALATE` result means the proposed transition cannot be allowed or denied solely by the current evaluator because the declared policy, authority, evidence, review posture, or boundary condition requires higher or different review.

`ESCALATE` is a governance result. It is not approval, denial, or execution.

## Example Transition

```json
{
  "transition_id": "example.transition.escalate.001",
  "from_state": "candidate",
  "to_state": "released",
  "actor": "repo_maintainer",
  "authority_class": "maintainer_release",
  "policy_ref": "policy.release.v1",
  "evidence_posture": "present",
  "review_posture": "quorum_required",
  "decision": "ESCALATE",
  "commit_time_validity": false
}
```

## Example Receipt

```json
{
  "receipt_id": "receipt.example.escalate.001",
  "transition_id": "example.transition.escalate.001",
  "decision": "ESCALATE",
  "authority_class": "maintainer_release",
  "policy_ref": "policy.release.v1",
  "evidence_hash": "sha256:example-evidence-hash",
  "context_hash": "sha256:example-context-hash",
  "required_review": "release_quorum",
  "review_posture": "quorum_required",
  "commit_time_validity": false,
  "issued_at": "2026-06-17T00:00:00Z"
}
```

## Replay Command

```bash
python verify_transition.py \
  --transition examples/example.transition.escalate.001.json \
  --receipt examples/receipt.example.escalate.001.json \
  --policy policies/policy.release.v1.json
```

## Expected Result

```text
ESCALATE: release policy requires quorum review before the candidate may become released.
```

## Interpretation

The transition is escalated because the actor has a relevant authority class, but the policy requires a quorum-level review before the transition can bind.

Escalation preserves the transition as reviewable work. It does not allow the transition to execute.

## Boundary

An escalation receipt should make the missing or required review path explicit. A later approval must be evaluated at its own commit-time boundary rather than inheriting standing from the escalation receipt.
