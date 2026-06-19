# Admissibility Wiki Mirror Handoff

Generated: 2026-06-19
Repository: `StegVerse-Labs/admissibility-wiki`
Role: non-Site/non-Publisher mirror and continuity handoff for Admissibility Wiki work

## Purpose

This file is the task-source-of-truth handoff for sessions working on `StegVerse-Labs/admissibility-wiki`.

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

## Current Assessment Goal

Continue build work until either the repo reaches completion or the repo contains enough handoff, governance, validation, and next-task structure for ecosystem-managed continuation.

A task is ready for ecosystem-managed continuation when this repository records the current goal, current activation target, installed structure, duplicate-risk paths, next safe build targets, governance records for mature changes, validation expectations, and enough continuity context for another session or ecosystem process to proceed without the originating chat.

## Current Activation Goal

```text
Publish and validate https://stegverse-labs.github.io/admissibility-wiki/ as the GitHub Pages public vocabulary, terminology convergence, proposal-review, and proof-path site.
```

Activation is not complete until the GitHub.io project page loads, GitHub Pages and HTTPS are working, the ontology JSON is reachable, and proposal and decision examples are reachable.

## GitHub Pages URL Configuration

The wiki is currently configured for GitHub Pages project hosting, not a custom domain.

```text
docusaurus.config.js:
  url: https://stegverse-labs.github.io
  baseUrl: /admissibility-wiki/

static/CNAME:
  removed
```

Do not re-add `static/CNAME` unless custom-domain activation is explicitly requested.

## Installed Structure

The repo currently includes:

- Docusaurus scaffold;
- GitHub Pages deployment workflow;
- validation workflow;
- GitHub.io project URL configuration;
- activation runbook;
- contribution guide;
- editorial policy;
- page template;
- terminology convergence governance page;
- proposal lifecycle governance page;
- decision record governance page;
- reconciled Site bridge status page;
- equivalence proposal template;
- equivalence proposal template validator;
- terminology convergence proposal, decision, replay, and evidence examples;
- user-submitted terminology proposal, decision, replay, and evidence examples;
- external-reference dispute proposal, decision, replay, and evidence examples;
- canonical public status JSON mirror with Site bridge posture;
- wiki status validator;
- ontology entries for proposal lifecycle, decision record, terminology convergence, and terminology relationship classes;
- glossary convergence pages;
- current task sync page;
- ontology validation script;
- issue templates;
- pull request template;
- StegVerse mapping pages;
- comparison pages;
- proof-path examples;
- machine-readable vocabulary artifact;
- Admissibility-Wiki AI Entity governance page.

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
docs/governance/site-bridge-status.md
docs/governance/admissibility-wiki-ai-entity.md
docs/governance/equivalence-proposal-template.md
```

## Known Governance Records

Do not recreate existing governance record IDs under `static/governance/`.

## Known Status Artifacts

```text
static/status/admissibility-wiki-status.json
scripts/check-wiki-status.mjs
```

Do not recreate versioned status mirrors unless the status schema is intentionally versioned and the canonical file points to the active version.

## Known Core Artifacts

```text
README.md
CONTRIBUTING.md
package.json
docusaurus.config.js
sidebars.js
scripts/validate-ontology.mjs
scripts/check-wiki-status.mjs
scripts/check-equivalence-proposal-template.mjs
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

## Current Editorial Rule

The Admissibility Wiki should operate as a terminology convergence layer for the sector.

When a StegVerse term and one or more external terms describe the same thing, the identically defined external terms must be added directly under the StegVerse term in an `Equivalent Terms` section.

If an external term is only partially shared, place it under `Overlapping Terms`.

If an external term is nearby but not the same concept, place it under `Adjacent Terms`.

Do not label a term StegVerse-specific until reasonable overlap search has been performed across relevant domains.

Initial glossary convergence should be conservative: if external equivalence has not been researched and accepted, record `No accepted equivalent terms are recorded yet` and place likely candidates under overlapping or adjacent terms.

## Equivalence Proposal Rule

Use this template before accepting an external term relationship claim:

```text
docs/governance/equivalence-proposal-template.md
```

Validate the template with:

```text
node scripts/check-equivalence-proposal-template.mjs
```

Do not add an external term to `Equivalent Terms` without a completed proposal, source evidence, mismatch analysis, overclaiming-risk analysis, and decision record.

## Validation Commands

```text
npm run build
node scripts/validate-ontology.mjs
node scripts/check-wiki-status.mjs
node scripts/check-equivalence-proposal-template.mjs
```

## Next Safe Build Targets

Priority order:

1. Verify GitHub Pages deployment at `https://stegverse-labs.github.io/admissibility-wiki/` after Actions completes.
2. Update activation posture only after public GitHub.io deployment status changes.
3. Add research-backed equivalence proposals only when they materially improve terminology classification.
4. Add additional dispute examples only when they cover a materially new dispute posture.
