# Admissibility Wiki Mirror Handoff

Generated: 2026-06-19
Repository: `StegVerse-Labs/admissibility-wiki`
Role: non-Site/non-Publisher mirror and continuity handoff for Admissibility Wiki work

## Purpose

This file is the task-source-of-truth handoff for sessions working on `StegVerse-Labs/admissibility-wiki`.

It serves the same coordination purpose as `StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md`, but is scoped to the Admissibility Wiki repository.

Use this handoff before continuing wiki, ontology, proof-path, governance, or activation work in this repo.

## Current Repo Goal

Make the Admissibility Wiki a governed, public-facing vocabulary layer and terminology convergence surface for:

- admissibility;
- transition governance;
- commit-time authority;
- receipt-bound execution;
- reconstructability;
- proof-path examples;
- machine-readable vocabulary artifacts;
- repo-local governance and validation;
- cross-domain equivalent, overlapping, and adjacent terminology;
- user-submitted, browser-originated, maintainer-submitted, and LLM-assisted terminology proposals.

## Current Activation Goal

The current activation goal is:

```text
Publish and validate admissibility.stegverse.org as a Docusaurus-powered public vocabulary, terminology convergence, proposal-review, and proof-path site.
```

Activation is not complete until:

- GitHub Pages deploys from GitHub Actions;
- Cloudflare DNS points `admissibility.stegverse.org` to GitHub Pages;
- GitHub validates the custom domain;
- HTTPS is provisioned and enforced;
- the public site loads;
- the ontology JSON is reachable from the published site;
- proposal and decision examples are reachable from the published site.

## Installed Structure

The repo currently includes:

- Docusaurus scaffold;
- GitHub Pages deployment workflow;
- validation workflow;
- custom-domain support file;
- activation runbook;
- contribution guide;
- editorial policy;
- page template;
- terminology convergence governance page;
- proposal lifecycle governance page;
- decision record governance page;
- current task sync page;
- ontology validation script;
- issue templates;
- pull request template;
- glossary wave 1;
- glossary wave 2;
- StegVerse mapping pages;
- comparison pages;
- proof-path examples;
- machine-readable vocabulary artifact;
- Admissibility-Wiki AI Entity governance page.

## Known Installed Proof-Path Examples

Do not recreate these under alternate names:

```text
docs/proof-path/transition-cell-example.md
docs/proof-path/receipt-example.md
docs/proof-path/replay-example.md
docs/proof-path/deny-example.md
docs/proof-path/escalate-example.md
docs/proof-path/refuse-example.md
docs/proof-path/drift-denial-example.md
```

## Known Governance Files

Do not recreate these under alternate names:

```text
docs/governance/editorial-policy.md
docs/governance/page-template.md
docs/governance/terminology-convergence.md
docs/governance/proposal-lifecycle.md
docs/governance/decision-record.md
docs/governance/validation.md
docs/governance/current-task-sync.md
docs/governance/admissibility-wiki-ai-entity.md
```

## Known Core Artifacts

```text
README.md
CONTRIBUTING.md
package.json
docusaurus.config.js
sidebars.js
scripts/validate-ontology.mjs
static/CNAME
static/img/favicon.svg
static/ontology/admissibility-vocabulary.v0.1.json
github/workflows/deploy.yml
github/workflows/validate.yml
github/PULL_REQUEST_TEMPLATE.md
github/ISSUE_TEMPLATE/config.yml
github/ISSUE_TEMPLATE/glossary-term.yml
github/ISSUE_TEMPLATE/proof-path-example.yml
github/ISSUE_TEMPLATE/activation-deploy.yml
```

Note: paths that normally begin with a leading dot are shown without the leading dot in this handoff display to avoid hidden-path ambiguity in copied instructions.

## Confirmed Cross-Session Overlap

At least one other chat session has worked on this repository.

Confirmed installed overlap includes:

- DENY proof-path example;
- ESCALATE proof-path example;
- REFUSE proof-path example;
- drift-denial proof-path example;
- Admissibility-Wiki AI Entity governance page;
- terminology convergence governance;
- proposal lifecycle governance;
- decision record governance.

Before adding a page, check exact paths and `sidebars.js`.

## Checked Missing Or Still Open

The following path was previously checked and not found, but is now installed:

```text
docs/governance/proposal-lifecycle.md
```

## Current Editorial Rule

The Admissibility Wiki should operate as a terminology convergence layer for the sector.

When a StegVerse term and one or more external terms describe the same thing, the identically defined external terms must be added directly under the StegVerse term in an `Equivalent Terms` section.

If an external term is only partially shared, place it under `Overlapping Terms`.

If an external term is nearby but not the same concept, place it under `Adjacent Terms`.

Do not label a term StegVerse-specific until reasonable overlap search has been performed across relevant domains.

## Next Safe Build Targets

Priority order:

1. Proposal JSON examples.
2. Decision JSON examples.
3. Replay skeleton for decision examples.
4. Reconstruction evidence skeleton for decision examples.
5. Add ontology entries for proposal lifecycle, decision record, and terminology relationship classes.
6. Update selected glossary pages to include equivalent, overlapping, and adjacent terminology sections.
7. Update validation expectations if new artifact directories are added.
8. Coordinate with `StegVerse-Labs/Site` only after checking `Site/docs/SITE_MIRROR_HANDOFF.md`.

## Mirror Coordination Rule

For Site or Publisher work:

1. First check `StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md`.
2. Treat that file as source of truth.
3. Do not mirror or alter public display files without reconciling that handoff.

For Admissibility Wiki work:

1. First check this file.
2. Then check `docs/governance/current-task-sync.md`.
3. Then check exact repo paths before creating new pages.
4. Update this file whenever goal, activation target, installed structure, or cross-session overlap changes.

## Current Redundancy Posture

This repository is actively touched by more than one session.

Do not assume a previously proposed next step is still missing.

Verify file presence first, then continue from the missing or explicitly open item.

## Archival Readiness Rule

A chat thread is archive-ready when this handoff and `docs/governance/current-task-sync.md` contain all remaining tasks needed to continue without reading the full chat transcript.

## Current Next Action

Build proposal and decision JSON examples, then build replay and reconstruction skeletons for those examples.
