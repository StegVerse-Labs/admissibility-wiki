# validate-chain-continuation iOS Mirror Sync Record

## Status

The iOS-safe mirror at `iosnoperiod/github/workflows/validate-chain-continuation.yml` is synchronized with the canonical workflow at `.github/workflows/validate-chain-continuation.yml`.

The earlier patch-delta state has been consumed. This file is retained as a historical remediation record and as the controlled location to describe a future delta if the canonical workflow changes before the iOS-safe mirror is refreshed.

Current state:

```text
canonical workflow: .github/workflows/validate-chain-continuation.yml
iOS-safe mirror: iosnoperiod/github/workflows/validate-chain-continuation.yml
status: synchronized
active patch delta: none
canonical workflow remains source of truth: true
mirror is activation evidence: false
patch record is activation evidence: false
```

## Historical delta classes that were reconciled

The prior mirror required reconciliation for validation and publication steps including:

```text
Validate ASRO commitment candidate
Validate governed LLM public pages
Validate governed LLM demo docs
Validate iOS workflow mirror status
Validate admissibility automation handoff
Verify governed LLM route set
Verify ASRO external framework page
```

The current synchronized mirror also carries the External Frameworks publication-proof chain from the canonical workflow:

```text
36-framework source-route contract
Docusaurus build
36-framework generated-route verification
Pages artifact upload
Pages deployment
36-framework deployed public-route/content verification
```

## Future drift rule

If the canonical workflow changes and the iOS-safe mirror is not updated in the same transition:

1. `static/status/ios-workflow-mirror-status.json` must return to `patched_delta_recorded`.
2. `mirror_must_not_be_used_as_current_workflow_until_synced` must become `true`.
3. This file must describe the complete current delta, including any External Frameworks source/build/deploy proof changes.
4. `scripts/check_ios_workflow_mirror_status.py` must fail if the divergent mirror lacks that controlled delta record.
5. Synchronization must restore byte equality before status returns to `synchronized`.

## Boundary

The iOS mirror is a usability copy, not a second workflow authority. Synchronization does not create activation, deployment, release, execution, standing, admissibility, certification, or publication authority.
