---
title: Admissibility Wiki
slug: /
---

# Admissibility Wiki

The Admissibility Wiki is a public vocabulary, terminology convergence, proposal-review, and proof-path site for transition governance.

It exists so that StegVerse concepts can be defined in stable, linkable, version-controlled pages before they are compressed into posts, demos, issues, papers, implementation claims, or external commentary.

## Why This Page Exists

This landing page explains the current standing of the wiki itself.

It answers four questions:

1. What is the Admissibility Wiki?
2. What is the AI-governed proposal system?
3. Which transition-table elements define the wiki system as it currently stands?
4. Which transition blocks describe how proposals move through the wiki?

The page is not a proof engine. It is a public orientation layer for understanding how the wiki, its proposal intake, and its governance records fit together.

## What This Wiki Is

This wiki is a reference and convergence layer for concepts such as:

- admissibility;
- transition governance;
- commit-time authority;
- commit-time validity;
- receipt-bound execution;
- governance boundaries;
- reconstructability;
- consequence standing;
- continuity;
- drift;
- authority classes;
- evidence posture;
- review posture;
- terminology equivalence;
- proposal lifecycle;
- decision records.

## Formalism Discovery

The Formalism Discovery Engine indexes formalism terms, generates review-required candidate relationships, preserves source origins, and prevents synonymy or equivalence from being promoted without a recorded decision.

Start here:

- [Discovery Index](./discovery/index.md)
- [Canonical Formalism Catalog](./formalisms/canonical-catalog.md)
- [Canonical Formalism Graph Index](./formalisms/formalism-graph-index.md)

## What This Wiki Is Not

This wiki is not Wikipedia.

It does not assert that every StegVerse term has independent encyclopedic notability. It provides a stable public vocabulary so that others can understand, critique, compare, cite, map, dispute, and test the concepts.

This wiki also does not make user submissions authoritative merely because they were received.

## AI-Governed Proposal System

The AI-governed proposal system is the wiki process by which user-submitted, maintainer-submitted, browser-originated, LLM-assisted, and AI-entity-suggested changes enter structured review.

A proposal may request a new term, a revised definition, an equivalence claim, an overlap claim, an adjacent-term mapping, an implementation mapping, an external reference, a counterexample, a dispute, or a proof-path example.

Submission creates a proposal record and a submission receipt. It does not create acceptance authority.

A proposal becomes accepted, rejected, deferred, escalated, refused, or superseded only through a decision record that identifies the relevant authority class, policy reference, evidence posture, review posture, and commit-time validity posture.

For user proposals, the submission receipt should also record relevant task timing for the intake process, including when the proposal was received, when the receipt was issued, which submission-stage tasks ran, and when those tasks started and completed.

## Transition-Table Elements Defining This Wiki

The wiki can be described as a governed system using the same transition-table vocabulary it documents.

| Element | Current Wiki Meaning |
| --- | --- |
| Transition | A proposed change to wiki content, ontology, governance policy, proof-path examples, status mirrors, or terminology mappings. |
| Actor / proposer | Maintainer, contributor, external user, browser-originated flow, LLM-assisted draft, or AI Entity suggestion. |
| Authority class | The declared standing of the actor or process, such as `wiki_maintainer`, `vocabulary_editor`, `contributor_suggest`, or `admissibility_wiki_ai_entity`. |
| Policy reference | The rule basis for the wiki decision, currently represented by `policy.wiki.page-review.v1` and related governance pages. |
| Evidence posture | The state of supporting information, such as none, partial, present, sufficient, conflicting, stale, or insufficient. |
| Review posture | The state of review, such as submitted, receipt issued, triaged, under review, needs evidence, entity reviewed, maintainer reviewed, or quorum reviewed. |
| Drift | A relevant change in page state, ontology state, evidence, proposal content, external terminology, or review context that may affect the decision. |
| Decision result | ALLOW, DENY, ESCALATE, REFUSE, DEFER, SUPERSEDE, or another declared wiki-governance result. |
| Receipt | A durable record of the proposal, timing, review, decision, replay, and reconstruction links. |
| Commit-time validity | Whether the page or governance change had standing when it was accepted into the wiki. |
| Reconstruction link | The evidence path needed to reconstruct why a wiki change appeared to have standing. |
| Replay link | The artifact or note used to re-check the decision path when available. |

## Transition Blocks For Wiki Proposals

The current wiki system is defined by these transition blocks.

### 1. Submission Block

A user, maintainer, browser flow, LLM-assisted process, or AI Entity suggestion submits a proposal.

The system records:

- proposal ID;
- proposer class;
- proposal class;
- target page or artifact;
- claimed terminology relationships;
- evidence posture;
- submission timing;
- receipt link.

The submission block produces a receipt, not an acceptance.

### 2. Intake Timing Block

The system records relevant task timing for the proposal intake path.

Timing may include:

- submission received;
- field normalization started and completed;
- relationship classification started and completed;
- duplicate or related-proposal check started and completed;
- review route assignment started and completed;
- receipt issued.

Timing supports reconstructability. It does not prove that the proposal is correct.

### 3. Relationship Classification Block

If the proposal includes terminology mapping, the wiki classifies each claim as one of:

- equivalent;
- overlapping;
- adjacent;
- broader than;
- narrower than;
- contradicts;
- unresolved.

Equivalent terms should appear directly under the StegVerse term only after review accepts the equivalence claim.

### 4. Review Block

The proposal is reviewed under the declared wiki policy and authority class.

Review may be human, AI Entity assisted, maintainer reviewed, quorum reviewed, external-reference reviewed, or escalated.

Review does not erase the proposal record. It produces or informs a decision record.

### 5. Decision Block

A decision record states whether the proposal is allowed, denied, escalated, refused, deferred, accepted experimentally, accepted as an external view, or superseded.

The decision record should identify:

- proposal ID;
- target page;
- authority class;
- policy reference;
- evidence posture;
- review posture;
- decision result;
- relationship disposition;
- commit-time validity;
- issued timestamp.

### 6. Publication Block

If accepted, the change becomes part of the wiki content, ontology, governance record set, or status mirror.

If rejected, deferred, escalated, or refused, the proposal may still remain useful as a reconstructable record of why the wiki did not accept the submitted claim.

### 7. Replay And Reconstruction Block

Mature wiki changes should provide enough links or records for a reviewer to reconstruct why the decision appeared to have standing.

Replay and reconstruction records do not make the wiki a formal proof authority. They make the wiki decision path visible.

## Current Standing Of The Wiki System

The wiki currently has:

- a Docusaurus site structure;
- a glossary surface;
- governance pages;
- terminology convergence rules;
- proposal lifecycle rules;
- a formalism discovery layer with generated term and candidate relationship stores;
- executable validation that regenerates discovery records and fail-closes on uncommitted generated drift.
