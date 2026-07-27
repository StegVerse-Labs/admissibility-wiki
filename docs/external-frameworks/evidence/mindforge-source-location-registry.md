# MindForge Source Location Registry

## Purpose

This registry aligns every MindForge-related source, derivative, validator, receipt, and public route used by `StegVerse-Labs/admissibility-wiki`.

It does not designate StegVerse as the canonical source for MindForge. It separates source provenance from StegVerse interpretation, deterministic evaluation, and public display.

## Authority classes

```text
External canonical MindForge source: NOT ATTACHED
Private correspondence: provenance evidence only
StegVerse doctrine: discussion-derived interpretation
StegVerse fixtures: deterministic conformance tests
StegVerse receipts/status: local evaluation records
Admissibility Wiki Pages: public vocabulary and proof-path display
Site / Publisher / StegGuardian: downstream mirrors only when separately authorized
```

## Aligned locations

| Class | Repository location | Public location | Standing |
|---|---|---|---|
| MindForge framework intake | `docs/external-frameworks/mindforge.md` | `https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/mindforge` | StegVerse intake and interpretation; not an official MindForge source. |
| Commit-time interoperability doctrine | `docs/external-frameworks/commit-time-interoperability-contract.md` | `https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/commit-time-interoperability-contract` | StegVerse doctrine derived from the reviewed boundary discussion. |
| Private-correspondence provenance narrative | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md` | Not a public MindForge source; publication remains governed by its own authorization posture. | Provenance for formulation only. |
| Private-correspondence provenance record | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json` | Repository artifact only unless separately authorized. | Hash-bound provenance; no framework standing or publication authority. |
| Discussion reconstruction fixtures | `docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json` | Repository artifact. | Reconstructs the reviewed boundary semantics; source posture remains private-correspondence provenance only. |
| Discussion reconstruction validator | `scripts/check_mindforge_commit_time_boundary.py` | Not a public framework source. | Verifies provenance posture and the original nine-case discussion matrix. |
| Standing Determination Receipt schema | `static/schemas/standing-determination-receipt.schema.json` | `https://stegverse-labs.github.io/admissibility-wiki/schemas/standing-determination-receipt.schema.json` after successful deployment. | General StegVerse receipt schema; not MindForge-owned. |
| Commit-time conformance fixtures | `tests/fixtures/standing-determination-cases.json` | Repository test artifact. | Ten deterministic StegVerse cases implementing Alane Zhang's clarifications. |
| Commit-time conformance validator | `scripts/check_standing_determination_receipt.py` | Not a public framework source. | Independently evaluates `ALLOW`, `DENY`, and `FAIL_CLOSED` semantics. |
| Boundary-review status | `static/status/mindforge-boundary-review-status.json` | `https://stegverse-labs.github.io/admissibility-wiki/status/mindforge-boundary-review-status.json` after successful deployment. | Local activation status; creates no external standing. |
| Boundary-review receipt | `receipts/mindforge-boundary-review-receipt.json` | Repository proof artifact unless included in a validated public artifact. | Records boundary-semantics review only; no endorsement, certification, compatibility, or authority. |
| Goal handoff | `docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md` | Repository continuation artifact. | Current task and continuation source of truth beneath the overall wiki handoff. |
| Overall repository handoff | `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` | Repository continuation artifact. | Governs repository-wide continuation and downstream mutation limits. |
| Root handoff pointer | `ADMISSIBILITY_MIRROR_HANDOFF.md` | Repository continuity pointer. | Points sessions to the overall and goal-specific handoffs. |

## Fixture distinction

The two fixture sets are intentionally separate and must not be silently merged:

```text
docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json
  -> nine-case reconstruction of the original private boundary discussion
  -> validated by scripts/check_mindforge_commit_time_boundary.py

tests/fixtures/standing-determination-cases.json
  -> ten-case StegVerse conformance suite incorporating the later review clarifications
  -> validated by scripts/check_standing_determination_receipt.py
```

The first preserves what was discussed. The second tests the generalized implementation. Neither becomes an official MindForge specification.

## Publication statement

The narrow public statement is:

> Reviewed for architectural boundary semantics. The reviewer found the boundary substantially correct subject to incorporated clarifications. This is not an official MindForge specification, implementation endorsement, compatibility certification, or execution-authority determination.

## Downstream alignment

```text
StegVerse-Labs/admissibility-wiki -> vocabulary, doctrine, evaluation, receipts, and proof-path display
StegVerse-Labs/Site -> public mirror/display only when its current handoff permits propagation
GCAT-BCAT-Engine/Publisher -> governed publication transport only when its current handoff permits ingestion
StegVerse-002/stegguardian-wiki -> downstream governance mirror only when its current handoff permits propagation
```

No downstream location becomes an independent editorial or canonical MindForge source.
