---
title: W3C DID Governance Compatibility Procedure
---
# W3C DID Governance Compatibility Procedure

## Current posture

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
```

This procedure tests how DID resolution, controller relationships, verification methods, and proof evidence may enter a StegVerse commit-time decision without treating identifier control as universal authority.

## Test assets

```text
fixture: tests/fixtures/external-frameworks/w3c-did-governance-compatibility-cases.v1.json
evaluator: scripts/run_w3c_did_governance_compatibility.py
result receipt: reports/external-frameworks/w3c-did/w3c-did-stegverse-governance-compatibility-receipt.json
canonical framework page: docs/external-frameworks/w3c-did.md
```

## Required cases

| Case family | DID evidence | Expected StegVerse result |
|---|---|---|
| Positive alignment | Current resolution, actor/controller match, valid method, current delegation and policy | `ALLOW` |
| Framework denial | Invalid identifier, document, or proof | `DENY` |
| Authority failure | Valid resolution but revoked or changed delegation | `DENY` |
| Stale evidence | Cached or superseded DID document or verification method | `FAIL_CLOSED` |
| Runtime error | Resolver, method-state, or proof-verification failure | `FAIL_CLOSED` |
| Semantic divergence | Valid DID control attributed to the wrong actor, action, or target scope | `DENY` |

## Translation boundary

```text
DID resolution -> identifier-document and method-state evidence
verification method -> control or proof evidence, not universal permission
controller relationship -> identity/control relationship, not current delegation
StegVerse -> independently evaluates actor control, policy, delegation freshness,
             target scope, execution context, recoverability, and consequence authority
```

## Current evaluator limitation

The evaluator uses predeclared resolution outcomes. No DID method, resolver, method-state source, DID document, historical resolution state, or proof-verification implementation has been executed. A passing evaluator result validates only the declared translation and decision contract.

## Runtime completion requirements

```text
pinned DID method specification
pinned resolver implementation and configuration
method-state or registry snapshot
DID document and verification-proof fixture
raw resolution and proof-verification output
timestamps and immutable hashes
same-environment replay
fresh-runner replay
expected and observed StegVerse outcomes
public machine-readable receipt
```

## Non-claims

DID control is not universal actor authority. Resolution success is not current delegation. A verification method is not permission for every action. This procedure does not certify DIDs, establish general compatibility, create standing, or grant execution authority.
