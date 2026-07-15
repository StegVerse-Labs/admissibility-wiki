---
title: Guardrails AI
---
# Guardrails AI

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

Guardrails AI provides tooling for validating, constraining, and correcting model inputs and outputs through programmable validators and guardrails.

Canonical source: https://guardrailsai.com/

Source snapshot posture: official project material is recorded, but no pinned package, validator set, model configuration, raw validation output, correction trace, or independent replay receipt is attached.

## Native terms

| Guardrails AI term | Meaning here | StegVerse relationship |
|---|---|---|
| Guard | Validation and correction configuration. | Runtime evidence boundary; not policy authority. |
| Validator | Rule or model checking an input or output. | Bounded evaluator whose scope and version must be pinned. |
| Pass or fail | Result of configured validation. | Evidence about configured checks; not transition admissibility. |
| Correction or reask | Remediation behavior after validation failure. | New transition requiring separate review and trace retention. |

## Relationship to admissibility

```text
Guardrails AI asks: Does this input or output satisfy configured validators?
StegVerse asks: May the resulting transition bind consequence under current authority and evidence?
```

A guardrail result can contribute model-input or output-validation evidence. Validator selection, coverage, policy legitimacy, actor authority, delegation, and consequence scope remain separately reconstructable.

## Observation boundary

No public StegVerse Guardrails AI runtime observation is claimed.

```text
shared test vector: missing
raw validator output: missing
timestamp: missing
validator and model configuration: missing
package and validator versions: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | The framework evaluates content, not actor standing. |
| Authority | Validator pass or block does not grant or revoke execution authority. |
| Policy | Configured validators may encode policy fragments, but legitimacy and scope remain external. |
| Delegation | Not established by validation. |
| Evidence | Raw validator results, correction traces, and configuration can become evidence when retained. |
| Replayability | Requires pinned package, validators, models, prompts, thresholds, and input. |
| Reconstructability | Partial until every validator invocation and remediation step is captured. |
| Failure behavior | Missing validator, exception, timeout, or ambiguous correction must fail closed. |
| Interoperability | Results can route into a Commitment Candidate as non-authorizing safety evidence. |

## Commit-time interoperability contract

```text
transition_id
actor
requested_action
target_system
input_or_output_hash
guard_configuration_reference
validator_ids
validator_versions
model_references
thresholds
raw_validation_results
correction_or_reask_trace
policy_reference
delegation_reference
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current boundary |
|---|---:|---|
| Coverage gap | Yes | Unconfigured risks cannot be treated as checked. |
| Semantic equivalence divergence | Yes | Validator pass is not StegVerse ALLOW. |
| Configuration drift | Yes | Validator sets and thresholds can change outcomes. |
| Correction opacity | Yes | Reasks or corrections can introduce unreviewed changes. |
| Replay divergence | Yes | Model, prompt, package, or validator changes can alter results. |
| Fail-open runtime error | Yes | Exceptions and timeouts must not authorize execution. |
| Evidence-class confusion | Yes | Source-reviewed behavior must not be described as tested. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/guardrails-ai.json
compatibility report: docs/external-frameworks/reports/guardrails-ai.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `guardrails-ai`, the validator, configuration, result, source, or claim at issue and provide public evidence supporting correction. Evidence strength cannot increase without reproducible execution artifacts.

## Validation completion criteria

```text
pinned package and validator versions
pinned models, prompts, and thresholds
shared input and output vectors
predeclared expected boundaries
raw validation and correction traces
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`execution_boundary`, `preparation_boundary`, `semantic_equivalence_boundary`, `unknown_trajectory_boundary`

## Non-claims

A validator pass is not execution authority. A guardrail block is not StegVerse certification. Coverage is bounded by configured validators and observed behavior. This page does not claim live integration or general compatibility.

## Next safe build target

Attach one pinned validator suite with shared vectors, raw results, correction traces, runtime configuration, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
