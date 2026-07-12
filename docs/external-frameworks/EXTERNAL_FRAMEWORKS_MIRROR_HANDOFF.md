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
generated capture artifact validation tooling: 2 of 7
fresh-runner replay jobs: 1 of 7
durable pipeline summary generators: 2 of 7
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

The canonical workflow performs bounded pinned capture, same-runner replay, generated-artifact validation, artifact upload, fresh-runner replay, cross-runner comparison, durable pipeline summarization, and fresh-runner artifact upload.

The durable OPA summary records artifact presence and hashes, capture validation, same-runner replay, fresh-runner replay, GitHub run/job/runner context, and explicit non-claims. It reports missing or incomplete artifacts rather than inferring success or failure.

The fresh-runner receipt may record `replay_confirmed_independent_environment` only when every comparison matches. That label means a fresh GitHub Actions runner, not an independent implementation, organization, provider, or authority.

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

The Cedar capture harness remains implementation-neutral. It requires the caller to provide:

```text
exact implementation identifier
exact version command
exact evaluation command template
```

The Cedar artifact validator requires allow and deny capture receipts, verifies exact implementation and version evidence, validates policy/request/output hashes, preserves `captured_unverified`, and writes `cedar-capture-status.json`.

The Cedar pipeline summary writes `cedar-evidence-pipeline-status.json` and reports one of:

```text
artifacts_not_available
artifacts_present_incomplete_or_unverified
captured_unverified_validated
```

It explicitly records same-runner replay, fresh-runner replay, independent implementation/provider review, compatibility, standing, and execution authority as not performed, not claimed, or not created. No Cedar implementation has been selected or pinned, and no Cedar runtime output is claimed.

## Other priority capture harnesses

```text
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
implementation selection != certification
matching output != current delegation
replay confirmation != execution authority
```

## Remaining modules and destinations

Destination: `StegVerse-Labs/admissibility-wiki`

```text
inspect first completed OPA capture and fresh-runner replay artifacts
record exact run, job, artifact, runtime, and receipt hashes after success
select a reproducible Cedar implementation and version before adding a pinned job
perform replay outside the same GitHub repository/provider before stronger independence claims
add artifact validators and pipeline summaries for MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails
produce observed-partial reports only after exact evidence exists
update public capture status from inspected receipts
capture public deployment/page verification receipts
```

## Next action

Inspect `opa-pinned-capture-replay` and `opa-fresh-runner-replay` when their run becomes accessible. In parallel, select and document an exact Cedar implementation and version before automating Cedar execution. Do not infer execution, compatibility, standing, certification, or authority from the existence of capture tooling.

## Release path

The repo is not ready to tag solely because structural capture, replay, validation, and status tooling exists. After artifact inspection, stronger independent replay, external evidence review, and deployment verification, check pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
