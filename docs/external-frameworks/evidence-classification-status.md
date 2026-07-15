---
title: External Framework Evidence Classification Status
---

# External Framework Evidence Classification Status

## Purpose

This page records the current evidence strength of registered external frameworks using the fail-closed classification implemented by the compatibility-report generator.

A framework's inclusion, source citation, crosswalk, screenshot, profile description, or author commentary does not constitute comparative testing.

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

## Audited priority cohorts

| Framework | Current evidence class | Public source | Implementation or artifact package | Parameterized observation | Independent reproduction | Comparative claim allowed |
|---|---|---:|---:|---:|---:|---:|
| GLM | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| EVIDE | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| DecisionAssure | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| MindForge | `MENTION_ONLY` | No public canonical source attached | Required | No public result | No | No |
| Morrison Runtime | `PARAMETERIZED_OBSERVATION` | Yes | Public surface and repository references | Yes, bounded cases | No | No |
| ASRO | `ARTIFACT_REVIEWED` | Yes | Repository reference and non-authorizing fixture | No reproduced run | No | No |
| AAR | `SOURCE_REVIEWED` | Yes | Not attached | No | No | No |
| MITRE ATLAS | `SOURCE_REVIEWED` | Yes | External knowledge base | Not applicable as runtime result | No | No |
| OWASP Top 10 for LLM Applications | `SOURCE_REVIEWED` | Yes | External guidance; no implementation package attached | No | No | No |
| NIST AI RMF | `SOURCE_REVIEWED` | Yes | Voluntary guidance; no runtime implementation | No | No | No |
| ISO/IEC 42001 | `SOURCE_REVIEWED` | Yes | Management-system standard; no runtime implementation | No | No | No |
| EU AI Act | `SOURCE_REVIEWED` | Yes | Legal text; no runtime implementation | No | No | No |
| Policy Cards | `SOURCE_REVIEWED` | Yes | Paper only; schema or implementation package not attached | No | No | No |
| Runtime Governance for AI Agents | `SOURCE_REVIEWED` | Yes | Paper only; path-policy implementation not attached | No | No | No |
| CARE Runtime | `MENTION_ONLY` | No official public source confirmed | Screenshot-only intake | No | No | No |
| KPT | `AUTHOR_COMMENTARY` | Public positioning only; no versioned technical source | No implementation package | No | No | No |

## Cohort findings

### Source-reviewed crosswalks

GLM, EVIDE, AAR, MITRE ATLAS, OWASP Top 10 for LLM Applications, NIST AI RMF, ISO/IEC 42001, the EU AI Act, Policy Cards, and Runtime Governance for AI Agents have public source material and StegVerse crosswalks. Their pages do not attach sufficient implementation, observed-output, replay, or independent-reproduction evidence to support stronger classifications.

```text
evidence_class: SOURCE_REVIEWED
crosswalk_available: true
implementation_reviewed: false unless separately stated
reproduced: false
comparative_testing_claim_allowed: false
```

### ASRO

ASRO has a public source, repository reference, and non-authorizing Commitment Candidate fixture. The fixture supports artifact review but does not include a pinned release, raw attestation output, verifier payload, timestamped execution, replay command, or independent reproduction.

```text
evidence_class: ARTIFACT_REVIEWED
reproduced: false
comparative_testing_claim_allowed: false
```

### DecisionAssure and MindForge

Both remain intake-only records because no public canonical source or authorized artifact package is attached to their pages.

```text
evidence_class: MENTION_ONLY
artifact_package_required: true
public_result_claim_allowed: false
comparative_testing_claim_allowed: false
```

Private, remembered, conversational, or unpublished results remain outside the public evidence posture.

### CARE Runtime

CARE Runtime is supported only by a supplied screenshot and observed terminology. No official website, repository, specification, release, paper, or authorized artifact package is confirmed.

```text
evidence_class: MENTION_ONLY
source_status: SOURCE_BLOCKED_FAIL_CLOSED
screenshot_is_official_source: false
public_runtime_result_claim_allowed: false
comparative_testing_claim_allowed: false
```

### KPT

KPT has public positioning and author-attributed descriptive language, but no versioned technical framework source, repository, schema, API, white paper, or executable artifact is recorded.

```text
evidence_class: AUTHOR_COMMENTARY
source_status: SOURCE_BLOCKED_FAIL_CLOSED
technical_source_confirmed: false
public_runtime_result_claim_allowed: false
comparative_testing_claim_allowed: false
```

KPT is classified above `MENTION_ONLY` only because attributed public positioning is preserved. That positioning remains commentary and cannot establish technical compatibility, runtime behavior, or execution authority.

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

## Remaining external-framework audit queue

Priority and source-blocked cohorts are classified. Remaining work is durable and proceeds in sidebar order:

```text
1. policy, identity, provenance, and supply-chain framework families
2. guardrail and agent-protocol framework families
3. required-section compliance across every framework page
4. generated report regeneration under schema 0.7
5. generated page-status synchronization
6. orphan, registry, and navigation coverage
```

Each remaining page must be checked for source authority, evidence provenance, observation strength, machine-readable companion, reproduction path, missing fields, non-claims, and challenge path.

## Boundary

```text
source availability != implementation evidence
implementation evidence != observed behavior
observed behavior != reproduced behavior
reproduced behavior != execution authority
crosswalk != compatibility
publication != standing
```
