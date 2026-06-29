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

Continue the active `declarative-external-framework-generation-pipeline` goal until framework pages can be generated, validated, and published from governed artifacts without page-status editing or separate result-posting work.

## Current Activation Goal

Publish and validate the Admissibility Wiki as the public vocabulary, terminology convergence, proposal-review, proposal-intake, proof-path, and external-framework crosswalk site.

Activation must remain evidence-bound. Public deployment, generated framework result pages, generated framework page-status blocks, and URL verification must be produced by repository automation before activation posture advances.

## Installed Activation Structure

Displayed without leading-dot paths for iOS readability. Actual repository paths beginning with `github/` use a leading `.github/` directory.

```text
docs/activation/github-pages-cloudflare.md
static/status/admissibility-wiki-activation.json
static/status/admissibility-wiki-status.json
static/status/public-activation-receipt.example.json
static/status/workflow-receipt-automation-status.json
static/status/workflow-evidence-status.json
static/status/proposal-core-lite-target-watch-status.json
static/status/no-manual-task-guard-status.json
static/status/mirror-handoff-guard-status.json
github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
workflow_manifest.json
docs/CHAIN_AUTO.json
docs/CI_EVIDENCE.json
docs/GOAL_STATE.json
```

## Single Workflow Policy

Only one active GitHub Actions workflow is intended to exist:

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

## Declarative External Framework Pipeline

The current build path is:

```text
framework manifest
  -> generated compatibility report
  -> generated evaluation results page
  -> generated framework page-status block
  -> Docusaurus build
  -> GitHub Pages deploy
  -> public URL verification
```

Installed generators and validators:

```text
scripts/generate_external_framework_reports.py
scripts/generate_external_framework_results.py
scripts/generate_external_framework_page_status.py
scripts/check_external_framework_reports.py
scripts/check_external_framework_report_coverage.py
scripts/check_external_framework_report_generation.py
scripts/check_external_framework_results_page.py
scripts/check_external_framework_page_status.py
scripts/check_external_framework_terminology.py
scripts/check_external_framework_expansion_policy.py
```

Generated publication surface:

```text
docs/external-frameworks/evaluation-results.md
```

Generated page-status blocks are inserted into registered framework pages from manifests plus compatibility reports. The generated blocks are compatibility evidence only and do not grant certification, endorsement, formalism adoption, admissibility proof, or execution authority.

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
scripts/check-external-framework-registry.mjs
scripts/check-publication-chain-guard.mjs
scripts/check-publication-verification-status.mjs
scripts/check-workflow-receipt-automation-status.mjs
scripts/check-workflow-evidence-status.mjs
scripts/check-workflow-evidence-watch-status.mjs
scripts/check-proposal-core-lite-target-watch-status.mjs
scripts/check-no-manual-task-assignments.mjs
scripts/check-mirror-handoff-guard.mjs
scripts/check-transition-origin-sections.mjs
scripts/check-proposal-governance-classes.mjs
scripts/check-proposal-governance-core-lite-seed.mjs
scripts/check-proposal-governance-core-lite-creation-task.mjs
scripts/check-proposal-intake-interface.mjs
scripts/check-proposal-intake-backend-contract.mjs
scripts/check-proposal-intake-backend-runtime.mjs
scripts/check-proposal-intake-api-server.mjs
scripts/check-proposal-intake-api-deployment.mjs
scripts/check-proposal-intake-api-deployment-receipt.mjs
scripts/check-proposal-intake-endpoint-verification-status.mjs
scripts/check-intake-api-deploy-config.mjs
scripts/check-public-share-readiness.mjs
scripts/check-entity-sandbox-runner-admissibility-plane-status.mjs
scripts/check_workflow_sprawl.py
scripts/check_chain_status_continuation.py
scripts/check_continuation_bundle.py
scripts/check_chain_snapshot.py
scripts/check_chain_snapshot_receipt.py
scripts/check_chain_auto.py
scripts/check_blocked_destination_record.py
scripts/check_goal_state.py
scripts/check_workflow_manifest.py
scripts/check_ci_evidence.py
```

Aggregate validation is run by repo automation through the single canonical workflow. Local aggregate validation remains:

```text
npm run validate
```

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
docs/external-frameworks/index.md
docs/external-frameworks/evaluation-results.md
```

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

## Current Continuation Rule

1. Check `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` first.
2. Check this file second.
3. Verify exact repo paths before creating or replacing files.
4. Repair the first failing validator, generated artifact drift, build issue, deploy issue, public URL verification issue, or handoff inconsistency identified by the active workflow.
5. Do not reintroduce separate active workflows for validation, deployment, evidence watch, success recording, proposal watching, or framework result posting.

## Current Redundancy Posture

This repository may be touched by more than one session. Do not assume a previously proposed next step is still missing. Verify file presence first, then continue from the missing or explicitly open item.
