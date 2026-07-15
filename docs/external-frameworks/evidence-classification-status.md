---
title: External Framework Evidence Classification Status
---

# External Framework Evidence Classification Status

## Purpose

This page records the current evidence strength of registered external frameworks using the fail-closed classification implemented by the compatibility-report generator.

A framework's inclusion, source citation, crosswalk, or author commentary does not constitute comparative testing.

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

## First cohort audit

| Framework | Current evidence class | Public source | Implementation or artifact package | Parameterized observation | Independent reproduction | Comparative claim allowed |
|---|---|---:|---:|---:|---:|---:|
| GLM | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| EVIDE | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| DecisionAssure | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| MindForge | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| Morrison Runtime | `PARAMETERIZED_OBSERVATION` | Yes | Public surface and repository references | Yes, bounded cases | No | No |

## Framework-specific findings

### GLM

The public page contains an official source and a StegVerse vocabulary crosswalk. It contains no attached implementation package, parser fixture, raw output, or independent reproduction.

```text
evidence_class: SOURCE_REVIEWED
crosswalk_available: true
implementation_reviewed: false
reproduced: false
comparative_testing_claim_allowed: false
```

### EVIDE

The public page contains an official source and a post-event evidence/reconstructability crosswalk. It contains no deposited-record fixture, raw reconstruction output, or independent reproduction.

```text
evidence_class: SOURCE_REVIEWED
crosswalk_available: true
implementation_reviewed: false
reproduced: false
comparative_testing_claim_allowed: false
```

### DecisionAssure

The page currently describes a candidate trace-integrity and causal-continuity relationship, but no public canonical source or authorized artifact package is attached to the page.

```text
evidence_class: MENTION_ONLY
artifact_package_required: true
public_runtime_result_claim_allowed: false
comparative_testing_claim_allowed: false
```

Any private, remembered, conversational, or unpublished trace result remains outside the public evidence posture until an authorized package is attached.

### MindForge

The page currently describes a candidate historical-governance-review relationship, but no public canonical source or authorized artifact package is attached.

```text
evidence_class: MENTION_ONLY
artifact_package_required: true
public_runtime_result_claim_allowed: false
comparative_testing_claim_allowed: false
```

### Morrison Runtime

The report includes bounded parameterized observations, but its own fields state that raw audit payloads, timestamps, runtime configuration, and source hashes are missing.

```text
evidence_class: PARAMETERIZED_OBSERVATION
independently_reproducible: false
comparative_testing_claim_allowed: false
```

The observed cases may be described only as bounded captured observations. They are not certification, general compatibility, or independently reproducible comparison results.

## Publication rule

Generated results and page-status blocks must use the evidence class derived from machine-readable report fields. A narrative page must not display a stronger classification than its report.

```text
page claim strength <= report evidence class
report evidence class <= available public artifacts
```

## Next cohort

The next audit cohort is:

```text
ASRO
AAR
MITRE ATLAS
OWASP Top 10 for LLM Applications
NIST AI RMF
ISO/IEC 42001
EU AI Act
Policy Cards
Runtime Governance for AI Agents
```

These are expected primarily to be source-reviewed crosswalks unless implementation, observation, or reproduction artifacts are attached.

## Boundary

```text
source availability != implementation evidence
implementation evidence != observed behavior
observed behavior != reproduced behavior
reproduced behavior != execution authority
crosswalk != compatibility
publication != standing
```
