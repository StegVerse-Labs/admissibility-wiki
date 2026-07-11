---
title: Tier 1 External Framework Source Promotion Status
---

# Tier 1 External Framework Source Promotion Status

## Current state

The first Tier 1 source-intake pass captured canonical public sources for all ten priority candidates and each now has an individual observatory page.

```text
Tier 1 packets: 10
canonical sources captured: 10
promotion state: sourced_intake
framework pages created: 10 of 10
benchmark mappings created: 0 of 10
fixture observations: 0 of 10
```

Source capture and page creation are not validation, certification, endorsement, equivalence, execution authority, or StegVerse standing.

## Promoted source intake

| Framework | Source posture | Page state | Next governed action |
|---|---|---|---|
| [Open Policy Agent](./open-policy-agent.md) | canonical official documentation captured | page complete | mapping |
| [Cedar Policy](./cedar-policy.md) | canonical official documentation captured | page complete | mapping |
| [OSCAL](./oscal.md) | canonical NIST source captured | page complete | mapping |
| [SPIFFE/SPIRE](./spiffe-spire.md) | canonical official documentation captured | page complete | mapping |
| [W3C Verifiable Credentials](./w3c-verifiable-credentials.md) | W3C Recommendation captured | page complete | mapping |
| [in-toto](./in-toto.md) | canonical project source captured | page complete | mapping |
| [SLSA](./slsa.md) | canonical specification captured | page complete | mapping |
| [Sigstore](./sigstore.md) | canonical official documentation captured | page complete | mapping |
| [Model Context Protocol](./model-context-protocol.md) | canonical protocol specification captured | page complete | mapping |
| [Agent2Agent Protocol](./agent2agent-protocol.md) | canonical protocol specification captured | page complete | mapping |

The machine-readable source records are in [promoted-intake-records.v0.1.json](./promoted-intake-records.v0.1.json).

## Promotion sequence

```text
canonical source captured
-> sourced_intake
-> framework page [COMPLETE 10/10]
-> benchmark applicability mapping [NEXT]
-> exact fixture or source-versioned example
-> observed result
-> compatibility report
-> Commitment Candidate when applicable
-> SPE standing reconstruction
```

A framework is not advanced to an observed-behavior or interoperability evidence posture without attached observations or artifacts.
