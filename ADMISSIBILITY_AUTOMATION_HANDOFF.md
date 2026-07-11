# Admissibility Automation Handoff

## Scope

This file extends `ADMISSIBILITY_MIRROR_HANDOFF.md` with automation-specific state for `StegVerse-Labs/admissibility-wiki`.

## Installed automation surfaces

```text
scripts/check_governed_llm_pages.py
scripts/check_governed_llm_demo_docs.py
scripts/check_governed_llm_deployment_status.py
scripts/check_ios_workflow_mirror_status.py
scripts/check_admissible_automated_transitions.py
static/status/ios-workflow-mirror-status.json
static/status/ios-workflow-mirror-sync-next.json
static/status/admissible-automated-transitions-status.json
static/governance/admissible-automated-transitions.v0.1.json
receipts/admissible-automated-transitions-observatory-receipt.json
workflow_manifest.json
package.json
.github/workflows/validate-chain-continuation.yml
```

## Validation chain

Current canonical chain:

```text
npm run validate
  -> validate:governed-llm-pages
  -> validate:governed-llm-demo-docs
  -> validate:ios-workflow-mirror
  -> npm run build
```

New local observatory validator:

```text
python scripts/check_admissible_automated_transitions.py
```

The validator checks the page, manifest, receipt, status artifact, sidebar entry, handoff catalog entry, lifecycle state, task-authority source, and authority boundaries.

The next automation task is to wire this command into `package.json` and the canonical `npm run validate` chain without adding another workflow.

## Manual-task reduction

```text
governed_llm_docs_check -> automated
governed_llm_demo_docs_check -> automated
ios_workflow_mirror_drift_detection -> automated
public_route_set_after_deploy -> automated
mirror_drift_status -> machine-readable
automated_transition_catalog_consistency -> locally automated
automated_transition_manifest_status -> machine-readable
```

## Remaining nonlocal confirmations

```text
wire validate:admissible-automated-transitions into package.json
GitHub Actions execution
GitHub Pages deployment propagation
public route reachability after deployment
cross-repo adapter and SDK generated receipt availability
run-specific bootstrap orchestration receipt availability
full iOS mirror sync when connector allows canonical replacement
```

## Boundary

Automation records status and fail-closed checks. It does not create execution authority, provider governance, external indexing, certification, cross-repository mutation authority, or master-record persistence.

The automated-transitions observatory is descriptive and reconstructive. A catalog entry does not prove that a specific run was admissible or successful; run-specific evidence and receipts remain required.

The iOS workflow mirror is not activation evidence. The canonical workflow remains source of truth.
