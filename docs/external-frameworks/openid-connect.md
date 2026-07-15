---
title: OpenID Connect
---
# OpenID Connect

## Status

```text
Relationship type: external framework crosswalk
Evidence class: SOURCE_REVIEWED
Page completeness: COMPLETE_WITH_EXTERNAL_GATES
Runtime observation: none attached
Independent reproduction: false
Comparative testing claim allowed: false
Execution authority claim allowed: false
Maintenance owner: admissibility-wiki External Frameworks audit
```

## Official Sources

- OpenID Connect Core: https://openid.net/specs/openid-connect-core-1_0.html
- AI-governance context: https://openid.net/tag/ai-governance/
- Source posture: official specification captured; no StegVerse relying-party or provider fixture is attached.

## Framework-Native Scope

OpenID Connect is an identity layer on OAuth 2.0. It enables a client to verify an end user's authentication at an OpenID Provider and obtain interoperable identity claims through ID Tokens and related endpoints.

## Evidence Provenance

| Evidence class | Current evidence | Status | Missing fields |
|---|---|---|---|
| Official framework source | Core specification | present | pinned publication snapshot hash |
| Implementation source | No provider/client release selected | missing | product, version, configuration |
| Observed behavior | No authentication flow captured | missing | request, response, token, validation output, timestamp |
| Reproduced behavior | No independent rerun | missing | replay procedure, test environment, second result |
| StegVerse analysis | Bounded crosswalk | present | common interoperability fixture |

## Relationship to Admissibility

```text
OpenID Connect asks: Did this provider authenticate the subject and issue claims acceptable to the relying party?
StegVerse Admissibility asks: Does this actor currently hold bounded authority to perform this action against this target and bind consequence?
```

Authentication and identity claims can contribute actor and session evidence. They do not establish current delegation, action scope, target permission, or commit-time validity.

## Execution Authority Boundary

```text
authenticated subject != authorized actor for every action
valid ID Token != current delegation
accepted issuer != consequence-binding authority
identity claim != transition admissibility
```

## Observation Boundary

```text
Pinned provider: none
Pinned client: none
Discovery document: none
ID Token fixture: none
Validation output: none
Timestamp and key-set snapshot: none
Independent replay: none
```

No interoperability or runtime result is claimed.

## StegVerse Analysis

| Criterion | Current result |
|---|---|
| Identity | OIDC may establish provider-asserted subject identity within a configured trust relationship. |
| Authority | Authentication does not prove action-level authority. |
| Policy | Issuer, audience, nonce, signature, time, and claim-validation policy must be explicit. |
| Delegation | Delegation requires separate scope and authority evidence. |
| Evidence | Tokens and validation records can support reconstruction if retained securely. |
| Replayability | Requires pinned provider/client configuration, keys, claims, and validation procedure. |
| Reconstructability | Depends on retained key sets, issuer metadata, token, and validation context. |
| Commit-time validity | Requires fresh identity, delegation, policy, action, target, and validity-window checks. |
| Failure behavior | Invalid issuer, audience, nonce, signature, or time claims must fail closed. |

## Commit-Time Interoperability Contract

```text
transition_id
issuer
subject
audience
authentication_time
id_token_digest
claim_set_digest
key_set_reference
validation_result
validation_timestamp
relying_party_id
policy_reference
delegation_reference
requested_action
target_system
validity_window
```

## Failure Classes

| Failure class | Applies | Notes |
|---|---:|---|
| Actor ambiguity | yes | Subject, client, operator, and executing service may differ. |
| Authority drift | yes | A valid session can outlive action authority. |
| Stale evidence | yes | Keys, sessions, account status, and claims change. |
| Delegation leakage | yes | Authentication may be overextended into authorization. |
| Replay divergence | yes | Provider configuration and keys can change validation results. |
| Evidence-class confusion | yes | Source review must not be described as an observed login flow. |

## Machine-Readable Companions

- Manifest: `docs/external-frameworks/openid-connect.json`
- Compatibility report: `docs/external-frameworks/reports/openid-connect.compatibility.json`
- Registry: `docs/external-frameworks/index.json`
- Canonical inventory: `static/external-frameworks/canonical-union-inventory.v1.json`

## Validation Completion Criteria

```text
pin one provider and relying-party implementation
publish configuration and discovery metadata
capture a bounded token-validation flow and raw output
publish key-set snapshot, timestamp, expected result, and replay steps
complete an independent rerun
route identity evidence into a Commitment Candidate without inheriting authority
```

## Non-Claims

OpenID Connect is not a StegVerse canonical formalism. Authenticated identity is not execution authority, current delegation, transition admissibility, certification, or general compatibility.

## Challenge Path

A challenge must identify the issuer, subject or claim, validation rule, source version, supporting evidence, and requested correction. Identity assertions receive only reconstructable standing.

## Next Safe Build Target

Publish one pinned provider/client token-validation fixture with raw validation output, key-set snapshot, immutable hashes, replay instructions, and an independent rerun.

This page reflects a bounded admissibility packet. Publication does not create standing.