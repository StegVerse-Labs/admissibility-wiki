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
upstream_canonical_execution: PENDING
proof_binding: INSTALLED
promotion_gate: FAIL_CLOSED
documentation_posture: PENDING_EXECUTABLE_VERIFICATION
authority_posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
downstream_mutation_authority: NONE
```

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