---
title: OSCAL External Framework Crosswalk
---

# OSCAL External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: machine-readable security control and assessment language
Evaluated OSCAL release: 1.2.2
evidence_class: SOURCE_REVIEWED
page_completeness: COMPLETE_WITH_EXTERNAL_GATES
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
Evidence posture: PINNED_PUBLIC_MODEL_RELEASE + PINNED_PUBLIC_SAMPLE + BOUNDED_STEGVERSE_CROSSWALK
Runtime posture: NOT_AN_AUTHORITY_ENGINE
Standing: no standing created
Execution authority: none
```

## Official Source And Version

This evaluation is pinned to NIST **OSCAL 1.2.2**, the latest released OSCAL model reference identified by the official NIST reference and project release surfaces at the time of this evaluation.

```text
project: https://pages.nist.gov/OSCAL/
release reference: https://pages.nist.gov/OSCAL-Reference/models/v1.2.2/
release tag: https://github.com/usnistgov/OSCAL/releases/tag/v1.2.2
release: OSCAL 1.2.2
release date: 2026-04-30
```

A second pinned official source demonstrates actual public content using OSCAL 1.2.2:

```text
repository: usnistgov/oscal-content
repository tag: v1.5.0
sample: nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_PRIVACY-baseline_profile.json
Git blob SHA: 85025c21e392ab4d67ad4b4490bbff6871811945
document metadata version: 5.2.0
document oscal-version: 1.2.2
```

The model-release version, OSCAL content-repository release, and an individual OSCAL document's own version are distinct identities. This evaluation keeps them separate rather than treating any one version string as a substitute for the others.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources | Official NIST OSCAL project, OSCAL 1.2.2 release reference/tag, and official model documentation. | present_pinned_release | No current source-identity gap for the bounded model crosswalk. |
| Official Implementation Sources | Official `usnistgov/oscal-content` v1.5.0 profile sample pinned by path and Git blob SHA; document metadata records `oscal-version: 1.2.2`. | present_pinned_public_sample | No claim that this sample represents a deployed system. |
| Observed Behavior | Direct source inspection confirms a real official OSCAL profile sample with separate document version `5.2.0` and `oscal-version` `1.2.2`. No native authorization runtime behavior is claimed. | source_structure_observed | Native validator/converter execution is not claimed by this transition. |
| Reproduced Behavior | No independent validator/converter reproduction is claimed. | not_applicable_for_runtime_result | A separate frozen tool-execution packet would be required for an interoperability-runtime claim. |
| StegVerse Analysis | OSCAL control and assessment artifacts are mapped to Policy Reference, Evidence Posture, Review Posture, Reconstructability, Drift, and Fail-Closed behavior. Six bounded cases exercise freshness, reference, authority, and scope boundaries. | control_assessment_crosswalk | Canonical merged-state validation is the remaining local gate. |
| Interoperability Assessment | OSCAL artifacts can enter a Commitment Candidate as structured control/assessment evidence, but schema validity and machine readability do not create standing or authority. | bounded_crosswalk_pending_merged_validation | No independent interoperability certification is claimed. |
| Standing | Publication, schema validity, role declarations, and assessment results create no StegVerse standing. | none_created | Standing and delegation must be independently reconstructed at commit time. |

Evidence classification:

```text
F1: official NIST OSCAL 1.2.2 project/release/reference sources.
F2: official usnistgov/oscal-content v1.5.0 sample pinned by repository tag, exact path, and Git blob SHA; metadata exposes document version 5.2.0 and oscal-version 1.2.2.
S1: StegVerse interpretation of OSCAL artifacts as structured policy/control/assessment evidence rather than authority.
S2: six-family StegVerse governance mapping for schema/reference validity, evidence freshness, current authority, and semantic scope.
H1: any future claim of native tool interoperability, implementation effectiveness, certification, standing, or execution authority remains prohibited until separately observed and governed.
```

## Framework-Term Definitions

| Native OSCAL Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| OSCAL | NIST Open Security Controls Assessment Language, evaluated here at release 1.2.2. | new | Structured security-control and assessment evidence language; not an admissibility engine. |
| Catalog | Machine-readable collection of control definitions. | adjacent | May provide Policy Reference evidence. |
| Profile | Selection, tailoring, and organization of controls from one or more catalogs. | adjacent | May provide scoped policy evidence; profile validity does not establish transition authority. |
| Component Definition | Reusable description of how a component may implement controls or capabilities. | adjacent | Implementation-claim evidence; declaration is not operational proof. |
| System Security Plan | System-specific description of control implementation and system context. | adjacent | Evidence Posture and reconstruction input; not current execution authority. |
| Assessment Plan | Structured plan for evaluating control implementation. | adjacent | Review Posture input; a plan is not an observed result. |
| Assessment Results | Structured findings and observations produced by an assessment. | adjacent | Evidence Posture and Review Posture; findings do not create delegation. |
| Plan of Action and Milestones | Structured remediation/planning information for identified findings or risks. | adjacent | May inform corrective-action review and continuity; does not authorize consequence. |
| Control Mapping | Structured relationship among controls or control concepts. | adjacent | Supports translation/reconstruction; semantic mapping is not equivalence by itself. |
| `oscal-version` | Metadata indicating the OSCAL model version used to represent the document. | new | Required for interpretation/replay and must not be conflated with the document's own content version. |
| Document version | Version metadata belonging to the represented content/artifact. | new | Evidence-freshness identity distinct from OSCAL model release identity. |

## Published Scope

OSCAL provides machine-readable models for security controls and their lifecycle artifacts, including catalogs, profiles, component definitions, system security plans, assessment plans, assessment results, plans of action and milestones, and control mappings. NIST publishes model references and official content in machine-readable formats.

The pinned public sample demonstrates that a real official profile artifact carries both a content version and an OSCAL model version. This is useful for reconstruction and version discipline. It does **not** establish that any represented control is implemented, effective, current, applicable, or authorized for a specific transition.

## Relationship to Admissibility

OSCAL belongs upstream of commit-time admissibility as structured control and assessment evidence. Its documents can contribute current, provenance-bound evidence, but OSCAL does not itself determine standing, delegation, admissibility, or execution authority.

## StegVerse Analysis

The strongest currently supported StegVerse use is a bounded source-versioned crosswalk: preserve model/document identity, validate references and freshness, map control/assessment semantics, and fail closed when authority or action scope cannot be reconstructed.

The six StegVerse case families are bounded mapping tests, not native NIST runtime tests:

| Family | Expected StegVerse Posture |
|---|---|
| positive alignment | ALLOW only when the document is valid, references resolve, evidence is fresh, responsible party/delegation/policy are current, scope matches, and recoverability is satisfied. |
| framework denial / negative result | DENY when the represented control evidence fails the evaluated validation boundary. |
| authority / delegation failure | DENY even when the OSCAL document is valid if current responsible-party/delegation authority is absent. |
| stale / missing evidence | FAIL_CLOSED when assessment evidence is stale. |
| malformed / undefined result | FAIL_CLOSED when the evidence package cannot be validly interpreted or resolved. |
| semantic divergence guard | DENY when the requested action is outside the scope represented by the OSCAL evidence. |

## Failure Classes

```text
CONTROL_EVIDENCE_VALIDATION_DENIAL
AUTHORITY_DRIFT
STALE_CONTROL_EVIDENCE
FRAMEWORK_RUNTIME_ERROR
ACTION_SCOPE_DIVERGENCE
```

`FRAMEWORK_RUNTIME_ERROR` in the StegVerse fixture is a fail-closed test label for malformed/undefined evaluation input; it is not evidence that NIST OSCAL itself experienced a runtime failure.

## Commit-Time Interoperability Contract

```text
transition_id
oscal_model_type
oscal_document_reference
oscal_document_hash
oscal_version
document_version
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

