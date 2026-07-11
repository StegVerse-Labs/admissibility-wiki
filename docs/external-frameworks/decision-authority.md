---
title: Decision Authority Compatibility
---

# Decision Authority Compatibility

<!-- GENERATED:EXTERNAL_FRAMEWORK_METADATA:START -->

## Generated Framework Metadata

This section is generated from the external-framework registry. Do not edit it manually.

- Framework ID: `decision-authority`
- Name: `Decision Authority Compatibility`
- Registry status: `SOURCED-CROSSWALK-PROVISIONAL`
- Testbench state: `SOURCE_RECORDED_CROSSWALK_PROVISIONAL`
- Manifest path: `docs/external-frameworks/decision-authority.json`
- Source reference: `StegVerse-Labs/repo-standards/schemas/decision-authority.schema.json`
- Metadata boundary: generated metadata is descriptive only; it does not create certification, endorsement, formalism adoption, admissibility proof, or execution authority.

<!-- GENERATED:EXTERNAL_FRAMEWORK_METADATA:END -->

<!-- GENERATED:EXTERNAL_FRAMEWORK_MAPPING:START -->

## Generated Transition Mapping

This section is generated from the framework manifest. Do not edit it manually.

| Field | Generated Value |
|---|---|
| `framework_identity` | Decision Authority Compatibility |
| `source_reference` | StegVerse-Labs/repo-standards/schemas/decision-authority.schema.json |
| `source_version` | canonical schema merged in repo-standards |
| `allowed_use_boundary` | compatibility evidence only |
| `claims` | public wiki values map to canonical ST-004 authority values |
| `non_claims` | no execution authority, admissibility proof, or commit-time standing |
| `input_artifact_type` | public vocabulary value |
| `output_artifact_type` | mapped ST-004 authority value |
| `actor_or_authority_model` | repo-standards defines canonical vocabulary; wiki records public compatibility only |
| `evidence_model` | source schema reference plus local compatibility record |
| `policy_or_rule_model` | ST-004 transition table authority vocabulary |
| `delegation_model` | not asserted by wiki entry |
| `decision_or_result_model` | ALLOW to allowed; DENY to denied; FAIL-CLOSED to fail-closed |
| `execution_authority_claim` | false |
| `receipt_or_trace_model` | manifest reference and compatibility report |
| `reconstruction_model` | source schema plus wiki mapping reconstruct the vocabulary relationship |
| `SPE_overlap` | authority vocabulary can support standing review but does not create standing |
| `StegVerse_ecosystem_overlap` | decision vocabulary reconciliation across repo-standards and wiki public doctrine |
| `fail_closed_conditions` | missing canonical schema, unmapped value, or authority overclaim |

Generated mapping is compatibility evidence only.

<!-- GENERATED:EXTERNAL_FRAMEWORK_MAPPING:END -->

<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:START -->

## Generated Evaluation Status

This section is generated from the framework manifest and compatibility report. Do not edit it manually.

- Framework ID: `decision-authority`
- Manifest: `docs/external-frameworks/decision-authority.json`
- Compatibility report: `./reports/decision-authority.compatibility.json`
- Evaluation result: `COMPATIBILITY_EVIDENCE_ONLY`
- Cycle status: `FIRST_FRAMEWORK_CYCLE_COMPLETE`
- Execution authority claim: `False`
- Posting source: generated compatibility report
- Generated status is descriptive compatibility evidence only.

<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:END -->

<!-- GENERATED:EXTERNAL_FRAMEWORK_ANALYSIS_BOUNDARY:START -->

## Generated Authored Analysis Boundary

This section is generated. Do not edit it manually.

- Framework ID: `decision-authority`
- Framework name: `Decision Authority Compatibility`
- Generated sections above this boundary may be rebuilt from registry, manifest, compatibility-report, and result artifacts.
- Authored analysis below this boundary may contain interpretation, notes, and framework-specific discussion.
- Generators must preserve authored analysis unless a future validator explicitly declares a migration path.
- Boundary rule: generated material is descriptive compatibility evidence only and does not create certification, endorsement, adoption, proof, or operational permission.

