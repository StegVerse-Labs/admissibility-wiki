---
title: Disciplinary Translation Groundwork
---

# Disciplinary Translation Groundwork

## Status

Canonical source posture: public-safe wiki groundwork

Wiki state: intake

Detail status: initial translation-groundwork section for mapping discipline-specific claims into transition-table language

## Purpose

Disciplinary Translation Groundwork defines the public-safe bridge between domain-specific formalisms and the Transition Table.

It does not claim that physics, biology, law, economics, AI governance, computer science, or social systems are the same discipline. It claims only that when a discipline describes a consequential change, the change can be represented as a state transition with explicit actors, states, boundary conditions, constraints, admissibility posture, consequence, and reconstruction evidence.

The page exists so external frameworks can be translated into Transition Table elements without forcing the external framework to abandon its own vocabulary or mathematics.

## Non-Claim Boundary

This page is not a unified theory of physics.

This page is not a replacement for General Relativity, quantum mechanics, thermodynamics, biology, law, economics, control theory, or any other source discipline.

This page does not prove equivalence between disciplines.

This page does not create commit-time authority.

This page defines a translation grammar only.

## Universal Transition Grammar

A discipline-specific claim enters the wiki through the following neutral grammar:

```text
source discipline event
-> observed or declared change
-> prior state S0
-> candidate transition T
-> boundary conditions
-> constraints and governing rules
-> admissibility question
-> commit or non-commit posture
-> resulting state S1, denial, escalation, refusal, or supersession
-> receipt and reconstruction evidence
```

The grammar is intentionally minimal. It preserves the source discipline's own definitions while making the transition posture explicit enough for comparison, review, and admissibility analysis.

## Translation Rule

A translation is acceptable only if it preserves the following fields:

| Field | Translation requirement |
|---|---|
| Source discipline | The domain that supplies the original vocabulary or formalism. |
| Native term | The term used by the source discipline. |
| Native meaning | The meaning within that discipline, without StegVerse overclaiming. |
| Transition role | The role the term plays when represented as a state transition. |
| Boundary condition | The condition that determines whether the transition remains inside the claimed domain or scope. |
| Constraint | The rule, invariant, law, policy, conservation relation, or declared limit that shapes the transition. |
| Admissibility question | The question that must be answered before the transition can bind consequence. |
| Consequence posture | The result if the transition is committed, denied, escalated, refused, or superseded. |
| Evidence posture | The evidence needed to reconstruct the translation and avoid silent equivalence claims. |

If any field is unknown, the value must be written explicitly as `unknown`, `null`, `partial`, `unresolved`, or `disputed`.

## Mapping to Transition Table Elements

| Transition Table element | Translation-groundwork meaning |
|---|---|
| Transition | The proposed or observed state change being translated. |
| Actor / source | The entity, process, field, theory, paper, model, measurement, or institution asserting the transition. |
| Authority class | The standing of the source claim: established law, theorem, model, hypothesis, analogy, operational rule, policy, or conjecture. |
| Policy reference / constraint reference | The rule basis for the transition: physical law, mathematical invariant, protocol rule, institutional policy, governance rule, or source-framework definition. |
| Evidence posture | Whether the translation has source text, math, test output, receipts, observations, citations, or only conceptual framing. |
| Review posture | Whether the translation is proposed, mapped, disputed, accepted, deferred, or needs specialist review. |
| Drift | Any change in source definition, boundary condition, evidence, interpretation, model version, or context that could invalidate the translation. |
| Decision result | ALLOW, DENY, ESCALATE, REFUSE, DEFER, SUPERSEDE, or another declared result under the target governance process. |
| Commit-time validity | Whether the translated transition still has standing at the moment it would bind consequence. |
| Receipt | The reconstruction record tying the source claim, translation choice, review posture, and decision result together. |

## Discipline Crosswalks

### Physics

Physics terms should not be treated as governance terms. They may be translated only by preserving their physical meaning and then mapping their role in a state transition.

| Physics framing | Transition-table role |
|---|---|
| State | Prior or resulting state. |
| Interaction | Candidate transition or transition driver. |
| Force / influence | Change-producing relation, not automatically an actor. |
| Conservation law | Constraint reference. |
| Boundary condition | Boundary condition. |
| Measurement | Observation or evidence event. |
| Entropy shift | Irreversibility, uncertainty, or reconstruction-relevant change, depending on source claim. |
| Horizon | Boundary beyond which information, recovery, or causal reconstruction may be unavailable under the declared model. |
| Singularity / translation failure | Unresolved or failed mapping where the source discipline cannot be safely reduced into the target transition grammar. |

