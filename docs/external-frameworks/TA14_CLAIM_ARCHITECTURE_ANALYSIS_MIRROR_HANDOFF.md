# TA-14 Claim-versus-Architecture Analysis Mirror Handoff

Repository: `StegVerse-Labs/admissibility-wiki`
Parent repository authority: `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`
Public analysis page: `docs/external-frameworks/ta-14-claim-architecture-analysis.md`
Machine-readable analysis record: `static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json`
Source/revision ledger: `static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json`
Validator: `scripts/check_ta14_claim_architecture_analysis.py`
Canonical validation binding: `npm run validate:ta14-claim-architecture-analysis` and `npm run validate`
Navigation binding: `sidebars.js`

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

## Installed files

```text
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/TA14_CLAIM_ARCHITECTURE_ANALYSIS_MIRROR_HANDOFF.md
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/ta-14-claim-architecture-analysis.md
StegVerse-Labs/admissibility-wiki/static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json
StegVerse-Labs/admissibility-wiki/static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json
StegVerse-Labs/admissibility-wiki/scripts/check_ta14_claim_architecture_analysis.py
StegVerse-Labs/admissibility-wiki/sidebars.js
StegVerse-Labs/admissibility-wiki/package.json
```

## Source custody posture

The supplied 2026-09-04 public Google Sites page is recorded in the source ledger as an owner-controlled public source observation. Exact external source bytes were not captured into canonical custody in this lane, so the ledger explicitly records:

```text
exact_byte_snapshot: NOT_CAPTURED
content_hash: null
hash_state: NOT_AVAILABLE_WITHOUT_EXACT_BYTE_SNAPSHOT
```

This prevents an observation record from being misrepresented as immutable source custody.

## Validation contract

The validator requires:

- all initial machine claim records and allowed status vocabulary;
- an explicit discriminating test for every `PUBLICLY_UNRESOLVED` claim;
- parentage to remain a positive-evidence question;
- StegVerse comparison to remain secondary to TA-14-internal analysis;
- required public-page sections and machine-record linkage;
- sidebar discoverability;
- source-ledger presence and explicit exact-byte/hash posture;
- this handoff to report validator, ledger, and navigation installation.

The validator is bound into the repository's canonical `npm run validate` chain. A repository write is not itself evidence that the canonical workflow has executed successfully; workflow observation remains separate.

## Completion predicate for v1

Repository-local v1 installation is complete when:

- the initial claim families are represented;
- conclusions remain source-bounded;
- public page and machine-readable record share the same analytical posture;
- parentage is treated as an affirmative claim requiring evidence rather than assumed true or false;
- authority/standing is analyzed as TA-14 models it, with StegVerse ontology differences labeled separately;
- discriminating tests exist for materially unresolved claims;
- correction and revision semantics are explicit;
- validator is installed and canonical-validation-bound;
- source/revision ledger is installed;
- navigation binding is installed.

## Remaining installation destinations

```text
StegVerse-Labs/admissibility-wiki
- observe canonical workflow result for the installed validator/build
- optionally extend source ledger with exact-byte source snapshots only when a governed capture surface exists
- update canonical external-framework inventory artifacts if existing inventory validators require explicit support-page enumeration

StegVerse-Labs/Site
- public discovery/link projection only after Site orchestration admits the work

GCAT-BCAT-Engine/Publisher
- optional publication projection after canonical analysis record is stable and publication lane admits it

StegVerse-002/stegguardian-wiki
- later guardian-facing projection only if findings materially affect protection doctrine
```

## Current state

```text
lane_state: REPOSITORY_LOCAL_V1_INSTALLED_VALIDATION_OBSERVATION_PENDING
source_substrate: EXISTING
public_analysis_page: INSTALLED
machine_record: INSTALLED
validator: INSTALLED
validator_canonical_binding: INSTALLED
source_revision_ledger: INSTALLED
navigation_binding: INSTALLED
canonical_workflow_observation: PENDING
site_projection: NOT_REQUESTED_FROM_SITE_ORCHESTRATOR
publisher_projection: NOT_REQUESTED
stegguardian_projection: NOT_REQUIRED_BY_CURRENT_FINDINGS
user_action_required: false
execution_authority_effect: none
```
