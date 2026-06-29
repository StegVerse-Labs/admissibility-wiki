# Admissibility Wiki Mirror Handoff

Generated: 2026-06-29
Repository: `StegVerse-Labs/admissibility-wiki`
Role: public vocabulary, terminology convergence, proposal-review, proof-path, and external-framework crosswalk site

## Purpose

This file is the task-source-of-truth handoff for sessions working on `StegVerse-Labs/admissibility-wiki`.

Use this handoff before continuing wiki, ontology, proof-path, governance, proposal-intake, proposal-governance, external-framework, or activation work in this repo.

## Current Repo Goal

The active goal is:

```text
declarative-external-framework-generation-pipeline
```

The goal is to make external-framework pages, evaluation status, compatibility reports, and public evaluation results reproducible from governed artifacts while preserving authored analysis and denying execution-authority inheritance.

## Current Assessment Goal

Continue build work until either the repo reaches completion or the repo contains enough handoff, governance, validation, and next-task structure for ecosystem-managed continuation.

A task is ready for ecosystem-managed continuation when this repository records the current goal, current activation target, installed structure, duplicate-risk paths, next safe build targets, governance records for mature changes, validation expectations, and enough continuity context for another session or ecosystem process to proceed without the originating chat.

## Current Activation Goal

```text
Publish and validate https://stegverse-labs.github.io/admissibility-wiki/ as the GitHub Pages public vocabulary, terminology convergence, proposal-review, proposal-intake, proof-path, and external-framework crosswalk site.
```

Activation is not complete until GitHub Pages loads, HTTPS works, ontology JSON is reachable, proposal and decision examples are reachable, generated external-framework evaluation results are reachable, generated framework page-status blocks are included in the build, and public endpoint status is not overclaimed.

## Path Display Rule

Paths normally beginning with a leading dot are displayed without that leading dot in this handoff for iOS readability. Actual repository paths that display as `github/...` use `.github/...` in the repository.

## Single Workflow Policy

Only one active workflow is intended to exist:

```text
github/workflows/validate-chain-continuation.yml
```

The iOS-safe mirror is inert and exists only for copied path readability:

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

Workflow sprawl is guarded by:

```text
scripts/check_workflow_sprawl.py
```

Do not reintroduce separate active workflows for validation, deployment, evidence watch, success recording, proposal watching, or framework result posting.

## Current Declarative External Framework Pipeline

The active external-framework pipeline is:

```text
framework manifest
  -> generated compatibility report
  -> generated evaluation results page
  -> generated framework page-status block
  -> Docusaurus build
  -> GitHub Pages deploy
  -> public URL verification
```

Installed generators:

```text
scripts/generate_external_framework_reports.py
scripts/generate_external_framework_results.py
scripts/generate_external_framework_page_status.py
```

Installed validators:

```text
scripts/check_external_framework_reports.py
scripts/check_external_framework_report_coverage.py
scripts/check_external_framework_report_generation.py
scripts/check_external_framework_results_page.py
scripts/check_external_framework_page_status.py
scripts/check_external_framework_terminology.py
scripts/check_external_framework_expansion_policy.py
```

Generated public surface:

```text
docs/external-frameworks/evaluation-results.md
```

Generated page-status blocks are inserted into registered framework pages from manifests plus compatibility reports. They are compatibility evidence only and are not certification, endorsement, formalism adoption, admissibility proof, or execution authority.

## Deployment Gate

The single canonical workflow performs validation and, on main-branch push, performs build/deploy/public verification.

```text
github/workflows/validate-chain-continuation.yml:
  validate single workflow policy
  generate external framework reports
  generate external framework evaluation results
  generate external framework page status
  validate governance/status/goal/workflow artifacts
  validate external framework registry, manifests, terminology, reports, coverage, generation, results page, and page status
  validate CI evidence state
  resolve Guardian destination
  build Docusaurus site
  deploy GitHub Pages
  verify deployed site root
  verify generated external-framework evaluation results page
```

