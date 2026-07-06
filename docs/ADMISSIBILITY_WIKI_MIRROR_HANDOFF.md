# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current Repo Goal

```text
Goal: complete governed LLM / admissibility-wiki public documentation activation under the single canonical validation workflow.
Current repo state: all-framework evidence-provenance rollout matrix installed; Batch 1, Batch 2, and Batch 3 page provenance refactors installed and validator-enforced.
Manual task requirement: none recorded in this handoff
No manual target-creation task is assigned in this handoff
```

## Current Activation Goal

```text
Publish and validate https://stegverse-labs.github.io/admissibility-wiki/ as the public vocabulary, terminology convergence, proposal-review, proof-path, governed LLM demo, repo-standards integration, and external-framework evaluation-standard site.
```

## Deployment Gate

```text
Canonical active workflow: .github/workflows/validate-chain-continuation.yml
Build job: build-pages
Deployment job: deploy-pages
Public verification job: verify-public-pages
Gate posture: validation must pass before build/deploy/verify can advance.
```

## Current goal

```text
all-external-framework-evidence-provenance-rollout
```

## Current version

```text
1.5.9-batch3-external-framework-provenance-refactor
```

## Current status

```text
REPO_STANDARDS_INTEGRATION_PAGE_WIRED
GOVERNED_LLM_DEMO_DOCS_WIRED
PROPOSAL_CORE_LITE_TARGET_WATCH_DECLARED_TASK_WIRED
SINGLE_WORKFLOW_POLICY_RESTORED
SIDEBAR_NAVIGATION_PRESENT
MORRISON_RUNTIME_SOURCED_AND_BOUNDARY_CASE_PARTIAL
EXTERNAL_FRAMEWORK_EVALUATION_STANDARD_INSTALLED
EXTERNAL_FRAMEWORK_FAILURE_CLASS_CATALOG_INSTALLED
EXTERNAL_FRAMEWORK_TEMPLATE_INSTALLED
EXTERNAL_FRAMEWORK_INDEX_UPDATED
EXTERNAL_FRAMEWORK_EXPANSION_POLICY_UPDATED
EXTERNAL_FRAMEWORK_EVIDENCE_PROVENANCE_VALIDATOR_INSTALLED
EXTERNAL_FRAMEWORK_EVIDENCE_PROVENANCE_VALIDATOR_WIRED_IN_PACKAGE
EXTERNAL_FRAMEWORK_EVIDENCE_PROVENANCE_VALIDATOR_WIRED_IN_CANONICAL_WORKFLOW
ALL_FRAMEWORK_EVIDENCE_PROVENANCE_ROLLOUT_MATRIX_INSTALLED
ALL_FRAMEWORK_EVIDENCE_PROVENANCE_ROLLOUT_PAGE_INSTALLED
ALL_FRAMEWORK_EVIDENCE_PROVENANCE_ROLLOUT_VALIDATOR_COVERAGE_INSTALLED
BATCH1_GLM_EVIDE_MORRISON_PROVENANCE_SECTIONS_INSTALLED
BATCH1_PROVENANCE_VALIDATOR_ENFORCED
BATCH2_DECISIONASSURE_MINDFORGE_ASRO_PROVENANCE_SECTIONS_INSTALLED
BATCH2_PROVENANCE_VALIDATOR_ENFORCED
BATCH3_MITRE_OWASP_NIST_ISO_EUAI_PROVENANCE_SECTIONS_INSTALLED
BATCH3_PROVENANCE_VALIDATOR_ENFORCED
UPSTREAM_REPO_STANDARDS_RELEASE_READY
UPSTREAM_TAG_RELEASE_PENDING_OUTSIDE_CONNECTOR
LOCAL_DOCS_ONLY
```

## Batch 1 complete

```text
GLM:
  - docs/external-frameworks/glm.md includes Evidence Provenance
  - claims classified as F1/S1/S2/H1
  - next target: GLM-to-Commitment-Candidate fixture

EVIDE:
  - docs/external-frameworks/evide.md includes Evidence Provenance
  - claims classified as F1/S1/S2/H1
  - next target: deposited-record reconstruction fixture

Morrison Runtime:
  - docs/external-frameworks/morrison-runtime.md includes parameterized boundary case posture
  - semantic-equivalence boundary remains bounded partial observation
  - next target: raw audit payload, timestamp, runtime configuration, source hash
```

## Batch 2 complete

```text
DecisionAssure:
  - docs/external-frameworks/decisionassure.md includes Evidence Provenance
  - remains artifact-package-required fail-closed
  - next target: authorized artifact package and Commitment Candidate fixture

MindForge:
  - docs/external-frameworks/mindforge.md includes Evidence Provenance
  - remains artifact-package-required fail-closed
  - next target: authorized evidence package and authority re-binding fixture

ASRO:
  - docs/external-frameworks/asro.md includes Evidence Provenance
  - public source and repository references classified as F1/F2
  - next target: validate ASRO commitment-candidate fixture and attach report
```

## Batch 3 complete

