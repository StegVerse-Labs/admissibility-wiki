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
executable capture harnesses: 2 of 7
observed external outputs attached: 0 of 18
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
scripts/check_observed_evidence_capture_queue.py
```

Priority capture frameworks:

```text
Open Policy Agent
Cedar Policy
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

## OPA capture harness

Installed:

```text
docs/external-frameworks/capture/opa/policy.rego
docs/external-frameworks/capture/opa/input-allow.json
docs/external-frameworks/capture/opa/input-deny.json
docs/external-frameworks/opa-observation-capture-runbook.md
scripts/capture_opa_observation.py
scripts/check_opa_observation_capture_harness.py
```

The harness requires a locally available OPA executable and writes a `captured_unverified` receipt containing runtime version, UTC timestamp, exact command, policy, input, output, exit code, SHA-256 hashes, authority context, freshness context, limitations, and replay instructions.

No OPA runtime output has been committed or claimed yet.

## Cedar capture harness

Installed:

```text
docs/external-frameworks/capture/cedar/policy.cedar
docs/external-frameworks/capture/cedar/request-allow.json
docs/external-frameworks/capture/cedar/request-deny.json
docs/external-frameworks/cedar-observation-capture-runbook.md
scripts/capture_cedar_observation.py
scripts/check_cedar_observation_capture_harness.py
scripts/check_goal5_external_frameworks_all.py -> Cedar harness validator integrated
```

The Cedar harness is implementation-neutral. The operator must provide the exact implementation identifier, version command, and evaluation command template. The resulting `captured_unverified` receipt preserves the implementation, exact commands, policy, request, output, hashes, timestamp, authority context, freshness context, limitations, and replay instructions.

No Cedar runtime output has been committed or claimed yet.

## Evidence progression

```text
fixture_ready
-> awaiting_capture
-> captured_unverified
-> observed_partial
-> replay_ready
-> replay_confirmed
-> interoperability_candidate
```

No state may advance beyond `captured_unverified` without exact source/model version, timestamp, execution environment, input, output, policy/configuration, authority context, freshness context, trace reference, artifact hashes, limitations, and replay instructions.

## Boundary

```text
fixture_ready != framework executed
capture harness != observed evidence
OPA ALLOW != execution authority
Cedar PERMIT != execution authority
OPA DENY != StegVerse certification
Cedar FORBID != StegVerse certification
single capture != replayability
matching output != current delegation
replay confirmation != execution authority
```

## Parallel coordination

This workstream owns candidate visibility, canonical-source capture, sourced-intake promotion records, framework pages, mappings, fixtures, capture queues, and capture harnesses. Do not overwrite newer CI repair, workflow receipt, deployment verification, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
execute the OPA allow and deny captures with a pinned runtime
execute Cedar allow and deny captures with an identified implementation and pinned version
attach generated OPA and Cedar receipts with hashes and timestamps
independently replay captures before observed_partial status
capture harnesses for MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails
observed-partial compatibility reports only after exact evidence exists
public capture-status page or generated results surface
```

## Next action

Run either the OPA or Cedar harness with a pinned runtime or implementation. Preserve generated receipts as `captured_unverified`; do not claim replayability or compatibility until an independent replay confirms the versioned artifacts and output hashes.

## Release path

The repo is not ready to tag solely because source capture, pages, mappings, fixtures, queues, and capture harnesses exist. After observed-evidence and replay review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
