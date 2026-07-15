---
title: Open Policy Agent
---
# Open Policy Agent

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

Open Policy Agent is a general-purpose policy engine that evaluates structured input against policy and produces policy decisions.

Canonical source: https://www.openpolicyagent.org/docs/latest/

Source snapshot posture: official documentation is recorded, but no pinned OPA release, policy bundle hash, runtime configuration, raw decision log, or independent replay receipt is attached to this page.

## Native terms

| OPA term | Meaning here | StegVerse relationship |
|---|---|---|
| Input | Structured facts supplied for evaluation. | Evidence input; not standing by itself. |
| Policy | Rego rules and data used to evaluate input. | Policy reference that must remain current and scoped. |
| Decision | OPA evaluation output. | Commitment Candidate evidence; not execution authority. |
| Bundle | Deployable policy and data package. | Versioned source artifact requiring hash and custody evidence. |

## Relationship to admissibility

```text
OPA asks: What result follows from this input, policy, and data?
StegVerse asks: May this transition bind consequence at commit time under current identity, authority, policy, delegation, and evidence?
```

OPA can contribute a policy-decision artifact to a governed transition path. That decision is evidence about policy evaluation; it does not establish that the actor has current authority, that delegation remains valid, or that consequence may bind now.

```text
OPA input + policy -> policy decision
policy decision -> Commitment Candidate evidence
SPE -> reconstruct current standing
SPE result -> ALLOW / DENY / FAIL-CLOSED
```

## Observation boundary

No public StegVerse runtime observation is claimed on this page.

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

The compatibility report must remain `SOURCE_REVIEWED` until these fields are public and inspectable.

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | OPA evaluates supplied attributes; it does not independently establish actor identity. |
| Authority | An allow decision does not establish current consequence-binding authority. |
| Policy | Strong overlap: OPA can produce inspectable policy decisions when policy identity is pinned. |
| Delegation | Delegation must be supplied and reconstructed separately. |
| Evidence | Decision logs can become evidence when inputs, policy bundle, version, and output are retained. |
| Replayability | Possible only with pinned engine, bundle, data, input, and configuration. |
| Reconstructability | Partial until complete input and decision provenance are retained. |
| Failure behavior | Integration must fail closed on missing policy, undefined result, stale bundle, or evaluation error. |
| Interoperability | OPA output can route into a Commitment Candidate as non-authorizing policy evidence. |

## Commit-time interoperability contract

Minimum OPA-specific fields:

```text
transition_id
actor
requested_action
target_system
opa_input
opa_decision
opa_query
policy_bundle_reference
policy_bundle_hash
opa_version
data_reference
decision_log_reference
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
| Semantic equivalence divergence | Yes | OPA allow/deny must not be equated with StegVerse ALLOW/DENY. |
| Authority drift | Yes | Authority can change after policy evaluation. |
| Stale evidence | Yes | Policy bundles and input facts can become stale. |
| Delegation leakage | Yes | Supplied roles or claims may exceed current delegation. |
| Replay divergence | Yes | Different engine, bundle, data, or configuration can change output. |
| Fail-open runtime error | Yes | Undefined or errored evaluations must not authorize execution. |
| Source-claim mismatch | Yes | Documentation or policy labels may not match the deployed artifact. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/open-policy-agent.json
compatibility report: docs/external-frameworks/reports/open-policy-agent.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify the framework ID `open-policy-agent`, the disputed field or claim, the source or artifact supporting the correction, and whether the requested change affects source posture, evidence class, page completeness, or standing. No challenge may increase evidence strength without corresponding public artifacts.

## Validation completion criteria

```text
pinned OPA release or binary identity
pinned policy bundle and data hashes
shared input vectors
predeclared expected boundaries
raw decision outputs and errors
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`commitment_boundary`, `authority_boundary`, `unknown_trajectory_boundary`, `interoperability_path`

## Non-claims

OPA inclusion is not certification, equivalence, admissibility proof, or StegVerse standing. A policy allow result does not independently authorize consequence binding. This page does not claim live integration, production deployment, or general compatibility.

## Next safe build target

Attach one pinned OPA decision bundle with input, Rego and data hashes, raw output, runtime configuration, expected StegVerse boundary, replay command, and an independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
