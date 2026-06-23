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

## Uniform Record Rule

Every formalism entry must expose the same record fields, even when a field is not yet populated.

The values `null`, `none`, `unknown`, `partial`, `disputed`, `unresolved`, and `in progress` are meaningful governance entries. They should be written explicitly instead of omitted.

For non-obvious StegVerse ecosystem entries, `in progress` may be used as a temporary status placeholder until source artifacts, dates, links, and relationship records are confirmed.

Each formalism record should preserve:

```yaml
record:
  formalism_name:
  definition:
  source_reference:
  source_visibility:
  first_known_stegverse_reference:
    artifact:
    date:
    link:
  original_drawing_or_seed_artifact:
    artifact:
    date:
    link:
    status:
  external_references:
    - term:
      source:
      date:
      link:
      relationship:
  known_contributors:
    - name:
      contribution:
      date:
      reference:
  chronology_status:
  attribution_status:
  evidence_status:
  review_status:
  relationship_status:
  commit_time_relevance:
  current_wiki_state:
  non_claim:
  open_questions:
```

## Formalism Terms

### Commit-Time Admissibility

**Definition:** A governing formalism for determining whether a proposed transition still has standing at the moment it crosses into commitment.

**Source reference:** `Admissible-Existence/CTA`  
**Source visibility:** private  
**Formalism page:** [Commit-Time Admissibility](./commit-time-admissibility.md)  
**Mirror handoff:** `CTA_MIRROR_HANDOFF.md`  
**Current wiki state:** mirrored  
**Non-claim:** CTA listing does not prove the complete formalism or create present standing for any transition.

```yaml
record:
  formalism_name: Commit-Time Admissibility
  definition: A governing formalism for determining whether a proposed transition still has standing at the moment it crosses into commitment.
  source_reference: Admissible-Existence/CTA
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: original admissibility / transition-boundary drawing
    date: in progress
    link: in progress
    status: candidate_seed_artifact
  external_references:
    - term: admissibility-before-execution
      source: external terminology discussion
      date: 2026-06-23
      link: in progress
      relationship: overlapping
    - term: consequence standing
      source: external terminology discussion
      date: 2026-06-23
      link: in progress
      relationship: overlapping
  known_contributors:
    - name: StegVerse ecosystem
      contribution: commit-time admissibility framing
      date: in progress
      reference: Admissible-Existence/CTA
    - name: external contributors
      contribution: adjacent terminology and prior-art discussion
      date: in progress
      reference: in progress
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: critical
  current_wiki_state: mirrored
  non_claim: CTA listing does not prove the complete formalism or create present standing for any transition.
  open_questions:
    - Confirm first public StegVerse artifact date.
    - Confirm and link the original drawing or seed artifact.
    - Map external terminology without collapsing referenced, compared, influenced, convergent, and incorporated relationships.
```

### Irreversibility-Inference Convergence Theorem

**Definition:** A theorem candidate proposing that governance systems subjected to repeated admissibility optimization converge toward structures that minimize the distance between irreversible commitment and the final admissible inference while preserving reconstructability.

**Source reference:** `Admissible-Existence/IICT`  
**Source visibility:** private  
**Formalism page:** [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md)  
**Mirror handoff:** `IICT_MIRROR_HANDOFF.md`  
**Current wiki state:** mirrored  
**Non-claim:** IICT does not replace Commit-Time Admissibility and is not proven by baseline tests.

```yaml
record:
  formalism_name: Irreversibility-Inference Convergence Theorem
  definition: A theorem candidate proposing that governance systems subjected to repeated admissibility optimization converge toward structures that minimize the distance between irreversible commitment and the final admissible inference while preserving reconstructability.
  source_reference: Admissible-Existence/IICT
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: none confirmed
      source: none confirmed
      date: unknown
      link: unknown
      relationship: unresolved
  known_contributors:
    - name: StegVerse ecosystem
      contribution: theorem candidate framing
      date: in progress
      reference: Admissible-Existence/IICT
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: direct
  current_wiki_state: mirrored
  non_claim: IICT does not replace Commit-Time Admissibility and is not proven by baseline tests.
  open_questions:
    - Confirm first public artifact date.
    - Identify structural-performance evidence and replay artifacts.
```

