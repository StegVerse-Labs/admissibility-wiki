---
title: Replay Example
---

# Replay Example

Replay is the act of checking whether a receipt and transition can be evaluated again against the declared policy and evidence posture.

## Example Command

```bash
python verify_transition.py \
  --transition examples/example.transition.allow.001.json \
  --receipt examples/receipt.example.001.json \
  --policy policies/policy.publish.v1.json
```

## Expected Result

```text
ALLOW: receipt matches transition, policy, authority class, and commit-time validity requirements.
```

## Rejection Case

A rejection case should show the same command returning `DENY` when policy, authority, evidence, identity, or context drift breaks admissibility.
