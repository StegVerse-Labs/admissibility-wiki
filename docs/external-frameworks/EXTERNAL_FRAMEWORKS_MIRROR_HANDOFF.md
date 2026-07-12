# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework intake, evidence capture, implementation selection, binary build and promotion, readiness, execution planning, materialization, runtime authorization, dispatch observation, replay, and publication work.

Preserve unrelated CI repair, conceptual-inheritance, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

## Current state

```text
registered framework and crosswalk entries: 19
candidate intake records: 42
visible observatory entries: 61
sourced-intake pages: 18
benchmark mappings: 18 of 18
non-authorizing fixtures: 18 of 18
priority capture queue entries: 7 of 7
capture harnesses: 7 of 7
artifact validators: 7 of 7
implementation-selection gates: installed
Cedar pinned build-and-hash automation: installed
Cedar build-receipt inspection candidate: installed
Cedar binary registry-promotion receipt layer: installed
readiness matrix: installed
fail-closed execution-plan matrix: installed
job-materialization layer: installed
runtime-authorization layer: installed
runtime-dispatch observation layer: installed
dispatch-state fixture coverage: 4 of 4
runtime jobs emitted by plan automation: 0
observed external outputs: pending workflow evidence
independent organization/provider replays: 0 of 18
```

## Validation-critical observed-evidence references

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
```

The queue remains `AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE` until exact source, version or commit, input, output, timestamp, environment, policy/configuration, authority context, freshness context, hashes, replay instructions, and limitations are attached.

## Governed transition chain

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> selected_binary_build_hashed_unexecuted
-> binary_build_receipt_inspection
-> registry_promotion_review
-> hash_only_registry_promotion_if_approved
-> automation_readiness_review
-> eligible_for_execution_job_materialization
-> governed_job_materialization_receipt
-> materialized_non_executable_descriptor
-> separate_runtime_authorization_review
-> commit_time_predicate_revalidation
-> authorized_not_dispatched_runtime_transition
-> separate_observed_runtime_dispatch_transition
-> dispatch_observation
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No stage advances merely because tooling, a schema, fixture, plan, authorization, promotion receipt, or observation record exists.

## Cedar binary build and registry promotion

Installed:

```text
scripts/build_selected_cedar_binary.py
scripts/check_cedar_selected_binary_build_harness.py
scripts/inspect_cedar_binary_build_receipt.py
scripts/check_cedar_binary_promotion_automation.py
static/schemas/cedar-binary-registry-promotion-receipt.schema.json
tests/fixtures/cedar-binary-registry-promotion-receipt.blocked.json
tests/fixtures/cedar-binary-registry-promotion-receipt.approved-not-applied.json
scripts/check_cedar_binary_registry_promotion_receipts.py
```

The build stage may produce only `BUILT_HASHED_UNEXECUTED`. The inspection stage may produce only a non-mutating promotion candidate. The promotion receipt distinguishes:

```text
BLOCKED_NO_VALID_CANDIDATE
PENDING_REVIEW
DENIED
APPROVED_NOT_APPLIED
APPLIED_HASH_ONLY
```

`ALLOW_REGISTRY_PROMOTION_ONLY` requires a ready candidate, a valid binary SHA-256, completed delegated review, and the exact target field:

```text
frameworks[cedar-policy].selection.compiled_binary_sha256
```

The approved fixture remains:

```text
promotion_state: APPROVED_NOT_APPLIED
registry_mutation_applied: false
runtime_execution_authorized: false
external_consequence_allowed: false
```

A real `APPLIED_HASH_ONLY` receipt must bind the actual workflow candidate and binary hashes and be produced in a separate governed commit after artifact inspection. Hash promotion is not compatibility, standing, runtime authority, dispatch authority, or consequence authority.

## Installed selection, planning, and materialization surfaces

```text
docs/external-frameworks/implementation-selection-gates.v0.1.json
scripts/check_external_framework_implementation_selection_gates.py
scripts/generate_external_framework_automation_readiness.py
scripts/check_external_framework_automation_readiness.py
scripts/generate_external_framework_execution_plans.py
scripts/check_external_framework_execution_plans.py
reports/external-frameworks/implementation-automation-readiness.json
reports/external-frameworks/implementation-execution-plans.json
static/schemas/external-framework-job-materialization-receipt.schema.json
tests/fixtures/external-framework-job-materialization-receipt.blocked.json
tests/fixtures/external-framework-job-materialization-receipt.approved-non-executable.json
scripts/check_external_framework_job_materialization_receipt.py
```

A plan may become eligible for review but may not self-materialize, schedule, dispatch, or execute.

## Runtime authorization

Installed:

```text
static/schemas/external-framework-runtime-authorization-receipt.schema.json
tests/fixtures/external-framework-runtime-authorization-receipt.blocked.json
tests/fixtures/external-framework-runtime-authorization-receipt.allowed-non-dispatched.json
scripts/check_external_framework_runtime_authorization_receipt.py
receipts/external-framework-runtime-authorization-receipt-layer-2026-07-12.json
receipts/external-framework-runtime-authorization-positive-fixture-2026-07-12.json
```

The positive authorization fixture requires all commit-time predicates to pass while preserving:

```text
transition_state: AUTHORIZED_NOT_DISPATCHED
scheduled: false
dispatched: false
execution_started: false
execution_endpoint: null
command: null
credentials_attached: false
external_consequence_allowed: false
required_next_transition: separate_observed_runtime_dispatch_transition
```

Runtime authorization is not scheduling, dispatch, execution, compatibility proof, or consequence authority.

## Runtime dispatch observation

Installed:

```text
static/schemas/external-framework-runtime-dispatch-observation.schema.json
tests/fixtures/external-framework-runtime-dispatch-observation.not-dispatched.json
tests/fixtures/external-framework-runtime-dispatch-observation.dispatch-attempted.json
tests/fixtures/external-framework-runtime-dispatch-observation.dispatched.json
tests/fixtures/external-framework-runtime-dispatch-observation.execution-observed.json
scripts/check_external_framework_runtime_dispatch_observation.py
receipts/external-framework-runtime-dispatch-observation-layer-2026-07-12.json
receipts/external-framework-runtime-dispatch-state-progression-fixtures-2026-07-12.json
scripts/check_goal5_external_frameworks_all.py
```

State coverage:

```text
NOT_DISPATCHED
DISPATCH_ATTEMPTED
DISPATCHED
EXECUTION_OBSERVED
```

State requirements:

```text
NOT_DISPATCHED:
  no attempt, dispatcher, transport, execution, output, exit status, or consequence

