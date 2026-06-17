---
title: Drift Denial Example
---

# Drift Denial Example

A drift-denial example shows how a transition that appeared admissible earlier can become inadmissible at commit time because identity, authority, policy, evidence, review posture, context, or system state changed before the result could bind.

The key rule is: prior approval is not commit-time admissibility.

## Example Transition

```json
{
  "transition_id": "example.transition.drift-deny.001",
  "from_state": "approved_candidate",
  "to_state": "published",
  "actor": "repo_maintainer",
  "authority_class": "maintainer_publish",
  "policy_ref": "policy.publish.v1",
  "evidence_posture": "stale",
  "review_posture": "previously_approved",
  "drift_detected": true,
  "drift_type": "policy_changed_after_review",
  "decision": "DENY",
  "commit_time_validity": false
}
```

## Example Receipt

```json
{
  "receipt_id": "receipt.example.drift-deny.001",
  "transition_id": "example.transition.drift-deny.001",
  "decision": "DENY",
  "authority_class": "maintainer_publish",
  "policy_ref": "policy.publish.v1",
  "evidence_hash": "sha256:stale-evidence-hash",
  "context_hash": "sha256:changed-context-hash",
  "previous_context_hash": "sha256:old-context-hash",
  "drift_detected": true,
  "drift_type": "policy_changed_after_review",
  "review_posture": "previously_approved",
  "commit_time_validity": false,
  "issued_at": "2026-06-17T00:00:00Z"
}
```

## Replay Command

```bash
python verify_transition.py \
  --transition examples/example.transition.drift-deny.001.json \
  --receipt examples/receipt.example.drift-deny.001.json \
  --policy policies/policy.publish.v1.json
```

## Expected Result

```text
DENY: policy or context drift detected after prior review; commit-time validity is false.
```

## Interpretation

The transition is denied even though it was previously approved because the state used to approve it no longer matches the state present at commit time.

A review artifact can remain reconstructable while no longer being admissible as execution authority.

## Boundary

Drift denial does not erase the earlier review. It records that the earlier review no longer supplies enough standing for the transition to bind consequence now.

A new review or updated receipt may be required before the transition can be reconsidered.
