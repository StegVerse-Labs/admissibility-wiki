---
title: External Framework Observed Evidence Capture Protocol
---

# External Framework Observed Evidence Capture Protocol

## Purpose

This protocol governs the transition from non-authorizing fixture definitions to observed external-framework evidence.

A framework must not advance from `fixture_ready` to `observed_partial`, `replay_ready`, or `interoperability_ready` unless exact inputs, outputs, source or model versions, timestamps, execution context, authority context, and reconstruction references are captured.

```text
fixture definition != observed output
observed output != compatibility
single run != replayability
framework verdict != StegVerse authority
```

## Required Capture Fields

Every observed-evidence record must include:

```text
observation_id
framework_id
fixture_reference
source_reference
source_version_or_commit
capture_timestamp_utc
execution_environment
exact_input
exact_output
exit_status_or_protocol_state
policy_or_configuration_reference
authority_context
freshness_context
trace_or_trajectory_reference
artifact_hashes
replay_instructions
capture_limitations
stegverse_expected_posture
non_claims
```

## Evidence States

| State | Meaning |
|---|---|
| awaiting_capture | Fixture exists; no external output is attached. |
| captured_unverified | Exact output is attached but has not been independently replayed. |
| observed_partial | Source/version/input/output/context are complete enough for a bounded observation. |
| replay_ready | Replay instructions and artifacts are complete. |
| replay_confirmed | Repeated runs are attached and compared. |
| interoperability_candidate | Observation may be routed into a Commitment Candidate for SPE review. |

## Priority Capture Set

The first capture wave covers frameworks that expose decision, protocol, classifier, or runtime behavior:

```text
Open Policy Agent
Cedar Policy
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

## Fail-Closed Rule

Missing source version, exact input, exact output, timestamp, policy/configuration, authority context, or trace reference prevents promotion beyond `captured_unverified`.

## Non-Claims

```text
capture protocol != framework certification
observed output != general compatibility
replay confirmation != execution authority
classifier label != admissibility determination
protocol completion != consequence authorization
policy allow != StegVerse standing
```
