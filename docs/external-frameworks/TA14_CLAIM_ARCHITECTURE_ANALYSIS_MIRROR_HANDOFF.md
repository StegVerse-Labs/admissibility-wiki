# TA-14 Claim-versus-Architecture Analysis Mirror Handoff

Repository: `StegVerse-Labs/admissibility-wiki`
Parent repository authority: `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`
Public analysis page: `docs/external-frameworks/ta-14-claim-architecture-analysis.md`
Machine-readable analysis record: `static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json`
Source/revision ledger: `static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json`
Validator: `scripts/check_ta14_claim_architecture_analysis.py`
Presentation semantics: `src/css/custom.css`
Canonical validation binding: `npm run validate:ta14-claim-architecture-analysis` and `npm run validate`
Navigation binding: `sidebars.js`

## Goal

Maintain a public, versioned analysis lane that evaluates TA-14's public claims against TA-14's publicly exposed architecture, mechanisms, artifacts, observed behavior, and production-verification evidence.

This is not a rebuttal lane. Sources, observations, analytical status, and production verification remain distinct.

## Analytical status vocabulary

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

`NOT_YET_FOUND` MUST NOT become nonexistence. Public doctrine MUST NOT become implementation proof. Architecture disagreement MUST NOT become implementation failure.

## Production-verification display contract — v1.3

Production verification is a separate binary display predicate for every atomized claim:

```text
GREEN = production_surface_evaluated == true
        AND exists_as_publicly_claimed == true

RED   = NOT GREEN
```

Semantics:

```text
green row = production claim evaluated and observed to exist as publicly claimed
red row = production-verification predicate is not satisfied
red row != automatic nonexistence
red row may mean NOT_EVALUATED, UNRESOLVED, or EVALUATED_AND_CONTRADICTED
```

The public table MUST expose a `Production version verified` column and preserve the reason for each row's state in text. Color is supplementary; it MUST NOT replace the written evidence boundary.

Current machine state:

```text
claims_total: 14
green_rows: 0
red_rows: 14
production_claims_verified_as_publicly_claimed: 0/14
```

Claim `TA14-CA-014` is a materially different red state from the other unresolved/unverified rows:

```text
production_surface_evaluated: true
exists_as_publicly_claimed: false
row_status: RED
display_status: EVALUATED — CONTRADICTED
```

For the remaining claims, production existence is not inferred false merely because production verification is not established; unresolved existence is represented as `null` where appropriate.

## Claim families

1. Parent-architecture / full-route ownership.
2. Eight-stage consequence-bearing route.
3. Authority, standing, consent, jurisdiction, delegation, revocation.
4. Binding and commit semantics.
5. Fail-closed execution boundary.
6. Continuity and chain of custody.
7. Outcome correspondence and post-execution verification.
8. Replay, reconstruction, auditability.
9. Cross-domain applicability.
10. Non-bypassability and complete mediation.
11. Reciprocal evaluation / independent review.
12. Registry, provenance, versioned governance records.
13. Privacy-preserving independent verification.

The machine record contains 14 atomized claims across these families.

## Privacy-preserving independent-verification finding

The preserved evidence-bound structure remains:

```text
meaningful testing: account-gated
fuller verification: associated with owner-controlled commercial path
pre-disclosure privacy boundary: not sufficiently independently established
data minimization / retention / deletion / secondary use / owner access / analytics-profiling / non-reuse: unresolved before account-linked submission
later usable controller-contact / deletion route: not established during preserved observation
```

Bounded determination:

```text
TA14-CA-014 status: CONTRADICTED_BY_PUBLIC_ARCHITECTURE
comparative dimension: privacy-preserving independent verification
StegVerse comparison: DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL
```

This finding does not claim unlawful retention, misuse, hidden motive, or universal TA-14 incapability.

## Neutrality and comparison rules

- Analyze TA-14 against TA-14 first.
- Preserve TA-14 terminology when characterizing TA-14.
- Do not require TA-14 Exchange participation for public architectural claims to be reviewable.
- Do not infer hidden implementation from doctrine.
- Do not infer absence from unavailable implementation.
- Apply the same evidence burden to affirmative StegVerse implementation/runtime claims.
- Secondary comparison does not require artificial leniency once TA-14-internal evidence establishes a material difference.
- The privacy-preserving verification opposition is dimension-specific, not a global claim that all aspects of TA-14 and StegVerse are opposite.

## Existing TA-14 evidence reused

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

## Source custody posture

The supplied 2026-09-04 TA-14 Google Sites page remains a public-source observation, not immutable exact-byte custody:

