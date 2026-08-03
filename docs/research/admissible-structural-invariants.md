---
title: Admissible Structural Invariants
sidebar_label: Admissible Structural Invariants
---

# Beyond Structural Invariants: Admissibility of Invariant Preservation

## Status

```text
Research state: FORMALIZATION_CANDIDATE
Novelty claim: NOT_ASSERTED
Execution authority: NONE
Canonical owner: StegVerse-Labs/admissibility-wiki
Goal id: admissible-structural-invariants-v0.1
```

This note separates two predicates that are often collapsed:

1. whether a property remains unchanged through transformation; and
2. whether preserving that property remains authorized, purpose-consistent, recoverable, and admissible.

The distinction is motivated by continuity-governance cases in which perfect preservation can sustain the wrong objective, obsolete authority, a purpose-inverting boundary, or a relationship that remains coherent but is no longer legitimate.

## Source Observation

A public Continuity Science discussion proposed that identity persists because structural invariants survive admissible transformation. A response question asked whether an invariant is temporal, environmentally conditioned, or subject to decay. The author clarified that invariants need not be timeless; they are preserved within a continuity thread that may begin, evolve, or terminate.

This repository does not treat that exchange as proof of novelty or as an adopted external specification. It is recorded as a research stimulus. The StegVerse contribution under examination is the stronger separation between invariant preservation and the admissibility of preservation.

## Baseline Model

Let a system state be \(S_i\), a transformation be

\[
T_i : S_i \rightarrow S_{i+1},
\]

and a candidate invariant be \(I_k\). A conventional preservation condition is

\[
I_k(S_i)=I_k(S_{i+1}).
\]

Equivalently, where the notation is meaningful,

\[
T_i(I_k)=I_k.
\]

This proves preservation. It does not by itself prove that continued preservation is legitimate.

## Second-Order Admissibility Predicate

Define a reconstructed commit-time context

\[
C_i=(A_i,P_i,E_i,B_i,R_i,G_i),
\]

where:

- \(A_i\): authority and delegation state;
- \(P_i\): governing purpose and policy state;
- \(E_i\): evidence available at the decision boundary;
- \(B_i\): boundary and constraint state;
- \(R_i\): recoverability posture;
- \(G_i\): affected entity or multi-entity governance state.

Define the preservation-admissibility predicate

\[
\operatorname{AdmPres}(I_k,T_i,C_i) \in \{\text{ALLOW},\text{DENY},\text{REVIEW\_REQUIRED},\text{FAIL\_CLOSED}\}.
\]

A candidate continuity claim requires both:

\[
I_k(S_i)=I_k(S_{i+1})
\]

and

\[
\operatorname{AdmPres}(I_k,T_i,C_i)=\text{ALLOW}.
\]

Preservation is therefore necessary only when the governing specification declares it necessary; it is never sufficient by itself.

## Admissible Structural Invariant

**Admissible Structural Invariant** — A property whose preservation across a specified transformation remains authorized, evidence-supported, purpose-consistent, boundary-recoverable, and non-inverting for all materially affected entities at the applicable commit-time boundary.

This definition is scoped. It does not imply that the property is absolute, timeless, universal, or permanent.

## Domain of Admissibility

Rather than model an invariant as merely decaying with time, define an admissibility domain

\[
D(I_k)=\{C \mid \operatorname{AdmPres}(I_k,T,C)=\text{ALLOW}\}.
\]

An invariant can remain mathematically unchanged while the current context leaves \(D(I_k)\). In that case, the property did not decay; its authority to remain controlling expired, was superseded, or became purpose-inverting.

This distinction supports four different outcomes:

| Preservation | Admissibility | Interpretation |
| --- | --- | --- |
| preserved | ALLOW | continuity candidate survives this gate |
| preserved | DENY | stable but illegitimate continuation |
| changed | ALLOW | governed invariant succession or identity-preserving replacement may be possible |
| changed | DENY / FAIL_CLOSED | neither preservation nor governed succession is established |

## Invariant Succession

