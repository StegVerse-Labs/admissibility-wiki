---
title: External Framework Evidence Classification Status
---

# External Framework Evidence Classification Status

## Purpose

This page records the current evidence strength of registered external frameworks using the fail-closed classification implemented by the compatibility-report generator.

A framework's inclusion, source citation, crosswalk, implementation reference, fixture, or author commentary does not by itself constitute comparative testing.

## Evidence classes

```text
MENTION_ONLY
AUTHOR_COMMENTARY
SOURCE_REVIEWED
ARTIFACT_REVIEWED
PARAMETERIZED_OBSERVATION
REPRODUCIBLE_COMPARATIVE_TEST
```

Only `REPRODUCIBLE_COMPARATIVE_TEST` permits an independently reproducible comparative-result claim.

## Reproducibility gate

All of the following must be public and inspectable:

```text
shared test vector
raw output
timestamp
runtime configuration
pinned source version or hash
replay commands
declared expected outcome
independent reproduction result
```

Missing fields fail closed and must be displayed rather than inferred.

## Audited framework cohorts

| Framework | Current evidence class | Public source | Implementation or artifact package | Parameterized observation | Independent reproduction | Comparative claim allowed |
|---|---|---:|---:|---:|---:|---:|
| GLM | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| EVIDE | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| DecisionAssure | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| MindForge | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| Morrison Runtime | `PARAMETERIZED_OBSERVATION` | Yes | Public surface and repository references | Yes, bounded cases | No | No |
| ASRO | `ARTIFACT_REVIEWED` | Yes | Public repository and non-authorizing fixture reference | No reproduced run | No | No |
| AAR | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| MITRE ATLAS | `SOURCE_REVIEWED` | Yes | External knowledge base; no test artifact attached | No | No | No |

## Framework-specific findings

### GLM

Official source and vocabulary crosswalk are present. No implementation package, parser fixture, raw output, or independent reproduction is attached.

```text
evidence_class: SOURCE_REVIEWED
comparative_testing_claim_allowed: false
```

### EVIDE

Official source and reconstructability crosswalk are present. No deposited-record fixture, raw reconstruction output, or independent reproduction is attached.

```text
evidence_class: SOURCE_REVIEWED
comparative_testing_claim_allowed: false
```

### DecisionAssure

No public canonical source or authorized artifact package is attached to the public page.

```text
evidence_class: MENTION_ONLY
artifact_package_required: true
comparative_testing_claim_allowed: false
```

Private, remembered, conversational, or unpublished trace results remain outside the public evidence posture.

### MindForge

No public canonical source or authorized artifact package is attached.

```text
evidence_class: MENTION_ONLY
artifact_package_required: true
comparative_testing_claim_allowed: false
```

### Morrison Runtime

Bounded parameterized observations are recorded, but raw audit payloads, timestamps, runtime configuration, source hashes, replay evidence, and independent reproduction remain absent.

```text
evidence_class: PARAMETERIZED_OBSERVATION
independently_reproducible: false
comparative_testing_claim_allowed: false
```

### ASRO

A public source, public repository reference, and non-authorizing Commitment Candidate fixture reference are present. This supports artifact review, but no pinned release, raw attestation output, verifier payload, timestamped run, replay command, or independent reproduction is attached.

```text
evidence_class: ARTIFACT_REVIEWED
fixture_is_execution_authority: false
independently_reproducible: false
comparative_testing_claim_allowed: false
```

### AAR

A public assessment source and StegVerse crosswalk are present. No implementation package, assessment schema, raw assessment output, or reproduction fixture is attached.

```text
evidence_class: SOURCE_REVIEWED
comparative_testing_claim_allowed: false
```

### MITRE ATLAS

The official knowledge-base source and threat-context crosswalk are present. No pinned technique snapshot, mapping fixture, raw output, or independent reproduction is attached.

```text
evidence_class: SOURCE_REVIEWED
knowledge_base_reference_is_runtime_result: false
comparative_testing_claim_allowed: false
```

## Publication rule

Generated results and page-status blocks must use the evidence class derived from machine-readable report fields. A narrative page must not display a stronger classification than its report.

```text
page claim strength <= report evidence class
report evidence class <= available public artifacts
```

## Remaining second-cohort audit

```text
OWASP Top 10 for LLM Applications
NIST AI RMF
ISO/IEC 42001
EU AI Act
Policy Cards
Runtime Governance for AI Agents
```

These are expected primarily to remain `SOURCE_REVIEWED` unless implementation, observation, or reproduction artifacts are actually attached.

## Boundary

```text
source availability != implementation evidence
implementation evidence != observed behavior
observed behavior != reproduced behavior
reproduced behavior != execution authority
crosswalk != compatibility
publication != standing
```
