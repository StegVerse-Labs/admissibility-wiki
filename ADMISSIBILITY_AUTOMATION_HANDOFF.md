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
scripts/check_portable_user_ai_pair_participation.py
static/status/ios-workflow-mirror-status.json
static/status/ios-workflow-mirror-sync-next.json
static/status/admissible-automated-transitions-status.json
static/governance/admissible-automated-transitions.v0.1.json
static/governance/portable-user-ai-pair-participation.v0.1.json
receipts/admissible-automated-transitions-observatory-receipt.json
receipts/portable-user-ai-pair-participation-receipt.json
workflow_manifest.json
package.json
.github/workflows/validate-chain-continuation.yml
```

## Automated transition-table derivation

The observatory derives and displays the elements required to treat a proposed automated action as a governed transition:

```text
transition_id
input_state
proposed_action
actor
target
scope
policy_reference
delegation_reference
evidence_references
authority_class
review_posture
execution_context
validity_window
recoverability_profile
admissibility_result
commit_time_validity
output_state
receipt_chain
continuation_rule
```

A scheduled trigger does not satisfy these elements by itself. They must be derived again for each run from the event, current handoff, repository state, policy, delegation, and evidence.

## Portable user/AI pair participation

Installed participant-origin distinction:

```text
PORTABLE_USER_AI_PAIR
  -> persistent user-controlled continuity
  -> independently attributable user and AI identities
  -> bounded delegation and consent
  -> local-first receipt custody
  -> network participation when standing is current
  -> user-authorized ecosystem reconstruction

THREAD_SCOPED_PARTICIPANT
  -> thread, session, or supplied-capability continuity only
  -> no persistent pair identity inferred
  -> no network standing inferred
  -> reconstruction limited to current thread and explicit records
```

Installed files:

```text
docs/governance/portable-user-ai-pair-participation.md
static/governance/portable-user-ai-pair-participation.v0.1.json
receipts/portable-user-ai-pair-participation-receipt.json
scripts/check_portable_user_ai_pair_participation.py
```

The portable node remains the user's continuity and reconstruction authority. Master-Records preserves final continuity records and reconstruction references without becoming the user's global identity authority.

## Validation chain

Current canonical chain:

```text
npm run validate
  -> validate:governed-llm-pages
  -> validate:governed-llm-demo-docs
  -> validate:ios-workflow-mirror
  -> npm run build
```

Local validators awaiting package-chain wiring:

```text
python scripts/check_admissible_automated_transitions.py
python scripts/check_portable_user_ai_pair_participation.py
```

The next automation task is to wire both commands into `package.json` and the canonical `npm run validate` chain without adding another workflow.

## Manual-task reduction

```text
governed_llm_docs_check -> automated
governed_llm_demo_docs_check -> automated
ios_workflow_mirror_drift_detection -> automated
public_route_set_after_deploy -> automated
mirror_drift_status -> machine-readable
automated_transition_catalog_consistency -> locally automated
automated_transition_table_derivation -> locally automated
portable_user_ai_pair_boundary -> locally automated
automated_transition_manifest_status -> machine-readable
```

## Remaining nonlocal confirmations

```text
add portable user/AI pair page to sidebars.js
wire both new validators into package.json
GitHub Actions execution
GitHub Pages deployment propagation
public route reachability after deployment
first run-specific bootstrap orchestration receipt availability
portable-node runtime implementation and network-standing proof
full iOS mirror sync when connector allows canonical replacement
```

## Boundary

Automation records status and fail-closed checks. It does not create execution authority, provider governance, external indexing, certification, cross-repository mutation authority, or master-record persistence.

The automated-transitions observatory and portable-pair model are descriptive and reconstructive. A catalog entry, origin class, or derived template does not prove that a specific run or participant currently has standing; run-specific evidence, commit-time validity, and receipts remain required.

The iOS workflow mirror is not activation evidence. The canonical workflow remains source of truth.