### State Transition Continuity Model

**Definition:** A formalism for examining whether a proposed or observed state transition preserves enough continuity, standing, and reconstruction context to be treated as admissibly related to the prior state.

**Source reference:** `Admissible-Existence/STCM`  
**Source visibility:** public  
**Mathematical proof candidate:** [Source repository](https://github.com/Admissible-Existence/STCM)  
**Current wiki state:** intake  
**Non-claim:** The wiki does not prove this formalism merely by listing it.

```yaml
record:
  formalism_name: State Transition Continuity Model
  definition: A formalism for examining whether a proposed or observed state transition preserves enough continuity, standing, and reconstruction context to be treated as admissibly related to the prior state.
  source_reference: Admissible-Existence/STCM
  source_visibility: public
  first_known_stegverse_reference:
    artifact: https://github.com/Admissible-Existence/STCM
    date: in progress
    link: https://github.com/Admissible-Existence/STCM
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: state transition validation
      source: established distributed-systems terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: state-transition continuity framing
      date: in progress
      reference: Admissible-Existence/STCM
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: direct
  current_wiki_state: intake
  non_claim: The wiki does not prove this formalism merely by listing it.
  open_questions:
    - Confirm proof-candidate completeness.
    - Confirm external adjacent terminology records.
```

### Runtime Transition Governance

**Definition:** A formalism for determining how runtime actions, executions, denials, escalations, or pauses should be governed while state, authority, policy, or evidence may still be changing.

**Source reference:** `Admissible-Existence/RTG`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Private source material must not be exposed through the public wiki without an approved public mirror boundary.

```yaml
record:
  formalism_name: Runtime Transition Governance
  definition: A formalism for determining how runtime actions, executions, denials, escalations, or pauses should be governed while state, authority, policy, or evidence may still be changing.
  source_reference: Admissible-Existence/RTG
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: runtime authority reports
      source: external terminology discussion
      date: 2026-06-23
      link: in progress
      relationship: overlapping
  known_contributors:
    - name: StegVerse ecosystem
      contribution: runtime transition governance framing
      date: in progress
      reference: Admissible-Existence/RTG
    - name: external contributors
      contribution: adjacent runtime-governance terminology
      date: in progress
      reference: in progress
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: direct
  current_wiki_state: intake
  non_claim: Private source material must not be exposed through the public wiki without an approved public mirror boundary.
  open_questions:
    - Identify public-safe source boundary.
    - Map runtime authority terminology against commit-time admissibility.
```

### Boundary Conditions

**Definition:** A formalism for identifying the conditions that must hold before a transition, decision, or claim can be treated as inside a governed admissibility boundary.

**Source reference:** `Admissible-Existence/BC`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Boundary-condition listing does not establish that a boundary was satisfied in any specific case.

```yaml
record:
  formalism_name: Boundary Conditions
  definition: A formalism for identifying the conditions that must hold before a transition, decision, or claim can be treated as inside a governed admissibility boundary.
  source_reference: Admissible-Existence/BC
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: original admissibility / transition-boundary drawing
    date: in progress
    link: in progress
    status: candidate_seed_artifact
  external_references:
    - term: replayable boundary results
      source: external terminology discussion
      date: 2026-06-23
      link: in progress
      relationship: overlapping
  known_contributors:
    - name: StegVerse ecosystem
      contribution: admissibility-boundary framing
      date: in progress
      reference: Admissible-Existence/BC
    - name: external contributors
      contribution: adjacent boundary-result terminology
      date: in progress
      reference: in progress
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: critical
  current_wiki_state: intake
  non_claim: Boundary-condition listing does not establish that a boundary was satisfied in any specific case.
  open_questions:
    - Confirm original drawing date and storage location.
    - Identify public-safe boundary formalism artifacts.
```

### Transition Table

**Definition:** A formalism for classifying proposed state changes by transition type, actor, authority class, policy reference, evidence posture, review posture, drift posture, decision result, commit-time validity, and receipt/reconstruction status.

**Source reference:** `Admissible-Existence/TT`  
**Source visibility:** private  
**Visual reference:** [Transition Table Visual](https://stegverse-labs.github.io/Site/transition-table-visual.html)  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A visual table is not itself proof of admissibility.

```yaml
record:
  formalism_name: Transition Table
  definition: A formalism for classifying proposed state changes by transition type, actor, authority class, policy reference, evidence posture, review posture, drift posture, decision result, commit-time validity, and receipt/reconstruction status.
  source_reference: Admissible-Existence/TT
  source_visibility: private
  first_known_stegverse_reference:
    artifact: Transition Table Visual
    date: in progress
    link: https://stegverse-labs.github.io/Site/transition-table-visual.html
  original_drawing_or_seed_artifact:
    artifact: original transition-table drawing
    date: in progress
    link: in progress
    status: candidate_seed_artifact
  external_references:
    - term: two-phase commit
      source: distributed-systems terminology
      date: unknown
      link: unknown
      relationship: adjacent
    - term: state machine validation
      source: distributed-systems terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: transition-table framing and visual reference
      date: in progress
      reference: Admissible-Existence/TT
    - name: external commenters
      contribution: comparison against 2PC and state-machine validation
      date: 2026-06-23
      reference: external terminology discussion
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: critical
  current_wiki_state: intake
  non_claim: A visual table is not itself proof of admissibility.
  open_questions:
    - Confirm original transition-table drawing artifact.
    - Clarify which cells have public-safe proof paths.
    - Map adjacent distributed-system terminology without claiming ownership over established patterns.
```

### Triad Governance Model

**Definition:** A formalism for modeling governance across three interacting roles, dimensions, or authorities where admissibility depends on the relationship among all three rather than a single actor or single approval path.

**Source reference:** `Admissible-Existence/Triad`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** The wiki does not infer which triad configuration applies without source-confirmed definition.

```yaml
record:
  formalism_name: Triad Governance Model
  definition: A formalism for modeling governance across three interacting roles, dimensions, or authorities where admissibility depends on the relationship among all three rather than a single actor or single approval path.
  source_reference: Admissible-Existence/Triad
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: none confirmed
      source: none confirmed
      date: unknown
      link: unknown
      relationship: unresolved
  known_contributors:
    - name: StegVerse ecosystem
      contribution: triad governance framing
      date: in progress
      reference: Admissible-Existence/Triad
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: direct
  current_wiki_state: intake
  non_claim: The wiki does not infer which triad configuration applies without source-confirmed definition.
  open_questions:
    - Confirm source definition and role set.
```

### Continuity Handoff Formalism

**Definition:** A formalism for preserving reconstructable task, authority, evidence, and state continuity when work moves across sessions, repositories, entities, reviewers, or execution surfaces.

**Source reference:** `Admissible-Existence/CHF`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A handoff record does not create authority by itself.

```yaml
record:
  formalism_name: Continuity Handoff Formalism
  definition: A formalism for preserving reconstructable task, authority, evidence, and state continuity when work moves across sessions, repositories, entities, reviewers, or execution surfaces.
  source_reference: Admissible-Existence/CHF
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: none confirmed
      source: none confirmed
      date: unknown
      link: unknown
      relationship: unresolved
  known_contributors:
    - name: StegVerse ecosystem
      contribution: continuity handoff framing
      date: in progress
      reference: Admissible-Existence/CHF
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: indirect
  current_wiki_state: intake
  non_claim: A handoff record does not create authority by itself.
  open_questions:
    - Confirm handoff receipt schema and first source artifact.
```

### Data Continuity

**Definition:** A formalism for preserving the identity, integrity, traceability, and reconstructability of data across transitions, transformations, mirrors, receipts, and derived artifacts.

**Source reference:** `Admissible-Existence/DaCo`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Data continuity does not prove decision legitimacy unless linked to the relevant authority, policy, and evidence context.

```yaml
record:
  formalism_name: Data Continuity
  definition: A formalism for preserving the identity, integrity, traceability, and reconstructability of data across transitions, transformations, mirrors, receipts, and derived artifacts.
  source_reference: Admissible-Existence/DaCo
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: data provenance
      source: general data-governance terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: data continuity framing
      date: in progress
      reference: Admissible-Existence/DaCo
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: indirect
  current_wiki_state: intake
  non_claim: Data continuity does not prove decision legitimacy unless linked to the relevant authority, policy, and evidence context.
  open_questions:
    - Confirm source artifact and relationship to provenance, receipt, and reconstruction records.
```

### Decision Continuity

**Definition:** A formalism for preserving the standing, review basis, policy reference, receipt path, and reconstructability of decisions across time and downstream consequence.

**Source reference:** `Admissible-Existence/DC`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A recorded decision does not remain valid if commit-time standing is lost.

```yaml
record:
  formalism_name: Decision Continuity
  definition: A formalism for preserving the standing, review basis, policy reference, receipt path, and reconstructability of decisions across time and downstream consequence.
  source_reference: Admissible-Existence/DC
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: decision record
      source: governance and architecture-decision terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: decision continuity framing
      date: in progress
      reference: Admissible-Existence/DC
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: direct
  current_wiki_state: intake
  non_claim: A recorded decision does not remain valid if commit-time standing is lost.
  open_questions:
    - Confirm first source artifact and relation to decision-record governance.
```

### Governance-Centered / Boundary-Centered Admissibility Testing

**Definition:** A formalism family for testing whether governance conditions and boundary conditions are satisfied before a transition, execution, publication, or consequence is treated as admissible.

**Source reference:** `Admissible-Existence/GCAT-BCAT`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Test-family identification does not prove any specific test result.

```yaml
record:
  formalism_name: Governance-Centered / Boundary-Centered Admissibility Testing
  definition: A formalism family for testing whether governance conditions and boundary conditions are satisfied before a transition, execution, publication, or consequence is treated as admissible.
  source_reference: Admissible-Existence/GCAT-BCAT
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: original admissibility / boundary-test drawing
    date: in progress
    link: in progress
    status: candidate_seed_artifact
  external_references:
    - term: none confirmed
      source: none confirmed
      date: unknown
      link: unknown
      relationship: unresolved
  known_contributors:
    - name: StegVerse ecosystem
      contribution: governance-centered and boundary-centered test framing
      date: in progress
      reference: Admissible-Existence/GCAT-BCAT
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: critical
  current_wiki_state: intake
  non_claim: Test-family identification does not prove any specific test result.
  open_questions:
    - Confirm test artifacts and public-safe examples.
```

### Core-Lite Admissibility Engine

**Definition:** A compact implementation-oriented formalism for evaluating admissibility claims through the smallest viable core of policy, authority, evidence, review, and receipt checks.

**Source reference:** `Admissible-Existence/core-lite`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Implementation presence does not equal production authority.

```yaml
record:
  formalism_name: Core-Lite Admissibility Engine
  definition: A compact implementation-oriented formalism for evaluating admissibility claims through the smallest viable core of policy, authority, evidence, review, and receipt checks.
  source_reference: Admissible-Existence/core-lite
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: policy engine
      source: established software-governance terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: minimal admissibility-engine framing
      date: in progress
      reference: Admissible-Existence/core-lite
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: critical
  current_wiki_state: intake
  non_claim: Implementation presence does not equal production authority.
  open_questions:
    - Confirm current public-safe implementation boundary.
```

### Learning Transition Governance

**Definition:** A formalism for applying transition-governance concepts to learning environments, including human learning, AI-assisted learning, instructional review, evaluation, and consequence-bearing educational decisions.

**Source reference:** `Admissible-Existence/learning-transition-governance`  
**Source visibility:** public  
**Mathematical proof candidate:** [Source repository](https://github.com/Admissible-Existence/learning-transition-governance)  
**Current wiki state:** intake  
**Non-claim:** The wiki does not prove educational validity merely by listing the formalism.

```yaml
record:
  formalism_name: Learning Transition Governance
  definition: A formalism for applying transition-governance concepts to learning environments, including human learning, AI-assisted learning, instructional review, evaluation, and consequence-bearing educational decisions.
  source_reference: Admissible-Existence/learning-transition-governance
  source_visibility: public
  first_known_stegverse_reference:
    artifact: https://github.com/Admissible-Existence/learning-transition-governance
    date: in progress
    link: https://github.com/Admissible-Existence/learning-transition-governance
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: learning governance
      source: education-governance terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: learning-transition governance framing
      date: in progress
      reference: Admissible-Existence/learning-transition-governance
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: indirect
  current_wiki_state: intake
  non_claim: The wiki does not prove educational validity merely by listing the formalism.
  open_questions:
    - Confirm educational proof-path examples.
```

### Admissible-Existence Validation Factory

**Definition:** A formalism and tooling surface for producing, organizing, or checking validation artifacts used by Admissible-Existence formal systems.

**Source reference:** `Admissible-Existence/ae-validation-factory`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Validation-factory existence does not mean a given formalism has passed validation.

```yaml
record:
  formalism_name: Admissible-Existence Validation Factory
  definition: A formalism and tooling surface for producing, organizing, or checking validation artifacts used by Admissible-Existence formal systems.
  source_reference: Admissible-Existence/ae-validation-factory
  source_visibility: private
  first_known_stegverse_reference:
    artifact: in progress
    date: in progress
    link: in progress
  original_drawing_or_seed_artifact:
    artifact: none confirmed
    date: unknown
    link: unknown
    status: in progress
  external_references:
    - term: validation factory
      source: software validation terminology
      date: unknown
      link: unknown
      relationship: adjacent
  known_contributors:
    - name: StegVerse ecosystem
      contribution: validation-factory framing
      date: in progress
      reference: Admissible-Existence/ae-validation-factory
  chronology_status: in progress
  attribution_status: in progress
  evidence_status: partial
  review_status: in progress
  relationship_status: unresolved
  commit_time_relevance: indirect
  current_wiki_state: intake
  non_claim: Validation-factory existence does not mean a given formalism has passed validation.
  open_questions:
    - Confirm validation artifact inventory and public-safe evidence references.
```

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

## Term Discovery Role

After formalism pages are mirrored, the wiki entity should periodically search for terms and ideas that are exactly or strongly correlated with existing terms.

Candidate origins must be formalized artifacts, such as:

```text
formalism repository
standards document
academic paper
technical report
public specification
machine-readable schema
reference implementation
policy framework
regulatory guidance
public ontology
stable whitepaper
```

Social posts or comments may be leads, but they are not acceptable origins.

When a social post, comment thread, or conversation identifies a candidate term, the wiki may record it as a lead only when the record explicitly says `source: social lead` or `relationship_status: unresolved`. It must not be treated as origin evidence until a stable artifact is linked.

## Validation

The current formalism registry is validated by:

```text
node scripts/check-formalism-registry.mjs
npm run validate
```

The term candidate queue is validated by:

```text
node scripts/check-term-candidate-queue.mjs
npm run validate
```

## Next Safe Build Target

Create source-confirmed detail pages and crosswalk records for each formalism term, then replace any pending proof-candidate placeholder with public-safe proof artifacts when available.
