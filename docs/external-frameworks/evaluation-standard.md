---
title: External Framework Evaluation Standard
---

# External Framework Evaluation Standard

## Purpose

This standard defines how the Admissibility Wiki evaluates, compares, and documents external frameworks.

External framework pages must separate:

```text
what the framework claims
what the implementation shows
what was observed
what StegVerse analyzed
what remains hypothetical
```

This protects comparative fairness, prevents accidental endorsement, and keeps every interoperability claim traceable to evidence.

## Scope

This standard applies to every page under:

```text
docs/external-frameworks/
```

It also applies to any compatibility report, fixture, test artifact, or generated result used to support an external-framework page.

## Required Evidence Provenance Section

Every external framework page must include an Evidence Provenance section or an equivalent structured block.

The section must identify each available evidence class:

| Evidence Class | Required Question | Examples |
|---|---|---|
| Official Framework Sources | What does the framework say about itself? | Website, docs, whitepaper, official repo, release page. |
| Official Implementation Sources | What does the released implementation show? | Repository code, package, example, configuration, policy file. |
| Observed Behavior | What was actually observed in a captured run? | Test parameters, output, screenshot, audit payload, timestamp, version. |
| Reproduced Behavior | What was independently rerun and matched? | Local reproduction, CI reproduction, fixture replay. |
| StegVerse Analysis | What does StegVerse conclude from its own formalisms? | Transition Table mapping, Commitment Candidate, SPE result, AE reflection. |
| Interoperability Assessment | How can the external artifact compose with StegVerse? | Compatibility report, cooperative validation path, governed return path. |
| Standing | What is the current evidence posture? | Evidence grade, reconstruction status, validation completeness. |

A page must not blur these classes.

## Evidence Classification Codes

Use these codes to mark substantive statements, compatibility-report fields, or validation notes:

| Code | Name | Meaning |
|---|---|---|
| F1 | Framework Claim | Directly stated by the framework's official website, docs, paper, or public materials. |
| F2 | Framework Implementation | Directly observed in an official repository, release, package, or source artifact. |
| O1 | Direct Observation | Observed in a demo, test, or run, but not yet fully parameterized. |
| O2 | Parameterized Observation | Observed with input parameters, expected boundary, output, and source context recorded. |
| R1 | Reproduced Result | Independently reproduced from documented parameters. |
| S1 | StegVerse Analysis | Analysis performed using Admissibility, AE, SPE, or related StegVerse semantics. |
| S2 | Transition Mapping | Mapping to Transition Table, authority, policy, evidence, standing, or recoverability primitives. |
| I1 | Interoperability Result | Result from routing an external artifact through a StegVerse compatibility or Commitment Candidate path. |
| V1 | Validation Artifact | Machine-readable artifact, fixture, report, receipt, or generated status file. |
| H1 | Hypothesis | Plausible explanation or future investigation, explicitly marked as non-result. |

## Claim Traceability Rule

Every substantive statement must answer:

```text
Where did this come from?
```

Valid answers include:

```text
official website
repository source
paper or specification
captured observation
reproduced test
StegVerse analysis
compatibility report
hypothesis
```

If the source class cannot be identified, the statement must be removed, rewritten as a question, or marked as `H1`.

## Comparative Fairness Rule

Every external framework must be evaluated against the same admissibility criteria where applicable:

```text
identity
authority
policy
delegation
evidence
standing
recoverability
replayability
reconstructability
commit-time validity
failure behavior
interoperability
governed return path
```

No framework may receive a custom easier standard unless the page explicitly records why the criterion is not applicable.

## Observed Behavior Rule

Observed behavior may be recorded only at the strength supported by its evidence.

```text
Observation without parameters -> internal observation only.
Observation with parameters but no raw output -> bounded partial observation.
Observation with parameters, output, timestamp, and source version -> public observation candidate.
Observation independently reproduced -> reproduced result.
```

Observed behavior must not be generalized beyond the captured evidence.

## Required Runtime Result Artifact Set

A runtime result claim should include:

```text
input prompt or planner output
selected demo, repository version, release, or commit
runtime configuration
policy or rule set
expected boundary
observed output
returned audit evidence or trace
screenshot or raw payload
timestamp
source URL or commit hash
operator notes, if any
```

A page may still document an incomplete case, but it must mark the missing fields.

## Standard Boundaries

Every external framework page must preserve these boundaries:

```text
Framework claims remain framework claims.
Repository behavior remains implementation evidence.
Observed behavior is limited to the captured evidence.
StegVerse analysis is identified as StegVerse analysis.
Compatibility is not certification.
Standing is reconstructed from evidence and is never inherited from publication.
A generated compatibility report is evidence, not execution authority.
Publication does not create standing.
```

## Required Page Sections

Each external framework page should include, or explicitly mark not applicable:

```text
Status
Source
Evidence Provenance
Definition
Framework-Term Definitions
Relationship To Admissibility
Execution Authority Boundary
Observed Behavior or Observation Boundary
Parameterized Test Cases
StegVerse Analysis
Interoperability Assessment
Commit-Time Interoperability Contract
Failure Classes
Evaluation Result Posting
Crosswalk Targets
AE Reflection Metadata
Validation Completion Criteria
Non-Claims
Challenge Path
Mandatory Footer
Next Safe Build Target
```

## Failure-Class Catalog Requirement

Failure observations should be classified by kind rather than only pass/fail.

The canonical catalog is:

```text
docs/external-frameworks/failure-class-catalog.md
```

Framework pages may add framework-specific details, but should reuse canonical failure classes whenever possible.

## Machine-Readable Companion Requirement

Every external framework page should have a machine-readable companion or compatibility report that preserves:

```text
framework identity
source URLs
implementation references
evidence classes
observed tests
missing fields
StegVerse analysis posture
interoperability status
boundary/non-claim flags
next required action
```

The report must not claim certification, endorsement, execution authority, or general compatibility unless an explicit governance process later authorizes such a claim.

## Completion Levels

| Level | Meaning |
|---|---|
| Intake | Framework identified; insufficient source or artifact evidence. |
| Sourced | Official source or authorized artifact identified. |
| Parameterized | At least one test or artifact has parameters recorded. |
| Reconstructable | Inputs, outputs, versions, timestamps, and evidence are sufficient to reconstruct the observation. |
| Reproduced | A documented result was independently reproduced. |
| Interoperability-Tested | External artifact was routed through StegVerse Commitment Candidate or SPE path. |
| Public-Ready | Page passes evidence provenance, non-claim, compatibility, and validation checks. |

## Non-Claims

```text
This standard does not certify any external framework.
This standard does not grant execution authority.
This standard does not make external terminology canonical.
This standard does not treat source availability as validation.
This standard does not treat observation as general compatibility.
```

## Mandatory Footer

External-framework evaluation is evidence-governance work. Publication does not create standing. Standing must be reconstructed from source, evidence, authority, admissibility, and current commit-time conditions.
