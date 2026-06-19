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

## Formalism Terms

### State Transition Continuity Model

**Definition:** A formalism for examining whether a proposed or observed state transition preserves enough continuity, standing, and reconstruction context to be treated as admissibly related to the prior state.

**Source reference:** `Admissible-Existence/STCM`  
**Source visibility:** public  
**Mathematical proof candidate:** [Source repository](https://github.com/Admissible-Existence/STCM)  
**Current wiki state:** intake  
**Non-claim:** The wiki does not prove this formalism merely by listing it.

### Runtime Transition Governance

**Definition:** A formalism for determining how runtime actions, executions, denials, escalations, or pauses should be governed while state, authority, policy, or evidence may still be changing.

**Source reference:** `Admissible-Existence/RTG`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Private source material must not be exposed through the public wiki without an approved public mirror boundary.

### Boundary Conditions

**Definition:** A formalism for identifying the conditions that must hold before a transition, decision, or claim can be treated as inside a governed admissibility boundary.

**Source reference:** `Admissible-Existence/BC`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Boundary-condition listing does not establish that a boundary was satisfied in any specific case.

### Transition Table

**Definition:** A formalism for classifying proposed state changes by transition type, actor, authority class, policy reference, evidence posture, review posture, drift posture, decision result, commit-time validity, and receipt/reconstruction status.

**Source reference:** `Admissible-Existence/TT`  
**Source visibility:** private  
**Visual reference:** [Transition Table Visual](https://stegverse-labs.github.io/Site/transition-table-visual.html)  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A visual table is not itself proof of admissibility.

### Triad Governance Model

**Definition:** A formalism for modeling governance across three interacting roles, dimensions, or authorities where admissibility depends on the relationship among all three rather than a single actor or single approval path.

**Source reference:** `Admissible-Existence/Triad`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** The wiki does not infer which triad configuration applies without source-confirmed definition.

### Continuity Handoff Formalism

**Definition:** A formalism for preserving reconstructable task, authority, evidence, and state continuity when work moves across sessions, repositories, entities, reviewers, or execution surfaces.

**Source reference:** `Admissible-Existence/CHF`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A handoff record does not create authority by itself.

### Data Continuity

**Definition:** A formalism for preserving the identity, integrity, traceability, and reconstructability of data across transitions, transformations, mirrors, receipts, and derived artifacts.

**Source reference:** `Admissible-Existence/DaCo`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Data continuity does not prove decision legitimacy unless linked to the relevant authority, policy, and evidence context.

### Decision Continuity

**Definition:** A formalism for preserving the standing, review basis, policy reference, receipt path, and reconstructability of decisions across time and downstream consequence.

**Source reference:** `Admissible-Existence/DC`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** A recorded decision does not remain valid if commit-time standing is lost.

### Governance-Centered / Boundary-Centered Admissibility Testing

**Definition:** A formalism family for testing whether governance conditions and boundary conditions are satisfied before a transition, execution, publication, or consequence is treated as admissible.

**Source reference:** `Admissible-Existence/GCAT-BCAT`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Test-family identification does not prove any specific test result.

### Core-Lite Admissibility Engine

**Definition:** A compact implementation-oriented formalism for evaluating admissibility claims through the smallest viable core of policy, authority, evidence, review, and receipt checks.

**Source reference:** `Admissible-Existence/core-lite`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Implementation presence does not equal production authority.

### Learning Transition Governance

**Definition:** A formalism for applying transition-governance concepts to learning environments, including human learning, AI-assisted learning, instructional review, evaluation, and consequence-bearing educational decisions.

**Source reference:** `Admissible-Existence/learning-transition-governance`  
**Source visibility:** public  
**Mathematical proof candidate:** [Source repository](https://github.com/Admissible-Existence/learning-transition-governance)  
**Current wiki state:** intake  
**Non-claim:** The wiki does not prove educational validity merely by listing the formalism.

### Admissible-Existence Validation Factory

**Definition:** A formalism and tooling surface for producing, organizing, or checking validation artifacts used by Admissible-Existence formal systems.

**Source reference:** `Admissible-Existence/ae-validation-factory`  
**Source visibility:** private  
**Mathematical proof candidate:** pending public-safe source identification  
**Current wiki state:** intake  
**Non-claim:** Validation-factory existence does not mean a given formalism has passed validation.

## Formalism Record States

| State | Meaning |
|---|---|
| intake | A formalism has been identified but not mapped. |
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
