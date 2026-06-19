---
title: Formalisms
---

# Formalisms

## Purpose

The Admissibility Wiki is the public convergence surface for formal systems that define, test, compare, or govern admissible AI-related action.

This page now lists the initial formalism set from the `Admissible-Existence` organization.

The wiki mirrors and classifies these formalisms for public review and convergence. It does not replace the originating repositories, formal proof artifacts, executable tests, decision records, or source authority.

## Current Formalism Source Family

```text
Origin organization: Admissible-Existence
Wiki mirror repository: StegVerse-Labs/admissibility-wiki
Registry artifact: static/formalisms/formalism-registry.v0.1.json
Registry state: intake
```

## Admissible-Existence Formalisms

| Formalism | Source Repository | Visibility | Wiki Detail Page | Current State |
|---|---|---:|---|---|
| STCM | `Admissible-Existence/STCM` | public | `docs/formalisms/admissible-existence-stcm.md` | intake |
| RTG | `Admissible-Existence/RTG` | private | `docs/formalisms/admissible-existence-rtg.md` | intake |
| BC | `Admissible-Existence/BC` | private | `docs/formalisms/admissible-existence-bc.md` | intake |
| TT | `Admissible-Existence/TT` | private | `docs/formalisms/admissible-existence-tt.md` | intake |
| Triad | `Admissible-Existence/Triad` | private | `docs/formalisms/admissible-existence-triad.md` | intake |
| CHF | `Admissible-Existence/CHF` | private | `docs/formalisms/admissible-existence-chf.md` | intake |
| DaCo | `Admissible-Existence/DaCo` | private | `docs/formalisms/admissible-existence-daco.md` | intake |
| DC | `Admissible-Existence/DC` | private | `docs/formalisms/admissible-existence-dc.md` | intake |
| GCAT-BCAT | `Admissible-Existence/GCAT-BCAT` | private | `docs/formalisms/admissible-existence-gcat-bcat.md` | intake |
| core-lite | `Admissible-Existence/core-lite` | private | `docs/formalisms/admissible-existence-core-lite.md` | intake |
| learning-transition-governance | `Admissible-Existence/learning-transition-governance` | public | `docs/formalisms/admissible-existence-learning-transition-governance.md` | intake |
| ae-validation-factory | `Admissible-Existence/ae-validation-factory` | private | `docs/formalisms/admissible-existence-ae-validation-factory.md` | intake |

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

Create public-safe detail pages and crosswalk records for each Admissible-Existence subject repository.
