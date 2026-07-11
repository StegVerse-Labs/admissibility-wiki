# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake and promotion work. Preserve unrelated CI repair and documentation-mesh work owned by other workstreams.

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

Each promoted framework has canonical-source capture, an individual observatory page, a benchmark applicability mapping, and a source-versioned non-authorizing fixture definition. Fixture coverage is enforced by `scripts/check_external_framework_benchmark_fixtures.py`.

## Observed-evidence capture structure

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
scripts/check_goal5_external_frameworks_all.py -> capture queue validator integrated
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

Each queue entry is currently `awaiting_capture` and declares target cases, required runtime, fixture reference, and the exact next capture action. The queue is structural work only and is not observed evidence.

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

## Fixture and capture posture

```text
fixture_ready != framework executed
fixture definition != observed result
capture queue != observed evidence
expected StegVerse posture != external framework verdict
single run != replayability
replay confirmation != execution authority
FAIL-CLOSED default != claim that the external framework fails
source reference != compatibility evidence
```

## Source classification posture

```text
canonical/official sources -> promotion evidence
secondary commentary -> context only
editor draft -> sourced with draft caution
distribution page -> sourced with distribution caution
Wikipedia -> discovery only; replaced by official W3C source
```

The NeuralTrust AI-governance guide and NHIMG OAuth FAQ remain secondary context. The OpenID AI-governance tag is official organizational context, while OpenID Connect Core is the canonical protocol source. The Wikipedia W3C PROV page is discovery-only and the W3C PROV Overview is canonical. Llama Guard remains explicitly bounded by distribution-source caution.

## Parallel coordination

Concurrent Goal 5 evolution exists. This workstream owns candidate visibility, canonical-source capture, sourced-intake promotion records, progressive framework-page/mapping/fixture creation, and observed-evidence capture structure. Do not overwrite newer CI repair, workflow receipt, deployment verification, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
exact source examples or runtime outputs for seven priority capture frameworks
capture receipts with hashes and timestamps
replay bundles where executable behavior is available
observed-partial compatibility reports only after exact evidence exists
promotion-status validator enforcing source/page/mapping/fixture/capture state
public capture-status page or generated results surface
```

## Next action

Capture the first exact external output using a pinned framework/runtime version. Prefer OPA or Cedar because their policy inputs and decisions can be represented deterministically. Record exact input, output, version, timestamp, policy/configuration, authority context, trace, hashes, replay instructions, and limitations. Do not claim compatibility from a single run.

## Release path

The repo is not ready to tag solely because source capture, pages, mappings, fixtures, and capture queues are complete. After observed-evidence and replay review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
