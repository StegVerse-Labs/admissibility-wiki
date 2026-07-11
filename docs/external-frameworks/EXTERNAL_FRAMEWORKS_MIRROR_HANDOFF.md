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
benchmark mappings for promoted candidates: 18 of 18
fixture observations for promoted candidates: 0
```

## Promotion waves

Tier 1 and second-wave promoted frameworks now each have canonical-source capture, an individual observatory page, and a `mapped_partial` benchmark applicability mapping.

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

The second-wave mappings classify all nine required benchmark dimensions: execution, preparation, commitment, semantic equivalence, unknown trajectory, authority, evidence freshness, reconstruction, and interoperability.

## Source classification posture

```text
canonical/official sources -> promotion evidence
secondary commentary -> context only
editor draft -> sourced with draft caution
distribution page -> sourced with distribution caution
Wikipedia -> discovery only; replaced by official W3C source
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
18 promoted-framework source-versioned fixture definitions
fixture validator coverage for all 18 promoted IDs
compatibility reports only after actual observations exist
promotion-status validator enforcing source/page/mapping state
canonical Goal 5 aggregate-check integration for any new validator
```

## Next action

Create non-authorizing source-versioned fixture definitions for the 18 promoted mappings. Fixtures remain expected-posture test definitions until exact external outputs are captured. Preserve exact source/model/version caution where required.

## Release path

The repo is not ready to tag solely because source capture, page creation, and mapping are complete. After fixture validation and evidence review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