<!-- GENERATED:EXTERNAL_FRAMEWORK_ANALYSIS_BOUNDARY:END -->

## Purpose

This page records the compatibility relationship between the public wiki vocabulary and the canonical ST-004 decision authority vocabulary maintained in `StegVerse-Labs/repo-standards`.

## Status

```text
Relationship type: internal ecosystem compatibility crosswalk
Canonical StegVerse formalism source: repo-standards ST-004
Wiki role: public doctrine vocabulary reconciliation
Citation status: repository source
Evidence provenance status: compatibility mapping installed
```

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources | Canonical decision-authority schema in `StegVerse-Labs/repo-standards`. | present | Public release tag and source hash when available. |
| Official Implementation Sources | Local compatibility manifest and compatibility report. | present_repository_reference | Versioned release reference after repo-standards tag. |
| Observed Behavior | No runtime behavior is claimed. | not_applicable_for_runtime_result | Not a runtime-result page. |
| Reproduced Behavior | No independent runtime reproduction is claimed. | not_applicable | Not a runtime-result page. |
| StegVerse Analysis | Public wiki shorthand is mapped to canonical ST-004 authority values. | decision_vocabulary_crosswalk_with_page_provenance | Downstream repo-specific mapping reports. |
| Interoperability Assessment | Compatibility evidence only. | compatibility_evidence_only | Downstream adoption reports. |
| Standing | Sourced provisional with provenance section. | sourced_provisional_with_provenance_section | Release/tag evidence for canonical schema. |

Evidence classification:

```text
F1: repo-standards canonical decision-authority schema.
F2: local wiki manifest and compatibility report.
S1: StegVerse interpretation of public wiki shorthand against ST-004 authority vocabulary.
S2: mapping to transition table decision_or_result_model and execution authority boundary.
H1: downstream runtime adoption status until repo-local mappings are attached.
```

## Canonical source

```text
StegVerse-Labs/repo-standards/schemas/decision-authority.schema.json
```

## Observed wiki vocabulary

The current public transition framing uses:

```text
ALLOW
DENY
FAIL-CLOSED
```

## Framework-Term Definitions

| Native Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| Decision authority schema | Canonical ST-004 machine vocabulary for transition authority values. | new | Provides vocabulary constraints but does not establish admissibility. |
| ALLOW | Public wiki shorthand for a transition allowed by a governed decision path. | adjacent | Maps to `allowed` only when policy, delegation, evidence, and validation support it. |
| DENY | Public wiki shorthand for a transition that may not proceed. | adjacent | Maps to `denied`; denial itself remains receipt-bound. |
| FAIL-CLOSED | Public wiki shorthand for stopping in a safe non-executing state. | adjacent | Maps to `fail-closed` when evidence, authority, or standing is missing or inconsistent. |

## Mapping

| Wiki value | ST-004 authority value |
| --- | --- |
| `ALLOW` | `allowed` |
| `DENY` | `denied` |
| `FAIL-CLOSED` | `fail-closed` |
| `FAIL_CLOSED` | `fail-closed` normalized alias |
| `DEFER` | `requires-human-review` reserved |
| `ADVISORY_ONLY` | `advisory-only` reserved |

## Relationship To Admissibility

Decision vocabulary compatibility does not prove admissibility, execution authority, standing, certification, endorsement, or commit-time authority.

The mapping only helps reconstruct how public wiki shorthand relates to ST-004 transition-table authority values.

## Prohibited Claims

```text
Decision Authority Compatibility does not grant execution authority.
Decision Authority Compatibility does not prove transition admissibility.
Decision Authority Compatibility does not certify or endorse any downstream runtime.
Decision Authority Compatibility does not create commit-time standing.
```

## Boundary

This page is compatibility evidence only. It does not certify, endorse, grant execution authority, or create commit-time standing.
