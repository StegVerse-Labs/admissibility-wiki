# Admissibility Wiki

The Admissibility Wiki is the public vocabulary layer for transition governance, commit-time authority, receipt-bound execution, and governed continuity.

This repository is a Docusaurus-ready knowledge base for StegVerse concepts, formal vocabulary, comparison pages, and minimal public proof paths.

## Purpose

This wiki exists to make the StegVerse governance vocabulary visible, stable, linkable, and reviewable without requiring Wikipedia approval first.

It is not a substitute for Wikipedia and does not claim independent notability by itself. It is a public reference layer that can help researchers, developers, reviewers, journalists, and contributors understand the concepts accurately.

## Governed Ecosystem Transition Framing

The current public framing is shifting from external-framework comparison toward a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs.

External frameworks are one input class. The broader path is:

```text
input or request
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

The framing page is:

```text
docs/governance/governed-ecosystem-transitions.md
```

## Governed LLM and Reconstructive Search

A StegVerse-governed LLM is a reasoning participant inside a governed transition path, not an execution authority.

The current public doctrine page is:

```text
docs/governance/governed-llm-reconstructive-search.md
```

The current activation map is:

```text
docs/governance/governed-llm-activation-map.md
```

The active implementation split is:

| Repository | Responsibility | Build state |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and explanatory pages. | Public doctrine and activation map. |
| `StegVerse-org/StegVerse-SDK` | Shared packet, receipt, evidence, manifest, and handoff contracts. | Governed LLM contract layer active. |
| `StegVerse-org/LLM-adapter` | Runtime adapter that converts model output into governed response artifacts. | Adapter boundary complete. |

The current proof path is:

```text
query
  -> provider request
  -> provider response
  -> continuity evidence
  -> adapter receipt
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
```

## Core Assumptions

The wiki treats governance as a layered constraint system, not a single approval event.

The current StegVerse interpretation separates:

- human experience before governance;
- inter-entity trust and intuition before boundary formation;
- boundary conditions before execution;
- governance standing at the moment a transition may affect reality;
- continuity records after execution or denial.

This matters because emotional state, intuition, trust, relational coherence, and boundary recoverability can affect whether a proposed transition should ever become admissible.

## Disciplinary Translation Groundwork

The current translation-groundwork section is:

```text
docs/formalisms/disciplinary-translation-groundwork.md
```

The current translation-records reference page is:

```text
docs/formalisms/translation-records.md
```

The current machine-readable translation-record artifact is:

```text
static/translation-records/disciplinary-translation-records.v0.1.json
```

The current validator is:

```text
scripts/check_translation_records.py
```

Run:

```bash
python scripts/check_translation_records.py
```

Expected current state:

```text
TRANSLATION RECORDS: PASS - 6 records validated
```

The validation workflow is displayed here without the leading period:

```text
github/workflows/validate-translation-records.yml
```

The actual repository path begins with a leading period.

The iOS-safe workflow mirror is:

```text
iosnoperiod/github/workflows/validate-translation-records.yml
```

## Triad Governance

Triad governance is the three-part StegVerse governance frame for distinguishing proposal, commitment, and reconstruction.

| Component | Core Question | Function |
| --- | --- | --- |
| Transition Governance | Can this transition be considered? | Determines whether a proposed state change is structurally valid. |
| Admissibility Governance | Can this transition be committed now? | Determines whether execution authority exists at the moment of commitment. |
| Continuity Governance | Can this transition be reconstructed later? | Determines whether the resulting decision path remains replayable, receipt-bound, and independently reviewable. |

The triad keeps these claims separate:

- approval is not continuity;
- execution is not admissibility;
- history is not authority.

A transition may be structurally valid, inadmissible at commit time, and still reconstructable later. A transition may also be admissible at commit time while failing continuity if receipts, manifests, or authority records are insufficient.

## CAT Governance Stack

The CAT stack is currently interpreted as:

| Layer | Working Name | Function |
| --- | --- | --- |
| ECAT | Emotional / Experiential Constraint Analysis | Models intra-entity state: emotion, intuition, perception, affective processing, coherence, and meaning before governance hardens into boundary or authority. |
| ICAT | Interpersonal / Intuitive Constraint Analysis | Models inter-entity state: trust, relationship continuity, shared understanding, social coherence, and intuition formed between entities. |
| BCAT | Boundary Constraint Analysis | Models the boundary conditions under which a transition, entity, claim, or interaction can remain recoverable and non-inverting. |
| GCAT | Governance Constraint Analysis | Models governance standing, admissibility, policy, delegation, authority, and fail-closed execution decisions. |

ECAT and ICAT should not be reduced to evidence and identity labels. Those interpretations may appear in narrower proof-path contexts, but the broader origin of ECAT/ICAT is the human-governance problem: how emotion, intuition, coherence, and relationship dynamics shape the constraints that later become boundary and governance determinations.

In shorthand:

```text
ECAT / ICAT -> BCAT -> GCAT
```

Meaning:

```text
experience and intuition -> boundary formation -> governance admissibility
```

## Existence Interpretation

The expression:

```text
GCAT / BCAT : ECAT / ICAT : %Existence
```

should be read as a governed existence formulation.

`%Existence` is not merely whether something can be observed. It is the degree to which an entity, claim, transition, relationship, or state can be treated as existing under the relevant governance frame.

A strong existence claim requires alignment across:

- ECAT: internal coherence and experiential standing;
- ICAT: relational coherence and inter-entity standing;
