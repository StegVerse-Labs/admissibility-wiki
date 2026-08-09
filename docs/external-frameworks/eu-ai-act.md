---
title: EU AI Act External Framework Crosswalk
---

# EU AI Act External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: legal/regulatory AI framework
Base act: Regulation (EU) 2024/1689 / CELEX 32024R1689
Current material amendment: Regulation (EU) 2026/1744 / CELEX 32026R1744
Wiki role: convergence, mapping, and relationship review
Evidence posture: OFFICIAL_LEGAL_ACTS_PINNED_MAPPING_OBSERVED_RUNTIME_NOT_APPLICABLE
Local completion posture: LOCAL_WORK_COMPLETE_BOUNDED_LEGAL_CROSSWALK
Crosswalk class: legal_obligation_crosswalk
General compatibility claimed: false
Legal advice claimed: false
Execution authority granted: false
```

## Official sources

```text
Base act:
Regulation (EU) 2024/1689 of 13 June 2024 (Artificial Intelligence Act)
Official Journal: OJ L, 2024/1689, 12.7.2024
ELI: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
CELEX: 32024R1689

Material amendment in force at this review:
Regulation (EU) 2026/1744 of 8 July 2026 (Digital Omnibus on AI)
Official Journal: OJ L, 2026/1744, 24.7.2026
ELI: https://eur-lex.europa.eu/eli/reg/2026/1744/oj
CELEX: 32026R1744
```

The 2026 amending regulation is part of the current source posture and must not be omitted when reconstructing the legal context. It changes portions of Regulation (EU) 2024/1689, including the staged application of certain high-risk-system provisions. This page records legal-source identity and bounded crosswalk semantics; it does not provide legal advice or determine whether a particular person or system is legally compliant.

## Current application-timeline boundary

The base Regulation entered into force on 1 August 2024 and retained a general application date of 2 August 2026, but Regulation (EU) 2026/1744 amended specific application dates. In particular, amended Article 113 provides later application for Chapter III Sections 1–3: 2 December 2027 for AI systems classified high-risk under Article 6(2) and Annex III, and 2 August 2028 for systems classified high-risk under Article 6(1) and Annex I. The amendment also makes Articles 102–110 applicable from 27 July 2026 and changes portions of the prohibited-practice timetable.

This timing record is evidence context only. A regulatory date becoming applicable does not itself establish StegVerse standing, delegation, transition admissibility, or execution authority.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Remaining gap |
|---|---|---|---|
| Official Framework Sources | Official EUR-Lex ELI/CELEX records for Regulation (EU) 2024/1689 and amending Regulation (EU) 2026/1744. | current_legal_sources_pinned | A later amendment or consolidation requires a new source review. |
| Official Implementation Sources | Legal/regulatory text rather than a runtime authorization implementation. | not_applicable_legal_text | A regulator, conformity-assessment, or compliance implementation is a separate evidence transition. |
| Observed Behavior | No native runtime behavior is claimed for legislation. | not_applicable_for_runtime_result | Runtime evidence must not be manufactured. |
| Reproduced Behavior | No independent runtime reproduction is claimed. | not_applicable | Not a runtime-result requirement for this bounded legal crosswalk. |
| StegVerse Analysis | Regulatory obligations, risk classification, documentation/traceability, human oversight, prohibited practices, and high-risk-system context mapped to admissibility primitives. | legal_obligation_crosswalk | Mapping remains bounded to identified legal sources and fixtures. |
| Interoperability Assessment | Installed mapping/report/contract surfaces exercised by hosted StegVerse validation. | bounded_crosswalk_observed | No legal opinion, certification, regulator endorsement, or execution authority. |
| Standing | Legal/regulatory context evidence only. | bounded | No actor standing, delegation, or execution authority inherited. |

Evidence classification:

```text
F1: official EUR-Lex identities and current relationship between Regulation (EU) 2024/1689 and Regulation (EU) 2026/1744.
S1: StegVerse interpretation of those legal sources as regulatory-obligation and review-context evidence.
S2: mapping to Policy Reference, Governance Boundary, Evidence Posture, Review Posture, Receipt-Bound Execution, Reconstructability, Triad Governance Model, Runtime Transition Governance, and Fail-Closed review.
H1: applicability to a specific entity, system, jurisdiction, or fact pattern requires separate legal and factual analysis and is not established here.
```

## Framework-Term Definitions

| Native EU AI Act Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| EU AI Act | Regulation (EU) 2024/1689 as currently modified by applicable amending acts. | new | Preserved as legal-framework terminology. |
| Regulatory obligation | A duty established by applicable legal provisions. | adjacent | May inform Policy Reference and Governance Boundary; not equivalent to execution authority. |
| Risk classification | Legal classification affecting which regulatory requirements apply. | adjacent | May inform Evidence Posture and Review Posture. |
| Documentation and traceability | Legally relevant records supporting inspection, compliance, or oversight. | adjacent | Related to Receipt-Bound Execution and Reconstructability. |
| Human oversight | Legally relevant human involvement or control requirements. | adjacent | Related to Triad Governance Model and Runtime Transition Governance. |
| Prohibited practice | AI practice restricted or prohibited by applicable provisions. | adjacent | May create a policy/legal deny condition; it does not create broader enforcement authority. |
| High-risk system | AI-system category subject to heightened requirements under applicable provisions. | adjacent | Related to Review Posture and Governance Boundary, with application dates that must remain current. |

## StegVerse testing actually observed

Canonical hosted validation run `31295861678` exercised the installed EU AI Act mapping, fixture, report, terminology, provenance, benchmark, and governance-contract surfaces. Relevant observed results included:

```text
EXTERNAL FRAMEWORK MANIFESTS: PASS
EXTERNAL FRAMEWORK TERMINOLOGY: PASS
EXTERNAL FRAMEWORK REPORTS: PASS
EXTERNAL FRAMEWORK EVIDENCE PROVENANCE: PASS
EXTERNAL FRAMEWORK BENCHMARK MAPPINGS: PASS
EXTERNAL FRAMEWORK BENCHMARK FIXTURES: PASS
EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS
eu-ai-act_case_families: 6
```

The repository-wide run remained fail-closed for unrelated workstreams. Those failures do not convert this legal crosswalk into authority and do not erase the directly observed EU-AI-Act surface validations.

## Six bounded governance cases

The installed compatibility fixture is explicitly simulation-only and tests six transition conditions:

| Case family | Legal-context input | Expected StegVerse treatment |
|---|---|---|
| Positive alignment | Current official legal reference and obligation context | `ALLOW` only if StegVerse standing, delegation, policy, evidence, and scope independently pass |
| Negative framework result | Mapped prohibited practice | `DENY` |
| Authority/delegation failure | Compliance context exists but delegation is invalid | `DENY` |
| Stale/missing evidence | Article/reference is stale or unverified | `FAIL_CLOSED` |
| Malformed/undefined input | Legal mapping cannot be deterministically evaluated | `FAIL_CLOSED` |
| Semantic divergence | Legal classification/reference is applied to the wrong scope | `DENY` |

These cases test StegVerse treatment of legal-context evidence. They are not court, regulator, or conformity-assessment decisions.

## Exact governance-chain position

```text
current EU legal source + applicable obligation/risk context
  -> Policy Reference / Governance Boundary
  -> Evidence Posture / Review Posture
  -> StegVerse standing + delegation reconstruction
  -> commit-time admissibility evaluation
  -> execution authority determination
  -> commitment / consequence
