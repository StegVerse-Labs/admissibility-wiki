# MindForge Source Location Registry

## Purpose

This registry aligns every MindForge-related source, derivative, validator, receipt, authorization record, reviewer-response record, publication-verification contract, and public route used by `StegVerse-Labs/admissibility-wiki`.

It does not designate StegVerse as the canonical source for MindForge. It separates source provenance from StegVerse interpretation, deterministic evaluation, conditional reviewer approval, attribution authorization, response evidence, and public display.

## Authority classes

```text
External canonical MindForge source: NOT ATTACHED
Private correspondence: provenance evidence only
StegVerse doctrine: discussion-derived interpretation
StegVerse fixtures: deterministic conformance tests
StegVerse receipts/status: local evaluation records
Conditional review intake: approval observed, conditions incomplete, fail closed
Reviewer attribution authorization: explicit complete conditions required
Reviewer response evidence: preserve what is observed; do not invent missing verbatim text
Publication verification: successful workflow, build, deployment, and route evidence required
Admissibility Wiki Pages: public vocabulary and proof-path display
Site / Publisher / StegGuardian: downstream mirrors only when separately authorized
```

## Aligned locations

| Class | Repository location | Standing |
|---|---|---|
| MindForge framework intake | `docs/external-frameworks/mindforge.md` | StegVerse intake and interpretation; not an official MindForge source. |
| Commit-time interoperability doctrine | `docs/external-frameworks/commit-time-interoperability-contract.md` | StegVerse doctrine derived from reviewed boundary discussion. |
| Private-correspondence provenance narrative | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md` | Provenance for formulation only. |
| Private-correspondence provenance record | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json` | Hash-bound provenance; no publication authority. |
| Conditional reviewer intake | `data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json` | Records narrow approval observation and incomplete two-condition capture; non-publishable. |
| Conditional reviewer intake validator | `scripts/check_mindforge_review_intake.py` | Enforces fail-closed condition capture and cross-record alignment. |
| Discussion reconstruction fixtures | `docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json` | Original nine-case private-discussion reconstruction. |
| Discussion reconstruction validator | `scripts/check_mindforge_commit_time_boundary.py` | Verifies original discussion matrix and provenance posture. |
| Standing Determination Receipt schema | `static/schemas/standing-determination-receipt.schema.json` | General StegVerse receipt schema; not MindForge-owned. |
| Commit-time conformance fixtures | `tests/fixtures/standing-determination-cases.json` | Ten-case generalized StegVerse conformance suite. |
| Commit-time conformance validator | `scripts/check_standing_determination_receipt.py` | Evaluates `ALLOW`, `DENY`, and `FAIL_CLOSED`. |
| Boundary-review status | `static/status/mindforge-boundary-review-status.json` | Local activation status; creates no external standing. |
| Boundary-review receipt | `receipts/mindforge-boundary-review-receipt.json` | Boundary-semantics review only; no certification or authority. |
| Attribution authorization record | `static/status/mindforge-publication-attribution-authorization.json` | Conditional approval pending complete condition capture; publication prohibited. |
| Reviewer response evidence | `docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json` | Records observed conditional approval without fabricating missing verbatim conditions. |
| Attribution authorization validator | `scripts/check_mindforge_publication_attribution_authorization.py` | Requires authorization, response, and intake evidence to agree. |
| Publication-verification template | `docs/external-frameworks/evidence/mindforge-publication-verification.template.json` | Requires workflow, build, deployment, and route evidence. |
| Publication-verification validator | `scripts/check_mindforge_publication_verification.py` | Prevents public activation without run-bound evidence. |
| Source-location alignment validator | `scripts/check_mindforge_source_location_registry.py` | Fails closed on missing or drifted source roles. |
| Goal handoff | `docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md` | Goal-specific continuation source of truth. |
| Overall repository handoff | `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` | Repository-wide continuation authority. |
| Root handoff pointer | `ADMISSIBILITY_MIRROR_HANDOFF.md` | Points to overall and goal-specific handoffs. |

## Fixture distinction

```text
docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json
  -> nine-case reconstruction of the original private boundary discussion

tests/fixtures/standing-determination-cases.json
  -> ten-case generalized StegVerse conformance suite
```

Neither becomes an official MindForge specification.

## Attribution and condition boundary

The narrow statement has an observed conditional approval, but two publication conditions are not captured verbatim. Therefore:

```text
authorization_state = CONDITIONAL_APPROVAL_PENDING_CONDITION_CAPTURE
publication_permitted = false
condition_gate = FAIL_CLOSED_UNTIL_COMPLETE
```

The missing condition text must not be reconstructed, paraphrased as verbatim, or inferred. Publication attribution remains prohibited until both conditions, durable evidence references, and final authorization timing are complete.

## Downstream alignment

```text
StegVerse-Labs/admissibility-wiki -> vocabulary, doctrine, evaluation, receipts, authorization state, response evidence, and proof-path display
StegVerse-Labs/Site -> public mirror/display only when its current handoff permits propagation
GCAT-BCAT-Engine/Publisher -> governed publication transport only when its current handoff permits ingestion
StegVerse-002/stegguardian-wiki -> downstream governance mirror only when its current handoff permits propagation
```

No downstream location becomes an independent editorial or canonical MindForge source.
