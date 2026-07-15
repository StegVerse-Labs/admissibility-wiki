---
title: Cedar Policy
---
# Cedar Policy

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

Cedar is an authorization policy language and evaluation model for deciding whether a principal may perform an action on a resource in context.

Canonical source: https://docs.cedarpolicy.com/

Source snapshot posture: official documentation is recorded, but no pinned Cedar release, policy set hash, entity store, request vector, evaluator configuration, raw response, or independent replay receipt is attached.

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

## Observation boundary

No public Cedar execution or StegVerse interoperability observation is claimed.

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
| Identity | Principal identity is supplied to Cedar and must be established elsewhere. |
| Authority | Permit does not establish current consequence-binding authority. |
| Policy | Strong overlap when the exact policy set and schema are pinned. |
| Delegation | Delegation relationships require separate source and validity evidence. |
| Evidence | Request, entities, schema, policy set, and response can form an inspectable packet. |
| Replayability | Requires pinned evaluator, schema, policy set, entities, and request. |
| Reconstructability | Partial until all input and version provenance is retained. |
| Failure behavior | Missing entities, schema errors, evaluator errors, or ambiguous scope must fail closed. |
| Interoperability | Cedar response can enter a Commitment Candidate as non-authorizing authorization evidence. |

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
| Semantic equivalence divergence | Yes | Cedar permit/forbid is not StegVerse ALLOW/DENY. |
| Authority drift | Yes | Authority can change between evaluation and consequence. |
| Stale evidence | Yes | Principal, resource, context, and entity relationships can become stale. |
| Delegation leakage | Yes | Entity relationships may overstate delegated scope. |
| Replay divergence | Yes | Schema, policy, entity, or evaluator changes may alter results. |
| Fail-open runtime error | Yes | Evaluation errors cannot become implicit permit. |
| Policy granularity gap | Yes | Authorization scope may be coarser than the governed transition. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/cedar-policy.json
compatibility report: docs/external-frameworks/reports/cedar-policy.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `cedar-policy`, the disputed claim or mapping, supporting source or artifact, and the requested evidence-class, completeness, or standing change. Evidence strength cannot increase without public inspectable artifacts.

## Validation completion criteria

```text
pinned Cedar implementation and version
pinned schema, policy set, and entity store
shared authorization requests
predeclared expected boundaries
raw responses and errors
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`authority_boundary`, `semantic_equivalence_boundary`, `commitment_boundary`, `interoperability_path`

## Non-claims

Cedar inclusion does not create certification, equivalence, execution authority, or StegVerse standing. Authorization evaluation is not independently reconstructed commit-time admissibility. This page does not claim live integration or general compatibility.

## Next safe build target

Attach one pinned Cedar request packet containing schema, policies, entities, request, raw authorization response, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from referenced evidence, authority, and admissibility conditions.