```

The legal framework can constrain policy and review posture. It does not independently establish who currently has authority to perform a StegVerse transition.

## Claims versus demonstrated abilities

| Claim or capability | Evidence-backed finding |
|---|---|
| Establishes EU harmonised rules on AI | Supported by the official base act and current amendment record. |
| Establishes staged application and risk/obligation structures | Supported by current official legal texts; dates must be reconstructed from the current acts rather than stale summaries. |
| Can inform StegVerse policy and review posture | Demonstrated by installed crosswalk surfaces and hosted validation. |
| Establishes that a specific system is legally compliant | **No; fact-specific legal analysis is outside this crosswalk.** |
| Provides legal advice | **No.** |
| Determines current StegVerse actor standing/delegation | **No.** |
| Decides commit-time admissibility | **No.** |
| Grants StegVerse execution authority | **No.** |
| Produces a native runtime authorization result | **Not applicable; legislation is not an authorization runtime.** |

## Failure Classes

```text
SOURCE_MISSING
SOURCE_VERSION_UNDEFINED
AMENDMENT_SET_STALE
LEGAL_REFERENCE_STALE
LEGAL_MAPPING_ERROR
PROHIBITED_PRACTICE
AUTHORITY_DRIFT
REGULATORY_SCOPE_DIVERGENCE
FACT_PATTERN_UNRESOLVED
LEGAL_ADVICE_OVERCLAIM
AUTHORITY_OVERCLAIM
```

## Validation Completion Criteria

A bounded legal crosswalk is locally complete when the official base act and material current amendment identity are pinned, stale pre-amendment timing is corrected, mapping/fixture/report surfaces validate, the six-family governance contract remains deterministic, terminology/provenance checks pass, governance-chain placement is explicit, and no legal-advice, certification, standing, or execution-authority claim is inferred.

## Next Safe Build Target

A later EU amendment, delegated/implementing act, authoritative consolidated text, regulator decision, or fact-specific compliance package is a new evidence transition. It must be ingested with its own source identity, effective/applicability dates, scope, and review posture rather than silently strengthening this record.

## Completion boundary

All locally executable work for this source-level legal crosswalk is represented by the official base-act identity, the current material amending act, corrected application-timeline boundary, installed mapping/fixture/report surfaces, six-family governance contract, hosted validation observation, terminology reconciliation, governance-chain placement, and explicit non-capabilities. No runtime execution is required or appropriate for legislation itself.

## Non-Claims

```text
The EU AI Act is not a StegVerse canonical formalism.
This page is not legal advice.
The EU AI Act does not prove transition admissibility.
Regulatory compliance does not automatically grant execution authority inside StegVerse.
StegVerse compatibility evidence is not EU certification, regulator endorsement, or a legal compliance determination.
```

## Challenge Path

A reader may challenge this reflection by identifying the legal source, provision or field, effective/applicability date, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.
