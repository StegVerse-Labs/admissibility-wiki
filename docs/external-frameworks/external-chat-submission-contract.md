---
title: External Chat Submission Contract
---

# External Chat Submission Contract

External Chat is the public compatibility-intake surface for frameworks, runtimes, protocols, policy systems, and governance tools that want to compare their own artifacts against the bounded external-framework criteria used by this wiki.

## Submission path

```text
External framework manifest or trace
-> External Chat JSON intake
-> bounded field mapping
-> missing-field and failure-class analysis
-> existing wiki report reconciliation when framework_id matches
-> compatibility evidence receipt
-> optional human review before any wiki update
```

## Minimum fields

```text
framework_id
framework_name
source_references
input_artifact_type
output_artifact_type
actor_or_authority_model
evidence_model
policy_or_rule_model
delegation_model
decision_or_result_model
receipt_or_trace_model
reconstruction_model
fail_closed_conditions
```

Optional submitted material may include a sample artifact, trace, decision result, policy reference, delegation reference, evidence references, runtime context, or reconstruction instructions.

## Returned result classes

```text
COMPATIBILITY_EVIDENCE_READY
PARTIAL_COMPATIBILITY_INTAKE
FAIL_CLOSED_BOUNDARY_REVIEW
```

`COMPATIBILITY_EVIDENCE_READY` means the minimum descriptive fields are present. It does not mean the framework was executed, independently reproduced, certified, endorsed, or found generally compatible.

`PARTIAL_COMPATIBILITY_INTAKE` means one or more required fields are absent. Missing fields remain visible and the result stays provisional.

`FAIL_CLOSED_BOUNDARY_REVIEW` means the submission asserted execution authority, commit-time authority, certification, or semantic equivalence in a way that conflicts with the non-claim boundary.

## Existing-report reconciliation

When `framework_id` matches an existing external-framework record, External Chat returns links to the corresponding wiki page and checked-in compatibility report.

The user may compare:

```text
submitted field coverage
existing transition-table mapping
failure classes
source posture
receipt or trace model
reconstruction posture
non-claim boundaries
```

Matching findings establish only structural overlap between the submitted description and the existing report. They do not establish semantic equivalence or current admissibility.

## Data handling boundary

```text
submission_retained = false
raw_artifact_published = false
wiki_record_created = false
execution_performed = false
review_required_before_publication = true
```

The public compatibility service evaluates the submitted JSON in memory. A result receipt identifies the evaluated content hash and result posture, but it is not a custody receipt or publication receipt.

## Authority boundary

```text
compatibility result != certification
compatibility result != endorsement
compatibility result != execution authority
compatibility result != commit-time admissibility
compatibility result != semantic equivalence
compatibility receipt != Master-Records custody
publication != standing
```

## Promotion path

A submission may advance toward a wiki record only after sourced review adds exact source references, implementation/version evidence, commands or reproduction steps where applicable, artifact hashes, observed outputs, and explicit non-claim language.

The existing evidence progression remains authoritative:

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> automation_readiness_review
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

External Chat does not skip any stage in that progression.

## Public surface

```text
https://stegverse-labs.github.io/Site/external-chat.html
```

## Mandatory footer

This page describes a bounded compatibility intake contract. Submission, evaluation, or publication does not create standing. Any reflected finding inherits only the standing that can be reconstructed from the referenced source, evidence, authority, and admissibility conditions.
