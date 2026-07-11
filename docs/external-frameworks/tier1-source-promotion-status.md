---
title: Tier 1 External Framework Source Promotion Status
---

# Tier 1 External Framework Source Promotion Status

## Current state

The first Tier 1 source-intake pass captured canonical public sources for all ten priority candidates. Each now has an observatory page, a machine-readable benchmark applicability mapping, and a non-authorizing source-versioned fixture definition.

```text
Tier 1 packets: 10
canonical sources captured: 10
promotion state: sourced_intake
framework pages created: 10 of 10
benchmark mappings created: 10 of 10
fixture definitions created: 10 of 10
observed external outputs attached: 0 of 10
```

Source capture, page creation, mapping, and fixture definition are not validation, certification, endorsement, equivalence, execution authority, or StegVerse standing.

## Promoted source intake

| Framework | Page | Mapping | Fixture | Next governed action |
|---|---|---|---|---|
| [Open Policy Agent](./open-policy-agent.md) | complete | mapped_partial | fixture_ready | capture exact decision/replay |
| [Cedar Policy](./cedar-policy.md) | complete | mapped_partial | fixture_ready | capture exact authorization/replay |
| [OSCAL](./oscal.md) | complete | mapped_partial | fixture_ready | attach model instances |
| [SPIFFE/SPIRE](./spiffe-spire.md) | complete | mapped_partial | fixture_ready | attach SVID/attestation examples |
| [W3C Verifiable Credentials](./w3c-verifiable-credentials.md) | complete | mapped_partial | fixture_ready | attach credential examples |
| [in-toto](./in-toto.md) | complete | mapped_partial | fixture_ready | attach signed layout/link examples |
| [SLSA](./slsa.md) | complete | mapped_partial | fixture_ready | attach provenance examples |
| [Sigstore](./sigstore.md) | complete | mapped_partial | fixture_ready | attach signature/log proofs |
| [Model Context Protocol](./model-context-protocol.md) | complete | mapped_partial | fixture_ready | capture tool-call traces |
| [Agent2Agent Protocol](./agent2agent-protocol.md) | complete | mapped_partial | fixture_ready | capture task/delegation traces |

Machine-readable source records are in [promoted-intake-records.v0.1.json](./promoted-intake-records.v0.1.json). Mapping companions are under `benchmark-mappings/`; fixtures are under `fixtures/`.

## Promotion sequence

```text
canonical source captured
-> sourced_intake
-> framework page [COMPLETE 10/10]
-> benchmark applicability mapping [COMPLETE 10/10]
-> non-authorizing fixture definition [COMPLETE 10/10]
-> exact observed result or source example [NEXT]
-> compatibility report
-> Commitment Candidate when applicable
-> SPE standing reconstruction
```

A `fixture_ready` state means a governed test definition exists. It does not assert that the external framework was run, that a result was observed, or that compatibility was established.
