---
title: Current Task Sync
---

# Current Task Sync

This page prevents duplicate work across parallel StegVerse build sessions working on `StegVerse-Labs/admissibility-wiki`.

## Done State

This sync page is useful when it clearly states:

- what is installed;
- what appears to overlap with another session;
- what was checked and not found;
- what should not be duplicated;
- what the next safe build target is.

## Current Assessment Goal

Continue build work until either the repo reaches completion or the repo contains enough handoff, governance, validation, and next-task structure for ecosystem-managed continuation.

A task is ready for ecosystem-managed continuation when the repo records enough current state, installed structure, duplicate-risk, validation, and next-action context for another session or ecosystem process to proceed without the originating chat.

## Installed In This Repo

The repository currently includes:

- Docusaurus site scaffold;
- expanded landing page defining the wiki, AI-governed proposal system, transition-table elements, and proposal transition blocks;
- GitHub Pages deployment workflow;
- custom-domain file for `admissibility.stegverse.org`;
- activation runbook;
- contribution guide;
- editorial policy;
- page template;
- terminology convergence governance page;
- proposal lifecycle governance page with submission timing receipt requirements;
- decision record governance page;
- reconciled Site bridge status page;
- equivalence proposal template;
- equivalence proposal template validator;
- terminology overlap research notes;
- terminology convergence proposal, decision, replay, and evidence examples;
- user-submitted terminology proposal, decision, replay, and evidence examples with submission timing;
- external-reference dispute proposal, decision, replay, and evidence examples;
- source-backed provenance overlap proposal, decision, replay, and evidence examples;
- public status JSON mirror at `static/status/admissibility-wiki-status.json`;
- wiki status validator;
- ontology entries for proposal lifecycle, decision record, terminology convergence, and terminology relationship classes;
- first glossary convergence wave for commit-time authority, commit-time validity, receipt-bound execution, and reconstructability;
- wave-2 glossary convergence for admissibility, transition, authority class, policy reference, evidence posture, review posture, drift, and governance boundary;
- validation runbook;
- validation workflow;
- ontology validation script;
- issue templates;
- pull request template;
- core glossary pages;
- proof-path examples;
- Admissibility-Wiki AI Entity governance page.

## Known Governance Records

Do not recreate these IDs:

```text
static/governance/proposals/proposal.example.001.json
static/governance/decisions/decision.example.001.json
static/governance/replay/decision.example.001.txt
static/governance/evidence/decision.example.001/README.md
static/governance/proposals/proposal.example.002.json
static/governance/decisions/decision.example.002.json
static/governance/replay/decision.example.002.txt
static/governance/evidence/decision.example.002/README.md
static/governance/proposals/proposal.example.003.json
static/governance/decisions/decision.example.003.json
static/governance/replay/decision.example.003.txt
static/governance/evidence/decision.example.003/README.md
static/governance/proposals/proposal.example.004.json
static/governance/decisions/decision.example.004.json
static/governance/replay/decision.example.004.txt
static/governance/evidence/decision.example.004/README.md
static/governance/proposals/proposal.example.005.json
static/governance/decisions/decision.example.005.json
static/governance/replay/decision.example.005.txt
static/governance/evidence/decision.example.005/README.md
```

## Known Public Governance Pages

Do not recreate these pages under alternate names:

```text
docs/governance/terminology-convergence.md
docs/governance/proposal-lifecycle.md
docs/governance/decision-record.md
docs/governance/site-bridge-status.md
docs/governance/admissibility-wiki-ai-entity.md
docs/governance/equivalence-proposal-template.md
docs/governance/current-task-sync.md
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/index.md
```

## Known Research Pages

```text
docs/research/terminology-overlap-research-notes.md
```

## Known Validators

```text
scripts/validate-ontology.mjs
scripts/check-wiki-status.mjs
scripts/check-equivalence-proposal-template.mjs
```

## Known Glossary Convergence Pages

The following glossary pages already include terminology relationship sections and should not be reworked without a specific improvement target:

```text
docs/glossary/admissibility.md
docs/glossary/transition.md
docs/glossary/authority-class.md
docs/glossary/policy-reference.md
docs/glossary/evidence-posture.md
docs/glossary/review-posture.md
docs/glossary/drift.md
docs/glossary/commit-time-authority.md
docs/glossary/commit-time-validity.md
docs/glossary/receipt-bound-execution.md
docs/glossary/governance-boundary.md
docs/glossary/reconstructability.md
```

## Current Editorial Rule

The wiki now treats terminology work as a convergence-layer task.

When a StegVerse term has materially identical terms in other domains, those terms should be placed directly under the StegVerse term in an `Equivalent Terms` section.

Overlapping and adjacent terms should be listed separately, so the page can distinguish shared vocabulary from StegVerse-specific extensions.

Initial glossary convergence should be conservative: if external equivalence has not been researched and accepted, record `No accepted equivalent terms are recorded yet` and place likely candidates under overlapping or adjacent terms.

## Equivalence Proposal Rule

Do not add an external term to `Equivalent Terms` without a completed proposal using:

```text
docs/governance/equivalence-proposal-template.md
```

Validate the template with:

```text
node scripts/check-equivalence-proposal-template.mjs
```

A proposal may classify a term as equivalent, overlapping, adjacent, broader, narrower, contradictory, or unresolved. Acceptance requires a decision record before glossary text changes.

## Accepted Relationship Updates

The following relationship decisions have changed target-page text:

```text
proposal.example.005 / decision.example.005:
  target_page: docs/glossary/reconstructability.md
  external_term: Provenance
  disposition: accepted as Overlapping Terms only
  equivalent_status: not accepted
```

## Landing Page Rule

The landing page should explicitly explain why the wiki exists, define the AI-governed proposal system, and show the current transition-table elements and proposal transition blocks that define the wiki as it stands.

## Submission Receipt Timing Rule

User-submitted proposals should include a `submission_timing` block in the submission receipt.

The timing block should record when the proposal was received, when the receipt was issued, and the start/completion/status/timing posture for relevant submission-stage tasks.

Submission timing records intake posture only. It does not accept the proposal, prove the submitted claim, or replace the decision record.

## Next Safe Build Targets

The safest next build targets are:

1. Add another source-backed relationship proposal using the installed equivalence proposal template, preferably for OPA/policy-as-code versus Policy Reference or Commit-Time Authority.
2. Update activation posture only after public deployment or DNS status changes.
3. Add additional dispute examples only when they cover a materially new dispute posture.

## Build Rule

Before adding a new page, check whether the exact concept already exists in:

- `docs/glossary/`;
- `docs/governance/`;
- `docs/proof-path/`;
- `static/ontology/admissibility-vocabulary.v0.1.json`;
- `sidebars.js`.

When a concept is added, update:

- the page itself;
- related pages;
- the sidebar;
- the ontology artifact if it is a core term;
- validation expectations if structure changes.
