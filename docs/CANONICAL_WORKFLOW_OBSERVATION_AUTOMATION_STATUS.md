# Canonical Workflow Observation Automation Status

## Goal

```text
Goal: Eliminate manual workflow observation, result reconciliation, health classification, and health-transition explanation.
Repository: StegVerse-Labs/admissibility-wiki
State: checkpoint_reached
Manual tasks required: none
User action required: false
```

## Automated Chain

```text
canonical workflow trigger
-> full validation chain
-> run-bound workflow observation receipt
-> bounded observation-history reconciliation
-> compact health classification
-> health-transition receipt comparing consecutive observations
-> GitHub Pages deployment
-> automatic endpoint verification
-> hourly scheduled re-observation
```

## Durable Surfaces

```text
scripts/write_canonical_workflow_observation_receipt.py
scripts/check_canonical_workflow_observation_receipt.py
scripts/publish_canonical_workflow_observation_receipt.py
scripts/check_canonical_workflow_observation_publication.py
scripts/reconcile_canonical_workflow_observation_history.py
scripts/check_canonical_workflow_observation_history.py
scripts/generate_canonical_workflow_health_summary.py
scripts/check_canonical_workflow_health_summary.py
scripts/check_canonical_workflow_health_transition_receipt.py
scripts/check_canonical_workflow_observation_automation_status.py
scripts/check_full_validation_chain.py
static/status/canonical-workflow-observation-automation.json
static/status/canonical-workflow-observation-receipt.json (generated)
static/status/canonical-workflow-observation-history.json (generated)
static/status/canonical-workflow-health-summary.json (generated)
static/status/canonical-workflow-health-transition-receipt.json (generated)
```

## Public Endpoints

```text
/status/canonical-workflow-observation-automation.json
/status/canonical-workflow-observation-receipt.json
/status/canonical-workflow-observation-history.json
/status/canonical-workflow-health-summary.json
/status/canonical-workflow-health-transition-receipt.json
```

The transition receipt records whether the health class changed, the prior and resulting classes, the evidence fields that caused each classification, and the fail-closed automated consequence. An unchanged class is also recorded so continuity does not depend on a human deciding whether a transition was important enough to preserve.

## No-Manual Boundary

```text
manual_tasks_required: []
user_action_required: false
reconciliation_owner: canonical build-pages job
health_owner: canonical build-pages job
health_transition_owner: canonical build-pages job
next_evaluation: next repository-owned canonical workflow trigger
scheduled_reobservation: hourly canonical workflow schedule
```

Cancelled, failed, incomplete, history-unavailable, unchanged, or externally deferred observations do not create user tasks. Missing external source locators and specialist reviews remain fail-closed under their declared owners.

## Validation

```bash
python scripts/check_canonical_workflow_observation_receipt.py
python scripts/check_canonical_workflow_observation_publication.py
python scripts/check_canonical_workflow_observation_history.py
python scripts/check_canonical_workflow_health_summary.py
python scripts/check_canonical_workflow_health_transition_receipt.py
python scripts/check_canonical_workflow_observation_automation_status.py
python scripts/check_full_validation_chain.py
```

## Workflow Ownership

The single canonical workflow owns validation, artifact transfer, publication, history reconciliation, health classification, health-transition explanation, deployment, endpoint observation, and scheduled re-evaluation. Its iOS-safe mirror remains synchronized under `iosnoperiod/github/workflows/validate-chain-continuation.yml`.

## Authority Boundary

These receipts record validation, publication, reachability, bounded history, health classification, and transitions between classifications only. They do not grant merge, release, deployment, publication, execution, acceptance, proof, custody, or downstream mutation authority.

## Next Goal

Automatically preserve a bounded public history of health-transition receipts, deduplicated by receipt identity and reconciled on every canonical workflow run, without assigning archival or review work to the user.
