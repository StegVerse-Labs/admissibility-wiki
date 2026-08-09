---
title: NIST AI RMF External Framework Crosswalk
---

# NIST AI RMF External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: voluntary AI risk-management framework
Source version: NIST AI RMF 1.0 / NIST AI 100-1 / 2023-01-26
Source content SHA-256: 7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1
Wiki role: convergence, mapping, and relationship review
Evidence posture: SOURCE_CONTENT_HASH_PINNED_MAPPING_OBSERVED_RUNTIME_NOT_APPLICABLE
Local completion posture: LOCAL_WORK_COMPLETE_BOUNDED_CROSSWALK
Crosswalk class: risk_management_crosswalk
General compatibility claimed: false
Execution authority granted: false
```

## Official source

Pinned official publication record:

```text
NIST AI Risk Management Framework (AI RMF 1.0)
NIST AI 100-1
published: 2023-01-26
publication: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
source PDF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
doi: https://doi.org/10.6028/NIST.AI.100-1
source content SHA-256: 7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1
source size: 1946127 bytes
```

The immutable hash was captured from the official NIST PDF by repository-native workflow run `31290014846`. The hash-only workflow artifact is `9031064931`, digest `sha256:367f339c5f8b4175ec9381042876531abff2ecaa97afd59e1cf22fe0e5b421ad`. The durable receipt is `docs/external-frameworks/source-receipts/nist-ai-rmf-1.0.source.json`. The source PDF itself is not redistributed by this repository.

NIST describes AI RMF 1.0 as voluntary guidance intended to help organizations manage AI risks and incorporate trustworthiness considerations into the design, development, deployment/use, and evaluation of AI systems. That source claim is preserved here as framework-native context; it is not converted into StegVerse execution authority.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Remaining gap |
|---|---|---|---|
| Official Framework Sources | NIST AI RMF 1.0 / NIST AI 100-1 publication record plus official PDF content hash and durable receipt. | source_content_hash_pinned | No local source-identification gap. |
| Official Implementation Sources | NIST AI RMF is guidance rather than a runtime authorization implementation. | not_applicable_standard_framework | A future implementation/profile is a new evidence transition. |
| Observed Behavior | No native runtime behavior is claimed for the guidance document. | not_applicable_for_runtime_result | Runtime evidence must not be manufactured. |
| Reproduced Behavior | No independent NIST runtime reproduction is claimed. | not_applicable | Not required for this bounded guidance crosswalk. |
| StegVerse Analysis | Risk management, trustworthiness, lifecycle review, and evaluation support are mapped to admissibility primitives. | risk_management_crosswalk | Mapping remains bounded to cited source and installed fixtures. |
| Interoperability Assessment | StegVerse mapping/report/contract surfaces were exercised by hosted validation; the result is review evidence only. | bounded_crosswalk_observed | No certification, endorsement, or execution authority. |
| Standing | Risk/review evidence only. | bounded | No standing, delegation, or execution authority inherited. |

Evidence classification:

```text
F1: official NIST AI RMF 1.0 / NIST AI 100-1 publication identity and immutable official-PDF content hash.
S1: StegVerse interpretation of NIST AI RMF as risk-management and trustworthiness review context.
S2: installed mapping to Evidence Posture, Review Posture, Governance Boundary, Policy Reference, Runtime Transition Governance, Decision Continuity, and Admissible-Existence Validation Factory.
H1: any future NIST-endorsed implementation/profile or independent interoperability package is a separate evidence transition and is not implied by this crosswalk.
```

## Framework-Term Definitions

| Native NIST AI RMF Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| AI Risk Management Framework | Voluntary external AI risk-management guidance. | new | Preserved as NIST-native framework terminology. |
| Risk management | Identification, evaluation, prioritization, and treatment of AI-related risk. | adjacent | Related to Evidence Posture and Review Posture; not equivalent to admissibility. |
| Trustworthiness considerations | Qualities and considerations used to evaluate whether AI systems may be trusted in context. | adjacent | Related to Governance Boundary and Policy Reference; does not create standing. |
| AI lifecycle review | Review across design, development, deployment/use, and evaluation phases. | adjacent | Related to Runtime Transition Governance and Decision Continuity. |
| Evaluation support | Guidance and material supporting evaluation of AI systems. | adjacent | Related to the Admissible-Existence Validation Factory without granting certification. |

## StegVerse testing actually observed

Canonical hosted validation run `31286539431` at commit `adefe149ed651af9c9912c01e33eb0f89794304c` preserved `full-validation-chain-report` artifact `9030026096` with digest `sha256:882a69adccc4268ab7a5e9a850fbd535bef0a5f0c301cb3b9d28df0dfdce4fed`.

Within that hosted run:

```text
check_external_framework_governance_compatibility.py: PASS
nist-ai-rmf_case_families: 6
check_external_framework_benchmark_mappings.py: PASS
check_external_framework_benchmark_fixtures.py: PASS
check_external_framework_reports.py: PASS
```

Source reconstruction was subsequently strengthened by run `31290014846`, which fetched the official NIST PDF, validated PDF magic, and produced the immutable source receipt above.

This establishes that the NIST mapping/report/contract surfaces were actually exercised by StegVerse's canonical validation chain and that the exact official source content used for the crosswalk is reconstructably identified. It does **not** establish a native NIST runtime execution, independent NIST implementation reproduction, NIST endorsement, certification, standing, or execution authority.

## Six bounded governance cases

The compatibility contract tests six distinct transition conditions:

| Case family | NIST/RMF evidence posture | Expected StegVerse treatment |
|---|---|---|
| Positive alignment | Current risk/review evidence aligns with current policy and authority | `ALLOW` only if StegVerse authority/admissibility predicates independently pass |
| Negative framework result | Risk/review evidence indicates unacceptable posture | `DENY` |
| Authority/delegation failure | RMF evidence exists but current actor/delegation is invalid | `DENY` |
| Stale/missing evidence | Required current evidence is absent or stale | `FAIL_CLOSED` |
| Malformed/undefined input | Mapping cannot be evaluated deterministically | `FAIL_CLOSED` |
| Semantic divergence | Organization/lifecycle risk posture is applied to the wrong transition scope | `DENY` |

## Exact governance-chain position

```text
NIST AI RMF source/profile evidence
  -> Evidence Posture / Review Posture input
  -> Governance Boundary / Policy Reference context
  -> StegVerse standing + authority + delegation reconstruction
  -> commit-time admissibility evaluation
  -> execution authority determination
  -> commitment / consequence
