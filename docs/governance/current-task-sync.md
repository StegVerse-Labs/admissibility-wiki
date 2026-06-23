---
title: Current Task Sync
---

# Current Task Sync

This page prevents duplicate work across parallel StegVerse build sessions working on `StegVerse-Labs/admissibility-wiki`.

## Current GitHub Pages Target

```text
https://stegverse-labs.github.io/admissibility-wiki/
```

```text
url: https://stegverse-labs.github.io
baseUrl: /admissibility-wiki/
custom_domain: not_configured
static/CNAME: removed
```

## Current Assessment Goal

Continue build work until either the repo reaches completion or the repo contains enough handoff, governance, validation, and next-task structure for ecosystem-managed continuation.

## Installed Activation Structure

```text
docs/activation/github-pages-cloudflare.md
static/status/admissibility-wiki-activation.json
static/status/admissibility-wiki-status.json
static/status/public-activation-receipt.example.json
github/workflows/deploy.yml
```

Note: paths that normally begin with a leading dot are shown without the leading dot in this display rule only.

## Installed Validators

```text
scripts/validate-ontology.mjs
scripts/check-wiki-status.mjs
scripts/check-activation-checklist.mjs
scripts/check-equivalence-proposal-template.mjs
scripts/check-relationship-status-summary.mjs
scripts/check-public-activation-receipt.mjs
scripts/check-formalism-registry.mjs
scripts/check-formalism-publication-artifacts.mjs
scripts/check-formalism-source-sync.mjs
scripts/check-external-frameworks.mjs
scripts/check-publication-chain-guard.mjs
scripts/check-publication-verification-status.mjs
scripts/check-transition-origin-governance.mjs
scripts/check-proposal-governance-classes.mjs
scripts/check-proposal-intake-interface.mjs
scripts/check-proposal-intake-backend.mjs
scripts/check-proposal-intake-runtime.mjs
scripts/check-proposal-intake-api.mjs
scripts/check-proposal-intake-api-deployment.mjs
scripts/check-proposal-intake-api-deployment-receipt.mjs
```

Aggregate validation is run by repo automation:

```text
npm run validate
```

The deploy workflow validates governance artifacts, builds the Docusaurus site, deploys to GitHub Pages, and verifies public URLs for the site root, formalism index, CTA formalism page, and IICT formalism page.

## Installed Formalism Mirrors

Do not recreate these pages under alternate names:

```text
docs/formalisms/index.md
docs/formalisms/canonical-catalog.md
docs/formalisms/commit-time-admissibility.md
docs/formalisms/irreversibility-inference-convergence-theorem.md
static/formalisms/formalism-registry.v0.1.json
```

Current source links:

```text
Admissible-Existence/CTA -> Commit-Time Admissibility
Admissible-Existence/IICT -> Irreversibility-Inference Convergence Theorem
```

Boundary:

```text
CTA baseline tests do not prove the complete CTA formalism.
IICT baseline tests do not prove the theorem.
IICT does not replace CTA.
The wiki mirrors and explains; it does not create source authority or proof authority.
```

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
static/governance/proposals/proposal.example.006.json
static/governance/decisions/decision.example.006.json
static/governance/replay/decision.example.006.txt
static/governance/evidence/decision.example.006/README.md
static/governance/proposals/proposal.example.007.json
static/governance/decisions/decision.example.007.json
static/governance/replay/decision.example.007.txt
static/governance/evidence/decision.example.007/README.md
static/governance/proposals/proposal.example.008.json
static/governance/decisions/decision.example.008.json
static/governance/replay/decision.example.008.txt
static/governance/evidence/decision.example.008/README.md
static/governance/proposals/proposal.example.009.json
static/governance/decisions/decision.example.009.json
static/governance/replay/decision.example.009.txt
static/governance/evidence/decision.example.009/README.md
```

## Known Public Pages

Do not recreate these pages under alternate names:

```text
docs/index.md
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/current-task-sync.md
docs/governance/terminology-convergence.md
docs/governance/proposal-lifecycle.md
docs/governance/decision-record.md
docs/governance/site-bridge-status.md
docs/governance/admissibility-wiki-ai-entity.md
docs/governance/equivalence-proposal-template.md
docs/research/terminology-overlap-research-notes.md
```

## Accepted Relationship Updates

```text
proposal.example.005 / decision.example.005: Provenance -> Reconstructability, Overlapping Terms only
proposal.example.006 / decision.example.006: policy-as-code -> Policy Reference, Overlapping Terms only
proposal.example.007 / decision.example.007: AI risk-management governance language -> Governance Boundary, Overlapping Terms only
proposal.example.008 / decision.example.008: policy decision -> Commit-Time Authority, Overlapping Terms only
proposal.example.009 / decision.example.009: Audit and Accountability -> Reconstructability, Overlapping Terms only
```

No accepted equivalence has been recorded yet.

## Editorial Rule

Do not add an external term to `Equivalent Terms` without a completed proposal, source evidence, mismatch analysis, overclaiming-risk analysis, and decision record.

## Submission Receipt Timing Rule

User-submitted proposals should include a `submission_timing` block in the submission receipt.

Submission timing records intake posture only. It does not accept the proposal, prove the submitted claim, or replace the decision record.

## Self-Managed Continuation

```text
Validation trigger: push to main
Validation command: npm run validate
Deployment trigger: successful validation and build
Public verification: deploy workflow verify-public-pages job
Manual task requirement: none recorded in this handoff
Failure posture: first failing validator or public URL check becomes the next bounded repair target
```

## Next Safe Build Targets

1. Let repo automation validate, build, deploy, and verify public URLs on push.
2. If automation fails, repair only the first failing validator field, missing artifact, or public URL check.
3. Update activation posture only from workflow evidence or source-confirmed deployment state.
