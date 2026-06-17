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

## Current Redundancy Posture

There is confirmed overlap with at least one other chat session working on this same repository.

This does not mean the work is invalid.

It means future tasks should check installed files before rebuilding pages, templates, workflows, or ontology entries.

## Installed In This Repo

The repository currently includes:

- Docusaurus site scaffold;
- GitHub Pages deployment workflow;
- custom-domain file for `admissibility.stegverse.org`;
- activation runbook;
- contribution guide;
- editorial policy;
- page template;
- validation runbook;
- validation workflow;
- ontology validation script;
- issue templates;
- pull request template;
- core glossary pages;
- glossary expansion wave 2;
- machine-readable vocabulary artifact;
- proof-path examples.

## Confirmed Overlap

The following proof-path expansion files were found in the repo and should not be recreated under alternate names:

```text
docs/proof-path/deny-example.md
docs/proof-path/escalate-example.md
```

## Checked And Not Found

The following expected or discussed paths were checked and were not present at the time of this sync page:

```text
docs/governance/ai-entity-review-posture.md
docs/governance/proposal-lifecycle.md
```

These may still exist under different filenames, may have been planned but not installed, or may be pending in another session.

## Do Not Duplicate

Do not create duplicate versions of these already-installed concepts without first checking exact paths:

- DENY proof path;
- ESCALATE proof path;
- authority class;
- policy reference;
- evidence posture;
- review posture;
- drift;
- commit-time validity;
- activation runbook;
- ontology validation;
- contributor and PR templates.

## Next Safe Build Targets

The safest next build targets are:

1. Proposal lifecycle vocabulary and page set.
2. Decision record vocabulary and page set.
3. AI entity review posture page, if still not found.
4. REFUSE proof-path example, if not already present.
5. Drift-denial proof-path example, if not already present.
6. StegVerse-Labs/Site bridge status page, if not already installed elsewhere.

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