Physics translation must preserve a strict non-claim: a Transition Table mapping does not prove a new physical theory.

### Governance and Law

| Governance or legal framing | Transition-table role |
|---|---|
| Authority | Authority class. |
| Law, policy, rule, contract, or delegation | Policy reference / constraint reference. |
| Decision | Review result or candidate commitment. |
| Execution | Commit or attempted commit. |
| Appeal, audit, or review | Reconstruction, challenge, or downstream review posture. |
| Remedy | Recovery or consequence-handling path. |

### AI and Runtime Systems

| AI/runtime framing | Transition-table role |
|---|---|
| Input | Candidate transition source material. |
| Manifest | Declared transition context. |
| Receipt | Reconstruction artifact. |
| Sandbox result | Evidence posture or proof-path input. |
| Policy gate | Constraint and admissibility check. |
| Runtime execution | Commit attempt. |
| Fail-closed path | DENY, REFUSE, safe mode, quarantine, or escalation. |

### Biology and Systems Theory

| Biological or systems framing | Transition-table role |
|---|---|
| Stimulus | Transition driver. |
| Response | Candidate transition or state evolution. |
| Adaptation | Resulting state or recovery path. |
| Homeostasis | Recoverability / stability condition. |
| Boundary | Boundary condition. |
| Collapse | Failure state or non-recoverable consequence. |

### Economics and Exchange

| Economic framing | Transition-table role |
|---|---|
| Market signal | Evidence or observation. |
| Transaction | Candidate transition. |
| Settlement | Commit. |
| Allocation | Resulting state. |
| Risk control | Constraint / admissibility check. |
| Reversal or default | Recovery, denial, or consequence-handling path. |

## Relationship to GCAT / BCAT Papers

This groundwork does not replace GCAT or BCAT. It explains how their terms can be translated for cross-disciplinary comparison.

| Paper family | Translation role |
|---|---|
| GCAT geometric framing | Supplies an admissibility geometry for governed autonomy. |
| GCAT control framing | Supplies a dynamic barrier interpretation for maintaining admissibility. |
| Rigel recoverability geometry | Supplies a recoverability and collapse-position layer. |
| Lag geometry | Supplies the temporal bridge from pointwise state to lag-conditioned recoverability. |
| Commit-time synthesis | Supplies the commit gate where a transition is allowed or denied at the point of action. |
| Consequence horizon | Supplies a horizon-style framing for consequence boundaries and irreversibility. |
| Data continuity | Supplies a reconstruction and continuity layer for state, evidence, and receipt paths. |

## Minimal Translation Record

Every proposed translation should be recordable in this shape:

```text
translation_id: <stable id>
source_discipline: <field>
source_reference: <paper, page, model, or artifact>
native_term: <source term>
native_meaning: <source-safe definition>
transition_role: <Transition Table element>
boundary_condition: <declared boundary or unknown>
constraint_reference: <rule, invariant, law, policy, or unknown>
admissibility_question: <question before consequence can bind>
evidence_posture: <none | partial | present | sufficient | conflicting | stale | unknown>
review_posture: <proposed | mapped | disputed | accepted | deferred | escalated>
non_claims: <what the mapping does not prove>
receipt_reference: <record pointer or null>
```

## Done Criteria

This section is done when:

1. The groundwork page exists in the Formalisms section.
2. The page links the Transition Table to a discipline-independent translation grammar.
3. The page provides a physics crosswalk without claiming a new physical theory.
4. The page provides non-physics crosswalks for governance/law, AI/runtime systems, biology/systems theory, and economics/exchange.
5. The sidebar exposes the page publicly.
6. The Formalisms index lists the page and preserves the non-claim boundary.

## Open Questions

```text
Which external physics papers should receive individual translation records?
Which GCAT / BCAT equations should be referenced in the first mathematics crosswalk?
Should translation records live in static JSON, docs pages, or both?
Which fields should be required before a translation can move from proposed to mapped?
Which specialist review classes are needed for physics, biology, law, economics, and AI-runtime translations?
```

## Non-Claims

This page does not define, prove, or validate any source discipline. It does not turn analogy into equivalence. It does not make physics claims, biological claims, legal claims, economic claims, or AI safety claims true by translating them into the Transition Table. A translation record is an interoperability artifact, not proof authority.