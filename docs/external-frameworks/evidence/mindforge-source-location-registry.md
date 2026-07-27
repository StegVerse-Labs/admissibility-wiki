# MindForge Source Location Registry

## Purpose

This registry aligns every MindForge-related source, derivative, validator, receipt, authorization record, reviewer-response record, publication-verification contract, and public route used by `StegVerse-Labs/admissibility-wiki`.

It does not designate StegVerse as the canonical source for MindForge. It separates source provenance from StegVerse interpretation, deterministic evaluation, reviewer-attribution authorization, response evidence, and public display.

## Authority classes

```text
External canonical MindForge source: NOT ATTACHED
Private correspondence: provenance evidence only
StegVerse doctrine: discussion-derived interpretation
StegVerse fixtures: deterministic conformance tests
StegVerse receipts/status: local evaluation records
Reviewer attribution authorization: explicit response required; silence creates no authorization
Reviewer response evidence: verbatim response plus channel, timestamp, and evidence reference
Publication verification: successful workflow, build, deployment, and route evidence required
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
| Discussion reconstruction fixtures | `docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json` | Repository artifact. | Reconstructs reviewed boundary semantics; private-correspondence provenance only. |
| Discussion reconstruction validator | `scripts/check_mindforge_commit_time_boundary.py` | Not a public framework source. | Verifies provenance posture and original nine-case discussion matrix. |
| Standing Determination Receipt schema | `static/schemas/standing-determination-receipt.schema.json` | `/schemas/standing-determination-receipt.schema.json` after successful deployment. | General StegVerse receipt schema; not MindForge-owned. |
| Commit-time conformance fixtures | `tests/fixtures/standing-determination-cases.json` | Repository test artifact. | Ten deterministic StegVerse cases implementing review clarifications. |
| Commit-time conformance validator | `scripts/check_standing_determination_receipt.py` | Not a public framework source. | Evaluates `ALLOW`, `DENY`, and `FAIL_CLOSED`. |
| Boundary-review status | `static/status/mindforge-boundary-review-status.json` | `/status/mindforge-boundary-review-status.json` after successful deployment. | Local activation status; creates no external standing. |
| Boundary-review receipt | `receipts/mindforge-boundary-review-receipt.json` | Repository proof artifact unless included in a validated public artifact. | Boundary-semantics review only; no endorsement, certification, compatibility, or authority. |
| Attribution authorization record | `static/status/mindforge-publication-attribution-authorization.json` | Status artifact only after successful deployment. | Pending state prohibits reviewer attribution. |
| Reviewer response evidence template | `docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json` | Repository evidence artifact only. | Captures an explicit response verbatim with timestamp, channel, evidence reference, and exact approved language. |
| Attribution authorization validator | `scripts/check_mindforge_publication_attribution_authorization.py` | Not a public framework source. | Requires authorization state to match explicit response evidence. |
| Publication-verification template | `docs/external-frameworks/evidence/mindforge-publication-verification.template.json` | Repository evidence artifact. | Requires workflow, build, deployment, and route observations. |
| Publication-verification validator | `scripts/check_mindforge_publication_verification.py` | Not a public framework source. | Prevents public activation without run-bound evidence. |
| Source-location alignment validator | `scripts/check_mindforge_source_location_registry.py` | Not a public framework source. | Fails closed on missing or drifted source roles. |
| Goal handoff | `docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md` | Repository continuation artifact. | Goal-specific source of truth. |
| Overall repository handoff | `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` | Repository continuation artifact. | Repository-wide continuation authority. |
| Root handoff pointer | `ADMISSIBILITY_MIRROR_HANDOFF.md` | Repository continuity pointer. | Points to overall and goal-specific handoffs. |

## Fixture distinction

```text
docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json
  -> nine-case reconstruction of the original private boundary discussion
  -> validated by scripts/check_mindforge_commit_time_boundary.py

tests/fixtures/standing-determination-cases.json
  -> ten-case StegVerse conformance suite incorporating later review clarifications
  -> validated by scripts/check_standing_determination_receipt.py
```

The first preserves what was discussed. The second tests the generalized implementation. Neither becomes an official MindForge specification.

## Attribution and response boundary

Publication attribution remains prohibited while `static/status/mindforge-publication-attribution-authorization.json` is `PENDING_REVIEWER_RESPONSE`.

Any explicit response must first be captured in `docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json`. The response text must be preserved verbatim. Approval may not be inferred from silence, delay, reactions, continued discussion, or a response that does not clearly authorize wording.

## Downstream alignment

```text
StegVerse-Labs/admissibility-wiki -> vocabulary, doctrine, evaluation, receipts, authorization state, response evidence, and proof-path display
StegVerse-Labs/Site -> public mirror/display only when its current handoff permits propagation
GCAT-BCAT-Engine/Publisher -> governed publication transport only when its current handoff permits ingestion
StegVerse-002/stegguardian-wiki -> downstream governance mirror only when its current handoff permits propagation
```

No downstream location becomes an independent editorial or canonical MindForge source.
