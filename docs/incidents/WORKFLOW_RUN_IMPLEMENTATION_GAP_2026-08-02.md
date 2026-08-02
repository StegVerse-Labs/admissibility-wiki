# Workflow Run / Implementation Gap Incident — 2026-08-02

## Observation

The `Validate chain continuation` workflow has accumulated more than 2,500 runs. Recent repository activity shows repeated cancelled/neutral workflow runs, plus failed runs, while handoff and session-consolidation records describe work as transferred, machine-owned, or archive-ready.

## Confirmed workflow mechanics

The canonical workflow:

- starts on every push to `main`;
- starts on pull requests;
- starts on manual dispatch;
- uses one concurrency group per ref;
- sets `cancel-in-progress: true`.

A rapid sequence of small commits therefore starts a run for each commit and cancels the preceding run. A cancelled run is not implementation evidence and contributes zero completion credit.

## Governance defect

The repository has been recognizing mutations, task-registry entries, documentation, status objects, and workflow starts as progress without consistently requiring a completed successful canonical workflow for the exact claimed commit SHA.

This permits contradictory states such as:

- canonical result recorded as failed;
- build/deploy/public verification skipped;
- activation recorded as not admissible;
- session nevertheless marked archive-ready;
- internal execution described as active without terminal run evidence.

## Required repair

1. Stop producing completion, release, activation, or archive-safe claims from commit intent or workflow start counts.
2. Inspect the latest completed failed manual run and record its failed job, step, command, and error output.
3. Repair the underlying validator/build/deployment failures.
4. Require exact-SHA terminal evidence: completed, non-cancelled canonical workflow; required jobs successful; required artifacts present; Pages deployment and public verification successful when publication is claimed.
5. Classify every workflow result as `success`, `failure`, `cancelled`, `skipped`, or `superseded`; only `success` may satisfy implementation completion.
6. Consolidate related changes so the workflow can finish rather than being continually superseded.
7. Correct the mirror handoff and machine-readable status records after successful verification, not before.

## Current disposition

```text
incident_status: OPEN
canonical_state: FAIL_CLOSED
implementation_complete: false
activation_admissible: false
release_ready: false
archive_safe_claim_supported: false
user_manual_action_required: false
```

## Closure evidence

This incident closes only when a fresh canonical run for the intended head SHA completes successfully and its artifacts, deployment result, and public verification are directly inspectable and bound into the handoff.
