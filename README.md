# Admissibility Wiki

The Admissibility Wiki is the public vocabulary layer for transition governance, commit-time authority, receipt-bound execution, and governed continuity.

This repository is a Docusaurus-ready knowledge base for StegVerse concepts, formal vocabulary, comparison pages, and minimal public proof paths.

## Purpose

This wiki exists to make the StegVerse governance vocabulary visible, stable, linkable, and reviewable without requiring Wikipedia approval first.

It is not a substitute for Wikipedia and does not claim independent notability by itself. It is a public reference layer that can help researchers, developers, reviewers, journalists, and contributors understand the concepts accurately.

## Core Assumptions

The wiki treats governance as a layered constraint system, not a single approval event.

The current StegVerse interpretation separates:

- human experience before governance;
- inter-entity trust and intuition before boundary formation;
- boundary conditions before execution;
- governance standing at the moment a transition may affect reality;
- continuity records after execution or denial.

This matters because emotional state, intuition, trust, relational coherence, and boundary recoverability can affect whether a proposed transition should ever become admissible.

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
- BCAT: boundary recoverability and constraint integrity;
- GCAT: governance admissibility and authority standing.

For commit-time effects, StegVerse should treat missing or failed layers as fail-closed unless a policy explicitly defines a safe partial-standing condition.

## Chain Status Surface

The current chain-status reference is:

```text
docs/CHAIN_STATUS.md
```

The current chain-status handoff is:

```text
docs/CHAIN_STATUS_HANDOFF.md
```

The current chain snapshot and receipt are:

```text
docs/CHAIN_SNAPSHOT_v0_1_0.md
docs/CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json
```

The current automation-state record is:

```text
docs/CHAIN_AUTO.json
```

The current blocked-destination records are:

```text
docs/CHAIN_STATUS_BLOCKED_DESTINATION.md
docs/CHAIN_STATUS_BLOCKED_DESTINATION.json
docs/CHAIN_STATUS_CONTINUATION.json
docs/CHAIN_STATUS_CONTINUATION.schema.json
```

The current automated validators are:

```text
scripts/check_chain_status_continuation.py
scripts/check_chain_snapshot_receipt.py
scripts/check_chain_auto.py
scripts/check_guardian_destination.py
```

Run:

```bash
python scripts/check_chain_status_continuation.py
python scripts/check_chain_snapshot_receipt.py
python scripts/check_chain_auto.py
python scripts/check_guardian_destination.py
```

Expected current state:

```text
CHAIN CONTINUATION: PASS
CHAIN SNAPSHOT RECEIPT: PASS
CHAIN AUTO: PASS
GUARDIAN DESTINATION: BLOCKED
```

The canonical validation workflow is displayed here without the leading dot:

```text
github/workflows/validate-chain-continuation.yml
```

It runs on push, pull request, workflow dispatch, and a daily schedule. The actual repository path begins with a leading dot.

The iOS-safe workflow mirror is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

The mapping is recorded in:

```text
workflow_manifest.json
```

The destination-status report is generated at:

```text
reports/guardian_destination_status.json
```

The blocked destination record exists because no Guardian standing-boundary repository was found under the checked names. This does not change the governance status of the chain. It only prevents future sessions from inventing a destination repo.

## Done State

This repository is considered initially established when it has:

- a publishable Docusaurus configuration;
- a core glossary;
- StegVerse implementation mapping pages;
- comparison pages that explain common governance distinctions;
- a minimal public proof path;
- essays suitable for public linking;
- version-controlled Markdown pages that can be cited, reviewed, and expanded.

## Local Development

```bash
npm install
npm run start
```

## Build

```bash
npm run build
```

## Deploy

This repository includes a GitHub Pages workflow at `github/workflows/deploy.yml`.

Note: the workflow path above is displayed without the leading period for iOS compatibility. The canonical repository path begins with a leading period.

Before enabling deployment, configure GitHub Pages to use **GitHub Actions** as the source.

## Site Structure

```text
docs/
  glossary/
  stegverse/
  comparisons/
  proof-path/
  essays/
  CHAIN_AUTO.json
  CHAIN_STATUS.md
  CHAIN_STATUS_HANDOFF.md
  CHAIN_STATUS_BLOCKED_DESTINATION.md
  CHAIN_STATUS_BLOCKED_DESTINATION.json
  CHAIN_STATUS_CONTINUATION.json
  CHAIN_STATUS_CONTINUATION.schema.json
  CHAIN_SNAPSHOT_v0_1_0.md
  CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json
iosnoperiod/
  github/workflows/validate-chain-continuation.yml
scripts/
  check_chain_status_continuation.py
  check_chain_snapshot_receipt.py
  check_chain_auto.py
  check_guardian_destination.py
workflow_manifest.json
```

## Editorial Standard

Pages should be:

- neutral;
- source-aware;
- distinction-focused;
- version-controlled;
- careful not to overclaim;
- clear about whether a claim is conceptual, implemented, experimental, or proposed.

## Relationship to StegVerse

StegVerse is the originating ecosystem. The Admissibility Wiki is the public vocabulary and explanation layer.

The goal is not to make every StegVerse artifact promotional. The goal is to define the language of admissible transition governance clearly enough that others can evaluate, compare, critique, reuse, or extend it.

StegVerse-Labs - 5% complete
admissibility-wiki - 43% complete
43% complete vs current activation
