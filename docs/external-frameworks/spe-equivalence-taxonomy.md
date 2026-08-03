---
title: SPE Equivalence Taxonomy
---

# SPE Equivalence Taxonomy

## Purpose

This page preserves the session question: whether any governance products or frameworks are equivalent to the StegVerse Standing-Proof Engine (SPE) or to the commit-time admissibility governance framework, and which systems are closest, overlapping, or adjacent.

The answer is recorded as a bounded external-framework taxonomy, not as a claim of market exclusivity, certification, superiority, or final research closure.

## Core Finding

No located external framework in the current wiki inventory is treated as fully equivalent to SPE.

The closest systems overlap with SPE in one or more regions: policy decision, authorization, supply-chain provenance, runtime guardrails, evidence preservation, identity attestation, or AI risk management.

The differentiating StegVerse question remains:

```text
May this proposed transition bind consequence now, at the commit boundary, using reconstructable current standing rather than historical approval alone?
```

A framework can be useful, mature, and necessary without being equivalent to SPE.

## Relationship Classes

| Class | Meaning | Commit-Time Authority Reconstruction |
|---|---|---|
| Closest conceptual equivalent | Attempts to decide or gate action from evidence, policy, state, or consequence before execution. | Partial or candidate only. |
| Similar | Shares runtime decision, policy, authorization, or enforcement behavior. | Usually checks permissions or policy, not full admissibility standing. |
| Overlapping | Supplies a required evidence, provenance, identity, risk, or governance input to SPE. | Evidence input only. |
| Adjacent | Governs surrounding management, lifecycle, assurance, compliance, or documentation context. | Usually not a commit-bound execution gate. |
| Not equivalent | Valuable but answers a different question. | No direct reconstruction of commit-time standing. |

## Closest Conceptual Equivalents

| Framework or Product Family | Why It Is Close | Boundary |
|---|---|---|
| DecisionAssure-style causal-continuity trace review | Tests whether a trace can support authority reconstruction and causal-continuity claims. | Candidate interoperability target; does not become authority. |
| CARE Runtime-style public runtime-governance platform | Uses runtime-governance and consequence-boundary language relevant to StegVerse. | Source status remains bounded by available public evidence; no equivalence claim. |
| Open Policy Agent / Rego | Evaluates policy decisions at runtime from structured input. | Policy decision is not the same as admissibility, authority, evidence, custody, and standing reconstruction. |
| Cedar Policy | Provides authorization policy semantics and permit/forbid decisions. | Strong authorization overlap, but not a full transition admissibility framework by itself. |
| XACML / ABAC / PBAC policy engines | Mature access-control and policy-decision model. | Primarily access authorization, not transition admissibility or continuity reconstruction. |
| Zanzibar / OpenFGA relationship authorization | Determines relation-based permissions at scale. | Answers who can access what, not whether a proposed consequence-binding transition is admissible now. |
| Workflow approval gates and CI/CD deployment approvals | Gate commits, releases, deployment, or execution. | Often rely on prior approval states and environment rules; may not independently reconstruct authority at the commit boundary. |

## Similar Runtime or Policy Frameworks

| Framework or Product Family | Similar Region | SPE Boundary |
|---|---|---|
| Runtime governance for AI agents | Checks next actions, paths, policies, or operating constraints. | Similar runtime gate, but must still prove evidence, authority, delegation, and standing at commit. |
| Policy Cards | Machine-readable policy artifact and runtime obligations. | Can feed SPE policy references; does not itself prove standing. |
| Guardrails AI, NeMo Guardrails, Llama Guard | Runtime output/action constraint and model behavior guardrails. | Useful safety constraints, but not a full admissibility proof engine. |
| Model Context Protocol / Agent2Agent Protocol | Agent/tool context and interoperation surfaces. | Transport or interoperability context; can supply events or evidence but not admissibility alone. |
| Robotic or autonomous-system safety cases | Pre-execution safety and accountability evidence. | Safety-case evidence may overlap, but safety approval is not commit-time admissibility. |

## Overlapping Evidence and Provenance Frameworks

| Framework or Product Family | Overlap | SPE Boundary |
|---|---|---|
| in-toto | Supply-chain layout, steps, and signed provenance. | Strong evidence chain input; does not decide transition admissibility. |
| SLSA | Supply-chain assurance levels and provenance requirements. | Assurance input only unless bound to SPE standing rules. |
| Sigstore | Signing, transparency log, and artifact identity evidence. | Cryptographic evidence input, not governance authority. |
| W3C PROV / OpenLineage | Provenance and lineage modeling. | Reconstruction input, not authority decision. |
| W3C Verifiable Credentials / DID / OpenID Connect / OAuth2 | Identity, claims, delegation, and access-token ecosystems. | Can represent identity and delegation evidence; token validity is not full admissibility. |
| SPIFFE / SPIRE | Workload identity and attestation. | Strong identity and workload-standing input; not transition governance alone. |
| OSCAL | Control and assessment representation. | Compliance/control evidence input, not commit-time execution authority. |

## Adjacent Governance and Standards Frameworks

| Framework or Product Family | Adjacent Region | SPE Boundary |
|---|---|---|
| NIST AI RMF | AI risk management lifecycle and trustworthiness framing. | Management framework, not a commit-time execution gate. |
| ISO/IEC 42001 | AI management system standard. | Organizational governance system, not SPE-equivalent standing reconstruction. |
| EU AI Act | Legal and regulatory obligation framework. | External legal duties can constrain SPE, but do not implement SPE. |
| AI incident reporting / assurance registries | Records events, reports, and reviews. | Useful continuity and accountability surface; post-event record is not current authority. |
| Audit logs and SIEM platforms | Operational evidence and detection. | Auditability is not admissibility. |

## Unique StegVerse Positioning

The current unique or under-matched StegVerse capability is the combination of all of the following in one governed grammar:

```text
transition candidate
+ current authority and delegation
+ evidence posture
+ review posture
+ boundary recoverability
+ continuity and reconstruction obligations
+ fail-closed unknown handling
+ receipt-bound outcome
+ public non-authorizing observation
```

SPE is therefore not merely a policy engine, risk framework, provenance ledger, approval workflow, guardrail, trust framework, or compliance standard.

SPE is best described as a commit-time standing reconstruction and consequence-binding decision layer that can ingest those systems as evidence, policy, identity, or review inputs.

## Practical Classification

```text
Equivalent: none confirmed
Closest: DecisionAssure-style trace review; CARE Runtime-style runtime-governance platform; policy decision engines when wrapped with evidence and standing reconstruction
Similar: OPA, Cedar, XACML/PBAC/ABAC, Zanzibar/OpenFGA, runtime agent governance
Overlapping: in-toto, SLSA, Sigstore, W3C PROV, OpenLineage, VC/DID, OIDC/OAuth2, SPIFFE/SPIRE, OSCAL
Adjacent: NIST AI RMF, ISO/IEC 42001, EU AI Act, compliance programs, audit systems, lifecycle governance standards
```

## Non-Claims

```text
This taxonomy does not prove novelty.
This taxonomy does not prove no equivalent exists.
This taxonomy does not certify StegVerse.
This taxonomy does not invalidate any external framework.
This taxonomy does not grant execution authority.
This taxonomy does not convert external evidence into admissibility.
```

## Next Build Target

Turn this taxonomy into a machine-checkable relationship registry and validator so future sessions can add or reclassify frameworks without relying on chat memory.
