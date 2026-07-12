# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, capture, replay, evidence-status, implementation-selection, automation-readiness, and execution-plan work. Preserve unrelated CI repair, deployment verification, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

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
executable capture harnesses: 7 of 7
artifact-validation tooling: 7 of 7
durable pipeline-summary tooling: 7 of 7
automated pinned capture jobs: 1 of 7
fresh-runner replay jobs: 1 of 7
implementation-selection gate records: 6 of 6 remaining unpinned frameworks
automated implementation-readiness matrix: installed and workflow-integrated
automated fail-closed execution-plan matrix: installed and chained from readiness generation
runtime jobs emitted by execution-plan automation: 0
observed external outputs attached: pending workflow result
fresh-runner replay outputs attached: pending workflow result
independent organization/provider replays: 0 of 18
```

## Latest Goal 5 validation repair

```text
Failure class: handoff_reference_omission
Failed validator: scripts/check_observed_evidence_capture_queue.py
Observed aggregate: GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: FAIL (1/22 failed)
Repair commit: d6b9db1e5b92471c05759723ce4302c3eda39e97
Receipt: receipts/goal5-observed-evidence-handoff-reference-repair-2026-07-11.json
State: repair installed; canonical workflow confirmation pending
```

The failure indicated that this handoff omitted validation-critical filename references. It did not indicate missing protocol or queue artifacts. The references remain preserved below.

## Observed evidence capture layer

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
```

The queue remains `AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE` until exact source, version or commit, input, output, timestamp, execution environment, policy or configuration, authority context, freshness context, hashes, replay instructions, and limitations are attached.

## Implementation selection, readiness, and plan automation

Installed:

```text
docs/external-frameworks/implementation-selection-gates.v0.1.json
scripts/check_external_framework_implementation_selection_gates.py
scripts/generate_external_framework_automation_readiness.py
scripts/check_external_framework_automation_readiness.py
scripts/generate_external_framework_execution_plans.py
scripts/check_external_framework_execution_plans.py
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

The readiness matrix records selection state, missing required fields, framework-specific context completeness, hash evidence, version or commit evidence, command evidence, selection completeness, registry authorization, execution-job eligibility, and automation state.

The canonical workflow invokes the readiness generator. Readiness generation now automatically invokes the execution-plan generator before the readiness validator and complete Goal 5 aggregate scan. The aggregate checker separately validates the generated plan matrix.

Generated reports:

```text
reports/external-frameworks/implementation-automation-readiness.json
reports/external-frameworks/implementation-execution-plans.json
```

Current expected readiness state for all six:

```text
selection_state: selection_required
execution_authorized_in_registry: false
execution_job_allowed: false
automation_state: blocked_selection_required
```

Current expected plan state for all six:

```text
plan_state: blocked_no_execution_plan
job_materialization_allowed: false
runtime_execution_requested: false
proposed_job: null
required_next_transition: complete_and_validate_implementation_selection
```

## Fail-closed plan behavior

For every framework the plan generator derives blockers from the readiness matrix. A blocked framework cannot emit a proposed job or request runtime execution. An eligible framework still receives no executable job; it only reaches `eligible_for_execution_job_materialization` and requires a separate governed transition.

The plan validator fails if:

```text
framework identity or ordering drifts
readiness hash does not match
job eligibility differs from the readiness matrix
a blocked plan lacks blockers
a blocked plan allows job materialization
runtime_execution_requested is true
proposed_job is non-null
runtime_jobs_emitted is not zero
a plan claims authority or external consequence permission
a separate governed materialization transition is not required
```

## Eligibility predicates

Execution-job review may become eligible only when all are true:

```text
all required selection fields are present
framework-specific context is complete
version or commit evidence is present
command evidence is present
artifact, package, configuration, or model hashes are present
selection_state is implementation_selected_hash_bound
execution_authorized is explicitly true in the registry
global execution_jobs_may_be_added is explicitly true
```

Eligibility still does not create or materialize a runtime job.

## OPA evidence pipeline

OPA remains the only pinned automated runtime path. The canonical workflow performs bounded pinned capture, same-runner replay, generated-artifact validation, artifact upload, fresh-runner replay, cross-runner comparison, durable pipeline summarization, and fresh-runner artifact upload.

No successful OPA capture or replay is claimed until workflow jobs and artifacts are inspected. The available connector still does not expose push or scheduled runs for the relevant commits, so no run, job, or artifact identifier has been inferred.

## Remaining framework posture

Cedar, MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails have complete capture, validation, summary, selection-gate, readiness, and blocked-plan automation. None has an exact selected implementation, version, command, hash-bound environment, provider, transport/model context, or observed output.

## Evidence progression

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> automation_readiness_review
-> eligible_for_execution_job_materialization
-> separate_governed_job_materialization_transition
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No framework may advance merely because tooling, readiness, or a plan exists.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
artifact validator != observed success
pipeline summary != compatibility proof
implementation selection != certification
implementation selection != execution authorization
automation readiness != execution authority
execution plan != executable job
execution-plan eligibility != job materialization
job materialization != authority to cause external consequence
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
inspect first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
populate one implementation-selection record from exact reproducible source evidence
keep execution jobs blocked until every required field, hash, and authorization predicate is present
add a separately governed job-materialization receipt before any newly eligible framework can run
perform replay outside the same GitHub repository/provider before stronger independence claims
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Add the separately governed job-materialization receipt schema and validator. It must consume an eligible execution-plan entry, preserve readiness and plan hashes, and remain non-executable until a distinct authority and consequence-boundary review is attached. In parallel, inspect OPA artifacts when the workflow run becomes accessible.

## Release path

The repo is not ready to tag solely because capture, validation, replay, selection-gating, readiness, and fail-closed execution-plan automation exist. After artifact inspection, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