## Installed Structure

The repo currently includes:

- Docusaurus scaffold;
- single canonical validation/build/deploy workflow;
- iOS-safe workflow mirror;
- workflow sprawl validator;
- workflow manifest;
- chain auto state;
- CI evidence state;
- goal state;
- generated external-framework report pipeline;
- generated external-framework result page pipeline;
- generated external-framework page-status pipeline;
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
- CTA and IICT formalism mirror pages;
- CTA and IICT formalism registry records.

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

## Known Formalism Files

Do not recreate these under alternate names:

```text
docs/formalisms/index.md
docs/formalisms/canonical-catalog.md
docs/formalisms/commit-time-admissibility.md
docs/formalisms/irreversibility-inference-convergence-theorem.md
static/formalisms/formalism-registry.v0.1.json
```

## Known Workflow Files

Displayed without leading dot for iOS readability; actual repository paths use the leading-dot directory.

```text
github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
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
static/status/workflow-receipt-automation-status.json
static/status/proposal-core-lite-target-watch-status.json
static/status/no-manual-task-guard-status.json
static/status/mirror-handoff-guard-status.json
static/status/workflow-evidence-status.json
```

## Validation and Receipt Automation

```text
Validation trigger: push, pull_request, workflow_dispatch, scheduled run
Validation command: python validators in canonical workflow plus npm run validate in build path
Deployment trigger: main-branch push after validation job
Public verification: canonical workflow verify-public-pages job
Failure evidence: workflow job result and bounded CI evidence state
Workflow evidence status validator: scripts/check-workflow-evidence-status.mjs
No-manual-task guard validator: scripts/check-no-manual-task-assignments.mjs
Mirror handoff guard validator: scripts/check-mirror-handoff-guard.mjs
Manual task requirement: none recorded in this handoff
```

`npm run validate` remains the preferred local aggregate command for Node/Docusaurus governance validation. The canonical workflow also runs Python validators for the external-framework and chain-continuation surfaces.

## Proposal Governance Core-Lite Status

The proposal-governance-core-lite seed remains installed at:

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

Do not create more proposal-governance-core-lite scaffolding in this repo unless a validator identifies a gap.

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

## Known Remaining Installation Targets

```text
StegVerse-Labs/admissibility-wiki:
  - framework-page full generator for non-status sections
  - generated framework-page validator for full declarative pages
  - generated narrative boundary that preserves authored analysis while generating repeatable metadata

StegVerse-Labs/Site:
  - mirror/public summary of generated external-framework evaluation results after admissibility-wiki release/tag

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness for generated external-framework result artifacts after admissibility-wiki release/tag

stegguardian-wiki:
  - downstream summary of framework execution-authority boundary once admissibility-wiki release/tag is stable
```

## Priority Order

1. Let repo automation validate, build, deploy, verify public URLs, generate framework reports, generate framework results, generate page-status blocks, and emit bounded artifacts.
2. If automation fails, repair only the first failing validator field, generated artifact drift, build issue, deployment issue, public URL check, or handoff inconsistency identified by failed job logs.
3. Continue the declarative external-framework generation pipeline by generating additional repeatable page sections from manifests and reports.
4. Deploy authorized intake API runtime only when source-confirmed runtime authority exists.
5. Update activation posture only after public GitHub.io deployment and endpoint evidence exists.
6. Add research-backed equivalence proposals only when they materially improve terminology classification.

## Mirror Coordination Rule

For Admissibility Wiki work:

1. First check this file.
2. Then check `docs/governance/current-task-sync.md`.
3. Then check exact repo paths before creating new pages.
4. Update this file whenever goal, activation target, installed structure, validation surface, or cross-session overlap changes.

## Current Redundancy Posture

This repository may be touched by more than one session.

Do not assume a previously proposed next step is still missing.

Verify file presence first, then continue from the missing or explicitly open item.
