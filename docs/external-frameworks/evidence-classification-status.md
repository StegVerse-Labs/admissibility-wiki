---
title: External Framework Evidence Classification Status
---

# External Framework Evidence Classification Status

## Purpose

This page records the current public evidence strength and authored-page completeness of the External Frameworks inventory. Evidence strength and page completeness are independent dimensions.

```text
complete documentation != reproduced behavior
source review != implementation test
artifact review != independent reproduction
parameterized observation != comparative testing
publication != standing or execution authority
```

## Evidence Classes

```text
MENTION_ONLY
AUTHOR_COMMENTARY
SOURCE_REVIEWED
ARTIFACT_REVIEWED
PARAMETERIZED_OBSERVATION
REPRODUCIBLE_COMPARATIVE_TEST
```

Only `REPRODUCIBLE_COMPARATIVE_TEST` permits an independently reproducible comparative-result claim.

## Reproducibility Gate

All eight fields must be public and inspectable:

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

Missing fields fail closed and remain visible in the schema-0.7 compatibility report.

## Current Evidence Exceptions

| Framework | Evidence class | Reason for exception |
|---|---|---|
| DecisionAssure | `MENTION_ONLY` | No public canonical source or authorized artifact package attached. |
| MindForge | `MENTION_ONLY` | No public canonical source or authorized artifact package attached. |
| CARE Runtime | `MENTION_ONLY` | Screenshot-only intake; no confirmed official technical source. |
| KPT | `AUTHOR_COMMENTARY` | Attributed public positioning exists, but no versioned technical source or executable artifact is recorded. |
| ASRO | `ARTIFACT_REVIEWED` | Public source and a non-authorizing fixture exist, but no reproduced run. |
| Morrison Runtime | `PARAMETERIZED_OBSERVATION` | Bounded observations exist; raw payload, timestamps, runtime configuration, source hashes, replay commands, and independent reproduction remain incomplete. |
| Admissible Existence Seed Cycle | `ARTIFACT_REVIEWED` | Internal ecosystem status mirror, not an external framework. |
| Decision Authority Compatibility | `ARTIFACT_REVIEWED` | Internal ecosystem compatibility crosswalk, not an external framework. |

All other currently classified external-framework records remain `SOURCE_REVIEWED` unless their machine-readable report states a weaker fail-closed posture.

## Policy, Identity, Provenance, and Supply-Chain Cohort

The following 13 pages are now `COMPLETE_WITH_EXTERNAL_GATES` at the documentation level while remaining `SOURCE_REVIEWED` at the evidence level:

| Framework | Evidence class | Page completeness |
|---|---|---|
| Open Policy Agent | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| Cedar Policy | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| OSCAL | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| SPIFFE/SPIRE | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| W3C Verifiable Credentials | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| in-toto | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| SLSA | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| Sigstore | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| OpenID Connect | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| OAuth 2.0 | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| W3C Decentralized Identifiers | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| OpenLineage | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |
| W3C PROV | `SOURCE_REVIEWED` | `COMPLETE_WITH_EXTERNAL_GATES` |

Machine-readable cohort status:

```text
static/external-frameworks/policy-identity-provenance-page-remediation.v1.json
```

Regression validator:

```text
scripts/check_external_framework_page_remediation.py
```

The validator is invoked by `scripts/check_goal5_external_frameworks_all.py`, which is already called through `npm run validate:goal5-external-frameworks` in the canonical validation chain.

## Family-Level Boundary

```text
policy decision != execution authority
authentication != delegation
identity != authority
token validity != transition admissibility
credential verification != current standing
attestation != admissibility
provenance != legitimacy
lineage != truth
supply-chain conformance != runtime authority
```

## Canonical Machine-Readable Surfaces

```text
docs/external-frameworks/index.json
static/external-frameworks/canonical-union-inventory.v1.json
static/external-frameworks/sidebar-page-associations.v1.json
static/external-frameworks/sidebar-framework-artifact-bindings.v1.json
docs/external-frameworks/reports/*.compatibility.json
```

## Publication Rule

Generated results and page-status blocks must use the evidence class derived from machine-readable report fields. A narrative page must not display a stronger classification than its report.

```text
page claim strength <= report evidence class
report evidence class <= available public artifacts
```

## Remaining External-Framework Audit Queue

```text
1. Review the remaining framework pages against the authored-page standard.
2. Regenerate all reports and generated page-status blocks under schema 0.7 in the canonical workflow.
3. Observe and inspect the canonical validation result and uploaded artifacts.
4. Repair any directly observed generation, validation, build, deployment, or public-route failure.
5. Recalculate the complete External Frameworks section audit.
```

## Boundary

```text
source availability != implementation evidence
implementation evidence != observed behavior
observed behavior != reproduced behavior
reproduced behavior != execution authority
crosswalk != compatibility
page completeness != evidence promotion
publication != standing
```
