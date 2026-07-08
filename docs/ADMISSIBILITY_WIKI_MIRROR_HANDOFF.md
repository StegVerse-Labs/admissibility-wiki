# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current Repo Goal

```text
Goal: complete governed LLM / admissibility-wiki public documentation activation under the single canonical validation workflow.
Current repo state: all-framework evidence-provenance rollout matrix installed; external framework report validation repair in progress.
Manual task requirement: none recorded in this handoff
No manual target-creation task is assigned in this handoff
```

## Current Activation Goal

```text
Publish and validate https://stegverse-labs.github.io/admissibility-wiki/ as the public vocabulary, terminology convergence, proposal-review, proof-path, governed LLM demo, repo-standards integration, and external-framework evaluation-standard site.
```

## Current Blocker

```text
Workflow: .github/workflows/validate-chain-continuation.yml
Job: validate-chain-continuation
Step: Validate external framework reports
Validator: scripts/check_external_framework_reports.py
Failure class: external framework report status vocabulary mismatch
Repair target: allow source-blocked status tokens only when result == SOURCE_BLOCKED_FAIL_CLOSED
```

Source-blocked reports may use the following status tokens as fail-closed evidence-status markers:

```text
SOURCE_REQUIRED
PROVISIONAL
MISSING
```

These tokens do not certify compatibility, grant authority, or complete validation. They only record that source evidence is unavailable or insufficient and must remain bounded by `SOURCE_BLOCKED_FAIL_CLOSED`.

## Proposal Governance Core-Lite Status

```text
Target repository: StegVerse-Labs/proposal-governance-core-lite
Status artifact: static/status/proposal-core-lite-target-watch-status.json
Validation command: npm run validate:proposal-core-lite-target-watch-status
Execution surface: .github/workflows/validate-chain-continuation.yml
Posture: declared task under the canonical workflow, not a second active workflow.
Last observed validator result: proposal core-lite target watch status OK
Manual task requirement: none recorded in this handoff
No manual target-creation task is assigned in this handoff
```

## Deployment Gate

```text
Canonical active workflow: .github/workflows/validate-chain-continuation.yml
Build job: build-pages
Deployment job: deploy-pages
Public verification job: verify-public-pages
Gate posture: validation must pass before build/deploy/verify can advance.
```

## Known Workflow Files

```text
Active canonical workflow:
.github/workflows/validate-chain-continuation.yml

iOS-safe workflow path references retained for continuity and migration history:
github/workflows/deploy.yml
github/workflows/record-latest-success.yml
github/workflows/proposal-core-lite-target-watch.yml

The proposal-core-lite target watch is represented as a declared task/status artifact under the canonical workflow, not as an additional active workflow file.
```

## Known Status Artifacts

```text
static/status/admissibility-wiki-status.json
static/status/admissibility-wiki-activation.json
static/status/proposal-core-lite-target-watch-status.json
static/status/no-manual-task-guard-status.json
static/status/mirror-handoff-guard-status.json
static/status/workflow-receipt-automation-status.json
static/status/workflow-evidence-status.json
static/status/workflow-evidence-watch-status.json
static/status/publication-verification-status.json
static/status/guardian-destination-resolution-status.json
static/status/repo-standards-integration-status.json
static/status/repo-standards-integration-release-update-queue.json
static/status/repo-standards-installation-bundle-plan.json
static/status/repo-standards-installation-validation-report.json
static/status/repo-standards-public-deployment-verification.json
```

## Validation and Receipt Automation

```text
npm run validate:wiki-status
npm run validate:activation-checklist
npm run validate:publication-verification-status
npm run validate:workflow-receipt-automation-status
npm run validate:workflow-evidence-status
npm run validate:workflow-evidence-watch-status
npm run validate:proposal-core-lite-target-watch-status
npm run validate:no-manual-task-assignments
npm run validate:mirror-handoff-guard
npm run validate:guardian-destination-resolution
npm run validate:guardian-handoff-destinations
npm run validate:repo-standards-integration
python scripts/check_external_framework_expansion_policy.py
python scripts/check_external_framework_evidence_provenance.py
python scripts/check_external_framework_reports.py
npm run validate
```

## Mirror Coordination Rule

```text
Check this file before continuing work in StegVerse-Labs/admissibility-wiki.
Check docs/SITE_MIRROR_HANDOFF.md before Site mirror work.
Do not create additional active GitHub Actions workflows unless repo standards explicitly change.
Do not treat public page visibility as governance authority.
Manual task requirement: none recorded in this handoff
```

## Guardian Destination Status

```text
Status artifact: static/status/guardian-destination-resolution-status.json
Public destination repo: StegVerse-002/stegguardian-wiki
Implementation destination repo: StegVerse-002/StegGuardian
Public destination summary: downstream public Guardian summary after wiki validation and repo-standards tag/release
Implementation destination summary: private Guardian implementation standing-boundary awareness after wiki validation
```

## Repo Standards Integration Status

```text
Goal id: repo-standards-integration-and-installation-bundle-pending-release
```

## Handoff Instruction

Continue from this file before relying on prior chat context. The complete thread can be archived without needing additional context to continue.
