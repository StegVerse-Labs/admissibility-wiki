---
title: Formalisms
---

# Formalisms

## Purpose

The Admissibility Wiki is the public convergence surface for formal systems that define, test, compare, or govern admissible AI-related action.

This page lists formalism terms from the `Admissible-Existence` organization using readable definitions first. Source-repository abbreviations are shown only as secondary identifiers.

The wiki mirrors and classifies these formalisms for public review and convergence. It does not replace the originating repositories, formal proof artifacts, executable tests, decision records, or source authority.

## Current Formalism Source Family

```text
Origin organization: Admissible-Existence
Wiki mirror repository: StegVerse-Labs/admissibility-wiki
Registry artifact: static/formalisms/formalism-registry.v0.1.json
Registry state: intake
```

## Current RTG / CHF Corrections

| Abbreviation | Corrected meaning | Status |
|---|---|---|
| RTG | Relational Transition Geometry | corrected foundation term |
| CHF | Coherency Horizon | corrected information-boundary term |

RTG is no longer treated as Runtime Transition Governance at the foundation layer. Runtime governance remains an execution-facing application of Relational Transition Geometry.

CHF is no longer treated as Continuity Handoff Formalism. Continuity handoff remains a related continuity concept, but CHF is reserved for Coherency Horizon.

## Uniform Record Rule

Every formalism entry must expose the same record fields, even when a field is not yet populated.

The values `null`, `none`, `unknown`, `partial`, `disputed`, `unresolved`, and `in progress` are meaningful governance entries. They should be written explicitly instead of omitted.

For non-obvious StegVerse ecosystem entries, `in progress` may be used as a temporary status placeholder until source artifacts, dates, links, and relationship records are confirmed.

## Formalism Terms

### Commit-Time Admissibility

**Definition:** A governing formalism for determining whether a proposed transition still has standing at the moment it crosses into commitment.

**Source reference:** `Admissible-Existence/CTA`  
**Source visibility:** private  
**Formalism page:** [Commit-Time Admissibility](./commit-time-admissibility.md)  
**Current wiki state:** mirrored  
**Non-claim:** CTA listing does not prove the complete formalism or create present standing for any transition.

### Inference-Window and Irreversibility-Bounded Governance

**Definition:** An executable governance formalism for evaluating whether evidence, authority, policy, scope, context, consequence, and recovery conditions retain sufficient standing at commitment.

**Source reference:** Admissibility Wiki public formalism  
**Source visibility:** public  
**Formalism page:** [Inference-Window and Irreversibility-Bounded Governance](./inference-window-irreversibility-governance.md)  
**Current wiki state:** validated implementation pending public deployment verification  
**Non-claim:** A passing validator does not prove factual correctness, legal compliance, or IICT.

### Conceptual Inheritance and Provenance Standing

**Definition:** A governed-transition formalism that separates architectural integrity, provenance continuity, and standing for public claims about independent origin, influence, interoperability, or derivation.

**Source reference:** Admissibility Wiki public formalism  
**Source visibility:** public  
**Formalism page:** [Conceptual Inheritance and Provenance Standing](./conceptual-inheritance-provenance.md)  
**Schema:** `static/schemas/conceptual-inheritance-record.schema.json`  
**Validator:** `scripts/check_conceptual_inheritance_claims.py`  
**Current wiki state:** validated implementation pending canonical workflow and public deployment verification  
**Non-claim:** Similarity alone does not prove derivation, and unresolved provenance does not certify independent origin or establish legal ownership, infringement, or intent.

### AI-Led Radiology Execution-Boundary Admissibility

**Definition:** A domain-specific execution-boundary formalism for determining when AI may assist radiology, when mandatory human review is required, and when autonomous clearance must be denied or fail closed.

**Source reference:** Admissibility Wiki public formalism  
**Source visibility:** public  
**Formalism page:** [AI-Led Radiology Execution-Boundary Admissibility](./ai-led-radiology-execution-boundary.md)  
**Schema:** `static/schemas/ai-led-radiology-execution-case.schema.json`  
**Validator:** `scripts/check_ai_led_radiology_execution.py`  
**Publication validator:** `scripts/check_ai_led_radiology_publication.py`  
**Current wiki state:** validated local implementation pending canonical workflow and public-route verification  
**Non-claim:** The formalism does not grant clinical authority, replace qualified radiologist judgment, certify a model, or authorize autonomous diagnostic clearance.

### Governed Action Lifecycle

**Definition:** A lifecycle formalism separating proposal, commit-time revalidation, bounded execution, consequence observation, recovery or accountability, and reconstruction.

**Source reference:** Admissibility Wiki public lifecycle doctrine  
**Source visibility:** public  
**Formalism page:** [Governed Action Lifecycle](./governed-action-lifecycle.md)  
**Current wiki state:** mirrored  
**Non-claim:** Lifecycle placement does not itself grant authority or prove that any particular transition was admissible.