```

NIST AI RMF sits **upstream of commit-time admissibility** as risk-management and review evidence. It does not independently perform StegVerse standing reconstruction, current delegation validation, target/consequence binding, or execution authorization.

## Claims versus demonstrated abilities

| Claim or capability | Evidence-backed finding |
|---|---|
| Provides AI risk-management guidance | Supported by the pinned and hashed official NIST publication. |
| Provides trustworthiness-oriented lifecycle guidance | Supported by the official framework description and StegVerse mapping. |
| Can inform StegVerse review/evidence posture | Demonstrated by the installed mapping fixture, report, and hosted validation PASS. |
| Determines current actor standing | **Not demonstrated / outside framework role.** |
| Reconstructs current delegation | **Not demonstrated / outside framework role.** |
| Decides commit-time admissibility | **Not demonstrated / explicitly not claimed.** |
| Grants execution authority | **No.** |
| Produces a native runtime authorization result | **Not applicable; AI RMF is guidance rather than an authorization runtime.** |

## Failure Classes

```text
SOURCE_MISSING
SOURCE_VERSION_UNDEFINED
SOURCE_HASH_MISMATCH
MAPPING_INCOMPLETE
EVIDENCE_STALE_OR_MISSING
AUTHORITY_OR_DELEGATION_INVALID
SEMANTIC_SCOPE_DIVERGENCE
MALFORMED_OR_UNDEFINED_MAPPING
AUTHORITY_OVERCLAIM
```

Any attempt to convert organization-level or lifecycle risk-management alignment into action-level permission fails closed at the StegVerse boundary.

## Validation Completion Criteria

This bounded evaluation is complete only when source identity and content hash are preserved, mapping/fixture/report surfaces validate, the six-family governance contract remains deterministic, terminology and provenance validators pass, and the public page continues to distinguish review evidence from standing, admissibility, certification, and execution authority.

## Next Safe Build Target

A later NIST-endorsed implementation, profile, or independent interoperability artifact may be ingested as a new evidence packet. It must not retroactively strengthen this bounded guidance crosswalk without its own provenance, validation, and authority review.

## Completion boundary

All locally executable work required for this bounded standards-framework evaluation is represented: official source/version identification, immutable source-content receipt, installed mapping fixture, benchmark mapping, compatibility report, six-family StegVerse governance contract, hosted validation observation, claims-versus-capabilities analysis, terminology reconciliation, governance-chain placement, failure classes, and explicit non-capabilities.

Because NIST AI RMF 1.0 is a guidance framework rather than an authorization runtime, native runtime execution and runtime replay are not applicable completion requirements and must not be manufactured. A future NIST-endorsed implementation, profile, or external interoperability package would constitute a new evidence transition rather than a missing local task in this bounded AI RMF 1.0 crosswalk.

## Non-Claims

```text
NIST AI RMF is not a StegVerse canonical formalism.
NIST AI RMF does not prove transition admissibility.
Voluntary risk-management guidance does not grant execution authority.
StegVerse compatibility evidence is not NIST certification or endorsement.
Hosted validation of the crosswalk is not native NIST runtime execution.
```

## Challenge Path

A reader may challenge this reflection by identifying the claim, challenged field, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.
