# Morrison Runtime Proof Promotion Handoff

## Current source of truth

This file is the goal-specific continuation source of truth for Morrison Runtime proof promotion in `StegVerse-Labs/admissibility-wiki`.

## Goal

Promote the Morrison Runtime commit-time scope package from pending executable comparison to verified bounded comparative evidence only after canonical proof execution and exact artifact equivalence are durable in `Data-Continuation/formalism-tests`.

## Upstream dependency

```text
repository: Data-Continuation/formalism-tests
goal handoff: MORRISON_RUNTIME_COMMIT_TIME_SCOPE_HANDOFF.md
canonical-run issue: Data-Continuation/formalism-tests#5
required upstream state: VERIFIED_CANONICAL_EXECUTION
```

## Installed wiki evidence surface

```text
docs/external-frameworks/evidence/morrison-runtime-commit-time-scope-clarification.v0.1.json
docs/external-frameworks/evidence/morrison-runtime-formalism-tests-binding.v0.1.json
docs/external-frameworks/evidence/morrison-runtime-promotion-gate.v0.1.json
docs/external-frameworks/evidence/morrison-runtime-orchestration-status.v0.1.json
docs/external-frameworks/morrison-runtime.md
docs/external-frameworks/morrison-runtime-boundary-observation.md
docs/external-frameworks/reports/morrison-runtime.compatibility.json
```

## Promotion owner

```text
issue: StegVerse-Labs/admissibility-wiki#39
title: Promote Morrison commit-time scope evidence after canonical proof run
state: open
```

## Current state

```text
upstream_canonical_execution: VERIFIED_CANONICAL_RUN
upstream_run_id: 33014956712
upstream_commit_sha: daca16578387c45cde616b82ba517d11314e1ef2
upstream_evidence_commit_sha: 42ac1a25cf4427290f0b239c8e069253c87f86ba
proof_binding: VERIFIED_AND_BOUND
promotion_gate: VERIFIED_BOUNDED_PROMOTION_ELIGIBLE
documentation_posture: VERIFIED_BOUNDED_COMPARATIVE_EVIDENCE_WIKI_PUBLIC_ROUTE_PENDING
authority_posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
downstream_mutation_authority: NONE
```

## 2026-08-26 canonical proof-contract key reconciliation

Exact hosted Goal-5 validation on run `33011831798` exposed a pending-state schema drift rather than missing upstream proof: the Morrison promotion-input template named the fourth artifact hash/equivalence fields `canonical_evidence_gate_sha256` / `canonical_evidence_gate`, while the current canonical promotion validator and public status use `canonical_gate_sha256` / `canonical_gate`.

Commit `a6636e6dafa34d006bf661b2afc1191d165eba92` reconciles only those field identities. Every proof-dependent value remains `PENDING` or `false`, upstream canonical execution remains pending, and no promotion eligibility or authority is created. The public-status artifact already used the canonical field names, so the template/status/validator contract is now structurally aligned pending successor hosted validation.

## 2026-08-26 canonical upstream proof consumed

The upstream dependency is now satisfied at the bounded comparative-evidence layer.

```text
Data-Continuation/formalism-tests issue #5: CLOSED COMPLETED
canonical execution run: 33014956712 SUCCESS
canonical execution commit: daca16578387c45cde616b82ba517d11314e1ef2
durable evidence commit: 42ac1a25cf4427290f0b239c8e069253c87f86ba
morrison_runtime_commit_time_scope_tests: PASS
verify_morrison_runtime_commit_time_scope_artifacts: PASS
check_morrison_runtime_canonical_evidence_gate: PASS
report_sha256: 47fe6f349b2a5f181c2653db8e874e7cd862287e69aa3ba80f762f4019079dd1
receipts_sha256: 0993a3c118de08ea9a4bdb1aac93cad3363893c1bf0b573edc057dc247d73ce2
verification_sha256: 7f067bf605d363850ead0acb6851ccc5d16aa3b90d07b96a35becf06f11fd3da
canonical_gate_sha256: e670e3487487db345fcd584526109cacad81d763b04415f6c1584b5da196eddf
all four equivalence predicates: true
authority posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
```