### Irreversibility-Inference Convergence Theorem

**Definition:** A theorem candidate proposing that governance systems subjected to repeated admissibility optimization converge toward structures that minimize the distance between irreversible commitment and the final admissible inference while preserving reconstructability.

**Source reference:** `Admissible-Existence/IICT`  
**Source visibility:** private  
**Formalism page:** [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md)  
**Current wiki state:** mirrored  
**Non-claim:** IICT does not replace Commit-Time Admissibility and is not proven by baseline tests.

### State Transition Continuity Model

**Definition:** A formalism for examining whether a proposed or observed state transition preserves enough continuity, standing, and reconstruction context to be treated as admissibly related to the prior state.

**Source reference:** `Admissible-Existence/STCM`  
**Source visibility:** public  
**Formalism page:** [State Transition Continuity Model](./state-transition-continuity-model.md)  
**Current wiki state:** mirrored  
**Non-claim:** The wiki does not prove this formalism merely by listing it.

### Relational Transition Geometry

**Definition:** The foundational RTG formalism for describing the geometry of a transition before it is reduced into table cells, proof paths, runtime checks, or commit-time outcomes.

**Source reference:** `Admissible-Existence/RTG`  
**Source visibility:** private  
**Formalism page:** [Relational Transition Geometry](./runtime-transition-governance.md)  
**Current wiki state:** mirrored  
**Non-claim:** Runtime governance remains a later execution-facing application of the transition geometry, not the corrected foundation meaning of RTG.

### Coherency Horizon

**Definition:** The CHF formalism for identifying the boundary beyond which no additional information can be obtained from within a stabilized coherent state, even though existence may continue inside that boundary.

**Source reference:** `Admissible-Existence/CHF`  
**Source visibility:** private  
**Formalism page:** [Coherency Horizon](./coherency-horizon.md)  
**Current wiki state:** mirrored  
**Non-claim:** Existence alone does not create governance standing, reconstructability, or execution authority.

### Boundary Conditions

**Definition:** A formalism for identifying the conditions that must hold before a transition, decision, or claim can be treated as inside a governed admissibility boundary.

**Source reference:** `Admissible-Existence/BC`  
**Source visibility:** private  
**Formalism page:** [Boundary Conditions](./boundary-conditions.md)  
**Current wiki state:** mirrored  
**Non-claim:** Boundary-condition listing does not establish that a boundary was satisfied in any specific case.

### Transition Table

**Definition:** A formalism for classifying proposed state changes by transition type, actor, authority class, policy reference, evidence posture, review posture, drift posture, decision result, commit-time validity, and receipt/reconstruction status.

