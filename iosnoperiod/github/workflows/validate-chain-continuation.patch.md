# validate-chain-continuation iOS Mirror Sync Patch

## Status

The canonical workflow at `.github/workflows/validate-chain-continuation.yml` is ahead of the iOS-safe mirror at `iosnoperiod/github/workflows/validate-chain-continuation.yml`.

A full mirror replacement was not applied in this session. This patch note records the required delta so the mirror can be safely refreshed without treating the stale mirror as activation evidence.

## Required additions to the validation job

Add these steps after external framework expansion policy validation and before CI evidence validation:

```yaml
      - name: Validate ASRO commitment candidate
        run: python scripts/check_asro_commitment_candidate.py

      - name: Validate governed LLM public pages
        run: python scripts/check_governed_llm_pages.py

      - name: Validate governed LLM demo docs
        run: python scripts/check_governed_llm_demo_docs.py

      - name: Validate iOS workflow mirror status
        run: python scripts/check_ios_workflow_mirror_status.py

      - name: Validate admissibility automation handoff
        run: python scripts/check_admissibility_automation_handoff.py
```

## Required additions to the build job

Ensure the build job includes both repo preflight steps before `npm run validate`:

```yaml
      - name: Repo preflight
        run: node scripts/repo_preflight.mjs

      - name: Validate repo preflight status
        run: node scripts/check-repo-preflight-status.mjs
```

## Required additions to the public verification job

The public verification job must include checkout, Node setup, every governed LLM route, ASRO route verification, and the deployment status checker:

```yaml
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Verify governed LLM reconstructive search
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-reconstructive-search"

      - name: Verify governed LLM activation map
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-activation-map"

      - name: Verify governed LLM demo overview
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview"

      - name: Verify governed LLM demo verification
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification"

      - name: Verify governed LLM site verification
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-site-verification"

      - name: Verify governed LLM deployment status
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-deployment-status"

      - name: Verify governed LLM archive handoff
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-archive-handoff"

      - name: Verify governed LLM route set
        run: python scripts/check_governed_llm_deployment_status.py

      - name: Verify ASRO external framework page
        run: curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors "https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/asro"
```

## Required activation receipt steps

The mirror must retain the public activation receipt writer and artifact upload steps:

```yaml
      - name: Write public activation receipt
        run: PAGE_URL="${{ needs.deploy-pages.outputs.page_url }}" node scripts/write-public-activation-receipt.mjs

      - name: Upload public activation receipt
        uses: actions/upload-artifact@v4
        with:
          name: public-activation-receipt
          path: reports/public-activation-receipt.json
```

## Boundary

The iOS mirror is not activation evidence. Until the mirror file itself matches the canonical workflow, this patch note is only a controlled remediation record.
