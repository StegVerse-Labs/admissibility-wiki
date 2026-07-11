---
title: Tier 1 External Framework Source Promotion Status
---

# Tier 1 External Framework Source Promotion Status

## Current state

The first Tier 1 source-intake pass has captured canonical public sources for all ten priority candidates.

```text
Tier 1 packets: 10
canonical sources captured: 10
promotion state: sourced_intake
framework pages created: 0 of 10
benchmark mappings created: 0 of 10
fixture observations: 0 of 10
```

Source capture is promotion into `sourced_intake` only. It is not validation, certification, endorsement, equivalence, execution authority, or StegVerse standing.

## Promoted source intake

| Framework | Source posture | Next governed action |
|---|---|---|
| Open Policy Agent | canonical official documentation captured | page + mapping |
| Cedar Policy | canonical official documentation captured | page + mapping |
| OSCAL | canonical NIST source captured | page + mapping |
| SPIFFE/SPIRE | canonical official documentation captured | page + mapping |
| W3C Verifiable Credentials | W3C Recommendation captured | page + mapping |
| in-toto | canonical project source captured | page + mapping |
| SLSA | canonical specification captured | page + mapping |
| Sigstore | canonical official documentation captured | page + mapping |
| Model Context Protocol | canonical protocol specification captured | page + mapping |
| Agent2Agent Protocol | canonical protocol specification captured | page + mapping |

The machine-readable source records are in [promoted-intake-records.v0.1.json](./promoted-intake-records.v0.1.json).

## Promotion sequence

```text
canonical source captured
-> sourced_intake
-> framework page
-> benchmark applicability mapping
-> exact fixture or source-versioned example
-> observed result
-> compatibility report
-> Commitment Candidate when applicable
-> SPE standing reconstruction
```

A framework is not advanced to an observed-behavior or interoperability evidence posture without attached observations or artifacts.
