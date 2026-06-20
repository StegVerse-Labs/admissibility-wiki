# Admissibility Wiki Mirror Handoff

Generated: 2026-06-20
Repository: `StegVerse-Labs/admissibility-wiki`
Role: non-Site/non-Publisher mirror and continuity handoff for Admissibility Wiki work

## Purpose

This file is the task-source-of-truth handoff for sessions working on `StegVerse-Labs/admissibility-wiki`.

Use this handoff before continuing wiki, ontology, proof-path, governance, proposal-intake, proposal-governance, or activation work in this repo.

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
- user-submitted, browser-originated, maintainer-submitted, and LLM-assisted terminology proposals;
- E/G/F proposal governance routing;
- proposal-governance-core-lite handoff.

## Current Assessment Goal

Continue build work until either the repo reaches completion or the repo contains enough handoff, governance, validation, and next-task structure for ecosystem-managed continuation.

A task is ready for ecosystem-managed continuation when this repository records the current goal, current activation target, installed structure, duplicate-risk paths, next safe build targets, governance records for mature changes, validation expectations, and enough continuity context for another session or ecosystem process to proceed without the originating chat.

## Current Activation Goal

```text
Publish and validate https://stegverse-labs.github.io/admissibility-wiki/ as the GitHub Pages public vocabulary, terminology convergence, proposal-review, proposal-intake, and proof-path site.
```

Activation is not complete until the GitHub.io project page loads, GitHub Pages and HTTPS are working, the ontology JSON is reachable, proposal and decision examples are reachable, and public endpoint status is not overclaimed.

## Proposal Governance Core-Lite Status

The target repository does not exist yet:

```text
StegVerse-Labs/proposal-governance-core-lite
```

A complete seed is installed at:

```text
repo-seeds/proposal-governance-core-lite/
```

Seed documentation and status:

```text
docs/governance/proposal-governance-core-lite-seed.md
docs/governance/proposal-governance-core-lite-creation-task.md
static/status/proposal-governance-core-lite-seed-status.json
scripts/check-proposal-governance-core-lite-seed.mjs
scripts/check-proposal-governance-core-lite-creation-task.mjs
```

Do not create more proposal-governance-core-lite scaffolding in this repo unless the seed validator identifies a gap.

The next formal task is external target repo creation:

```text
Create StegVerse-Labs/proposal-governance-core-lite
Copy repo-seeds/proposal-governance-core-lite/* into it
Run npm run validate in the target repo
```

## Proposal Intake and Governance Routing

Installed proposal governance routing:

```text
E = Editorial
G = Governance
F = Formalism
```

Every ingestion/CGE pass must emit to master-records.

Public display is a consequence path only and requires a decision record.

The proposal page or shared SDK entry point emits governed manifest/receipt data. The sandbox is non-authoritative and preserves candidate paths. After sandbox return, ingestion/CGE routes to master-records and then to the second StegVerse-Labs core-lite target.

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

## Deployment Gate

The GitHub Pages deploy workflow is validation-gated.

```text
github/workflows/deploy.yml:
  install dependencies
  npm run validate
  upload build artifact
  deploy pages
```

`npm run validate` is the preferred aggregate command and must pass before the Pages artifact is uploaded.

Note: paths that normally begin with a leading dot are shown without the leading dot in this handoff display to avoid hidden-path ambiguity in copied instructions.

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
- proposal governance class page;
- proposal-governance-core-lite seed page;
- proposal-governance-core-lite creation task page;
- proposal intake interface, backend contract, API deployment, endpoint verification, and final activation handoff pages;
- reconciled Site bridge status page;
- equivalence proposal template;
- equivalence proposal template validator;
- activation checklist and validator;
- relationship status summary and validator;
- public activation receipt example and validator;
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
- Admissibility-Wiki AI Entity governance page;
- proposal-governance-core-lite seed and validators.

## Known Governance Files

Do not recreate these under alternate names:

```text
docs/governance/editorial-policy.md
docs/governance/page-template.md
docs/governance/terminology-convergence.md
docs/governance/proposal-lifecycle.md
docs/governance/decision-record.md
docs/governance/proposal-governance-classes.md
docs/governance/proposal-governance-core-lite-seed.md
docs/governance/proposal-governance-core-lite-creation-task.md
docs/governance/proposal-intake-interface.md
docs/governance/proposal-intake-backend-contract.md
docs/governance/proposal-intake-api-deployment.md
docs/governance/intake-api-final-activation-handoff.md
docs/governance/validation.md
docs/governance/current-task-sync.md
docs/governance/site-bridge-status.md
docs/governance/admissibility-wiki-ai-entity.md
docs/governance/equivalence-proposal-template.md
docs/governance/relationship-status-summary.md
docs/governance/relationship-validator-status.md
docs/governance/public-activation-verification.md
```

## Known Status Artifacts

```text
static/status/admissibility-wiki-status.json
static/status/admissibility-wiki-activation.json
static/status/public-activation-receipt.example.json
static/status/proposal-governance-core-lite-seed-status.json
static/status/proposal-intake-backend-status.json
static/status/proposal-intake-endpoint-verification-status.json
static/status/intake-api-deploy-config-status.json
scripts/check-wiki-status.mjs
scripts/check-activation-checklist.mjs
scripts/check-public-activation-receipt.mjs
scripts/check-proposal-governance-core-lite-seed.mjs
scripts/check-proposal-governance-core-lite-creation-task.mjs
```

Do not recreate versioned status mirrors unless the status schema is intentionally versioned and the canonical file points to the active version.

## Validation Commands

```text
npm run validate
node scripts/validate-ontology.mjs
node scripts/check-wiki-status.mjs
node scripts/check-activation-checklist.mjs
node scripts/check-equivalence-proposal-template.mjs
node scripts/check-relationship-status-summary.mjs
node scripts/check-public-activation-receipt.mjs
node scripts/check-proposal-governance-classes.mjs
node scripts/check-proposal-governance-core-lite-seed.mjs
node scripts/check-proposal-governance-core-lite-creation-task.mjs
npm run build
```

`npm run validate` is the preferred aggregate command because it runs the installed validators and the Docusaurus build. If a newly installed validator is not yet included in `npm run validate`, run it directly and then wire it into the aggregate when safe.

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

## Next Safe Build Targets

Priority order:

1. Create `StegVerse-Labs/proposal-governance-core-lite` externally, copy the seed, and validate it independently.
2. Verify GitHub Pages deployment at `https://stegverse-labs.github.io/admissibility-wiki/` after Actions completes.
3. Deploy authorized intake API runtime, then run endpoint verification workflow.
4. Update activation posture only after public GitHub.io deployment and endpoint evidence exists.
5. Add research-backed equivalence proposals only when they materially improve terminology classification.

## Mirror Coordination Rule

For Admissibility Wiki work:

1. First check this file.
2. Then check `docs/governance/current-task-sync.md`.
3. Then check exact repo paths before creating new pages.
4. Update this file whenever goal, activation target, installed structure, validation surface, or cross-session overlap changes.

## Current Redundancy Posture

This repository is actively touched by more than one session.

Do not assume a previously proposed next step is still missing.

Verify file presence first, then continue from the missing or explicitly open item.
