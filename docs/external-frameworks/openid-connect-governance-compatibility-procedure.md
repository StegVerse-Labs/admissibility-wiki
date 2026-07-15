---
title: OpenID Connect Governance Compatibility Procedure
---
# OpenID Connect Governance Compatibility Procedure

## Current state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
case_families: 6
native_execution_observed: false
fresh_runner_replay_observed: false
governance_compatibility_observed: false
```

This procedure tests whether an OpenID Connect validation result can enter StegVerse as bounded identity evidence without being promoted into current delegation, action authority, target permission, or transition admissibility.

## Test contract

Fixture:

`tests/fixtures/external-frameworks/openid-connect-governance-compatibility-cases.v1.json`

Evaluator:

`scripts/run_openid_connect_governance_compatibility.py`

Expected receipt:

`reports/external-frameworks/openid-connect/openid-connect-stegverse-governance-compatibility-receipt.json`

## Required case families

| Family | Native posture | Expected StegVerse boundary |
|---|---|---|
| Positive alignment | Valid provider assertion and current governed fields | `ALLOW` |
| Framework denial | Invalid audience or rejected assertion | `DENY / IDENTITY_ASSERTION_DENIAL` |
| Authority failure | Valid identity assertion with revoked delegation | `DENY / AUTHORITY_DRIFT` |
| Stale evidence | Expired or stale token evidence | `FAIL_CLOSED / STALE_IDENTITY_EVIDENCE` |
| Runtime error | Malformed or undefined validation | `FAIL_CLOSED / FRAMEWORK_RUNTIME_ERROR` |
| Semantic divergence | Valid authentication outside requested action scope | `DENY / ACTION_SCOPE_DIVERGENCE` |

## Translation rule

```text
OpenID Connect validation
  -> provider-asserted identity evidence
  -> actor-correlation input
  -> not current delegation
  -> not action authorization
  -> not transition admissibility
```

StegVerse independently evaluates issuer and audience posture, token freshness, actor correlation, delegation, policy, action scope, target, execution context, and consequence authority.

## Runtime evidence still required

Promotion beyond the authored contract requires one pinned OpenID Provider and relying party, discovery metadata, key-set snapshot, ID Token fixture, raw validation transcript, timestamps, replay commands, and a fresh-runner result. Independent implementation reproduction remains a separate higher gate.

## Non-claims

Authentication is not action authority. A valid ID Token is not current delegation. Acceptance by a relying party is not a StegVerse `ALLOW`. This procedure does not certify OpenID Connect, create standing, or establish general compatibility.
