---
title: Tier 1 External Framework Source Promotion Status
---

# Tier 1 External Framework Source Promotion Status

## Current state

The first Tier 1 source-intake pass captured canonical public sources for all ten priority candidates. Each now has an observatory page and a machine-readable benchmark applicability mapping.

```text
Tier 1 packets: 10
canonical sources captured: 10
promotion state: sourced_intake
framework pages created: 10 of 10
benchmark mappings created: 10 of 10
fixture observations: 0 of 10
```

Source capture, page creation, and mapping are not validation, certification, endorsement, equivalence, execution authority, or StegVerse standing.

## Promoted source intake

| Framework | Page state | Mapping state | Next governed action |
|---|---|---|---|
| [Open Policy Agent](./open-policy-agent.md) | complete | mapped_partial | fixture |
| [Cedar Policy](./cedar-policy.md) | complete | mapped_partial | fixture |
| [OSCAL](./oscal.md) | complete | mapped_partial | fixture |
| [SPIFFE/SPIRE](./spiffe-spire.md) | complete | mapped_partial | fixture |
| [W3C Verifiable Credentials](./w3c-verifiable-credentials.md) | complete | mapped_partial | fixture |
| [in-toto](./in-toto.md) | complete | mapped_partial | fixture |
| [SLSA](./slsa.md) | complete | mapped_partial | fixture |
| [Sigstore](./sigstore.md) | complete | mapped_partial | fixture |
| [Model Context Protocol](./model-context-protocol.md) | complete | mapped_partial | fixture |
| [Agent2Agent Protocol](./agent2agent-protocol.md) | complete | mapped_partial | fixture |

Machine-readable source records are in [promoted-intake-records.v0.1.json](./promoted-intake-records.v0.1.json). Mapping companions are under `benchmark-mappings/`.

## Promotion sequence

```text
canonical source captured
-> sourced_intake
-> framework page [COMPLETE 10/10]
-> benchmark applicability mapping [COMPLETE 10/10]
-> exact fixture or source-versioned example [NEXT]
-> observed result
-> compatibility report
-> Commitment Candidate when applicable
-> SPE standing reconstruction
```

A `mapped_partial` state records benchmark applicability only. It does not assert observed behavior or compatibility.
