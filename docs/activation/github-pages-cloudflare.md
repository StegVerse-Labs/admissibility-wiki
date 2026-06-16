---
title: GitHub Pages and Cloudflare Activation
---

# GitHub Pages and Cloudflare Activation

This runbook activates `admissibility.stegverse.org` for the Admissibility Wiki.

## Done State

Activation is complete when:

- GitHub Pages is set to deploy from GitHub Actions;
- the deploy workflow completes successfully;
- `admissibility.stegverse.org` resolves in DNS;
- GitHub validates the custom domain;
- HTTPS is provisioned and enforced;
- the Docusaurus landing page loads at the custom domain.

## GitHub Pages Settings

In the repository:

```text
Settings → Pages
Source: GitHub Actions
Custom domain: admissibility.stegverse.org
Enforce HTTPS: enabled after validation succeeds
```

## Cloudflare DNS

Create this DNS record for `stegverse.org`:

```text
Type: CNAME
Name: admissibility
Target: stegverse-labs.github.io
Proxy status: DNS only at first
TTL: Auto
```

## Why DNS Only First

DNS-only mode reduces moving parts during first validation.

After GitHub validates the custom domain and HTTPS is stable, Cloudflare proxying can be tested separately if needed.

## Repo Files Supporting Activation

The repo includes:

```text
static/CNAME
static/img/favicon.svg
.github/workflows/deploy.yml
```

The Docusaurus build copies `static/CNAME` to the build output so GitHub Pages can retain the custom-domain marker.

## Troubleshooting

If the domain does not resolve:

1. Confirm the Cloudflare CNAME exists.
2. Confirm the CNAME target is `stegverse-labs.github.io`.
3. Confirm proxy status is DNS only.
4. Confirm GitHub Pages source is GitHub Actions.
5. Run the deployment workflow manually.
6. Wait for GitHub custom-domain validation.
7. Enable HTTPS only after validation succeeds.

If the workflow fails:

1. Open the failed Actions run.
2. Check the `Install dependencies` step.
3. Check the `Build site` step.
4. Confirm `npm run build` is available in `package.json`.
5. Confirm Docusaurus did not report broken links.

## Current Activation Posture

The repository-side files are present.

The remaining activation dependency is external configuration in GitHub Pages settings and Cloudflare DNS.
