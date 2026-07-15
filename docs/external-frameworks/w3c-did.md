---
title: W3C Decentralized Identifiers
---
# W3C Decentralized Identifiers

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

## Official Source

- DID Core editor draft: https://w3c.github.io/did/
- Source posture: editor draft captured; draft status is preserved and no resolver or method implementation is selected.

## Framework-Native Scope

Decentralized Identifiers define identifiers and DID documents containing verification methods, services, and controller relationships without requiring one centralized identifier registry. Resolution behavior and security properties remain dependent on the selected DID method and implementation.

## Evidence Provenance

| Evidence class | Current evidence | Status | Missing fields |
|---|---|---|---|
| Official framework source | W3C editor draft | present with caution | stable recommendation status, immutable source hash |
| Method specification | No DID method selected | missing | method version and security model |
| Implementation source | No resolver pinned | missing | resolver version, configuration, commit |
| Observed behavior | No resolution or proof verification run | missing | DID, document, output, timestamp |
| Reproduced behavior | No independent rerun | missing | replay command, environment, second result |
| StegVerse analysis | Bounded crosswalk | present | method-specific fixture |

## Relationship to Admissibility

```text
DID infrastructure asks: What identifier document, verification methods, services, and controller relationships resolve for this identifier?
StegVerse Admissibility asks: Does the current actor hold bounded authority for this action and consequence now?
```

DID resolution and proof verification can contribute identity and control evidence. They do not independently establish current delegation, action scope, policy validity, or transition admissibility.

## Execution Authority Boundary

```text
DID control != universal actor authority
resolution success != current delegation
verification method != permission for every action
identifier persistence != current standing
```

## Observation Boundary

```text
Selected DID method: none
Pinned resolver: none
DID document fixture: none
Verification proof fixture: none
Raw resolution output: none
Timestamp and method snapshot: none
Independent replay: none
```

No method-specific interoperability result is claimed.

## StegVerse Analysis

| Criterion | Current result |
|---|---|
| Identity | A DID may identify a subject or controller within a method-specific trust model. |
| Authority | Controller relationships do not by themselves prove action-level authority. |
| Policy | Method rules, resolver policy, verification-purpose rules, and target policy must be explicit. |
| Delegation | Delegation requires separate evidence tying actor, action, target, and validity window. |
| Evidence | DID documents and proofs can support reconstruction when versions and method state are retained. |
| Replayability | Requires pinned method, resolver, network state, DID document, and proof. |
| Reconstructability | Depends on historical resolution state, method registries, and retained evidence. |
| Commit-time validity | Requires current resolution plus independent authority and policy checks. |
| Failure behavior | Unresolvable, ambiguous, stale, or unverifiable identifiers must fail closed. |

## Commit-Time Interoperability Contract

```text
transition_id
did
did_method
did_document_digest
controller_relationships
verification_method
verification_purpose
resolution_result
resolution_timestamp
resolver_version
method_state_reference
policy_reference
delegation_reference
requested_action
target_system
validity_window
```

## Failure Classes

| Failure class | Applies | Notes |
|---|---:|---|
| Actor ambiguity | yes | Subject, controller, key holder, and executing actor may differ. |
| Authority drift | yes | Controller and verification-method state may change. |
| Stale evidence | yes | Cached DID documents may no longer be current. |
| Delegation leakage | yes | Identifier control can be overread as broad authority. |
| Replay divergence | yes | Method state or resolver behavior can alter results. |
| Source-claim mismatch | yes | Draft or method-specific behavior may be described too generally. |

## Machine-Readable Companions

- Manifest: `docs/external-frameworks/w3c-did.json`
- Compatibility report: `docs/external-frameworks/reports/w3c-did.compatibility.json`
- Registry: `docs/external-frameworks/index.json`
- Canonical inventory: `static/external-frameworks/canonical-union-inventory.v1.json`

## Validation Completion Criteria

```text
select one DID method and pin its specification
pin one resolver implementation and state source
publish a DID document and proof fixture
capture raw resolution and verification output with timestamp
publish replay commands and expected result
complete an independent rerun
route identity evidence into a Commitment Candidate without inheriting authority
```

## Non-Claims

DIDs are not a StegVerse canonical formalism. Identifier control and resolution success are not current delegation, transition admissibility, execution authority, certification, or general compatibility. This page does not treat the editor draft as a final recommendation.

## Challenge Path

A challenge must identify the DID method, resolver, document version, controller or proof claim, supporting evidence, and requested correction. Method-specific evidence cannot be generalized silently.

## Next Safe Build Target

Publish one pinned DID-method resolution and proof-verification fixture with raw output, historical state references, immutable hashes, replay instructions, and an independent rerun.

This page reflects a bounded admissibility packet. Publication does not create standing.