Continuity may require replacing a lower-order invariant while preserving a higher-order governing relation. Let \(I_k\) be superseded by \(I'_k\). A succession claim requires a receipt-bound relation

\[
\Sigma(I_k,I'_k,C_i),
\]

showing at minimum:

- the supersession authority;
- the reason for replacement;
- the governing purpose retained or intentionally changed;
- the evidence and policy references;
- the affected entities;
- the recoverability path;
- the commit-time determination;
- the receipt connecting predecessor and successor.

The higher-order continuity claim is not “nothing changed.” It is “the change was governed, reconstructable, and admissible.”

## Failure Classes

### Preserved-but-obsolete

The property remains stable after the authority or policy that justified it has expired.

### Preserved-but-purpose-inverting

Maintaining the property prevents convergence toward the purpose the property originally served.

### Preserved-but-unrecoverable

The property can be maintained only while operator authority or system coherence remains high; degradation removes a safe recovery path.

### Preserved-but-relationally-inadmissible

An invariant valid for one entity imposes an unauthorized or nonrecoverable constraint on another affected entity.

### Preserved-but-unreconstructable

The property appears stable, but the evidence needed to reconstruct why its preservation was authorized is unavailable.

## Multi-Entity Extension

For entities \(e_1,\ldots,e_n\), define entity-relative admissibility determinations

\[
\operatorname{AdmPres}_{e_j}(I_k,T_i,C_i).
\]

A system-wide determination must not silently collapse disagreement. A conservative aggregate is:

\[
\operatorname{AdmPres}^{*}=\text{ALLOW}
\]

only when every required standing class returns ALLOW and all quorum, conflict, and evidence rules are satisfied. Otherwise the result is DENY, REVIEW_REQUIRED, or FAIL_CLOSED according to the governing contract.

This changes continuity from a single-object identity question into a coupled governance problem: can the transition preserve or succeed the relevant structures without defeating another entity's standing, authority, recoverability, or legitimate purpose?

## Relationship to the StegVerse Governance Triad

| Layer | Question applied to invariants |
| --- | --- |
| Transition Governance | Is preservation or succession structurally constructable? |
| Admissibility Governance | May this invariant remain controlling at commit time? |
| Continuity Governance | Can the preservation or succession determination be independently reconstructed later? |

The triad prevents three invalid substitutions:

```text
preservation != legitimacy
stability != authority
reconstruction != admissibility
```

## Minimal Decision Record

A preservation-admissibility record should contain:

```text
record_id
continuity_thread_id
transition_id
candidate_invariant_id
pre_state_reference
post_state_reference
preservation_result
invariant_scope
affected_entities
authority_references
policy_references
evidence_references
purpose_consistency
boundary_recoverability
multi_entity_dispositions
commit_time
decision
reason_codes
supersession_reference
receipt_chain_reference
```

The machine-readable candidate record is maintained at:

```text
static/research/admissible-structural-invariants.v0.1.json
```

## Testable Propositions

### ASI-P1 — Preservation insufficiency

There exists a transition for which \(I(S_i)=I(S_{i+1})\) while preservation admissibility is DENY.

### ASI-P2 — Governed succession

There exists a transition for which \(I(S_i)\neq I(S_{i+1})\) while a receipt-bound invariant succession relation permits a higher-order continuity claim.

### ASI-P3 — Context-conditioned domain

A candidate invariant can move outside its admissibility domain without changing its represented value.

### ASI-P4 — Multi-entity conflict

An invariant can be admissible relative to one entity and inadmissible relative to another; a system-wide ALLOW requires an explicit aggregation and standing rule.

### ASI-P5 — Reconstruction independence

Preservation, commit-time admissibility, and later reconstructability are independently variable properties.

## Literature-Review Program

The novelty question remains open. Research must compare this formulation with primary literature in:

- invariant preservation, refinement, and simulation relations;
- temporal and dynamic authorization;
- runtime assurance and safety envelopes;
- deontic and defeasible logic;
- institutional and constitutional rule change;
- policy versioning and revocation;
- multi-agent norm conflict;
- identity criteria, persistence, and process ontology;
- category-theoretic morphisms and structure-preserving maps;
- provenance, auditability, and independently reconstructable decisions.

The review must distinguish exact precedent, partial analogue, vocabulary overlap, and a genuinely missing composition. No public novelty claim is admissible until sources, comparison records, and counterexamples are installed and reviewed.

## Current Determination

```text
Structural invariant preservation: NECESSARY IN SOME SPECIFICATIONS
Structural invariant preservation: NOT SUFFICIENT FOR GOVERNED CONTINUITY
Admissibility of preservation: FIRST-CLASS CANDIDATE PREDICATE
Novelty: NOT DETERMINED
Publication posture: RESEARCH NOTE
Execution authority: NONE
```
