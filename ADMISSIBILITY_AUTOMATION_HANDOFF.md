# Admissibility Automation Handoff

## Scope

This file extends `ADMISSIBILITY_MIRROR_HANDOFF.md` with automation-specific state for `StegVerse-Labs/admissibility-wiki`.

## Installed automation surfaces

```text
scripts/check_governed_llm_pages.py
scripts/check_governed_llm_demo_docs.py
scripts/check_governed_llm_deployment_status.py
scripts/check_ios_workflow_mirror_status.py
static/status/ios-workflow-mirror-status.json
static/status/ios-workflow-mirror-sync-next.json
workflow_manifest.json
package.json
.github/workflows/validate-chain-continuation.yml
```

## Validation chain

```text
npm run validate
  -> validate:governed-llm-pages
  -> validate:governed-llm-demo-docs
  -> validate:ios-workflow-mirror
  -> npm run build
```

The canonical workflow runs governed LLM page checks before CI evidence validation and verifies the governed LLM public route set after deployment.

## Manual-task reduction

```text
governed_llm_docs_check -> automated
governed_llm_demo_docs_check -> automated
ios_workflow_mirror_drift_detection -> automated
public_route_set_after_deploy -> automated
mirror_drift_status -> machine-readable
```

## Remaining nonlocal confirmations

```text
GitHub Actions execution
GitHub Pages deployment propagation
public route reachability after deployment
cross-repo adapter and SDK generated receipt availability
full iOS mirror sync when connector allows canonical replacement
```

## Boundary

Automation records status and fail-closed checks. It does not create execution authority, provider governance, external indexing, certification, or master-record persistence.

The iOS workflow mirror is not activation evidence. The canonical workflow remains source of truth.
