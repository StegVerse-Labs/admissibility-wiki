---
title: External Framework Inventory Record-Type and Evidence Closure
---

# External Framework Inventory Record-Type and Evidence Closure

## Purpose

This record closes the evidence classification of the nine records that remained after the priority, source-blocked, and policy/identity/provenance/supply-chain cohorts.

It also corrects a taxonomy defect: not every record stored in the External Frameworks registry is itself an external framework.

## Reconciled inventory totals

```text
distinct records across registry and sidebar: 38
actual external-framework or external-convention records: 36
internal ecosystem records stored in the same inventory: 2
records with explicit evidence classification or internal-record disposition: 38
```

The two internal records are:

```text
Admissible Existence Seed Cycle
Decision Authority Compatibility
```

They remain visible because they explain ecosystem relationships, but they must not inflate the external-framework count.

## Remaining external records

| Record | Record type | Evidence class | Source posture | Page completeness | Comparative claim allowed |
|---|---|---|---|---|---|
| Agent Governance Playbook | external governance playbook | `SOURCE_REVIEWED` | Public versioned release referenced; asset and commit hashes not attached locally. | `PARTIAL` | No |
| KILLSWITCH.md / Emergency Stop Convention | external convention | `SOURCE_REVIEWED` | Public convention source; example implementation and replay fixture absent. | `PARTIAL` | No |
| Model Context Protocol | external protocol | `SOURCE_REVIEWED` | Canonical protocol specification referenced; no StegVerse tool-execution observation. | `PARTIAL` | No |
| Agent2Agent Protocol | external protocol | `SOURCE_REVIEWED` | Canonical protocol specification referenced; no StegVerse agent-runtime observation. | `PARTIAL` | No |
| Guardrails AI | external runtime guardrail framework | `SOURCE_REVIEWED` | Official project source referenced; no pinned configuration or runtime result. | `PARTIAL` | No |
| Llama Guard | external safety-classifier family | `SOURCE_REVIEWED` | Distribution source captured; canonical model-governance package and exact fixture absent. | `PARTIAL_SOURCE_LIMITED` | No |
| NeMo Guardrails | external runtime guardrail framework | `SOURCE_REVIEWED` | Official documentation referenced; no pinned rails, model, integration, or runtime result. | `PARTIAL` | No |

## Internal records

### Admissible Existence Seed Cycle

```text
record_type: INTERNAL_ECOSYSTEM_STATUS_MIRROR
evidence_disposition: INTERNAL_ARTIFACT_STATUS_REVIEWED
external_framework: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
```

The page explicitly states that it is an ecosystem seed-cycle status mirror and is not external in the same sense as third-party frameworks. It records internal artifacts and a bounded completion status, while independent reconstruction and current hash-chain receipts remain pending.

### Decision Authority Compatibility

```text
record_type: INTERNAL_ECOSYSTEM_COMPATIBILITY_CROSSWALK
evidence_disposition: INTERNAL_ARTIFACT_MAPPING_REVIEWED
external_framework: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
```

The page maps public wiki terminology to the canonical ST-004 decision-authority vocabulary in `StegVerse-Labs/repo-standards`. It is internal compatibility evidence, not an external-framework evaluation.

## Classification boundaries

```text
record inclusion != external-framework identity
public release reference != reviewed implementation
protocol specification != observed runtime behavior
guardrail configuration != current policy authority
classifier output != transition admissibility
internal compatibility mapping != external comparison
internal status mirror != independent reconstruction
```

## Page-completeness finding

The seven external pages are evidence-classified but remain structurally partial. The protocol and guardrail pages are particularly thin and generally omit:

```text
explicit missing-field matrix
machine-readable manifest and report link
source snapshot or hash
pinned implementation/configuration version
mapping or reproduction fixture
raw result and replay instructions
challenge path
maintenance owner
next bounded build target
```

## Inventory rule

Future reporting must distinguish:

```text
external framework records: 36
internal ecosystem records carried in the section: 2
distinct inventory records: 38
support/audit pages: 22
total External Frameworks sidebar pages: 48
```

No report should refer to all 38 records as external frameworks without noting the two internal records.

## Next actions

```text
1. Add the 18 sidebar-only external records to the machine-readable registry.
2. Add navigation or explicit non-public status for the 12 registry-only records.
3. Add record_type to every registry entry.
4. Require external_framework=true or false explicitly.
5. Generate one reconciled inventory from registry, sidebar, manifests, and reports.
6. Validate one-to-one page, manifest, report, navigation, and evidence-class coverage.
7. Remediate all PARTIAL framework pages to the required-section standard.
```

## Boundary

This closure classifies the current inventory. It does not certify any framework, prove compatibility, grant execution authority, or establish independent reproduction.