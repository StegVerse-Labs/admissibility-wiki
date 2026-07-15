# Governed LLM Site Verification

## Purpose

This page defines repository-local and deployed verification for the governed LLM documentation topology. It does not treat page presence as proof that Site entry surfaces, providers, custody, or execution are operational.

## Repository-local documentation set

The local checker should cover at least:

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/governance/governed-llm-site-verification.md
docs/governance/governed-llm-deployment-status.md
docs/governance/llm-free-tier-trust-chain.md
docs/governance/portable-governed-return-path.md
docs/governance/governed-ecosystem-index.md
docs/governance/governed-input-classes.md
docs/governance/governed-output-classes.md
docs/governance/governed-transition-map.md
docs/governance/capability-lifecycle.md
docs/governance/ecosystem-capability-status.md
sidebars.js
docusaurus.config.js
README.md
```

## Local verification

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run validate
```

A local pass establishes that required files, references, and build constraints are satisfied. It does not prove that the same commit was deployed.

## Public deployment verification

Public route verification is owned by the canonical workflow:

```text
.github/workflows/validate-chain-continuation.yml
  -> validate-chain-continuation
  -> build-pages
  -> deploy-pages
  -> verify-public-pages
  -> public-activation-receipt
```

The public checker is:

```bash
python scripts/check_governed_llm_deployment_status.py
```

The public result may be claimed only from observed route evidence for the deployed commit and its workflow-owned receipt.

## Site integration coordinates

Documentation verification must remain distinct from the downstream Site implementation:

| Coordinate | Owner | Current posture |
|---|---|---|
| `ecosystem-chat.html` | `StegVerse-Labs/Site` | `PREPARED_NOT_DEPLOYED` |
| `ecosystem-usage.html` | `StegVerse-Labs/Site` | `PREPARED_NOT_DEPLOYED` |
| `ecosystem-comparison.html` | `StegVerse-Labs/Site` | `PREPARED_NOT_DEPLOYED` |
| `governed-transitions.html` | `StegVerse-Labs/Site` | Public projection; not execution authority |
| Same-origin usage API | Site plus authorized destination | `NOT_DEPLOYED` |
| LLM adapter gateway | `StegVerse-org/LLM-adapter` | Source installed; deployment evidence pending |
| Master-Records custody | `master-records/orchestration` | External authenticated evidence required |

The current Site boundary remains:

```text
contract_status: PREPARED_NOT_DEPLOYED
live_transport_enabled: false
usage_api_base: null
activation: blocked pending evidence
```

## Evidence required for Site activation

```text
destination current-main validation
authorized same-origin deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records authenticated custody
reconstructability PASS
```

## Navigation exposure

The governed LLM documentation should remain reachable from the Governance sidebar, repository index, and related-page links. Navbar and footer exposure may improve discoverability but do not create completeness or deployment proof by themselves.

## Boundary

```text
local documentation pass != deployed commit confirmation
wiki deployment != Site application deployment
Site display != execution
prepared client != deployed endpoint
response conformance != authority
retrieval receipt != Master-Records custody
workflow receipt != operational standing
public reachability != external indexing
```
