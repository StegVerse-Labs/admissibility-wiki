# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, and observed-evidence work. Preserve unrelated CI repair, deployment verification, and documentation-mesh work owned by other workstreams.

## Current goal

Progress documented external-framework candidates through explicit states without collapsing visibility, source intake, mapping, fixtures, observed behavior, replayability, compatibility, or execution authority.

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
automated pinned capture jobs: 1 of 7
generated capture artifact validators: 1 of 7
observed external outputs attached: pending workflow result
independently replayed outputs: 0 of 18
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

## Observed-evidence capture structure

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
docs/external-frameworks/observed-evidence-capture-status.md
docs/external-frameworks/command-capture-runbook.md
scripts/check_observed_evidence_capture_queue.py
scripts/capture_external_command_observation.py
scripts/check_priority_command_capture_harnesses.py
```

The public status surface reports structural readiness separately from observed outputs and independent replay.

## Dedicated capture harnesses

### Open Policy Agent

```text
docs/external-frameworks/capture/opa/policy.rego
docs/external-frameworks/capture/opa/input-allow.json
docs/external-frameworks/capture/opa/input-deny.json
docs/external-frameworks/opa-observation-capture-runbook.md
scripts/capture_opa_observation.py
scripts/run_pinned_opa_ci_capture.py
scripts/validate_opa_capture_artifacts.py
scripts/check_opa_observation_capture_harness.py
```

The pinned runner downloads OPA `v1.0.0` from the official GitHub release, verifies its published SHA-256 file, executes allow and deny cases twice in separate processes on the same runner, and writes capture plus replay receipts. The receipt preserves the runtime binary hash, runtime version, GitHub run/SHA context, exact commands, source artifacts, outputs, hashes, limitations, and replay comparison.

The generated-artifact validator requires all four capture/replay files plus the replay receipt, confirms the `captured_unverified` and `replay_confirmed_same_environment` boundaries, checks the authority and compatibility non-claims, verifies every replay comparison, hashes each generated JSON file, and writes `opa-capture-status.json`. It explicitly records independent replay as `not_performed`, compatibility as `not_claimed`, and execution authority as `not_created`.

The canonical `validate-chain-continuation.yml` contains a `capture-opa-evidence` job. It runs automatically on main push, workflow dispatch, and scheduled executions, validates generated receipts before upload, uploads `opa-pinned-capture-replay`, and does not block site deployment when an external download or capture fails. The iOS workflow mirror is logically identical and validator-enforced.

No successful workflow capture is claimed until the job result and uploaded artifact are inspected. The GitHub connector currently exposes no push or scheduled workflow run for the relevant commits, so no run, job, or artifact identifier has been inferred.

### Cedar Policy

```text
docs/external-frameworks/capture/cedar/policy.cedar
docs/external-frameworks/capture/cedar/request-allow.json
docs/external-frameworks/capture/cedar/request-deny.json
docs/external-frameworks/cedar-observation-capture-runbook.md
scripts/capture_cedar_observation.py
scripts/check_cedar_observation_capture_harness.py
```

## Reusable command capture harnesses

The reusable command engine covers:

```text
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

Installed manifests:

```text
docs/external-frameworks/capture/mcp/capture-manifest.json
docs/external-frameworks/capture/a2a/capture-manifest.json
docs/external-frameworks/capture/guardrails-ai/capture-manifest.json
docs/external-frameworks/capture/llama-guard/capture-manifest.json
docs/external-frameworks/capture/nemo-guardrails/capture-manifest.json
```

The engine requires an exact implementation identifier, version command, and execution command. It passes canonical JSON on standard input and records UTC time, exact input/output, source posture, commands, exit code, SHA-256 hashes, authority context, freshness context, limitations, and replay instructions.

## Evidence progression

```text
fixture_ready
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> observed_partial
-> replay_ready
-> replay_confirmed_independent_environment
-> interoperability_candidate
```

Same-environment deterministic replay is useful evidence but is not independent replay and does not establish compatibility.

No state may advance beyond `captured_unverified` without exact source/model version, timestamp, execution environment, input, output, policy/configuration, authority context, freshness context, trace reference, artifact hashes, limitations, and replay instructions.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
policy decision != execution authority
protocol response != standing
classifier result != admissibility
same-environment replay != independent replay
single capture != replayability
matching output != current delegation
replay confirmation != execution authority
```

## Parallel coordination

This workstream owns candidate visibility, canonical-source capture, sourced-intake promotion records, framework pages, mappings, fixtures, capture queues, capture harnesses, automated capture jobs, generated-artifact validators, and the public capture-status surface. Do not overwrite newer CI repair, workflow receipt, deployment verification, lifecycle-formalism, inference-window, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
inspect the first automated OPA capture job and artifact
record exact run, job, artifact, and receipt hashes after success
run OPA replay in a second independent environment before observed_partial
add automated pinned capture jobs and generated-artifact validators for other priority frameworks when reproducible runtimes are selected
produce observed-partial compatibility reports only after exact evidence exists
update capture queue and public status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Observe the workflow triggered by the OPA artifact-validation commits. If the capture job succeeds, inspect and preserve the uploaded allow, deny, replay, replay-receipt, and `opa-capture-status.json` artifacts as `captured_unverified` plus `replay_confirmed_same_environment`. Do not advance to independent replay, observed compatibility, or execution authority.

## Release path

The repo is not ready to tag solely because source capture, pages, mappings, fixtures, queues, all seven priority harnesses, one automated capture job, and one generated-artifact validator exist. After observed-evidence, independent replay, and deployment review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