DISPATCH_ATTEMPTED:
  attempt id and dispatcher evidence required
  no execution, output, exit status, or consequence

DISPATCHED:
  attempt id, dispatcher reference, and transport reference required
  no execution, output, exit status, or consequence

EXECUTION_OBSERVED:
  attempt id, dispatcher reference, transport reference, execution_started=true, and output_ref required
  completed execution additionally requires exit_status
  fixture remains external_consequence_observed=false
```

The schema and validator enforce these boundaries independently. Fixture coverage must include all four states exactly once. The validator rejects state inflation, including attempted-as-dispatched, dispatched-as-executed, or execution-without-output evidence.

The observation layer is descriptive only. It cannot initiate dispatch, attach credentials, execute a command, or create an external consequence.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
artifact validator != observed success
implementation selection != certification
binary build != runtime execution
binary hash != compatibility proof
promotion candidate != registry mutation
promotion approval != mutation applied
registry hash promotion != execution authority
readiness != execution authority
execution plan != executable job
plan eligibility != job materialization
materialization != runtime authority
runtime authorization != scheduling
runtime authorization != dispatch
dispatch attempted != dispatched
dispatched != execution observed
execution observed != compatibility
observation receipt != authority
fixture state progression != observed production execution
replay confirmation != execution authority
```

## Canonical integration

```text
Aggregate: scripts/check_goal5_external_frameworks_all.py
Canonical workflow: .github/workflows/validate-chain-continuation.yml
iOS mirror: iosnoperiod/github/workflows/validate-chain-continuation.yml
Additional active workflow created: no
```

The aggregate includes:

```text
scripts/check_cedar_binary_registry_promotion_receipts.py
scripts/check_external_framework_job_materialization_receipt.py
scripts/check_external_framework_runtime_authorization_receipt.py
scripts/check_external_framework_runtime_dispatch_observation.py
```

Canonical workflow confirmation remains pending because the available connector has not exposed a status result for the newest commits.

## Remaining work

```text
confirm the repaired Goal 5 aggregate passes in the canonical workflow
inspect the Cedar selected-binary build artifact and promotion candidate
bind the real candidate and binary hashes into an approved promotion receipt
apply only the compiled_binary_sha256 registry field in a separate governed commit
confirm all four dispatch-observation fixtures pass in the aggregate
add dispatch-observation progression validation with prior-receipt hash chaining
inspect the first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
perform replay outside the same repository/provider before stronger independence claims
publish observed-partial reports only after exact evidence exists
capture public deployment and downstream propagation receipts
```

## Next action

Inspect the first accessible `cedar-selected-binary-build` artifact. If its receipt and promotion candidate validate, create an evidence-bound `APPROVED_NOT_APPLIED` receipt using the actual hashes; only then apply the single compiled-binary hash field in a separate commit. In parallel, add dispatch-observation progression validation without initiating dispatch or execution.

## Release path

No release tag is authorized solely from schema, fixture, validation, promotion, or automation installation. After canonical validation, artifact inspection, independent replay, and public deployment verification, check destination handoffs before updating:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

The complete prior thread is not required to continue from this handoff.
