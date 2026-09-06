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

This is not a rebuttal lane and does not depend on continued dialogue with TA-14's author. Sources are preserved, claims are atomized, architecture evidence is mapped, confidence is bounded, and changes are tracked over time.

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

## Claim families

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
13. Privacy-preserving independent-verification claims.

The machine record currently contains 14 atomized claims across these families.

## Core question

For each public claim:

> What does TA-14 say the architecture guarantees, where does TA-14 place that guarantee in its own architecture, and what public architecture or observed behavior presently supports, limits, or contradicts that claim?

## Neutrality and comparison rules

- Analyze TA-14 against TA-14's own stated architecture before comparing it with StegVerse.
- Preserve TA-14 terminology when characterizing TA-14.
- Separate ontology disagreement from internal inconsistency.
- Do not require participation in the TA-14 Exchange for a public architectural claim to be reviewable.
- Do not infer hidden implementation from doctrine.
- Do not infer absence from unavailable implementation.
- Apply the same evidence burden to affirmative StegVerse comparative claims.
- Preserve corrections and superseded determinations rather than silently rewriting history.
- Secondary comparison does not require artificial neutrality after the TA-14-internal evidence mapping establishes a material architectural difference.
- On privacy-preserving independent verification, the current bounded finding is `DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL` between the reviewed TA-14 access model and the StegVerse design principle.
- That direct opposition is dimension-specific and MUST NOT be generalized into a claim that every aspect of TA-14 and StegVerse is opposite.

## Relationship to existing TA-14 evidence

This lane extends, but does not replace:

```text
docs/external-frameworks/ta-14.md
docs/external-frameworks/ta-14-public-review-docket.md
docs/external-frameworks/ta-14-stegverse-public-evidence-gap-review-v2-intake.md
docs/external-frameworks/ta-14-testing-support-determination-2026-08-01.md
docs/external-frameworks/ta-14-account-data-request-channel-observation-2026-08-01.md
static/data/framework-evaluations/ta-14.json
static/data/governed-framework-reviews/ta-14.reference-docket.v1.json
static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.adjudication.json
```

Existing determinations remain bounded to their recorded scope and observation dates.

## v1.2 privacy-preserving independent-verification finding

Revision v1.2 adds claim `TA14-CA-014` and strengthens `TA14-CA-012`.

The evidence-bound structure is:

```text
meaningful testing: account-gated
fuller verification: associated with owner-controlled commercial path
pre-disclosure privacy boundary: not sufficiently independently established
data minimization / retention / deletion / secondary use / owner access / analytics-profiling / non-reuse: unresolved before account-linked submission
later usable controller-contact / deletion route: not established during preserved observation
```

The bounded determination is:

```text
TA14-CA-014 status: CONTRADICTED_BY_PUBLIC_ARCHITECTURE
comparative dimension: privacy-preserving independent verification
StegVerse comparison: DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL
```

This finding does **not** claim unlawful retention, misuse, hidden motive, or universal TA-14 incapability. It concerns the observed verification-access architecture and whether a reviewer must surrender additional sensitive/account-linked information before being able to meaningfully inspect the stronger production-capable evidence surface.

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

The supplied 2026-09-04 public Google Sites page remains recorded in the source ledger as an owner-controlled public source observation. Exact external source bytes were not captured into canonical custody in this lane, so the ledger explicitly records:

```text
exact_byte_snapshot: NOT_CAPTURED
content_hash: null
hash_state: NOT_AVAILABLE_WITHOUT_EXACT_BYTE_SNAPSHOT
```

The v1.2 privacy-access finding additionally relies on already-preserved StegVerse observation records from 2026-08-01. Those records remain bounded observations and are not converted into claims about hidden motive or unlawful conduct.

## Validation contract

The validator now requires:

