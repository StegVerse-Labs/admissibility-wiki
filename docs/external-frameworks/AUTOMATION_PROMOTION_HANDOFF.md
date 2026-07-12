# External Framework Automation Promotion Handoff

## Promotion completed

Automation now advances through four generated, fail-closed layers:

```text
implementation selection gates
-> automation readiness matrix
-> execution-plan matrix
-> non-executable job-materialization candidate matrix
```

The promoted layer does **not** create or dispatch a runtime job.

## Installed artifacts

```text
docs/external-frameworks/job-materialization-candidate.schema.json
scripts/generate_external_framework_job_materialization_candidates.py
scripts/check_external_framework_job_materialization_candidates.py
reports/external-frameworks/job-materialization-candidates.json  # generated in validation/runtime context
```

The existing materialization receipt contract remains separately installed:

```text
static/schemas/external-framework-job-materialization-receipt.schema.json
tests/fixtures/external-framework-job-materialization-receipt.blocked.json
scripts/check_external_framework_job_materialization_receipt.py
```

The candidate matrix and the materialization receipt are distinct:

- A **candidate** is automatically derived from readiness and execution-plan evidence.
- A **materialization receipt** records a separate governed review decision.
- Neither artifact authorizes runtime execution.

## Automated behavior

The readiness generator invokes the execution-plan generator. The execution-plan generator now invokes the job-materialization-candidate generator. Goal 5 aggregate validation checks the readiness matrix, execution plans, generated candidates, and the separate materialization receipt contract.

For every ineligible framework, automation must produce:

```text
candidate_state: blocked_plan_ineligible
runtime_job_materialized: false
runtime_execution_requested: false
materialized_job: null
authority_review.state: not_performed
consequence_boundary_review.state: not_performed
```

For a future eligible framework, automation may produce only:

```text
candidate_state: awaiting_authority_and_consequence_review
runtime_job_materialized: false
runtime_execution_requested: false
materialized_job: null
```

Eligibility therefore creates a review candidate, not a job.

## Bound evidence

Every candidate preserves:

- readiness artifact SHA-256
- execution-plan artifact SHA-256
- framework identity
- source plan state
- source job-eligibility state
- unresolved blockers
- authority-review state
- consequence-boundary-review state
- explicit non-execution boundaries

## Required governed transition

Before any runtime-job object can be materialized, a separate receipt must attach:

- reviewer identity
- valid delegation reference
- review validity window
- target and bounded scope
- recoverability profile
- rollback or stop condition
- exact readiness and execution-plan hashes
- a decision limited to materialization, not runtime execution

A later runtime transition must remain separate from materialization and reconstruct current authority again.

## Current posture

```text
priority frameworks: 7
pinned runtime paths: 1
unpinned selection-gated frameworks: 6
readiness matrices generated: yes
execution-plan matrices generated: yes
job-materialization candidate matrices generated: yes
runtime jobs emitted by promoted automation: 0
runtime execution requested by promoted automation: false
```

## Boundary

```text
candidate generation != job materialization
job materialization candidate != executable job
materialization receipt != runtime execution authority
review completion != permission to cause external consequence
plan eligibility != current delegation
runtime execution still requires a separate governed transition
```

## Next action

Populate one exact, hash-bound implementation-selection record from canonical source evidence. When it becomes eligible, inspect the generated materialization candidate and attach a separate authority and consequence-boundary review receipt. Do not create a runnable workflow job in the same transition.