Governance-chain placement:

```text
pinned OSCAL artifact + model version + document version + references/hashes
  -> Policy Reference / Evidence Posture / Review Posture
  -> freshness + reference-resolution + system/action-scope checks
  -> independent standing / delegation reconstruction
  -> Commitment Candidate evidence set
  -> commit-time admissibility decision
  -> consequence binding only when separately authorized
```

Machine readability improves transport, inspection, and reconstruction. It does not convert represented claims into truth or convert named responsible parties into current execution authority.

## Machine-Readable Companions

```text
manifest: docs/external-frameworks/oscal.json
benchmark mapping: docs/external-frameworks/benchmark-mappings/oscal.mapping.json
benchmark fixture: docs/external-frameworks/fixtures/oscal-benchmark-fixture.v0.1.json
governance fixture: tests/fixtures/external-frameworks/oscal-governance-compatibility-cases.v1.json
compatibility report: docs/external-frameworks/reports/oscal.compatibility.json
case families: 6
canonical workflow: .github/workflows/validate-chain-continuation.yml
```

## Claims Versus Demonstrated Abilities

| Question | Current Evidence |
|---|---|
| Is an official current OSCAL release pinned? | Yes: 1.2.2. |
| Is a real official OSCAL 1.2.2 content sample pinned? | Yes, by repository tag, path, and Git blob SHA. |
| Are OSCAL release version and document version kept distinct? | Yes. |
| Can OSCAL represent controls and assessment lifecycle artifacts? | Yes, per the official model reference. |
| Has StegVerse installed a six-family governance mapping? | Yes. |
| Has native OSCAL validator/converter execution been observed in this transition? | No. |
| Does schema validity prove represented controls are implemented or effective? | No. |
| Does an OSCAL responsible-party record establish current delegation? | No. |
| Does OSCAL establish StegVerse standing or execution authority? | No. |
| Is NIST certification or endorsement claimed? | No. |

