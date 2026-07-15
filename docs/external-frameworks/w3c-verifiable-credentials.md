---
title: W3C Verifiable Credentials
---
# W3C Verifiable Credentials

## Evidence posture

```text
evidence_class: SOURCE_REVIEWED
page_completeness: COMPLETE_WITH_EXTERNAL_GATES
runtime_observation: none attached
independent_reproduction: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
```

## Published scope

The Verifiable Credentials Data Model 2.0 defines a model for credentials and presentations involving issuers, holders, verifiers, credential status, and securing mechanisms.

Canonical source: https://www.w3.org/TR/vc-data-model-2.0/

Source snapshot posture: the W3C Recommendation is recorded, but no pinned securing mechanism, issuer policy, credential schema, status method, example credential, verification transcript, or independent replay receipt is attached.

## Native terms

| VC term | Meaning here | StegVerse relationship |
|---|---|---|
| Issuer | Entity making credential claims. | Claim-source identity requiring standing and policy review. |
| Holder | Entity possessing or presenting a credential. | Presenter identity; not necessarily the subject or authorized actor. |
| Verifier | Entity evaluating a credential or presentation. | Evidence evaluator; not automatic execution authority. |
| Credential subject | Entity about which claims are made. | Subject identity requiring correlation and freshness checks. |
| Credential status | Revocation or suspension information. | Freshness evidence that must be checked at commit time. |
| Verifiable presentation | Holder-mediated presentation of credentials. | Evidence package; not current standing by itself. |

## Relationship to admissibility

```text
Verifiable Credentials asks: Can these claims and their securing material be verified under the selected trust and status rules?
StegVerse asks: Do the claims establish current identity, standing, delegation, and permission for this exact transition at commit time?
```

A verified credential may become identity, claim, qualification, or status evidence. The verifier's trust decision, issuer legitimacy, current credential status, delegation scope, and the transition's consequence-binding authority remain distinct.

## Observation boundary

No public issuance, presentation, verification, status-check, or StegVerse interoperability observation is claimed.

```text
shared test vector: missing
raw output: missing
timestamp: missing
runtime configuration: missing
source version or hash: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Credentials can carry identity claims but do not independently establish current actor identity. |
| Authority | Verified claims do not automatically establish action-level authority. |
| Policy | Issuance and verification policy must be identified, current, and scoped. |
| Delegation | Delegation must be represented and validated separately unless explicitly carried and governed. |
| Evidence | Credential, presentation, proof, status, schema, issuer, and verification transcript can form evidence. |
| Replayability | Requires pinned data model, proof suite, resolver, status method, trust inputs, and verification configuration. |
| Reconstructability | Possible when complete credential, proof, status, resolver, and verification provenance is retained. |
| Failure behavior | Invalid proof, unresolved issuer, stale status, unsupported proof, or ambiguous subject must fail closed. |
| Interoperability | Verified claims can populate identity and qualification evidence in a Commitment Candidate. |

## Commit-time interoperability contract

```text
transition_id
actor
credential_subject
holder
issuer
verifier
credential_reference
credential_hash
presentation_reference
proof_mechanism
verification_method_reference
credential_schema_reference
credential_status_reference
status_checked_at
verification_transcript_reference
policy_reference
delegation_reference
evidence_references
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current evidence posture |
|---|---:|---|
| Semantic equivalence divergence | Yes | Credential validity is not transition admissibility. |
| Authority drift | Yes | Authority can change while a credential remains valid. |
| Stale evidence | Yes | Status, issuer standing, schemas, and verification methods can change. |
| Delegation leakage | Yes | Qualification or identity claims can be overread as delegated permission. |
| Replay divergence | Yes | Proof suites, resolvers, trust inputs, and status methods can alter verification. |
| Recoverability loss | Yes | Missing contexts, methods, status data, or issuer records impair reconstruction. |
| Source-claim mismatch | Yes | A valid signature does not prove claim truth or issuer legitimacy. |
| Actor ambiguity | Yes | Holder, subject, presenter, and acting principal may differ. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/w3c-verifiable-credentials.json
compatibility report: docs/external-frameworks/reports/w3c-verifiable-credentials.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `w3c-verifiable-credentials`, the disputed claim, trust assumption, proof or status mechanism, supporting source or artifact, and requested correction. Cryptographic verification alone cannot increase standing without current claim, issuer, policy, authority, and delegation evidence.

## Validation completion criteria

```text
pinned VC data model and proof mechanism
public credential and presentation vectors
issuer, schema, resolver, and status inputs
raw verification transcript and errors
status-check timestamp and validity window
predeclared expected StegVerse boundary
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`authority_boundary`, `evidence_freshness_boundary`, `reconstruction_boundary`, `interoperability_path`

## Non-claims

Credential verification is not execution authority. Issuer trust is not inherited automatically. Inclusion does not establish StegVerse standing. A valid proof does not independently prove claim truth, current delegation, or transition admissibility.

## Next safe build target

Attach one pinned credential and presentation verification packet with proof suite, issuer and schema references, status method and timestamp, raw verifier output, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from referenced evidence, authority, and admissibility conditions.
