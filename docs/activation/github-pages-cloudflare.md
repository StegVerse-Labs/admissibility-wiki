---
title: GitHub Pages Activation
---

# GitHub Pages Activation

This runbook activates the Admissibility Wiki at the GitHub.io project URL.

```text
https://stegverse-labs.github.io/admissibility-wiki/
```

## Done State

Activation is complete when:

- GitHub Pages is set to deploy from GitHub Actions;
- the deploy workflow completes successfully;
- the public page loads at `https://stegverse-labs.github.io/admissibility-wiki/`;
- the Docusaurus landing page loads without a 404;
- internal wiki routes load under `/admissibility-wiki/`;
- the ontology JSON is reachable under the GitHub.io project URL;
- proposal, decision, replay, and evidence examples are reachable under the GitHub.io project URL.

## Current Domain Policy

Custom domains are not configured for this wiki.

```text
custom_domain: not_configured
static/CNAME: removed
```

Do not add a CNAME file or Cloudflare DNS requirement unless the activation goal explicitly changes back to a custom domain.

## GitHub Pages Settings

In the repository:

```text
Settings → Pages
Source: GitHub Actions
Custom domain: blank
Enforce HTTPS: enabled by default for github.io
```

## Docusaurus Settings

The Docusaurus config should use GitHub Pages project hosting values:

```text
url: https://stegverse-labs.github.io
baseUrl: /admissibility-wiki/
organizationName: StegVerse-Labs
projectName: admissibility-wiki
```

## Repo Files Supporting Activation

The repo should include:

```text
docusaurus.config.js
.github/workflows/deploy.yml
static/img/favicon.svg
```

The repo should not include:

```text
static/CNAME
```

Note: paths that normally begin with a leading dot are shown without the leading dot in this display rule only.

## Expected Published Paths

After deployment, these paths should be reachable:

```text
https://stegverse-labs.github.io/admissibility-wiki/
https://stegverse-labs.github.io/admissibility-wiki/glossary/admissibility
https://stegverse-labs.github.io/admissibility-wiki/governance/proposal-lifecycle
https://stegverse-labs.github.io/admissibility-wiki/proof-path/minimal-public-proof-path
https://stegverse-labs.github.io/admissibility-wiki/ontology/admissibility-vocabulary.v0.1.json
https://stegverse-labs.github.io/admissibility-wiki/status/admissibility-wiki-status.json
```

## Troubleshooting GitHub.io 404

If `https://stegverse-labs.github.io/admissibility-wiki/` returns 404:

1. Confirm the repository is public or GitHub Pages is available for the repository visibility level.
2. Confirm `Settings → Pages → Source` is set to `GitHub Actions`.
3. Confirm the deploy workflow has completed successfully after the latest commit.
4. Confirm the workflow deploy step used `actions/deploy-pages`.
5. Confirm `docusaurus.config.js` has `baseUrl: '/admissibility-wiki/'`.
6. Confirm `static/CNAME` does not exist.
7. Confirm the Pages deployment URL in the Actions output matches the GitHub.io project URL.
8. If the workflow has not run since the config change, run the deploy workflow manually.

## Troubleshooting Build Failures

If the workflow fails:

1. Open the failed Actions run.
2. Check the `Install dependencies` step.
3. Check the `Build site` step.
4. Confirm `npm run build` is available in `package.json`.
5. Confirm Docusaurus did not report broken links.
6. Confirm sidebar entries point to real docs.
7. Confirm static JSON and TXT files are valid or intentionally plain static assets.

## Current Activation Posture

```text
repository_config: github_io_project_url
custom_domain: not_configured
cname_file: removed
remaining_dependency: GitHub Pages settings and successful Actions deployment
```