## Non-Claims

```text
OSCAL is not a StegVerse canonical formalism.
OSCAL does not prove transition admissibility.
Schema-valid OSCAL content does not prove represented controls are implemented, effective, current, or applicable.
Responsible-party declarations do not independently establish current delegation.
Assessment findings are evidence, not consequence-binding authority.
Machine readability does not create standing.
The StegVerse six-case fixture is bounded crosswalk evidence, not NIST certification or endorsement.
Comparative testing claim allowed: false.
Execution authority claim allowed: false.
Publication creates no standing.
```

## Replay And Reconstruction Boundary

The current source-level packet is reconstructable from the pinned OSCAL release and pinned public sample identity. A stronger native interoperability claim would require a frozen validation/conversion tool version, exact input package, commands, raw output, timestamps, environment, expected output, and an independent replay or reconstruction receipt.

No such stronger runtime claim is made here.

## Validation Completion Criteria

The official model release, pinned public sample, version distinctions, terminology reconciliation, six-family mapping, governance-chain placement, failure boundaries, and non-authority language must all remain installed and validator-compatible. Canonical validation must observe OSCAL manifest, terminology, page remediation, benchmark mapping/fixture, report, provenance, and governance-compatibility checks without OSCAL-specific failures.

## Next Safe Build Target

After the current source-versioned bounded crosswalk is canonically validated, a stronger optional evidence transition may execute a frozen official OSCAL validation/conversion tool against the pinned sample, preserving exact tool version, command, raw output, timestamps, environment, source hashes, and replay receipt. That stronger transition is not required to claim the bounded source-reviewed terminal class and must not be inferred from page publication alone.

## Challenge Path

A challenge must identify the OSCAL source/release, model/document version distinction, affected model or artifact, disputed mapping, failure class, or authority boundary, and provide inspectable evidence for correction.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from referenced evidence, authority, and admissibility conditions.
