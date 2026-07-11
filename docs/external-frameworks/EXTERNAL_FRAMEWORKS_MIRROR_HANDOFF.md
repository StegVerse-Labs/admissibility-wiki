# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff for Goal 5 external-framework source intake and promotion work. Preserve unrelated CI repair and documentation-mesh work owned by other workstreams.

## Current goal

Progress documented external-framework candidates through explicit states without collapsing visibility, source intake, mapping, fixtures, observed behavior, compatibility, or execution authority.

## Current state

```text
registered framework and crosswalk entries: 19
candidate intake records: 42
total visible observatory entries: 61
sourced_intake records: 18
individual sourced-intake pages: 18
benchmark mappings for promoted candidates: 10
fixture observations for promoted candidates: 0
```

## Second-wave source classification

Supplied URLs were classified before use:

```text
canonical/official sources -> promotion evidence
secondary commentary -> context only
editor draft -> sourced with draft caution
distribution page -> sourced with distribution caution
Wikipedia -> discovery only; replaced by official W3C source
```

Record:

```text
docs/external-frameworks/supplied-source-classification-2026-07-11.md
```

## Tier 1 complete through mapping

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
```

Each has canonical source capture, sourced-intake record, individual page, and `mapped_partial` benchmark applicability mapping.

## Second-wave sourced intake and pages

```text
OpenID Connect
OAuth 2.0
W3C Decentralized Identifiers
OpenLineage
W3C PROV
Guardrails AI
Llama Guard
NeMo Guardrails
```

Installed pages:

```text
docs/external-frameworks/openid-connect.md
docs/external-frameworks/oauth2.md
docs/external-frameworks/w3c-did.md
docs/external-frameworks/openlineage.md
docs/external-frameworks/w3c-prov.md
docs/external-frameworks/guardrails-ai.md
docs/external-frameworks/llama-guard.md
docs/external-frameworks/nemo-guardrails.md
```

The NeuralTrust AI-governance guide and NHIMG OAuth FAQ remain secondary context. The OpenID AI-governance tag is official organizational context, while OpenID Connect Core is the canonical protocol source. The Wikipedia W3C PROV page is discovery-only and the W3C PROV Overview is canonical. Llama Guard remains explicitly bounded by distribution-source caution.

## Boundary

```text
source capture != validation
sourced_intake != compatibility
framework page != benchmark pass
mapped_partial != observed behavior
secondary commentary != canonical specification
distribution availability != model-behavior proof
editor draft != final recommendation
fixture != execution authority
```

## Parallel coordination

Concurrent Goal 5 evolution exists. This workstream owns candidate visibility, canonical-source capture, sourced-intake promotion records, and progressive framework-page/mapping/fixture creation. Do not overwrite newer CI repair, workflow receipt, deployment verification, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
8 second-wave benchmark applicability mappings
10 Tier 1 source-versioned fixture artifacts
fixture validator coverage for promoted IDs
compatibility reports only after actual observations exist
promotion-status validator enforcing source/page/mapping state
canonical Goal 5 aggregate-check integration for any new validator
```

## Next action

Create benchmark applicability mappings for the eight second-wave pages, then create non-authorizing source-versioned fixture definitions. Do not claim observed behavior until exact external outputs are captured.

## Release path

The repo is not ready to tag solely because source capture and page creation are complete. After mapping/fixture validation and evidence review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