```text
exact_byte_snapshot: NOT_CAPTURED
content_hash: null
hash_state: NOT_AVAILABLE_WITHOUT_EXACT_BYTE_SNAPSHOT
```

No source hash may be inferred without exact-byte capture.

## Installed v1.3 files

```text
docs/external-frameworks/TA14_CLAIM_ARCHITECTURE_ANALYSIS_MIRROR_HANDOFF.md
docs/external-frameworks/ta-14-claim-architecture-analysis.md
static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json
static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json
scripts/check_ta14_claim_architecture_analysis.py
src/css/custom.css
sidebars.js
package.json
```

## Validation contract — v1.3

The validator requires:

- exact claim IDs `TA14-CA-001` through `TA14-CA-014`;
- the established claim-family set;
- `production_verification` on every claim;
- boolean `production_surface_evaluated`;
- `exists_as_publicly_claimed` as `true`, `false`, or `null`;
- `GREEN` only when both evaluation and correspondence are true;
- `RED` otherwise;
- a textual display status and reason for every production row;
- public red/green row-marker counts to match the machine record;
- a public `Production version verified` column;
- CSS bindings for production green/red presentation;
- red-row semantics not to be converted into automatic nonexistence;
- the existing privacy-verification contradiction and comparative-opposition guards;
- all prior source, navigation, parentage, status-vocabulary, and authority-effect guards.

The validator remains bound into canonical `npm run validate`.

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

That historical evidence MUST NOT be projected onto v1.2 or v1.3.

## README impact determination — v1.3

The v1.3 change adds claim-specific production-verification presentation semantics to the TA-14 review and machine record. The repository README describes the wiki's general purpose and governance/proof boundaries but does not define this review table's row-color or production-verification semantics.

```text
README_update_required: false
determination: localized review presentation + machine-state refinement
repository_behavior_change: none
runtime_semantics_change: none
repository_interface_contract_change: none
public_review_presentation_change: yes
governance_or_authority_boundary_change: none
status_vocabulary_change: none
prerequisite_or_dependency_change: none
failure_behavior_change: none
capability_meaning_change: none
```

Updating README would not improve completeness for this localized review surface, so no README mutation is required.

## Completion predicate for v1.3

Repository-local v1.3 installation is complete when:

- all 14 claims carry production-verification state;
- page and machine record have matching green/red counts;
- the public table exposes production verification for every claim;
- visual row coloring reflects the current machine predicate;
- red/nonexistence distinction is explicit;
- privacy-verification contradiction remains bounded and explicit;
- validator enforces all of the above;
- canonical workflow observation exists for the v1.3 head.

All source mutations are installed. Canonical workflow observation for the v1.3 head remains pending until GitHub Actions produces it.

## Remaining destinations

```text
StegVerse-Labs/admissibility-wiki
- observe canonical workflow result for v1.3
- turn rows green only when production evidence satisfies both predicate terms
- maintain source/page/machine-record parity as evidence changes

StegVerse-Labs/Site
- discovery/link projection only after Site orchestration admits it

GCAT-BCAT-Engine/Publisher
- optional publication projection only after Publisher admits it

StegVerse-002/stegguardian-wiki
- only if findings materially affect protection doctrine
```

## Current state

```text
lane_state: REPOSITORY_LOCAL_V1_3_INSTALLED_VALIDATION_OBSERVATION_PENDING
source_substrate: EXISTING
public_analysis_page: UPDATED_V1_3_PRODUCTION_MATRIX
machine_record: UPDATED_V1_3_14_CLAIMS_WITH_PRODUCTION_STATUS
validator: UPDATED_V1_3_PRODUCTION_COLOR_CONTRACT
presentation_css: UPDATED_V1_3
validator_canonical_binding: INSTALLED
source_revision_ledger: INSTALLED
navigation_binding: INSTALLED
historical_canonical_workflow_observation: PASS_OBSERVED_RUN_33943582305_FOR_V1_1
v1_3_canonical_workflow_observation: PENDING
production_verified_green_rows: 0
production_not_verified_red_rows: 14
privacy_preserving_verification_finding: CONTRADICTED_BY_PUBLIC_ARCHITECTURE
stegverse_privacy_verification_comparison: DIRECT_ARCHITECTURAL_OPPOSITION_ON_OBSERVED_ACCESS_MODEL
site_projection: NOT_ADMITTED_BY_SITE_ORCHESTRATOR
publisher_projection: NOT_ADMITTED_BY_CURRENT_PUBLISHER_WORKSTREAM
stegguardian_projection: NOT_REQUIRED_BY_CURRENT_FINDINGS
user_action_required: false
execution_authority_effect: none
```
