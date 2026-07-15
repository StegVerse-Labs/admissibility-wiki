---
title: GitHub Pages Activation
---

# GitHub Pages Activation

This runbook describes automated activation of the Admissibility Wiki at the GitHub.io project URL.

```text
https://stegverse-labs.github.io/admissibility-wiki/
```

## Authority and ownership boundary

```text
Canonical active workflow: .github/workflows/validate-chain-continuation.yml
Validation job: validate-chain-continuation
Build job: build-pages
Deployment job: deploy-pages
Public verification job: verify-public-pages
Manual task requirement: none
User manual action required: false
```

The workflow owns validation, build, deployment, public-route observation, and publication-receipt generation. Documentation does not grant release authority, execution authority, or permission to bypass the validation gate.

## Done state

Activation is complete only when observed workflow evidence establishes that:

- the canonical validation job passed;
- the Pages build completed from the validated commit;
- the Pages deployment completed successfully;
- the public root loads at `https://stegverse-labs.github.io/admissibility-wiki/`;
- the Docusaurus landing page loads without a 404;
- internal wiki routes load under `/admissibility-wiki/`;
- the ontology JSON is reachable under the GitHub.io project URL;
- proposal, decision, replay, evidence, and status examples are reachable;
- the public activation receipt records the bounded result.

A configured workflow, successful local build, or reachable root alone is not sufficient to establish the complete done state.

## Current domain policy

Custom domains are not configured for this wiki.

```text
custom_domain: not_configured
static/CNAME: absent
cloudflare_dependency: none
```

Do not add a CNAME file or Cloudflare DNS requirement unless a later governed activation decision changes the public target.

## GitHub Pages configuration

The repository is configured for GitHub Pages project hosting through the canonical Actions workflow.

```text
Pages source: GitHub Actions
Custom domain: blank
HTTPS: github.io managed
```

Repository settings are an external GitHub control surface. A prose assertion that the setting is correct is not deployment evidence; the workflow and public verification receipts remain the observable evidence path.

## Docusaurus settings

The checked-in Docusaurus configuration uses:

```text
url: https://stegverse-labs.github.io
baseUrl: /admissibility-wiki/
organizationName: StegVerse-Labs
projectName: admissibility-wiki
onBrokenLinks: throw
```

Canonical configuration source:

```text
docusaurus.config.js
```

## Repository files supporting activation

Required source surfaces include:

```text
docusaurus.config.js
.github/workflows/validate-chain-continuation.yml
sidebars.js
static/img/favicon.svg
scripts/check_governed_llm_deployment_status.py
scripts/write-public-activation-receipt.mjs
```

The repository must not contain:

```text
static/CNAME
```

Paths beginning with a leading dot are shown normally here because this page is a repository runbook, not an iOS bootstrap mirror.

## Expected published paths

After a successful canonical deployment and public verification, these paths are expected to be reachable:

```text
https://stegverse-labs.github.io/admissibility-wiki/
https://stegverse-labs.github.io/admissibility-wiki/glossary/admissibility
https://stegverse-labs.github.io/admissibility-wiki/governance/proposal-lifecycle
https://stegverse-labs.github.io/admissibility-wiki/proof-path/minimal-public-proof-path
https://stegverse-labs.github.io/admissibility-wiki/ontology/admissibility-vocabulary.v0.1.json
https://stegverse-labs.github.io/admissibility-wiki/status/admissibility-wiki-status.json
```

Route reachability proves only that a bounded public surface responded. It does not establish source authority, proof authority, current admissibility, custody, or execution authority.

## Failure handling

If validation fails, the workflow must fail closed before build and deployment. The first deterministic failure should be repaired from the uploaded `full-validation-chain-report` artifact.

If build fails, inspect the workflow-owned Docusaurus build output for broken links, missing pages, invalid sidebar entries, or invalid generated artifacts.

If deployment or public verification fails, preserve the failed observation in the workflow and public activation receipt. Do not replace the automated evidence path with a manual user task.

```text
validation failure -> build skipped
build failure -> deployment skipped
deployment failure -> public verification blocked or fail-closed
public-route failure -> no completed activation claim
```

## Current activation posture

```text
repository_config: github_io_project_url
canonical_workflow: .github/workflows/validate-chain-continuation.yml
custom_domain: not_configured
cname_file: absent
manual_task_required: false
activation_claim: requires observed workflow, deployment, route, and receipt evidence
```

## Non-claims

```text
workflow configuration != workflow pass
workflow pass != public deployment
public deployment != route verification
route verification != source authority
publication receipt != execution authority
queued propagation != completed propagation
```