**Source reference:** `Admissible-Existence/TT`  
**Source visibility:** private  
**Formalism page:** [Transition Table](./transition-table.md)  
**Visual reference:** [Transition Table Visual](https://stegverse-labs.github.io/Site/transition-table-visual.html)  
**Current wiki state:** mirrored  
**Non-claim:** A visual table is not itself proof of admissibility.

### Disciplinary Translation Groundwork

**Definition:** A public-safe translation groundwork for expressing discipline-specific consequential changes as state transitions without claiming that the source disciplines are equivalent.

**Source reference:** Admissibility Wiki public groundwork  
**Source visibility:** public  
**Formalism page:** [Disciplinary Translation Groundwork](./disciplinary-translation-groundwork.md)  
**Current wiki state:** intake  
**Non-claim:** This page does not prove a new physical theory, replace source-discipline mathematics, or turn analogy into equivalence.

### Translation Records

**Definition:** A machine-readable and human-readable record layer for mapping source-discipline terms into Transition Table roles while preserving native meaning, evidence posture, review posture, and non-claim boundaries.

**Source reference:** `static/translation-records/disciplinary-translation-records.v0.1.json`  
**Source visibility:** public  
**Formalism page:** [Translation Records](./translation-records.md)  
**Current wiki state:** intake  
**Non-claim:** Translation records are interoperability artifacts, not proof authority or commit-time authority.

### Mathematics Crosswalk

**Definition:** A public-safe crosswalk from selected GCAT / BCAT equation forms into Transition Table roles and translation-record IDs.

**Source reference:** `static/translation-records/mathematics-crosswalk.v0.1.json`  
**Source visibility:** public  
**Formalism page:** [Mathematics Crosswalk](./mathematics-crosswalk.md)  
**Current wiki state:** intake  
**Non-claim:** This page does not validate equations, prove physical interpretation, or authorize any transition.

### Triad Governance Model

**Definition:** A formalism for modeling governance across three interacting roles, dimensions, or authorities where admissibility depends on the relationship among all three rather than a single actor or single approval path.

**Source reference:** `Admissible-Existence/Triad`  
**Source visibility:** private  
**Formalism page:** [Triad Governance Model](./triad-governance-model.md)  
**Current wiki state:** mirrored  
**Non-claim:** The wiki does not infer which triad configuration applies without source-confirmed definition.

### Continuity Handoff Formalism

**Definition:** A formalism for preserving reconstructable task, authority, evidence, and state continuity when work moves across sessions, repositories, entities, reviewers, or execution surfaces.

**Source reference:** pending abbreviation-safe source confirmation  
**Source visibility:** private  
**Formalism page:** [Continuity Handoff Formalism](./continuity-handoff-formalism.md)  
**Current wiki state:** mirrored  
**Non-claim:** This page does not claim the abbreviation CHF.

### Data Continuity

**Definition:** A formalism for preserving the identity, integrity, traceability, and reconstructability of data across transitions, transformations, mirrors, receipts, and derived artifacts.

**Source reference:** `Admissible-Existence/DaCo`  
**Source visibility:** private  
**Formalism page:** [Data Continuity](./data-continuity.md)  
**Current wiki state:** mirrored  
**Non-claim:** Data continuity does not prove decision legitimacy unless linked to the relevant authority, policy, and evidence context.

### Decision Continuity

**Definition:** A formalism for preserving the standing, review basis, policy reference, receipt path, and reconstructability of decisions across time and downstream consequence.

**Source reference:** `Admissible-Existence/DC`  
**Source visibility:** private  
**Formalism page:** [Decision Continuity](./decision-continuity.md)  
**Current wiki state:** mirrored  
**Non-claim:** A recorded decision does not remain valid if commit-time standing is lost.

### Governance-Centered / Boundary-Centered Admissibility Testing

**Definition:** A formalism family for testing whether governance conditions and boundary conditions are satisfied before a transition, execution, publication, or consequence is treated as admissible.

**Source reference:** `Admissible-Existence/GCAT-BCAT`  
**Source visibility:** private  
**Formalism page:** [Governance-Centered / Boundary-Centered Admissibility Testing](./governance-centered-boundary-centered-admissibility-testing.md)  
**Current wiki state:** mirrored  
**Non-claim:** Test-family identification does not prove any specific test result.

### Core-Lite Admissibility Engine

**Definition:** A compact implementation-oriented formalism for evaluating admissibility claims through the smallest viable core of policy, authority, evidence, review, and receipt checks.

**Source reference:** `Admissible-Existence/core-lite`  
**Source visibility:** private  
**Formalism page:** [Core-Lite Admissibility Engine](./core-lite-admissibility-engine.md)  
**Current wiki state:** mirrored  
**Non-claim:** Implementation presence does not equal production authority.

### Learning Transition Governance

**Definition:** A formalism for applying transition-governance concepts to learning environments, including human learning, AI-assisted learning, instructional review, evaluation, and consequence-bearing educational decisions.

**Source reference:** `Admissible-Existence/learning-transition-governance`  
**Source visibility:** public  
**Formalism page:** [Learning Transition Governance](./learning-transition-governance.md)  
**Current wiki state:** mirrored  
**Non-claim:** The wiki does not prove educational validity merely by listing the formalism.

### Admissible-Existence Validation Factory

**Definition:** A formalism and tooling surface for producing, organizing, or checking validation artifacts used by Admissible-Existence formal systems.

**Source reference:** `Admissible-Existence/ae-validation-factory`  
**Source visibility:** private  
**Formalism page:** [Admissible-Existence Validation Factory](./admissible-existence-validation-factory.md)  
**Current wiki state:** mirrored  
**Non-claim:** Validation-factory existence does not mean a given formalism has passed validation.

## Formalism Record States

| State | Meaning |
|---|---|
| intake | A formalism has been identified but not mapped. |
| in progress | A non-obvious StegVerse ecosystem entry has been acknowledged, but its source date, link, contributor record, or relationship classification is still being confirmed. |
| mirrored | A public wiki page exists and links to public-safe source artifacts. |
| crosswalked | The formalism has mapped glossary, ontology, receipt, and proof-path relationships. |
| validated | The formalism has a validator, example, replay path, or formalism-test artifact. |
| superseded | A newer formalism has replaced or narrowed this one. |

## Authority Boundary

The wiki may explain or mirror a formalism, but it must not overclaim what the formalism proves.

```text
Wiki page = public explanation and convergence layer
Source repository = originating artifact authority
Formalism test = executable proof or validation authority when present
Decision record = accepted governance disposition
Continuity receipt = reconstructability and handoff evidence
StegCore = admissibility interpretation where applicable
```

Private source repositories must not have private content copied into the public wiki. They may be represented by public-safe metadata, source identity, boundary declarations, and later approved public mirror excerpts.
