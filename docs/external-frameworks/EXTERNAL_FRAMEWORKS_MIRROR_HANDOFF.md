# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, capture, replay, evidence-status, and implementation-selection work. Preserve unrelated CI repair, deployment verification, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

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
observed external outputs attached: pending workflow result
fresh-runner replay outputs attached: pending workflow result
independent organization/provider replays: 0 of 18
```

## Promoted framework set

```text
Open Policy Agent
Cedar Policy
OSCAL
SPIFFE/SPIRE
W3C Verifiable Credentials
in-toto
SLSA
Sigstore
Model Context Protocol
Agent2Agent Protocol
OpenID Connect
OAuth 2.0
W3C Decentralized Identifiers
OpenLineage
W3C PROV
Guardrails AI
Llama Guard
NeMo Guardrails
```

Each promoted framework has canonical-source capture, an individual observatory page, a benchmark applicability mapping, and a source-versioned non-authorizing fixture definition.

## Evidence tooling coverage registry

Installed:

```text
docs/external-frameworks/evidence-tooling-coverage.v0.1.json
scripts/check_external_framework_evidence_tooling_coverage.py
scripts/check_goal5_external_frameworks_all.py -> coverage validator integrated
```

The registry accounts for all seven priority frameworks and binds each to its capture harness, artifact validator, pipeline summarizer, implementation-selection state, and observed-evidence state. Shared command tooling is used for MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails without collapsing their framework identities or evidence records.

## Implementation-selection gates

Installed:

```text
docs/external-frameworks/implementation-selection-gates.v0.1.json
scripts/check_external_framework_implementation_selection_gates.py
scripts/check_goal5_external_frameworks_all.py -> selection-gate validator integrated
```

The selection registry covers the six priority frameworks that do not yet have a pinned execution job:

```text
Cedar Policy
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

Every record remains `selection_required` and `execution_authorized: false`. Before an execution job may be added, the record requires an exact implementation or model identity, version or commit, execution command, artifact/package/model hashes, execution environment, and framework-specific context such as transport, capability negotiation, delegation, guard configuration, model digest, tokenizer/quantization posture, or rails configuration.

The aggregate validator fails if any framework is omitted, reordered, marked selected without evidence, given fewer than the required selection fields, or allowed to authorize execution.

Machine-readable boundaries:

```text
implementation selection != certification
implementation selection != compatibility
implementation selection != standing
implementation selection != execution authority
selection gate != authority to cause external consequence
```

## OPA evidence pipeline

Installed:

```text
docs/external-frameworks/capture/opa/policy.rego
docs/external-frameworks/capture/opa/input-allow.json
docs/external-frameworks/capture/opa/input-deny.json
scripts/capture_opa_observation.py
scripts/run_pinned_opa_ci_capture.py
scripts/validate_opa_capture_artifacts.py
scripts/run_independent_opa_ci_replay.py
scripts/summarize_opa_evidence_pipeline.py
scripts/check_opa_observation_capture_harness.py
.github/workflows/validate-chain-continuation.yml
its iOS workflow mirror
```

The canonical workflow performs bounded pinned capture, same-runner replay, generated-artifact validation, artifact upload, fresh-runner replay, cross-runner comparison, durable pipeline summarization, and fresh-runner artifact upload.

No successful OPA capture or replay is claimed until the corresponding workflow jobs and artifacts are inspected. The available connector still does not expose push or scheduled runs for the relevant commits, so no run, job, or artifact identifier has been inferred.

## Cedar evidence tooling

Installed:

```text
docs/external-frameworks/capture/cedar/policy.cedar
docs/external-frameworks/capture/cedar/request-allow.json
docs/external-frameworks/capture/cedar/request-deny.json
docs/external-frameworks/cedar-observation-capture-runbook.md
scripts/capture_cedar_observation.py
scripts/validate_cedar_capture_artifacts.py
scripts/summarize_cedar_evidence_pipeline.py
scripts/check_cedar_observation_capture_harness.py
```

The Cedar harness remains implementation-neutral. No Cedar implementation has been selected or executed. The new selection gate requires exact evaluator identity, source, version/commit, version command, evaluation command template, package/artifact hash, environment, license/usage boundary, parser/evaluator identity, entity-store/schema posture, and request serialization contract before automation.

## Reusable command evidence tooling

Installed common components:

```text
scripts/capture_external_command_observation.py
scripts/validate_command_capture_artifacts.py
scripts/summarize_command_evidence_pipeline.py
scripts/check_priority_command_capture_harnesses.py
```

Coverage:

```text
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

Each framework retains its own manifest under `docs/external-frameworks/capture/<framework>/capture-manifest.json`. The validator preserves exact implementation, version, command, manifest, input, output, and hash evidence while keeping every first capture at `captured_unverified`. The summary reports artifact availability and structural validation only.

No client/server pair, agent implementation, guard configuration, model digest, runtime, provider, transport, authentication/delegation context, or output has been selected or observed for these five frameworks.

## Evidence progression

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No framework may advance from implementation selection to capture merely because tooling exists.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
artifact validator != observed success
pipeline summary != compatibility proof
policy decision != execution authority
protocol response != standing
tool discovery != tool-call authority
task acceptance != consequence authority
classifier result != admissibility
same-runner replay != fresh-runner replay
fresh-runner replay != independent implementation
fresh-runner replay != independent provider or authority review
implementation selection != certification
implementation selection != execution authorization
matching output != current delegation
replay confirmation != execution authority
```

## Remaining modules and destinations

Destination: `StegVerse-Labs/admissibility-wiki`

```text
inspect first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
populate one implementation-selection record only from exact reproducible source evidence
keep execution_jobs_may_be_added false until every required field and hash is present
perform replay outside the same GitHub repository/provider before stronger independence claims
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Populate and validate the first exact implementation-selection record, preferably Cedar because its deterministic allow/deny fixtures already exist. Do not add a pinned Cedar execution job until the selection record contains exact implementation source, version/commit, commands, artifact hash, environment, and framework-specific context. In parallel, inspect the OPA artifacts when the run becomes accessible.

## Release path

The repo is not ready to tag solely because capture, validation, replay, pipeline-summary, and implementation-selection tooling exists. After artifact inspection, selected implementations, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