- exact claim IDs `TA14-CA-001` through `TA14-CA-014`;
- privacy-preserving independent-verification family presence;
- `TA14-CA-014` status to remain `CONTRADICTED_BY_PUBLIC_ARCHITECTURE` unless the analysis is deliberately revised with new evidence;
- a falsifiable privacy-preserving production-verification test;
- the comparative finding `DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL`;
- StegVerse comparison to remain secondary to TA-14-internal mapping but available after that mapping is explicit;
- all prior source, navigation, parentage, status-vocabulary, and authority-effect guards.

The validator remains bound into the repository's canonical `npm run validate` chain. A repository write is not itself evidence that the revised lane has executed successfully under canonical validation.

## Historical canonical validation evidence

The prior v1.1 installation was validated at commit `da2365baa6b6436f6bfc794968d29da64ea89a0a` by:

```text
workflow: Validate chain continuation
run_id: 33943582305
run_number: 4766
workflow_conclusion: SUCCESS
canonical_pre_scan: 11/11 PASS
full_validation_chain: 56/56 PASS
canonical_workflow_observation: PASS_OBSERVED
source_route_contract: 36/36 PASS
built_route_verification: 36/36 PASS
authority_effect: none
```

That historical evidence remains valid for the v1.1 state only. It MUST NOT be used as validation proof for the v1.2 revision.

## README impact determination — v1.2

The v1.2 revision changes analytical content and adds a new claim family while preserving the existing evidence-status vocabulary and repository behavior.

```text
README_update_required: false
determination: bounded review-content and machine-record revision
repository_behavior_change: none
runtime_semantics_change: none
interface_change: none
governance_or_authority_boundary_change: none
status_vocabulary_change: none
prerequisite_or_dependency_change: none
failure_behavior_change: none
capability_meaning_change: none
```

The public review's conclusion changed because preserved evidence was reclassified more precisely; the repository's evidence semantics did not change. Therefore no README mutation is required for this revision.

## Completion predicate for v1.2

Repository-local v1.2 installation is complete when:

- the 14 machine claim records are represented;
- `TA14-CA-014` is present with the bounded privacy-preserving verification contradiction finding;
- the public page and machine record express the same comparative posture;
- the independent/reciprocal review claim no longer treats owner-controlled participation as equivalent to independently accessible production verification;
- the privacy-preserving production-verification discriminating test is published;
- validator enforces the new claim family and comparative posture;
- a canonical workflow observation exists for the v1.2 head.

All repository-local source mutations for v1.2 are installed. Canonical workflow observation for the revised head remains pending until GitHub Actions produces it.

## Remaining installation destinations

```text
StegVerse-Labs/admissibility-wiki
- observe canonical workflow result for v1.2
- maintain page / machine-record / source-ledger parity as new TA-14 evidence appears
- optionally extend source custody with exact-byte snapshots only when a governed capture surface exists

StegVerse-Labs/Site
- public discovery/link projection only after Site orchestration admits the work

GCAT-BCAT-Engine/Publisher
- optional publication projection only after its publication lane admits the work

StegVerse-002/stegguardian-wiki
- later guardian-facing projection only if findings materially affect protection doctrine
```

## Current state

```text
lane_state: REPOSITORY_LOCAL_V1_2_INSTALLED_VALIDATION_OBSERVATION_PENDING
source_substrate: EXISTING
public_analysis_page: UPDATED_V1_2
machine_record: UPDATED_V1_2_14_CLAIMS
validator: UPDATED_V1_2
validator_canonical_binding: INSTALLED
source_revision_ledger: INSTALLED
navigation_binding: INSTALLED
historical_canonical_workflow_observation: PASS_OBSERVED_RUN_33943582305_FOR_V1_1
v1_2_canonical_workflow_observation: PENDING
privacy_preserving_verification_finding: CONTRADICTED_BY_PUBLIC_ARCHITECTURE
stegverse_privacy_verification_comparison: DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL
site_projection: NOT_ADMITTED_BY_SITE_ORCHESTRATOR
publisher_projection: NOT_ADMITTED_BY_CURRENT_PUBLISHER_WORKSTREAM
stegguardian_projection: NOT_REQUIRED_BY_CURRENT_FINDINGS
user_action_required: false
execution_authority_effect: none
```
