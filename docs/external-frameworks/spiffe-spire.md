---
title: SPIFFE/SPIRE
---
# SPIFFE/SPIRE

## Evidence posture
`sourced_intake` — canonical official documentation captured; no runtime observation claimed.

## Published scope
SPIFFE defines workload identity standards; SPIRE implements workload attestation and issuance of short-lived workload credentials within trust domains.

Canonical source: https://spiffe.io/docs/latest/spiffe-about/overview/

## StegVerse relationship
`adjacent`

Workload identity and attestation may establish actor or workload evidence. Current delegation, transition scope, and consequence-binding authority remain separately reconstructable.

## Benchmark relevance
`authority_boundary`, `evidence_freshness_boundary`, `commitment_boundary`, `reconstruction_boundary`

## Non-claims
Identity is not authority. Attestation is not admissibility. Credential possession does not independently grant execution authority.
