# External Health Guidance Public Mirror Handoff

Updated: 2026-08-27
Repository: `StegVerse-Labs/admissibility-wiki`
Canonical issue: `#109`
Goal ID: `PUBLIC-HEALTH-GUIDANCE-QUALITY-001`
State: `IMPLEMENTED_AWAITING_HOSTED_VALIDATION_AND_PUBLIC_ROUTE_PROOF`

## Goal

Publish a bounded, non-PHI research projection of external patient-education quality findings originating from `StegVerse-Labs/StegHealth#27`.

Initial source family:
- CVS Caremark / CVS Weight Management educational guides associated with health-and-wellness / GLP-1 participation.

## Collision boundary

This workload is independent from:
- issue #50 canonical validation;
- issue #66 External Framework evaluations;
- Riverbraid;
- MindForge provenance;
- Generated StegPay.

It creates no admissibility, certification, clinical, regulatory, execution, custody, or release authority.

## Public posture

This is recommendation-oriented quality-improvement research, not a complaint or allegation.

Public records may include:
- source/program name;
- reviewed statement;
- authoritative comparator;
- evidence classification;
- explanation;
- recommendation;
- review date;
- correction/version response history.

Public records must exclude:
- participant identity;
- member/account identifiers;
- prescription details;
- private medical history;
- PHI;
- individualized clinical conclusions.

## Evidence classifications

- `CONFIRMED_CURRENT`
- `CONFIRMED_DISCREPANCY`
- `OUTDATED_REFERENCE`
- `OVERSIMPLIFIED`
- `AMBIGUOUS`
- `PROGRAM_SPECIFIC_CONVENTION`
- `REQUIRES_MORE_EVIDENCE`
- `CORRECTED_BY_SOURCE`

## Machine surfaces

Implemented:
- `data/health-guidance/external-health-guidance-quality.v1.json` — structured non-PHI comparison record;
- `docs/health-guidance/external-health-guidance-quality.md` — public research page;
- `scripts/check_public_health_guidance_quality.py` — consistency, classification, privacy, and authority-boundary validator;
- `package.json` prebuild binding runs the health-guidance validator before every `npm run build`; the canonical workflow remains byte-identical to `main` and the canonical 56-check semantic denominator is unchanged.

Current structured record:
- findings: 9;
- authoritative sources: 6;
- correction history: empty / awaiting future source response;
- participant identifying information: explicitly false;
- clinical/regulatory/certification/complaint authority: explicitly false.

## Upstream source of truth

The private/source implementation authority remains:
- `StegVerse-Labs/StegHealth/docs/research/external-health-guidance/EXTERNAL_HEALTH_GUIDANCE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegHealth#27`

The public repo must not reinterpret a candidate finding as confirmed unless the upstream evidence state supports that classification.

## Release boundary

Publication of this research page means only that the bounded research record is publicly rendered.

It does not mean:
- clinical recommendation for an individual;
- proof of harm;
- regulatory violation;
- certification;
- endorsement;
- complaint disposition.

## Current next actions

1. obtain hosted exact-PR-head canonical 56/56 PASS plus `npm run build` evidence showing the health-guidance prebuild validator PASS;
2. merge only if canonical workflow remains PASS;
3. obtain post-merge public route/content proof;
4. preserve future source correction responses as successor records.

## Archive posture

Issue #109 and this handoff are the canonical continuation surfaces for this public research lane. The originating chat is not required after the structured comparison and publication surfaces are durable.


## Canonical-workflow mutation lesson

An initial implementation called the health-guidance validator directly from the canonical workflow. Hosted run `33135704946` proved the bounded health validator itself PASS but correctly failed five canonical validators because changing canonical workflow bytes invalidated workflow-manifest, Pages-receipt, iOS-mirror, Goal-5 publication-proof, and sandbox-derived contracts. That workflow change was reverted.

Current design:
```text
canonical workflow bytes: RESTORED TO MAIN
canonical 56-check denominator: UNCHANGED
health validator enforcement: package.json prebuild
site build path: npm run build -> prebuild validator -> docusaurus build
publication authority effect: false
```

The failed run is preserved as useful fail-closed evidence; it must not be promoted to success.


## Current validation blocker — concurrent main churn

```text
current PR: #111
supersedes shell PR: #110
branch: public/health-guidance-quality
branch head before this handoff reconciliation: 15998767e314168522e0b4b17d8b1231b1bf620a
canonical workflow bytes: RESTORED TO MAIN
health validation integration: package.json prebuild
structured findings: 9
authoritative sources: 6
privacy/authority validator: IMPLEMENTED
navigation binding: IMPLEMENTED
merge: BLOCKED / NOT FORCED
public route proof: PENDING
```

The repository is concurrently advancing on unrelated active `main` workloads. During the final observation window, canonical push runs were repeatedly superseding/canceling each other and PR #111 had not received a valid exact-current-base canonical Actions run. The health branch therefore remains intentionally unmerged. A stale predecessor run must not be transferred to the corrected branch.

Required continuation:
1. wait for the repository canonical lane to stabilize on the current live `main`;
2. obtain an exact-current-base PR #111 canonical run;
3. require the unchanged 56-check canonical chain to PASS;
4. require `npm run build` to execute the health-guidance `prebuild` validator and Docusaurus build successfully;
5. merge only then;
6. require post-merge build/deploy/public-route proof for `/health-guidance/external-health-guidance-quality`;
7. reconcile issue #109, this handoff, orchestration, and root handoff.

This is an execution-order/concurrency blocker, not missing health-guidance source implementation and not authorization to mutate unrelated OPA/Cedar/External Framework lanes.
