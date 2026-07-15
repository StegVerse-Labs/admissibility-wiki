---
title: OSCAL
---
# OSCAL

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

OSCAL provides machine-readable models for control catalogs, profiles, implementation descriptions, assessment plans, assessment results, and plans of action and milestones.

Canonical source: https://pages.nist.gov/OSCAL/

Source snapshot posture: the canonical NIST source is recorded, but no pinned OSCAL release, model profile, validation toolchain, sample assessment package, conversion output, or independent reconstruction receipt is attached.

## Native terms

| OSCAL term | Meaning here | StegVerse relationship |
|---|---|---|
| Catalog | Structured control definitions. | Policy/control source evidence. |
| Profile | Selected and tailored controls. | Scoped policy evidence requiring provenance. |
| Component definition | Reusable implementation description. | Implementation-claim evidence, not operational proof. |
| System security plan | System control implementation description. | Declared posture evidence. |
| Assessment results | Findings and observations from assessment. | Review evidence; not execution authority. |

## Relationship to admissibility

```text
OSCAL asks: How can controls, implementation claims, assessments, and findings be represented consistently?
StegVerse asks: Does the specific transition have current standing and permission to bind consequence now?
```

OSCAL artifacts may contribute structured control and assessment evidence to reconstruction. Machine readability improves transport and inspection but does not establish the truth, freshness, legitimacy, or consequence-binding authority of the represented claims.

## Observation boundary

No public OSCAL interoperability conversion or runtime validation result is claimed.

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

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | OSCAL can name parties and roles but does not prove current identity. |
| Authority | Control ownership and assessment roles do not create execution authority. |
| Policy | Strong overlap for structured policy and control references. |
| Delegation | Responsibility assignments require separate current delegation evidence. |
| Evidence | OSCAL can carry structured evidence references and findings. |
| Replayability | Requires pinned OSCAL version, profile, source package, validation tools, and conversion rules. |
| Reconstructability | Strong potential when source packages, references, and transformations are retained. |
| Failure behavior | Invalid models, unresolved references, stale assessments, or transformation loss must fail closed. |
| Interoperability | OSCAL records can enter a Commitment Candidate as structured control and assessment evidence. |

## Commit-time interoperability contract

```text
transition_id
oscal_model_type
oscal_document_reference
oscal_document_hash
oscal_version
profile_reference
control_references
assessment_result_references
responsible_party_references
validation_tool_reference
transformation_receipt
policy_reference
delegation_reference
evidence_references
source_timestamp
validity_window
```

## Failure classes

| Failure class | Applies | Current evidence posture |
|---|---:|---|
| Semantic equivalence divergence | Yes | OSCAL control status is not StegVerse admissibility. |
| Authority drift | Yes | Named roles may no longer hold current authority. |
| Stale evidence | Yes | Assessments and implementation claims age. |
| Replay divergence | Yes | Model versions and transformations can change meaning. |
| Recoverability loss | Yes | Broken references or missing source packages impair reconstruction. |
| Source-claim mismatch | Yes | Structured claims can diverge from actual implementation. |
| Evidence class confusion | Yes | Assessment results must not be presented as reproduced runtime behavior. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/oscal.json
compatibility report: docs/external-frameworks/reports/oscal.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `oscal`, the disputed mapping or source claim, the affected OSCAL model or version, supporting evidence, and the requested correction. A structured OSCAL record cannot increase standing merely because it validates against a schema.

## Validation completion criteria

```text
pinned OSCAL release and schemas
public source package and hashes
validation and transformation commands
raw validation or conversion outputs
reference-resolution results
timestamps and toolchain configuration
predeclared expected boundaries
independent reconstruction receipt
non-claim language preserved
```

## Benchmark relevance

`evidence_freshness_boundary`, `reconstruction_boundary`, `authority_boundary`, `interoperability_path`

## Non-claims

OSCAL inclusion is not certification, equivalence, transition admissibility, or execution authority. Schema-valid OSCAL content is not proof that the represented controls are implemented, current, effective, or authorized.

## Next safe build target

Attach one pinned OSCAL package with source hash, schema version, validation command, raw output, reference-resolution record, expected StegVerse evidence posture, and independent reconstruction receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from referenced evidence, authority, and admissibility conditions.
