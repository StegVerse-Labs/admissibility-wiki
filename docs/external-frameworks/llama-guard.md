---
title: Llama Guard
---
# Llama Guard

## Evidence posture

```text
evidence_class: SOURCE_REVIEWED
page_completeness: COMPLETE_WITH_EXTERNAL_GATES
runtime_observation: none attached
independent_reproduction: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
source_limitation: distribution page is not a complete canonical model-governance record
```

## Published scope

Llama Guard is a safety-classification model family intended to classify model inputs and outputs against a safety taxonomy.

Distribution source: https://ollama.com/library/llama-guard3

Source snapshot posture: the recorded source identifies a distributed model package, but does not provide a complete canonical record of model lineage, training, taxonomy governance, prompt contract, thresholds, or release authority.

## Native terms

| Model term | Meaning here | StegVerse relationship |
|---|---|---|
| Safety taxonomy | Categories used to classify content. | Policy-like evidence whose version and scope must be pinned. |
| Classifier output | Safety label or decision text. | Bounded model evidence; not an authorization result. |
| Prompt template | Instructions and format controlling classification. | Runtime configuration that materially affects output. |
| Model package | Distributed weights and metadata. | Source artifact requiring identity, hash, and custody evidence. |

## Relationship to admissibility

```text
Llama Guard asks: How does this content classify under this model, taxonomy, and prompt?
StegVerse asks: May the related transition bind consequence under current authority and evidence?
```

A classifier result can contribute safety-category evidence. It does not establish policy legitimacy, complete risk coverage, actor standing, delegation, or consequence-binding permission.

## Observation boundary

No public StegVerse Llama Guard runtime observation is claimed.

```text
shared test vector: missing
raw classifier output: missing
timestamp: missing
runtime and prompt configuration: missing
model package version or hash: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Model package identity is incomplete without canonical release provenance and hash. |
| Authority | Classifier output does not grant or revoke execution authority. |
| Policy | Taxonomy categories may resemble policy classes but do not inherit StegVerse legitimacy. |
| Delegation | Not established by content classification. |
| Evidence | Raw labels, scores, prompt, taxonomy, and runtime data can become evidence when retained. |
| Replayability | Requires exact weights, package hash, prompt template, taxonomy, parameters, and runtime. |
| Reconstructability | Partial until source provenance and complete inference trace are captured. |
| Failure behavior | Unknown label, parsing error, model failure, or taxonomy mismatch must fail closed. |
| Interoperability | Classification can enter a Commitment Candidate as non-authorizing safety evidence. |

## Commit-time interoperability contract

```text
transition_id
actor
requested_action
target_system
content_hash
model_family
model_package_reference
model_package_hash
taxonomy_reference
taxonomy_version
prompt_template_hash
runtime_parameters
raw_classifier_output
parsed_label
confidence_or_score_if_available
policy_reference
delegation_reference
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current boundary |
|---|---:|---|
| Taxonomy drift | Yes | Category meaning can change across model or taxonomy versions. |
| Distribution-source limitation | Yes | Package listing does not establish complete canonical provenance. |
| Semantic equivalence divergence | Yes | Safety label is not StegVerse ALLOW or DENY. |
| Threshold or prompt drift | Yes | Prompt and parameter changes can alter classification. |
| Coverage gap | Yes | Unrepresented risks cannot be treated as evaluated. |
| Replay divergence | Yes | Weights, runtime, tokenizer, or prompt changes can alter output. |
| Fail-open inference error | Yes | Missing or malformed output must not authorize execution. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/llama-guard.json
compatibility report: docs/external-frameworks/reports/llama-guard.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `llama-guard`, the model package, taxonomy, prompt, runtime, output, or source limitation at issue and provide public evidence supporting correction. A distribution listing alone cannot support stronger provenance or runtime claims.

## Validation completion criteria

```text
canonical model and taxonomy references
pinned package, weights, tokenizer, and hashes
pinned prompt template and runtime parameters
shared content vectors
predeclared expected boundaries
raw classifier outputs and parsing behavior
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`execution_boundary`, `semantic_equivalence_boundary`, `unknown_trajectory_boundary`, `evidence_freshness_boundary`

## Non-claims

Classifier output is not execution authority, certification, transition admissibility, or proof of complete safety coverage. The recorded distribution page is not treated as a complete canonical model-governance record.

## Next safe build target

Attach one pinned model package and taxonomy fixture with content vectors, prompt hash, raw outputs, runtime configuration, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
