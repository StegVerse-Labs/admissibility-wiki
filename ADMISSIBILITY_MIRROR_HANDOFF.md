# Admissibility Wiki Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/admissibility-wiki`.

## Current Priority

The current active task is Formalism Discovery Engine activation inside `StegVerse-Labs/admissibility-wiki`.

The discovery layer now indexes canonical formalism terms, generates review-required candidate relationships, preserves source origins, and validates that generated discovery outputs do not drift silently.

## Current Discovery Install

Destination: `StegVerse-Labs/admissibility-wiki`

Installed docs:

- `docs/discovery/index.md`
- `docs/discovery/discovery-engine.md`
- `docs/discovery/relationship-types.md`
- `docs/discovery/review-queue.md`
- `docs/discovery/relationship-decision-validation.md`

Installed stores:

- `static/discovery/discovered-terms.json`
- `static/discovery/candidate-relationships.json`
- `static/discovery/relationship-decisions.json`

Installed scripts:

- `scripts/discovery/build-term-index.mjs`
- `scripts/discovery/build-relationship-candidates.mjs`
- `scripts/discovery/check-discovery-stores.mjs`

Installed npm paths:

- `npm run discovery:build`
- `npm run validate:discovery-stores`
- `npm run validate`

Visible entry points:

- `docs/index.md`
- `docs/discovery/index.md`
- `docs/formalisms/canonical-catalog.md`
- `docs/formalisms/formalism-graph-index.md`

## Source Artifacts

Publisher source: `GCAT-BCAT-Engine/Publisher`

- `PUBLISHER_MIRROR_HANDOFF.md`
- `data/stegtalk-local-candidate.json`
- `data/stegtalk-local-candidate-publisher-receipt.json`

Site source: `StegVerse-Labs/Site`

- `SITE_MIRROR_HANDOFF.md`
- `data/stegtalk-local-candidate.json`
- `data/stegtalk-local-candidate-receipt.json`

Origin source: `StegVerse-Labs/StegTalk`

- `STEGTALK_MIRROR_HANDOFF.md`
- `STEGTALK_CANDIDATE_STATUS.json`
- `STEGTALK_LOCAL_CANDIDATE.json`
- `STEGTALK_RELEASE_HANDOFF.json`

## Admissibility Install Complete

Destination: `StegVerse-Labs/admissibility-wiki`

- `pages/stegtalk-admissibility-boundary.md`
- `receipts/stegtalk-admissibility-boundary-receipt.json`

## Downstream Propagation Complete

Destination: `StegVerse-002/stegguardian-wiki`

- `STEGGUARDIAN_WIKI_MIRROR_HANDOFF.md`
- `pages/stegtalk-guardian-account-boundary.md`
- `receipts/stegtalk-boundary-receipt.json`

## Remaining Known Files Or Modules To Install

Destination: `StegVerse-Labs/admissibility-wiki`

- `sidebars.js` discovery navigation category remains desirable, but direct sidebar update was blocked during the current build pass.
- Release/tag candidate evaluation remains pending after validation confirms the discovery layer and site build.

Destination: `StegVerse-Labs/Site`

- No discovery-layer propagation target is currently confirmed by this handoff.

Destination: `GCAT-BCAT-Engine/Publisher`

- No discovery-layer propagation target is currently confirmed by this handoff.

Destination: `StegVerse-002/stegguardian-wiki`

- No discovery-layer propagation target is currently confirmed by this handoff.

## Build Rule

Before continuing any admissibility-wiki mirror task, check this file first and treat it as the current handoff and task source of truth.

## Boundary

StegTalk remains a non-production local prototype candidate. Do not describe it as production ready.

The Formalism Discovery Engine is a discovery and review-support layer. It does not define terms, assert synonymy, prove equivalence, replace source authority, or expose private source content.

## Next Integration Candidate

Validate the discovery layer through `npm run validate`. If validation and build pass and the repository reaches release standing, tag/release the admissibility-wiki state and create a follow-up verification task to confirm whether StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki need mirror updates.
