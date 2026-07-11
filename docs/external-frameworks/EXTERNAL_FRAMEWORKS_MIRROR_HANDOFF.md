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
Tier 1 source-intake packets: 10
Tier 1 canonical sources captured: 10
Tier 1 sourced_intake records: 10
Tier 1 framework pages: 10 of 10
Tier 1 benchmark mappings: 10 of 10
Tier 1 fixture observations: 0 of 10
```

## Newly installed

```text
docs/external-frameworks/promoted-intake-records.v0.1.json
docs/external-frameworks/tier1-source-promotion-status.md
docs/external-frameworks/open-policy-agent.md
docs/external-frameworks/cedar-policy.md
docs/external-frameworks/oscal.md
docs/external-frameworks/spiffe-spire.md
docs/external-frameworks/w3c-verifiable-credentials.md
docs/external-frameworks/in-toto.md
docs/external-frameworks/slsa.md
docs/external-frameworks/sigstore.md
docs/external-frameworks/model-context-protocol.md
docs/external-frameworks/agent2agent-protocol.md
docs/external-frameworks/benchmark-mappings/opa.mapping.json
docs/external-frameworks/benchmark-mappings/cedar-policy.mapping.json
docs/external-frameworks/benchmark-mappings/oscal.mapping.json
docs/external-frameworks/benchmark-mappings/spiffe-spire.mapping.json
docs/external-frameworks/benchmark-mappings/w3c-verifiable-credentials.mapping.json
docs/external-frameworks/benchmark-mappings/in-toto.mapping.json
docs/external-frameworks/benchmark-mappings/slsa.mapping.json
docs/external-frameworks/benchmark-mappings/sigstore.mapping.json
docs/external-frameworks/benchmark-mappings/mcp.mapping.json
docs/external-frameworks/benchmark-mappings/a2a.mapping.json
docs/external-frameworks/benchmark-mapping-rollout.json updated
```

## Tier 1 state

```text
Open Policy Agent: page complete; mapped_partial
Cedar Policy: page complete; mapped_partial
OSCAL: page complete; mapped_partial
SPIFFE/SPIRE: page complete; mapped_partial
W3C Verifiable Credentials: page complete; mapped_partial
in-toto: page complete; mapped_partial
SLSA: page complete; mapped_partial
Sigstore: page complete; mapped_partial
Model Context Protocol: page complete; mapped_partial
Agent2Agent Protocol: page complete; mapped_partial
```

Each mapping classifies execution, preparation, commitment, semantic equivalence, unknown trajectory, authority, freshness, reconstruction, and interoperability boundaries.

## Boundary

```text
source capture != validation
sourced_intake != compatibility
framework page != benchmark pass
mapped_partial != observed behavior
fixture != execution authority
protocol authorization != StegVerse standing
credential verification != current delegation
signature verification != transition admissibility
```

## Parallel coordination

Concurrent Goal 5 evolution exists. This workstream owns candidate visibility, Tier 1 canonical-source capture, sourced-intake promotion records, and progressive framework-page/mapping/fixture creation. Do not overwrite newer CI repair, workflow receipt, deployment verification, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
10 Tier 1 source-versioned fixture artifacts
fixture validator coverage for all Tier 1 IDs
compatibility reports only after actual observations exist
promotion-status validator enforcing 10/10 source records, pages, and mappings
canonical Goal 5 aggregate-check integration for any new validator
```

## Next action

Create non-authorizing source-versioned fixture artifacts for the ten Tier 1 mappings. Fixtures must remain expected-posture test definitions until exact external outputs are captured.

## Release path

The repo is not ready to tag solely because Tier 1 source capture, pages, and mappings are complete. After fixture validation and evidence review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
