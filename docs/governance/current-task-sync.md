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

Continue the active `governed-ecosystem-transition-framing` goal until the wiki presents external frameworks as one governed input class within the broader transition ecosystem.

## Current Activation Goal

Publish and validate the Admissibility Wiki as the public vocabulary, terminology convergence, proposal-review, proposal-intake, proof-path, external-framework input-class, and governed ecosystem transition framing site.

Activation must remain evidence-bound. Public deployment, generated framework result pages, governed ecosystem transition pages, generated framework page-status blocks, and URL verification must be produced by repository automation before activation posture advances.

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
static/status/governed-ecosystem-transitions-status.json
static/status/external-framework-input-class-status.json
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

## Governed Ecosystem Transition Framing

The current governed ecosystem transition path is:

```text
input or request
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

Installed pages and status:

```text
docs/governance/governed-ecosystem-transitions.md
docs/governance/external-frameworks-as-input-class.md
static/status/governed-ecosystem-transitions-status.json
static/status/external-framework-input-class-status.json
scripts/check_governed_ecosystem_transitions_status.py
scripts/check_external_framework_input_class_status.py
```

## Declarative External Framework Pipeline

External frameworks remain supported as one governed input-class surface:

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

Generated page-status blocks are compatibility evidence only and do not grant certification, endorsement, formalism adoption, admissibility proof, execution authority, or canonical STRP admission.

## Aggregate Validation

```text
npm run validate
```

The aggregate validation now includes:

```text
npm run validate:governed-ecosystem-transitions
npm run validate:external-framework-input-class
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
docs/governance/governed-ecosystem-transitions.md
docs/governance/external-frameworks-as-input-class.md
docs/research/terminology-overlap-research-notes.md
docs/external-frameworks/index.md
docs/external-frameworks/evaluation-results.md
```

## Known Remaining Installation Targets

```text
StegVerse-Labs/admissibility-wiki:
  - public deployment verification for governed ecosystem transition and external-framework input-class pages
  - optional generated status surface grouping all input classes

StegVerse-Labs/Site:
  - mirror/public summary of governed ecosystem transition framing after admissibility-wiki validation

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness for governed ecosystem transition framing after admissibility-wiki validation

stegguardian-wiki:
  - downstream summary of governed input/output transition boundary once admissibility-wiki validation is stable
```

## Current Continuation Rule

1. Check `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` first.
2. Check this file second.
3. Verify exact repo paths before creating or replacing files.
4. Repair the first failing validator, generated artifact drift, build issue, deploy issue, public URL verification issue, or handoff inconsistency identified by the active workflow.
5. Do not reintroduce separate active workflows for validation, deployment, evidence watch, success recording, proposal watching, or framework result posting.

## Current Redundancy Posture

This repository may be touched by more than one session. Do not assume a previously proposed next step is still missing. Verify file presence first, then continue from the missing or explicitly open item.
