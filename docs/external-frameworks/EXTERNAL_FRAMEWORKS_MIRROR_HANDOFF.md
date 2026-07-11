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
Tier 1 benchmark mappings: 0 of 10
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
docs/external-frameworks/EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md
sidebars.js -> Tier 1 source promotion status visible
```

## Tier 1 sourced intake and page state

```text
Open Policy Agent: page complete
Cedar Policy: page complete
OSCAL: page complete
SPIFFE/SPIRE: page complete
W3C Verifiable Credentials: page complete
in-toto: page complete
SLSA: page complete
Sigstore: page complete
Model Context Protocol: page complete
Agent2Agent Protocol: page complete
```

Each source record includes canonical source, source version/date posture, published scope, published non-claim, artifact type, relationship class, benchmark relevance, authority boundary, evidence posture, promotion state, and next action.

## Boundary

```text
source capture != validation
sourced_intake != compatibility
framework page != benchmark pass
mapping != observed behavior
fixture != execution authority
protocol authorization != StegVerse standing
credential verification != current delegation
signature verification != transition admissibility
```

## Parallel coordination

Concurrent Goal 5 evolution exists. This workstream owns candidate visibility, Tier 1 canonical-source capture, sourced-intake promotion records, and progressive framework-page/mapping creation. Do not overwrite newer CI repair, workflow receipt, deployment verification, or documentation-mesh state from other workstreams.

## Remaining files/modules to install

Destination: `StegVerse-Labs/admissibility-wiki`

```text
10 Tier 1 benchmark applicability mappings
source-versioned fixtures where canonical examples are available
compatibility reports only after observations exist
promotion-status validator enforcing 10/10 source records and 10/10 pages
canonical Goal 5 aggregate-check integration for that validator
```

## Next action

Create the ten Tier 1 benchmark applicability mappings from the captured source records and pages. Do not claim observed behavior until exact fixtures or captured outputs are attached.

## Release path

The repo is not ready to tag solely because Tier 1 source capture and page creation are complete. After mapping validation and evidence review, verify pertinent updates for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/stegguardian-wiki`.

The complete prior thread is not required to continue from this handoff.
