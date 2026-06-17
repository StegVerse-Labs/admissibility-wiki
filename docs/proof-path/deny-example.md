---
title: DENY Example
---

# DENY Example

A `DENY` result means the proposed transition does not have standing to bind consequence under the declared authority, policy, evidence, review, and context state present at commit time.

`DENY` is not a punishment, reversal, or post-hoc criticism. It is a commit-time admissibility result.

## Example Transition

```json
{
  "transition_id": "example.transition.deny.001",
  "from_state": "draft",
  "to_state": "published",
  "actor": "external_contributor",
  "authority_class": "contributor_suggest",
  "policy_ref": "policy.publish.v1",
  "evidence_posture": "present",
  "review_posture": "not_approved",
  "decision": "DENY",
  "commit_time_validity": false
}
```

## Example Receipt

```json
{
  "receipt_id": "receipt.example.deny.001",
  "transition_id": "example.transition.deny.001",
  "decision": "DENY",
  "authority_class": "contributor_suggest",
  "policy_ref": "policy.publish.v1",
  "evidence_hash": "sha256:example-evidence-hash",
  "context_hash": "sha256:example-context-hash",
  "drift_detected": false,
  "review_posture": "not_approved",
  "commit_time_validity": false,
  "issued_at": "2026-06-17T00:00:00Z"
}
```

## Replay Command

```bash
python verify_transition.py \
  --transition examples/example.transition.deny.001.json \
  --receipt examples/receipt.example.deny.001.json \
  --policy policies/policy.publish.v1.json
```

## Expected Result

```text
DENY: actor authority class may suggest, but does not have commit-time authority to publish under policy.publish.v1.
```

## Interpretation

The transition is denied because the actor can propose or suggest a change, but the declared policy requires an approved publishing authority before the transition may bind.

The evidence is present, but evidence presence alone is not enough. Authority, policy, review posture, and commit-time validity must also align.

## Boundary

A denied transition may still be useful as a proposal, draft, review artifact, or evidence object. It simply cannot bind consequence as the requested state transition.
