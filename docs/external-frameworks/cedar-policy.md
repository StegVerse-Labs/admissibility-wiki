---
title: Cedar Policy
---
# Cedar Policy

## Evidence posture

```text
evidence_class: IMPLEMENTATION_BUILT_HASHED_UNEXECUTED
source_evidence_class: SOURCE_REVIEWED
page_completeness: PARTIAL_RUNTIME_EVIDENCE_PENDING
runtime_observation: not_observed
independent_reproduction: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
```

## Published scope

Cedar is an authorization policy language and evaluation model for deciding whether a principal may perform an action on a resource in context.

Canonical source: https://docs.cedarpolicy.com/

StegVerse has selected and built a pinned Cedar CLI implementation and inspected the resulting build artifact. That evidence establishes implementation identity and binary provenance only. No Cedar authorization decision or StegVerse runtime interoperability result is claimed yet.

## Native terms

| Cedar term | Meaning here | StegVerse relationship |
|---|---|---|
| Principal | Actor or identity making a request. | Actor evidence; not current standing by itself. |
| Action | Requested operation. | Requested action in a Commitment Candidate. |
| Resource | Object acted upon. | Governed target requiring current scope. |
| Context | Additional request facts. | Evidence that must be current and attributable. |
| Authorization response | Permit or forbid decision. | Policy evidence; not execution authority. |

## Relationship to admissibility

```text
Cedar asks: Is this principal authorized for this action on this resource in this context?
StegVerse asks: May this transition bind consequence now under current authority, delegation, policy, evidence, and recoverability conditions?
```

Cedar authorization results can become policy and authority evidence for a Commitment Candidate. StegVerse still reconstructs current standing at the consequence boundary.

## Evidence Provenance

Canonical build observation:

```text
workflow run: 31272895338
job: build-selected-cedar-binary / 93141992388
artifact: cedar-selected-binary-build / 9026196254
artifact zip SHA-256: 7067090a90f5ba74384b7488522559f630120c9d32350f171283e7af92d7907b
implementation: cedar-policy-cli 4.11.0
pinned commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
resolved commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
build command: cargo build --locked --release -p cedar-policy-cli
build exit code: 0
Cargo.lock SHA-256: 6efd3893a3c32d463748edfbd8361152e26dd17964d61bbe94cc4a390cd887b1
compiled binary SHA-256: 2f85096e819a40b90a11d45e971c9bb1f6cc1024aa20f00bfc593893d7a3b6d3
binary size bytes: 16325032
binary executed after build: false
source build receipt SHA-256: 0b9004042129effeb9627fc952dd0fd497095c8e042b43c36f00db0aefb259d8
promotion candidate SHA-256: b500a8d0b42eb48236e5f603c706587fe2c259af81be2408ae33f4492e41cbec
promotion candidate state: READY_FOR_REGISTRY_PROMOTION_REVIEW
```

The build receipt was directly inspected before this page was advanced. Build success and binary hashing do not establish a policy decision, compatibility, standing, or execution authority.

## Observation Boundary

Current observed boundary:

```text
source implementation identity: observed and pinned
locked build: observed
compiled binary hash: observed
artifact inspection: observed
hash-only registry promotion: governed transition in progress
Cedar authorization output: not observed
StegVerse runtime compatibility execution: not observed
fresh-runner authorization replay: not observed
independent reproduction: not observed
```

The selected binary remains non-executing evidence until a separate governed runtime transition permits the existing Cedar capture path to invoke it.

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Principal identity is supplied to Cedar and must be established elsewhere. |
| Authority | Permit does not establish current consequence-binding authority. |
| Policy | Strong overlap when the exact policy set and schema are pinned. |
| Delegation | Delegation relationships require separate source and validity evidence. |
| Evidence | Request, entities, schema, policy set, response, binary identity, and build provenance can form an inspectable packet. |
| Replayability | Binary provenance is now pinned; policy/entity/request replay is still unobserved. |
| Reconstructability | Build provenance is reconstructable; authorization-result reconstruction remains pending runtime capture. |
| Failure behavior | Missing entities, schema errors, evaluator errors, or ambiguous scope must fail closed. |
| Interoperability | Cedar response can enter a Commitment Candidate as non-authorizing authorization evidence after runtime observation. |
| Execution authority | Not granted by source review, binary build, hash inspection, or registry promotion. |

## Commit-time interoperability contract

```text
transition_id
principal
action
resource
context
cedar_request
cedar_response
policy_set_reference
policy_set_hash
schema_reference
entity_store_reference
cedar_version
compiled_binary_sha256
policy_reference
delegation_reference
evidence_references
execution_context
validity_window
source_timestamp
```

## Failure Classes

| Failure class | Applies | Current evidence posture |
|---|---:|---|
| Semantic equivalence divergence | Yes | Cedar permit/forbid is not StegVerse ALLOW/DENY. |
| Authority drift | Yes | Authority can change between evaluation and consequence. |
| Stale evidence | Yes | Principal, resource, context, and entity relationships can become stale. |
| Delegation leakage | Yes | Entity relationships may overstate delegated scope. |
| Replay divergence | Yes | Schema, policy, entity, or evaluator changes may alter results. |
| Fail-open runtime error | Yes | Evaluation errors cannot become implicit permit. |
| Policy granularity gap | Yes | Authorization scope may be coarser than the governed transition. |
| Binary provenance mismatch | Yes | A runtime binary differing from the promoted SHA-256 must fail closed. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/cedar-policy.json
compatibility report: docs/external-frameworks/reports/cedar-policy.compatibility.json
selection registry: docs/external-frameworks/implementation-selection-gates.v0.1.json
selection evidence: docs/external-frameworks/implementation-selections/cedar-policy-cli-4.11.0.selection-evidence.json
build handoff: docs/external-frameworks/CEDAR_BINARY_BUILD_AUTOMATION_HANDOFF.md
promotion handoff: docs/external-frameworks/CEDAR_BINARY_PROMOTION_AUTOMATION_HANDOFF.md
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `cedar-policy`, the disputed claim or mapping, supporting source or artifact, and the requested evidence-class, completeness, or standing change. Evidence strength cannot increase without inspectable artifacts.

## Validation Completion Criteria

```text
pinned Cedar implementation and version: complete
locked build and binary hash observation: complete
current hash-only selection-registry binding: in progress
pinned schema, policy set, and entity store: pending runtime capture
shared authorization requests: pending runtime capture
predeclared expected boundaries: fixture present; runtime observation pending
raw responses and errors: pending runtime capture
timestamps and runtime configuration: build complete; authorization runtime pending
replay commands: authored; execution pending
fresh-runner rerun receipt: pending
non-claim language preserved: complete
```

## Benchmark relevance

`authority_boundary`, `semantic_equivalence_boundary`, `commitment_boundary`, `interoperability_path`

## Non-claims

Cedar inclusion does not create certification, equivalence, execution authority, or StegVerse standing. A successful build does not establish authorization behavior. Authorization evaluation is not independently reconstructed commit-time admissibility. This page does not claim live integration or general compatibility.

## Next Safe Build Target

Complete the governed hash-only registry promotion for binary `2f85096e819a40b90a11d45e971c9bb1f6cc1024aa20f00bfc593893d7a3b6d3`, preserve `execution_authorized=false`, revalidate provenance, then use the existing governed Cedar capture path to execute the pinned authorization fixture and retain raw output before any compatibility claim is advanced.

This page reflects bounded evidence-governance work. Publication does not create standing.