```text
MITRE ATLAS:
  - docs/external-frameworks/mitre-atlas.md includes Evidence Provenance
  - treated as threat-knowledge evidence, not runtime result or authority
  - next target: threat-context Commitment Candidate fixture

OWASP Top 10 for LLM Applications:
  - docs/external-frameworks/owasp-top-10-llm.md includes Evidence Provenance
  - treated as LLM-risk guidance evidence, not runtime result or authority
  - next target: LLM-risk Commitment Candidate fixture

NIST AI RMF:
  - docs/external-frameworks/nist-ai-rmf.md includes Evidence Provenance
  - treated as voluntary risk-management context, not runtime result or authority
  - next target: risk-management mapping fixture

ISO/IEC 42001:
  - docs/external-frameworks/iso-iec-42001.md includes Evidence Provenance
  - treated as AI management-system context, not runtime result or authority
  - next target: organizational-control mapping fixture

EU AI Act:
  - docs/external-frameworks/eu-ai-act.md includes Evidence Provenance
  - treated as legal/regulatory context, not runtime result or authority
  - next target: legal-obligation mapping fixture
```

## External Framework Evaluation Standard pages

```text
docs/external-frameworks/evaluation-standard.md
docs/external-frameworks/failure-class-catalog.md
docs/external-frameworks/external-framework-template.md
docs/external-frameworks/evidence-provenance-rollout.md
docs/external-frameworks/evidence-provenance-rollout.json
docs/external-frameworks/morrison-runtime.md
docs/external-frameworks/reports/morrison-runtime.compatibility.json
docs/external-frameworks/EXPANSION_POLICY.json
```

## All-framework rollout coverage

```text
GLM
EVIDE
DecisionAssure
MindForge
Morrison Runtime
CARE Runtime
AAR
ASRO
MITRE ATLAS
OWASP Top 10 for LLM Applications
Agent Governance Playbook
Emergency Stop Convention
NIST AI RMF
ISO/IEC 42001
EU AI Act
Policy Cards
Runtime Governance for AI Agents
Admissible Existence Seed Cycle
```

## Validator additions

```text
scripts/check_external_framework_evidence_provenance.py
  -> validates standard files
  -> validates rollout page and JSON matrix
  -> confirms every registry framework appears in rollout exactly once
  -> validates Batch 1, Batch 2, and Batch 3 page Evidence Provenance sections
  -> confirms no unsupported Morrison historical result table is restored

package.json -> validate:external-framework-evidence-provenance
package.json -> npm run validate includes expansion-policy and evidence-provenance validators
.github/workflows/validate-chain-continuation.yml -> validates external framework evidence provenance in canonical validation job
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
python scripts/check_external_framework_expansion_policy.py
python scripts/check_external_framework_evidence_provenance.py
npm run validate
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/SITE_MIRROR_HANDOFF.md
docs/MIRROR_HANDOFF_GUARD_ADDENDUM.md
docs/external-frameworks/glm.md
docs/external-frameworks/evide.md
docs/external-frameworks/decisionassure.md
docs/external-frameworks/mindforge.md
docs/external-frameworks/asro.md
docs/external-frameworks/mitre-atlas.md
docs/external-frameworks/owasp-top-10-llm.md
docs/external-frameworks/nist-ai-rmf.md
docs/external-frameworks/iso-iec-42001.md
docs/external-frameworks/eu-ai-act.md
docs/external-frameworks/morrison-runtime.md
docs/external-frameworks/evaluation-standard.md
docs/external-frameworks/failure-class-catalog.md
docs/external-frameworks/external-framework-template.md
docs/external-frameworks/evidence-provenance-rollout.md
docs/external-frameworks/evidence-provenance-rollout.json
docs/external-frameworks/reports/morrison-runtime.compatibility.json
docs/external-frameworks/EXPANSION_POLICY.json
docs/external-frameworks/index.md
scripts/check_external_framework_evidence_provenance.py
.github/workflows/validate-chain-continuation.yml
sidebars.js
package.json
```

## Remaining targets

```text
StegVerse-Labs/admissibility-wiki:
  - complete canonical validate-chain-continuation workflow
  - confirm build-pages, deploy-pages, and verify-public-pages
  - public deployment verification after site deploys
  - Batch 4 refactor: Policy Cards, Runtime Governance for AI Agents, Agent Governance Playbook, Emergency Stop Convention, CARE Runtime, AAR
  - extend validator from Batch 3 to Batch 4 after refactor

StegVerse-Labs/repo-standards:
  - propagate external-framework evidence provenance standard and failure-class catalog as org-level standard

StegVerse-Labs/Site:
  - mirror public summary after wiki validation and repo-standards tag/release

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after wiki validation and repo-standards tag/release

StegVerse-002/stegguardian-wiki:
  - downstream public Guardian summary after wiki validation and repo-standards tag/release

StegVerse-002/StegGuardian:
  - private Guardian implementation standing-boundary awareness after wiki validation
```

## Boundary rules

This wiki records vocabulary, proof framing, lifecycle classification, public explanation paths, release-gated integration references, release-gated bundle installation doctrine, governed LLM demo documentation, external-framework evidence-provenance standards, all-framework rollout state, and public deployment verification requirements.

It does not claim production authority or release status.

It must not treat an untagged upstream release as final authority.

It must not treat bundle installation as admissibility or runtime authority.

It must not treat public page visibility as governance authority.

External framework compatibility is not certification.

Observed behavior must not be generalized beyond captured evidence.

## Handoff instruction

Continue from this file before relying on prior chat context.
