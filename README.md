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

The governed LLM demo overview page is:

```text
docs/governance/governed-llm-demo-overview.md
```

The governed LLM demo verification page is:

```text
docs/governance/governed-llm-demo-verification.md
```

The bounded free-tier trust chain page is:

```text
docs/governance/llm-free-tier-trust-chain.md
```

The local Site verification page is:

```text
docs/governance/governed-llm-site-verification.md
```

The Site mirror handoff is:

```text
docs/SITE_MIRROR_HANDOFF.md
```

The archive handoff page is:

```text
docs/governance/governed-llm-archive-handoff.md
```

Run:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
python scripts/check_llm_free_tier_trust_chain.py
```

Expected current state:

```text
GOVERNED LLM PAGES: PASS - docs and navigation references present
GOVERNED LLM DEMO DOCS: PASS - demo pages and navigation references present
LLM FREE TIER TRUST CHAIN: PASS
```

The active implementation split is:

| Repository | Responsibility | Build state |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and explanatory pages. | Public doctrine, activation map, Site verification, demo overview, demo verification, deployment status, free-tier trust chain, and archive handoff. |
| `StegVerse-org/StegVerse-SDK` | Shared packet, receipt, evidence, manifest, handoff, and metadata ingestion contracts. | Governed LLM contract layer active with demo packet verification and free-tier metadata ingestion. |
| `StegVerse-org/LLM-adapter` | Runtime adapter that converts model output into governed response artifacts. | Adapter boundary complete with fixture-first end-to-end demo files and `free_tier_trust` metadata. |
| `StegVerse-Labs/Site` | Public display surface for governed LLM entry and bounded trust envelope. | Ecosystem Chat displays bounded free-tier trust and guards it with the public mirror status workflow. |

The current proof path is:

```text
query
  -> provider request
  -> provider response
  -> continuity evidence
  -> governed session packet
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
  -> public demo overview
  -> public demo verification
```

The bounded free-tier trust chain is:

```text
LLM-adapter free_tier_trust metadata
  -> Site display and checker
  -> SDK metadata ingestion and workflow verification
  -> wiki public chain documentation
```

## ASRO comparison state

The ASRO comparison lane preserves external-framework evidence without turning evidentiary participation into execution authority. As of the 2026-09-19 correspondence reconciliation, the four StegVerse-side preconditions are externally acknowledged closed. ASRO's role is recorded as evidentiary, and any future bounded ASRO-side exercise remains ASRO-side deferred pending ASRO's own definition and authorization rather than a StegVerse implementation prerequisite.

The Contributor Protocol remains proposed and not bilaterally authorized pending identification of an actual legal counterparty and sufficient authority scope. Independent reviewer/issuer status remains unresolved, reciprocal execution is not authorized, and no bilateral Seam Comparison Record has been issued.


Canonical retirement evidence for the bounded ASRO disposition goal is now recorded in StegVerse-Labs/.github Task Registry generation 116 via PR #2267 / merge `ea62499be02ed84ddeee3b2957129e3b19ecec19`. Goal `ADMISSIBILITY-ASRO-REVIEW-DISPOSITION-001` is terminal `CLOSED` with COSV `71000000100100`. This retires only the bounded ASRO goal; the shared issue #50 worker remains active for the issue's other coordinated tracks.

Canonical continuation records:

```text
docs/external-frameworks/ASRO_REVIEW_DISPOSITION_MIRROR_HANDOFF.md
docs/external-frameworks/asro-response-disposition-2026-09-19.md
static/data/framework-evaluations/asro/contribution-ledger.jsonl
```

## Reconstructable Singularity

The Reconstructable Singularity research formalism defines a bounded continuity-reconstruction threshold: a selected set of observational frameworks is sufficient when its combined affirmative and exclusionary evidence leaves exactly one admissibility-consistent history.

Canonical public source and machine-checkable assets:

```text
docs/formalisms/reconstructable-singularity.md
static/formalisms/reconstructable-singularity.v0.1.schema.json
static/formalisms/reconstructable-singularity.v0.1.example.json
scripts/check_reconstructable_singularity.py
```

This is a research formalism, not a claim of empirical proof, physical-history collapse, execution authority, or universal completeness. Its deterministic validator establishes contract/example consistency and minimum-set behavior only within the declared fixture.

## Temporal Governed Analysis

Temporal Governed Analysis (TGA) is the explanatory projection layer for inspecting a recorded event against versioned rule, law, interpretation, or enforcement contexts while keeping observation, representation, evaluation, uncertainty, and authority distinct.

The public doctrine page is:

```text
docs/governance/temporal-governed-analysis.md
```

The canonical goal handoff and deterministic observer are:

```text
docs/TGA_ADMISSIBILITY_PROJECTION_MIRROR_HANDOFF.md
scripts/check_tga_admissibility_projection.py
static/status/wiki-public-anchor-internal-task-registry.tga-projection-extension.json
```

The TGA projection is owned by the repository's existing non-halting internal task executor. Its explanatory boundary is:

```text
canonical_representation != canonical_reality
compact_encoding_may_be_wrong_or_ambiguous = true
exact_source_and_time_reference != proof_of_source_authenticity
contemporaneous_evaluation != counterfactual_evaluation
rule_or_law_version != interpretation_profile != enforcement_profile
unresolved_or_contradictory_evidence != forced_binary_conclusion
predicate_matching != legal_guilt_or_adjudication
publication_or_validation != authority
TGA_admissibility_authority_effect = NONE_EXPLANATORY_ONLY
```

The wiki projection does not create legal guilt, admissibility standing, custody, execution, publication, certification, or adjudicative authority. It explains and preserves the governed evidence path; it does not become that evidence's truth source.

## Core Assumptions

The wiki treats governance as a layered constraint system, not a single approval event.

The current StegVerse interpretation separates:

- human experience before governance;
- inter-entity trust and intuition before boundary formation;
- boundary conditions before execution;
- governance standing at the moment a transition may affect reality;
- continuity records after execution or denial.

This matters because emotional state, intuition, trust, relational coherence, and boundary recoverability can affect whether a proposed transition should ever become admissible.

## Governed Relationship Transitions

A relationship may persist, remain coherent, and preserve continuity while no longer being legitimate or admissible.

The doctrine page is:

```text
docs/governance/governed-relationship-transitions.md
```

The page distinguishes governed architectural relationships from the governed transition determinations required to decide whether those relationships may legitimately continue at the commit-time boundary.

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


External-framework findings source contract: [Exact manifested transition findings](docs/external-frameworks/TRANSITION_DISPOSITION_FINDINGS_CONTRACT.md) binds each finding to the actual attempted boundary, declared manifest route/capability and verifiable disposition/repair. This source-only template does not promote unrun tests or local diagnostics to runtime evidence or change the 36-framework denominator.
