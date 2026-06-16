---
title: Transition Cell Example
---

# Transition Cell Example

This page defines a simple example transition cell for public explanation.

## Example

```json
{
  "transition_id": "example.transition.allow.001",
  "from_state": "draft",
  "to_state": "published",
  "actor": "repo_maintainer",
  "authority_class": "maintainer_publish",
  "policy_ref": "policy.publish.v1",
  "evidence_posture": "present",
  "review_posture": "not_required",
  "decision": "ALLOW",
  "commit_time_validity": true
}
```

## Interpretation

The proposed transition moves an artifact from draft to published.

The transition receives an `ALLOW` result because the actor authority class matches the policy reference, required evidence is present, and no review requirement prevents the result.
