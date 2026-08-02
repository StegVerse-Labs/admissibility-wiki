---
title: TA-14 Observation and Completion Plan
sidebar_label: TA-14 Observation Plan
---

# TA-14 Observation and Completion Plan

## Determination

The reciprocal review and remediation layer is **being built** in `StegVerse-Labs/admissibility-wiki` on branch `feature/ta14-public-evidence-review` through PR #52.

It is not yet activatable because the source PDF is not committed, navigation and validators are not installed, and public-route verification has not occurred.

## No-external-task rule

There are no external tasks in this program. A control, fact, authority statement, runtime behavior, or outcome that originates outside StegVerse is represented internally as an **observable requirement**, not as a task assigned to an external party.

StegVerse does not claim ownership of the external control. StegVerse does own the work required to:

1. define what must be observed;
2. define acceptable evidence;
3. provide an intake route;
4. generate synthetic and negative fixtures;
5. record absence, refusal, or unverifiability;
6. keep unrelated development moving;
7. re-evaluate automatically when evidence appears.

## Task-state rule

No task may remain in a generic `BLOCKED` state solely because evidence is external.

Use one of these states:

- `BUILD_INTERNAL`: StegVerse implementation work can proceed now.
- `OBSERVE`: an observer, intake contract, or probe must be built or run.
- `EVIDENCE_ABSENT_FAIL_CLOSED`: required evidence is absent; the associated claim remains unavailable, but unrelated work continues.
- `SIMULATED_ONLY`: synthetic fixtures exist, but no external fact is claimed.
- `VERIFIED_BOUNDED`: sufficient bounded evidence has been preserved for the exact claim.
- `DISPUTED_REVIEWER_BURDEN`: the reviewer has not supplied enough evidence for its allegation.
- `COMPLETE`: the task's repository-owned exit criterion is satisfied.

`EVIDENCE_ABSENT_FAIL_CLOSED` is not a development halt. It blocks only the specific claim that requires the missing evidence.

## Completion architecture

Each TA-14 issue is decomposed into four repository-owned units:

```text
requirement specification
-> observer or evidence-intake implementation
-> fixture and validator implementation
-> bounded status publication
```

The observer may conclude that evidence is absent or that the relevant control is not StegVerse-owned. That is still a completed observation cycle.

## Canonical task locations

| Task | Repository location | Purpose |
|---|---|---|
| Issue and ownership matrix | `docs/reviews/ta14-remediation-task-list.md` | Human-readable G-01 through G-18 coordination source. |
| Machine-readable observation registry | `static/reviews/ta14/task-observation-registry.v0.1.json` | Exact task paths, states, evidence requirements, observers, and claim effects. |
| Registry validator | `scripts/check_ta14_task_observation_registry.py` | Prevents missing paths, unbounded blockers, and silent ownership transfer. |
| Reciprocal analysis | `docs/reviews/ta14-public-evidence-gap-review-v2-analysis.md` | Public interpretation and bounded findings. |
| Track handoff | `docs/reviews/TA14_PUBLIC_EVIDENCE_REVIEW_MIRROR_HANDOFF.md` | Current task authority and continuation state. |
| Claim inventory | `static/reviews/ta14/claim-inventory.v0.1.json` | Exact public claims and proof posture. |
| Architecture manifest | `static/reviews/ta14/canonical-architecture-manifest.v0.1.json` | Owned components and external observation boundaries. |
| Source PDF target | `static/evidence/ta14/TA-14-StegVerse-Public-Evidence-Gap-Review-v2.0.pdf` | Exact source artifact; currently pending binary installation. |

## Immediate coordinated tasks

### TA14-OBS-001 — Install task-observation registry

Location: `static/reviews/ta14/task-observation-registry.v0.1.json`

Exit: every T14-001 through T14-018 entry names its task file, implementation path, observer path, evidence state, claim effect, and next executable repository action.

### TA14-OBS-002 — Install fail-closed registry validator

Location: `scripts/check_ta14_task_observation_registry.py`

Exit: validator rejects tasks with missing locations, generic external blockers, absent next actions, or claims upgraded from simulated/absent evidence.

### TA14-OBS-003 — Build evidence intake contracts

Locations:

- `static/reviews/ta14/evidence-contracts/authority-evidence.schema.json`
- `static/reviews/ta14/evidence-contracts/receipt-trust-evidence.schema.json`
- `static/reviews/ta14/evidence-contracts/execution-boundary-evidence.schema.json`
- `static/reviews/ta14/evidence-contracts/outcome-evidence.schema.json`
- `static/reviews/ta14/evidence-contracts/neutral-review-evidence.schema.json`

Exit: externally originating evidence has a repository-owned intake and validation surface.

### TA14-OBS-004 — Build synthetic and negative observation fixtures

Locations:

- `static/reviews/ta14/fixtures/`
- `scripts/check_ta14_observation_fixtures.py`

Exit: absent evidence, stale authority, revoked signer, bypass attempt, object substitution, outage, refusal, and outcome mismatch can be tested without waiting for a third party.

### TA14-OBS-005 — Bind observation validation into the canonical workflow

Locations:

- `.github/workflows/validate-chain-continuation.yml`
- `scripts/check_governed_llm_pages.py`

Exit: the existing single canonical workflow validates the registry, evidence contracts, fixtures, source digest, analysis posture, and task coverage.

### TA14-OBS-006 — Publish bounded status without halting unrelated work

Locations:

- `static/status/ta14-remediation-status.json`
- `docs/reviews/ta14-remediation-task-list.md`

Exit: status distinguishes `VERIFIED_BOUNDED`, `EVIDENCE_ABSENT_FAIL_CLOSED`, `SIMULATED_ONLY`, and `DISPUTED_REVIEWER_BURDEN`; no repository-wide blocked state is emitted solely because evidence is absent.

## Activation condition

This layer may activate when:

- the exact PDF is committed and digest-verified;
- public analysis and task pages are navigable;
- the registry and validators pass;
- every issue has a named repository path and executable next action;
- absent external evidence affects only its bounded claim;
- the canonical workflow passes;
- the Pages deployment and public routes are observed.
