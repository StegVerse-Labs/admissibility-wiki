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
- GitHub Pages deployment workflow;
- custom-domain file for `admissibility.stegverse.org`;
- activation runbook;
- contribution guide;
- editorial policy;
- page template;
- terminology convergence governance page;
- proposal lifecycle governance page;
- decision record governance page;
- terminology convergence proposal, decision, replay, and evidence examples;
- user-submitted terminology proposal, decision, replay, and evidence examples;
- public status JSON mirror at `static/status/admissibility-wiki-status.json`;
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

## Next Safe Build Targets

The safest next build targets are:

1. Add StegVerse-Labs/Site bridge status page, if not already installed elsewhere.
2. Add external-reference dispute examples if needed.
3. Add research-backed equivalence proposals for selected glossary pages after broad cross-domain terminology review.

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
