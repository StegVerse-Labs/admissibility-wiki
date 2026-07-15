---
title: NeMo Guardrails
---
# NeMo Guardrails

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

NeMo Guardrails is a programmable framework for controlling conversational flows, content, topics, retrieval, and tool interactions around LLM applications.

Canonical source: https://docs.nvidia.com/nemo/guardrails/home

Source snapshot posture: official documentation is recorded, but no pinned package, rail configuration, model and retrieval stack, tool integration, raw event trace, or independent replay receipt is attached.

## Native terms

| NeMo Guardrails term | Meaning here | StegVerse relationship |
|---|---|---|
| Rail | Configured conversational or execution constraint. | Runtime boundary evidence; not inherited authority. |
| Colang or rail configuration | Logic defining flows and interventions. | Policy-like artifact requiring version and scope checks. |
| Input or output rail | Check around user input or model output. | Validation evidence; not commit-time admissibility. |
| Retrieval or execution rail | Constraint around retrieval or tools. | Preparation or execution evidence requiring separate authorization. |

## Relationship to admissibility

```text
NeMo Guardrails asks: Does this interaction follow the configured rails and flows?
StegVerse asks: May the resulting transition bind consequence under current authority and evidence?
```

Configured rails can contribute runtime-boundary and intervention evidence. Rail configuration, model behavior, retrieval state, policy legitimacy, delegation, and consequence authority remain separately reconstructable.

## Observation boundary

No public StegVerse NeMo Guardrails runtime observation is claimed.

```text
shared test vector: missing
raw rail event trace: missing
timestamp: missing
rail, model, retrieval, and tool configuration: missing
package and configuration hashes: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Rails evaluate interaction state; they do not establish actor standing. |
| Authority | A rail pass or block does not grant or revoke execution authority. |
| Policy | Rail logic may encode policy fragments, but legitimacy and current applicability remain external. |
| Delegation | Tool or retrieval access must be reconstructed separately. |
| Evidence | Rail events, model calls, retrieval records, tool traces, and configuration can become evidence. |
| Replayability | Requires pinned package, rail files, models, prompts, retrieval corpus, tools, and runtime. |
| Reconstructability | Partial until the full intervention and execution trace is retained. |
| Failure behavior | Missing rail, exception, unknown flow, or tool ambiguity must fail closed. |
| Interoperability | Rail outcomes can enter a Commitment Candidate as non-authorizing runtime evidence. |

## Commit-time interoperability contract

```text
transition_id
actor
requested_action
target_system
input_hash
rail_configuration_reference
rail_configuration_hash
nemo_guardrails_version
model_references
prompt_hashes
retrieval_context_reference
tool_registry_reference
raw_rail_events
intervention_result
policy_reference
delegation_reference
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current boundary |
|---|---:|---|
| Rail coverage gap | Yes | Unconfigured paths cannot be treated as governed. |
| Configuration drift | Yes | Rail, prompt, model, retrieval, or tool changes can alter behavior. |
| Semantic equivalence divergence | Yes | Rail pass or block is not StegVerse ALLOW or DENY. |
| Delegation leakage | Yes | Tool or retrieval access may exceed current delegation. |
| Replay divergence | Yes | External model, corpus, or integration changes can alter results. |
| Recoverability loss | Yes | Hidden intervention state can prevent reconstruction. |
| Fail-open runtime error | Yes | Exceptions and unknown flows must not authorize execution. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/nemo-guardrails.json
compatibility report: docs/external-frameworks/reports/nemo-guardrails.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `nemo-guardrails`, the disputed rail, configuration, integration, event, source, or claim and provide public evidence supporting correction. No evidence-strength increase is allowed without a complete replayable runtime trace.

## Validation completion criteria

```text
pinned package and rail configuration
pinned models, prompts, retrieval corpus, and tools
shared interaction vectors
predeclared expected boundaries
raw rail events and intervention traces
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`execution_boundary`, `preparation_boundary`, `commitment_boundary`, `unknown_trajectory_boundary`

## Non-claims

A rail pass is not transition admissibility. A rail block is not certification. Observed behavior depends on configuration, models, retrieval, integrations, and runtime context. This page does not claim live integration or general compatibility.

## Next safe build target

Attach one pinned rail configuration with shared interaction vectors, model and retrieval identities, raw events, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
