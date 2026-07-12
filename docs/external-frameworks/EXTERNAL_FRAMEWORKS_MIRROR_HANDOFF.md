# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, capture, replay, evidence-status, implementation-selection, and automation-readiness work. Preserve unrelated CI repair, deployment verification, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

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

The failure did not indicate missing protocol or queue artifacts. It indicated that the source-of-truth handoff omitted two validation-critical filename references. The references were restored without changing workflow logic, authority state, evidence state, or execution authorization.

## Observed evidence capture layer

Installed and required by the Goal 5 aggregate validator:

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
```

The protocol governs the transition from non-authorizing fixture definitions to observed evidence. The queue remains explicitly `AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE` until exact source, version or commit, input, output, timestamp, execution environment, policy or configuration, authority context, freshness context, hashes, replay instructions, and limitations are attached.

These references are validation-critical. Removing either `observed-evidence-capture-protocol.md` or `observed-evidence-capture-queue.v0.1.json` from this handoff causes the Goal 5 external-framework aggregate to fail closed.

## Automation readiness layer

Installed:

```text
docs/external-frameworks/implementation-selection-gates.v0.1.json
scripts/check_external_framework_implementation_selection_gates.py
scripts/generate_external_framework_automation_readiness.py
scripts/check_external_framework_automation_readiness.py
scripts/check_goal5_external_frameworks_all.py
.github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

The readiness generator evaluates all six unpinned priority frameworks:

```text
Cedar Policy
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

For each framework it records:

```text
selection state
missing required fields
framework-specific context completeness
hash evidence presence
version or commit evidence presence
command evidence presence
selection completeness
registry execution authorization
execution-job eligibility
automation state
```

The current expected state for all six is:

```text
selection_state: selection_required
execution_authorized_in_registry: false
execution_job_allowed: false
automation_state: blocked_selection_required
```

The matrix is written to:

```text
reports/external-frameworks/implementation-automation-readiness.json
```

The canonical workflow now generates, validates, and uploads it on push, pull request, workflow dispatch, and schedule as:

```text
external-framework-automation-readiness
```

The canonical and iOS workflow copies are byte-identical after this change.

## Fail-closed behavior

An execution job may only become eligible when all of the following are true:

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

The readiness checker fails if a `selection_required` framework permits execution or if execution is allowed while any required predicate is absent.

## OPA evidence pipeline

OPA remains the only pinned automated runtime path. The canonical workflow performs bounded pinned capture, same-runner replay, generated-artifact validation, artifact upload, fresh-runner replay, cross-runner comparison, durable pipeline summarization, and fresh-runner artifact upload.

No successful OPA capture or replay is claimed until the corresponding workflow jobs and artifacts are inspected. The available connector still does not expose push or scheduled runs for the relevant commits, so no run, job, or artifact identifier has been inferred.

## Remaining framework posture

Cedar, MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails have complete capture, validation, summary, selection-gate, and readiness-automation structure. None has an exact selected implementation, version, command, hash-bound environment, provider, transport/model context, or observed output.

## Evidence progression

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> automation_readiness_review
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No framework may advance merely because tooling or automation exists.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
artifact validator != observed success
pipeline summary != compatibility proof
implementation selection != certification
implementation selection != execution authorization
automation readiness != execution authority
readiness receipt != permission to cause external consequence
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
perform replay outside the same GitHub repository/provider before stronger independence claims
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Confirm the repaired Goal 5 aggregate passes. Then populate the first exact implementation-selection record, preferably Cedar because deterministic allow/deny fixtures already exist. The automated readiness matrix must remain blocked until the record contains exact implementation source, version or commit, commands, artifact hash, environment, framework-specific context, and explicit authorization predicates. In parallel, inspect OPA artifacts when the run becomes accessible.

## Release path

The repo is not ready to tag solely because capture, validation, replay, selection-gating, and readiness automation exist. After artifact inspection, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
