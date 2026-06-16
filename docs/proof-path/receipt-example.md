---
title: Receipt Example
---

# Receipt Example

A transition receipt records the decision basis for a transition.

## Example Receipt

```json
{
  "receipt_id": "receipt.example.001",
  "transition_id": "example.transition.allow.001",
  "decision": "ALLOW",
  "authority_class": "maintainer_publish",
  "policy_ref": "policy.publish.v1",
  "evidence_hash": "sha256:example-evidence-hash",
  "context_hash": "sha256:example-context-hash",
  "drift_detected": false,
  "commit_time_validity": true,
  "issued_at": "2026-06-15T00:00:00Z"
}
```

## Receipt Question

The receipt should help a reviewer determine whether the transition had standing when it bound.
