# TA-14 Claim-versus-Architecture Analysis Mirror Handoff

Repository: `StegVerse-Labs/admissibility-wiki`
Parent repository authority: `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`
Public analysis page: `docs/external-frameworks/ta-14-claim-architecture-analysis.md`
Machine-readable analysis record: `static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json`

## Goal

Create and maintain a public, versioned analysis lane that evaluates TA-14's own published claims against the architecture, mechanisms, artifacts, and observed behavior TA-14 publicly exposes.

This is not a rebuttal lane and does not depend on continued dialogue with TA-14's author. It is an external-framework analysis surface analogous to other StegVerse public analysis lanes: sources are preserved, claims are atomized, architecture evidence is mapped, confidence is bounded, and changes are tracked over time.

## Analytical boundary

The lane MUST distinguish:

```text
CLAIM_OBSERVED
ARCHITECTURE_SUPPORT_OBSERVED
BEHAVIOR_OBSERVED
IMPLEMENTATION_EVIDENCE_OBSERVED
PARTIALLY_SUPPORTED
PUBLICLY_UNRESOLVED
CONTRADICTED_BY_PUBLIC_ARCHITECTURE
NOT_YET_FOUND
OUT_OF_SCOPE
```

It MUST NOT convert `NOT_YET_FOUND` into nonexistence, private implementation claims into public proof, publication into correctness, or architectural disagreement into implementation failure.

## Unit of analysis

Each claim record should preserve:

```text
claim_id
claim_text
source_url
source_date_or_observed_at
source_revision_or_snapshot
claim_class
claimed_architectural_location
public_architecture_evidence
public_behavior_evidence
implementation_artifacts
counterevidence
status
confidence
reasoning_summary
open_test
change_history
```

## Initial claim families

1. Parent-architecture / full-route ownership claims.
2. Eight-stage consequence-bearing route claims.
3. Authority, standing, consent, jurisdiction, delegation, and revocation claims.
4. Binding and commit semantics.
5. Fail-closed execution-boundary claims.
6. Continuity and chain-of-custody claims.
7. Outcome correspondence and post-execution verification claims.
8. Replay, reconstruction, and auditability claims.
9. Cross-domain applicability claims.
10. Non-bypassability and complete-mediation claims.
11. Reciprocal evaluation / independent review claims.
12. Registry, provenance, and versioned-governance-record claims.

## Core question

For each public claim:

> What does TA-14 say the architecture guarantees, where does TA-14 place that guarantee in its own architecture, and what public architecture or observed behavior presently supports, limits, or contradicts that claim?

## Neutrality rules

- Analyze TA-14 against TA-14's own stated architecture before comparing it with StegVerse.
- Preserve TA-14 terminology when characterizing TA-14.
- Separate ontology disagreement from internal inconsistency.
- Do not require participation in the TA-14 Exchange for a public architectural claim to be reviewable.
- Do not infer hidden implementation from doctrine.
- Do not infer absence from unavailable implementation.
- Apply the same evidence burden to affirmative StegVerse comparative claims.
- Preserve corrections and superseded determinations rather than silently rewriting history.

## Relationship to existing TA-14 work

This lane extends, but does not replace:

```text
docs/external-frameworks/ta-14.md
docs/external-frameworks/ta-14-public-review-docket.md
docs/external-frameworks/ta-14-stegverse-public-evidence-gap-review-v2-intake.md
static/data/framework-evaluations/ta-14.json
static/data/governed-framework-reviews/ta-14.reference-docket.v1.json
static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.adjudication.json
```

Existing determinations remain bounded to their recorded scope and observation dates.

## Public-page structure

The public analysis page exposes:

1. Current assessment summary.
2. Claim-to-architecture matrix.
3. Strongest publicly supported claims.
4. Claims that are doctrinally stated but not publicly implementation-backed.
5. Public architecture tensions or contradictions.
6. Open discriminating tests.
7. Method and correction semantics.
8. Machine-readable analysis linkage.
9. Comparative notes only after the TA-14-internal analysis is explicit.

## Completion predicate for v1

`v1` is complete when:

- the initial claim families are represented;
- each conclusion is source-bounded;
- the public page and machine-readable record agree;
- parentage is treated as an affirmative claim requiring evidence rather than assumed either true or false;
- authority/standing is analyzed as TA-14 models it, with StegVerse ontology differences labeled separately;
- at least one discriminating test is recorded for every `PUBLICLY_UNRESOLVED` material claim;
- correction and revision semantics are explicit;
- a validator checks page/record agreement;
- source/revision records are bound to the claim matrix.

## Installed files

```text
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/TA14_CLAIM_ARCHITECTURE_ANALYSIS_MIRROR_HANDOFF.md
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/ta-14-claim-architecture-analysis.md
StegVerse-Labs/admissibility-wiki/static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json
```

## Remaining installation destinations

```text
StegVerse-Labs/admissibility-wiki
- validator for page/record agreement
- source revision ledger / source snapshots for the 2026-09-04 TA-14 page and future revisions
- navigation/index binding so the analysis is discoverable from the external-framework review surface

StegVerse-Labs/Site
- public discovery/link projection only after Site orchestration admits the work

GCAT-BCAT-Engine/Publisher
- optional publication projection after canonical analysis record is stable

StegVerse-002/stegguardian-wiki
- later guardian-facing projection only if findings materially affect protection doctrine
```

## Current state

```text
lane_state: INITIALIZED_AND_SEEDED
source_substrate: EXISTING
public_analysis_page: INSTALLED
machine_record: INSTALLED
validator: PENDING_INSTALL
source_revision_ledger: PENDING_INSTALL
navigation_binding: PENDING_INSTALL
site_projection: NOT_REQUESTED_FROM_SITE_ORCHESTRATOR
user_action_required: false
execution_authority_effect: none
```
