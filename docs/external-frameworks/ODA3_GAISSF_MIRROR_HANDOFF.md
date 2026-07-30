# ODA3 / GAISSF Mirror Handoff

This file is the current source of truth for the bounded ODA3 Institute / GAISSF comparison track in `StegVerse-Labs/admissibility-wiki`.

## Goal

Build a non-authorizing, evidence-bounded comparison between StegVerse commit-time admissibility and ODA3 Institute's GAISSF control-and-evidence methodology.

## Current State

```text
Track id: oda3-gaissf-commit-time-interoperability
State: INITIAL_BOUNDED_INTAKE_INSTALLED
External outreach: RECEIVED
Public-source review: PARTIAL
Canonical GAISSF control mapping: NOT_STARTED
Controlled proof of concept: NOT_RUN
Independent reconstruction: NOT_RUN
Endorsement: false
Certification: false
Execution authority: false
Authority inheritance: false
```

## Preserved Distinction

```text
identity verification != current standing
prior approval != commit-time authority
framework alignment != interoperability
interoperability != adoption
correspondence != endorsement
faculty pathway != appointment
public documentation != implementation evidence
control coverage != admissible execution
receipt generation != receipt correctness
```

## Bounded Comparison Path

```text
proposed action
-> actor identity
-> current standing
-> authority and delegation
-> consent conditions
-> policy applicability
-> commit-time admissibility decision
-> execution evidence
-> post-event reconstruction
```

The first comparison must determine which stages are explicitly represented by GAISSF controls, which are only inferable, and which require StegVerse-native transition machinery.

## Source Boundary

Permitted public sources:

- ODA3 Institute faculty and research-team page
- ODA3 public GAISSF documentation
- ODA3 public assurance, evidence, conformance, schema, crosswalk, and publication-limit documentation

Private correspondence may be preserved only as a dated outreach record. It must not be represented as GAISSF doctrine, institutional endorsement, appointment, partnership, or validation.

## Required Artifacts

```text
docs/external-frameworks/oda3-gaissf.md
static/data/framework-evaluations/oda3-gaissf.json
static/data/framework-evaluations/examples/oda3-gaissf.commit-time-crosswalk.pending.v1.json
scripts/check_oda3_gaissf_intake.py
static/status/oda3-gaissf-intake-status.json
```

## Next Build

1. Freeze exact public source locators and retrieval dates.
2. Identify canonical GAISSF controls relevant to authorization, delegation, revocation, evidence, safe state, distributed orchestration, and assurance.
3. Populate the pending transition crosswalk without inferring unsupported semantics.
4. Implement deterministic validation for prohibited claims and required boundary fields.
5. Bind the validator into the canonical aggregate validation path.
6. Run a synthetic transition through both representations.
7. Record AGREE, DISAGREE, or DEFER per transition stage.
8. Request external correction only after the StegVerse-authored mapping is public and source-bounded.

## Known Remaining Files and Destinations

```text
StegVerse-Labs/admissibility-wiki:
- canonical GAISSF source-location registry
- control-level commit-time crosswalk
- deterministic validator and status receipt
- synthetic transition fixture and result
- external correction record
- independent reconstruction receipt

StegVerse-Labs/Site:
- public comparison route, pending docs/SITE_MIRROR_HANDOFF.md authority

GCAT-BCAT-Engine/Publisher:
- canonical comparison packaging and publication receipt, pending PUBLISHER_MIRROR_HANDOFF.md authority

StegVerse-Labs/stegguardian-wiki:
- reviewer standing, conflict, correction, dissent, and appeal projection, pending destination handoff authority
```

## Handoff Instruction

Continue from this file before relying on prior chat context. Preserve the comparison as StegVerse-authored analysis until ODA3 supplies an attributable correction, canonical source artifact, or explicit bounded acknowledgment.