The wiki has consumed that proof into the canonical promotion input, public status, compatibility report, and Morrison page. The resulting state is **VERIFIED_BOUNDED_COMPARATIVE_EVIDENCE**, not certification, endorsement, production validation, execution authority, public-route verification, release, or downstream propagation approval.

Current next transition:

```text
WIKI_VALIDATED_AND_PUBLIC_ROUTE_VERIFIED
```

Only after that exact transition may issue #39 begin the bounded downstream propagation review against the then-current Site, Publisher, and Guardian handoffs.

## 2026-08-26 evidence-class separation repair

The verified repository-owned StegVerse commit-time comparison and the older Morrison demo observations are deliberately separate evidence classes.

```text
StegVerse-authored commit-time comparative package:
  VERIFIED_CANONICAL_RUN
  run: 33014956712
  deterministic cases: 7/7 PASS
  artifact equivalence: 4/4 true
  authority: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY

Morrison runtime/demo benchmark observations:
  evidence class: PARAMETERIZED_OBSERVATION
  raw audit payloads: incomplete
  timestamps: incomplete
  runtime configuration: incomplete
  source hashes: incomplete
  independent reproduction: not complete
```

A prior promotion edit changed the top-level compatibility `result` to a new value. The canonical report generator only preserves enriched Morrison observations when the established result remains `COMPATIBILITY_EVIDENCE_ONLY_PARAMETERIZED_BOUNDARY_CASE_PARTIAL`; consequently hosted regeneration dropped the enriched observations and Goal 5 failed.

Commit `68bc4a8ece579b77f45aa6d0f98f18a72451014f` restores the established report result while retaining the separate `canonical_commit_time_scope_evidence` block. This is not a demotion of the verified StegVerse comparison. It prevents that proof from being misrepresented as full reproducibility of Morrison Runtime itself.

Successor canonical validation is required before the Morrison Wiki/public-route gate is promoted.

## Promotion preconditions

All conditions must be true:

```text
- upstream issue #5 is completed with durable canonical execution evidence
- both declared tasks passed in a repository checkout or existing CI surface
- report and receipt outputs exactly match committed baselines
- artifact verification is PASS
- upstream proof commit and execution receipt are identified
- Morrison source clarification remains bounded to its documented provenance
- no framework verdict is treated as StegVerse execution authority
```

## Authorized promotion actions

After all preconditions are met:

```text
1. update docs/external-frameworks/reports/morrison-runtime.compatibility.json
2. bind canonical run identity, commit, task results, report hash, receipt hash, and verifier status
3. update Morrison documentation from pending executable verification to verified bounded comparative evidence
4. preserve the distinction between pre-execution re-evaluation and full fresh-state reconstruction
5. update docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md with exact evidence commits
6. run the single canonical validation workflow
7. retain public-route and publication-receipt evidence
8. review destination handoffs before any propagation
```

## Prohibited promotions

```text
verified comparative evidence != Morrison certification
verified comparative evidence != Resurrection Tech endorsement
runtime re-evaluation != full fresh-state reconstruction
framework ALLOW/BLOCK != StegVerse execution authority
wiki publication != commit-time admissibility
public route reachability != governance authority
queued downstream propagation != completed propagation
```

## Downstream review order

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
```

No destination may be mutated until its current handoff is read and grants the required scope.

## Fail-closed rule

Missing upstream execution evidence, artifact mismatch, incomplete provenance, failed canonical wiki validation, unreachable public routes, or authority-language drift keeps the promotion gate closed.

## Archive posture

This handoff preserves the upstream dependency, installed evidence, promotion conditions, authorized actions, prohibited claims, validation requirements, and downstream restrictions so continuation does not depend on prior chat context.