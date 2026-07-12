# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake, mapping, fixture, capture, replay, and evidence-status work. Preserve unrelated CI repair, deployment verification, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

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
fresh-runner replay jobs: 1 of 7
durable pipeline summary generators: 1 of 7
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

The canonical workflow performs these bounded stages:

```text
pinned OPA capture
-> same-runner replay and generated-artifact validation
-> artifact upload
-> fresh-runner job downloads the upstream artifact
-> independently downloads and checksum-verifies the same pinned OPA binary
-> executes allow and deny cases on a new runner
-> compares output, stdout, policy, input, and runtime-version evidence
-> writes a fresh-runner replay receipt
-> writes opa-evidence-pipeline-status.json
-> uploads opa-fresh-runner-replay
```

The durable pipeline summary records artifact presence and hashes, capture validation, same-runner replay, fresh-runner replay, GitHub run/job/runner context, and explicit non-claims. It reports missing or incomplete artifacts rather than inferring success or failure.

The fresh-runner receipt may record `replay_confirmed_independent_environment` only when every comparison matches. That label means a fresh GitHub Actions runner, not an independent implementation, organization, provider, or authority. The summary separately records independent implementation/provider review as `not_performed`, compatibility as `not_claimed`, standing as `not_created`, and execution authority as `not_created`.

No successful capture or replay is claimed until the corresponding workflow jobs and artifacts are inspected. The available connector still does not expose push/scheduled runs for the relevant commits, so no run, job, or artifact identifier has been inferred.

## Other priority capture harnesses

```text
Cedar Policy: dedicated implementation-neutral harness
Model Context Protocol: reusable command harness
Agent2Agent Protocol: reusable command harness
Guardrails AI: reusable command harness
Llama Guard: reusable command harness
NeMo Guardrails: reusable command harness
```

## Evidence progression

```text
fixture_ready
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

The fresh-runner stage does not itself establish compatibility, standing, delegation, admissibility, or execution authority.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
policy decision != execution authority
protocol response != standing
classifier result != admissibility
same-runner replay != fresh-runner replay
fresh-runner replay != independent implementation
fresh-runner replay != independent provider or authority review
pipeline summary != compatibility proof
matching output != current delegation
replay confirmation != execution authority
```

## Remaining modules and destinations

Destination: `StegVerse-Labs/admissibility-wiki`

```text
inspect first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
perform replay outside the same GitHub repository/provider before stronger independence claims
add pinned jobs, validators, and pipeline summaries for other frameworks when reproducible runtimes are selected
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Observe the workflow triggered by the durable-summary commits. Inspect `opa-pinned-capture-replay` and `opa-fresh-runner-replay`, including `opa-evidence-pipeline-status.json`. Preserve the first as `captured_unverified` plus same-environment replay and the second only as fresh-runner replay. Do not claim independent implementation, compatibility, standing, or execution authority.

## Release path

The repo is not ready to tag solely because the structural capture, replay, and status pipeline exists. After artifact inspection, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
