# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, capture, replay, evidence status, implementation selection, readiness, execution-plan generation, and job-materialization governance.

Preserve unrelated CI repair, deployment verification, lifecycle-formalism, inference-window, conceptual-inheritance, and documentation-mesh work owned by other workstreams.

## Current state

```text
registered framework and crosswalk entries: 19
candidate intake records: 42
total visible observatory entries: 61
sourced_intake records: 18
individual sourced-intake pages: 18
benchmark mappings for promoted candidates: 18 of 18
non-authorizing fixture definitions: 18 of 18
priority observed-evidence queue entries: 7 of 7
capture harnesses: 7 of 7
artifact-validation tooling: 7 of 7
durable pipeline-summary tooling: 7 of 7
automated pinned capture jobs: 1 of 7
fresh-runner replay jobs: 1 of 7
implementation-selection gate records: 6 of 6 unpinned frameworks
readiness matrix: installed and workflow-integrated
fail-closed execution-plan matrix: installed and chained
job-materialization receipt layer: installed and aggregate-validated
job-materialization fixtures: blocked + approved-non-executable
runtime jobs emitted by plan automation: 0
observed external outputs: pending workflow evidence
independent organization/provider replays: 0 of 18
```

## Latest observed validation repair

```text
Failure class: handoff_reference_omission
Failed validator: scripts/check_observed_evidence_capture_queue.py
Observed aggregate: GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: FAIL (1/22 failed)
Repair commit: d6b9db1e5b92471c05759723ce4302c3eda39e97
Receipt: receipts/goal5-observed-evidence-handoff-reference-repair-2026-07-11.json
State: repair installed; canonical workflow confirmation pending
```

The failure concerned missing references in this handoff, not missing protocol or queue artifacts.

Validation-critical references:

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
```

The queue remains `AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE` until exact source, version or commit, input, output, timestamp, execution environment, policy/configuration, authority context, freshness context, hashes, replay instructions, and limitations are attached.

## Selection, readiness, and execution-plan automation

Installed:

```text
docs/external-frameworks/implementation-selection-gates.v0.1.json
scripts/check_external_framework_implementation_selection_gates.py
scripts/generate_external_framework_automation_readiness.py
scripts/check_external_framework_automation_readiness.py
scripts/generate_external_framework_execution_plans.py
scripts/check_external_framework_execution_plans.py
reports/external-frameworks/implementation-automation-readiness.json
reports/external-frameworks/implementation-execution-plans.json
scripts/check_goal5_external_frameworks_all.py
.github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

Coverage:

```text
Cedar Policy
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

Expected readiness state for all six:

```text
selection_state: selection_required
execution_authorized_in_registry: false
execution_job_allowed: false
automation_state: blocked_selection_required
```

Expected execution-plan state for all six:

```text
plan_state: blocked_no_execution_plan
job_materialization_allowed: false
runtime_execution_requested: false
proposed_job: null
required_next_transition: complete_and_validate_implementation_selection
```

A generated plan may establish eligibility for later review. It may not create, materialize, schedule, dispatch, or execute a runtime job.

## Governed job-materialization receipt layer

Installed:

```text
static/schemas/external-framework-job-materialization-receipt.schema.json
tests/fixtures/external-framework-job-materialization-receipt.blocked.json
tests/fixtures/external-framework-job-materialization-receipt.approved-non-executable.json
scripts/check_external_framework_job_materialization_receipt.py
receipts/external-framework-job-materialization-receipt-layer-2026-07-11.json
scripts/check_goal5_external_frameworks_all.py
```

The receipt layer binds readiness and execution-plan artifacts by SHA-256 and requires distinct authority and consequence-boundary review.

### Blocked fixture

```text
materialization_state: BLOCKED_NOT_ELIGIBLE
decision: FAIL_CLOSED
runtime_execution_authorized: false
runtime_job: null
authority_review.status: NOT_STARTED
consequence_boundary_review.status: NOT_STARTED
```

### Approved-but-non-executable fixture

```text
materialization_state: MATERIALIZED_NOT_EXECUTABLE
decision: ALLOW_MATERIALIZATION_ONLY
runtime_execution_authorized: false
runtime_job.job_state: NON_EXECUTABLE_MATERIALIZED_DESCRIPTOR
runtime_job.execution_endpoint: null
runtime_job.command: null
runtime_job.credentials_attached: false
runtime_job.external_consequence_allowed: false
runtime_job.required_next_transition: separate_runtime_authorization_review
authority_review.status: PASS
consequence_boundary_review.status: PASS
```

The validator now checks both fixtures and rejects any receipt that:

```text
omits readiness or execution-plan hashes
allows runtime execution inside the materialization receipt
allows BLOCKED, DENY, or REVIEW_REQUIRED to contain a job
permits an approved descriptor to contain an endpoint or command
attaches credentials to a materialized descriptor
allows external consequence
omits separate authority or consequence-boundary review
claims an eligible plan can self-materialize
claims materialization is runtime authority
omits the later distinct runtime-authorization transition
```

## Evidence progression

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> automation_readiness_review
-> eligible_for_execution_job_materialization
-> governed_job_materialization_receipt
-> materialized_non_executable_descriptor
-> separate_runtime_authorization_review
-> runtime_execution_authorization_if_admissible
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No framework advances because tooling, readiness, a plan, a materialization receipt, or a materialized descriptor exists.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
artifact validator != observed success
pipeline summary != compatibility proof
implementation selection != certification
implementation selection != execution authority
automation readiness != execution authority
execution plan != executable job
execution-plan eligibility != job materialization
job-materialization receipt != runtime execution authority
materialized descriptor != executable job
materialization approval != consequence authority
runtime authorization != proof of compatibility
policy decision != execution authority
protocol response != standing
tool discovery != tool-call authority
task acceptance != consequence authority
classifier result != admissibility
fresh-runner replay != independent implementation
fresh-runner replay != independent provider or authority review
matching output != current delegation
replay confirmation != execution authority
```

## Remaining work

```text
confirm the repaired Goal 5 aggregate passes in the canonical workflow
confirm both materialization fixtures pass in the aggregate
inspect the first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
populate one implementation-selection record from exact reproducible source evidence
keep runtime jobs blocked until all required field, hash, authority, and consequence predicates hold
add the separate runtime-authorization receipt schema and validator
perform replay outside the same GitHub repository/provider before stronger independence claims
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Build a separate runtime-authorization receipt schema and validator that consumes a `MATERIALIZED_NOT_EXECUTABLE` descriptor, binds the materialization receipt hash, requires current authority/delegation/policy/freshness evidence, and still emits no execution unless every commit-time predicate passes.

In parallel, inspect OPA workflow artifacts when a run becomes accessible.

## Release path

The repo is not ready to tag solely because capture, validation, replay, selection-gating, readiness, execution-plan automation, and materialization-receipt validation exist. After artifact inspection, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-Labs/stegguardian-wiki
```

The complete prior thread is not required to continue from this handoff.
