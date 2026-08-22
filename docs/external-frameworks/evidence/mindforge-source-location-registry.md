# MindForge Source Location Registry

## Purpose

This registry aligns every MindForge-related source, derivative, validator, receipt, authorization record, reviewer-response record, publication-verification contract, provenance-correction record, source-recovery record, and public route used by `StegVerse-Labs/admissibility-wiki`.

It does not designate StegVerse as the canonical source for MindForge. It separates private provenance, StegVerse interpretation, deterministic evaluation, narrow reviewer attribution authorization, publication verification, source-date verification, and execution authority.

## Authority classes

```text
External canonical MindForge source: NOT ATTACHED
Private correspondence: hash-bound provenance only; not publicly quoted or reproduced
StegVerse doctrine: discussion-derived interpretation
StegVerse fixtures: deterministic conformance tests
StegVerse receipts/status: local evaluation records
Review attribution: exact approved description only
Publication boundaries: no scope expansion, private correspondence, screenshots, unpublished drafts, or stronger attribution
Publication verification: successful workflow, build, deployment, and route evidence required
Source-date verification: exact recovery of one or more seven hash-bound captures required; negative search is not proof of absence
Admissibility Wiki Pages: public vocabulary and proof-path display
Site / Publisher / StegGuardian: downstream mirrors only when separately authorized
```

## Aligned locations

| Class | Repository location | Standing |
|---|---|---|
| MindForge framework intake | `docs/external-frameworks/mindforge.md` | StegVerse intake and interpretation; not an official MindForge source. |
| Commit-time interoperability doctrine | `docs/external-frameworks/commit-time-interoperability-contract.md` | StegVerse doctrine derived from reviewed boundary discussion. |
| Private-correspondence provenance narrative | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md` | Provenance for formulation only; private text remains non-public; source-date range currently unverified. |
| Private-correspondence provenance record | `docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json` | Seven source hashes bound; `captured_date_range` remains null until direct recovery. |
| Provenance date-correction receipt | `receipts/mindforge-provenance-date-correction-2026-08-18.json` | Retracts the prior unverified date range from asserted provenance without inventing a replacement. |
| Provenance source-recovery receipt | `receipts/mindforge-provenance-source-recovery-search-2026-08-21.json` | Records expanded bounded exact-hash search; 16 candidates checked, zero exact source matches. |
| Current review/provenance handoff | `data/external-reviews/mindforge/MINDFORGE_REVIEW_MIRROR_HANDOFF.md` | Active source-date verification continuation; no release/execution/cross-repository authority. |
| Reviewer intake | `data/external-reviews/mindforge/alane-zhang-boundary-semantics-review-intake.json` | Records exact approved public description, normalized publication boundaries, and private hash-bound evidence custody. |
| Reviewer intake validator | `scripts/check_mindforge_review_intake.py` | Enforces exact-description authorization and private-correspondence prohibition. |
| Current bounded intake validator | `scripts/check_alane_zhang_boundary_review_intake.py` | Enforces the current normalized narrow-publication state without promoting source-date verification. |
| Discussion reconstruction fixtures | `docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json` | Original nine-case private-discussion reconstruction. |
| Discussion reconstruction validator | `scripts/check_mindforge_commit_time_boundary.py` | Verifies original discussion matrix and provenance posture. |
| Standing Determination Receipt schema | `static/schemas/standing-determination-receipt.schema.json` | General StegVerse receipt schema; not MindForge-owned. |
| Commit-time conformance fixtures | `tests/fixtures/standing-determination-cases.json` | Ten-case generalized StegVerse conformance suite. |
| Commit-time conformance validator | `scripts/check_standing_determination_receipt.py` | Evaluates `ALLOW`, `DENY`, and `FAIL_CLOSED`. |
| Boundary-review status | `static/status/mindforge-boundary-review-status.json` | Local activation status; creates no external standing. |
| Boundary-review receipt | `receipts/mindforge-boundary-review-receipt.json` | Boundary-semantics review only; no certification or authority. |
| Attribution authorization record | `static/status/mindforge-publication-attribution-authorization.json` | Authorizes only the exact approved review description within explicit boundaries. |
| Reviewer response evidence | `docs/external-frameworks/evidence/mindforge-reviewer-attribution-response.template.json` | Public-safe normalized authorization record; private response text and screenshots are not reproduced. |
| Attribution authorization validator | `scripts/check_mindforge_publication_attribution_authorization.py` | Requires authorization, response, and intake evidence to agree. |
| Publication-verification template | `docs/external-frameworks/evidence/mindforge-publication-verification.template.json` | Requires workflow, build, deployment, and route evidence. |
| Publication-verification validator | `scripts/check_mindforge_publication_verification.py` | Prevents public activation without run-bound evidence. |
| Source-location alignment validator | `scripts/check_mindforge_source_location_registry.py` | Fails closed on missing, stale, or internally inconsistent source roles. |
| Completed publication handoff | `docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md` | Bounded publication route completion; does not close the separate source-date verification lane. |
| Overall repository handoff | `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` | Repository-wide continuation authority. |
| Public-anchor goal handoff | `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` | Public-anchor reconstruction/docket continuation only. |
| Root compatibility pointer | `ADMISSIBILITY_MIRROR_HANDOFF.md` | Points to repository-wide and goal-specific handoffs. |

## Fixture distinction

```text
docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json
  -> nine-case reconstruction of the original private boundary discussion

tests/fixtures/standing-determination-cases.json
  -> ten-case generalized StegVerse conformance suite
```

Neither becomes an official MindForge specification.

## Authorized attribution boundary

The only authorized reviewer-attributed statement is:

> Reviewed for architectural boundary semantics. The reviewer found the boundary substantially correct subject to incorporated clarifications. This is not an official MindForge specification, implementation endorsement, compatibility certification, or execution-authority determination.

```text
authorization_state = AUTHORIZED_EXACT_WITH_BOUNDARIES
publication_permitted = true
scope = ARCHITECTURAL_BOUNDARY_SEMANTICS_ONLY
private_correspondence_publication_permitted = false
screenshot_publication_permitted = false
unpublished_draft_publication_permitted = false
stronger_attribution_requires_separate_approval = true
```

The approved description must not be expanded into an endorsement of StegVerse, SPE implementation readiness, MindForge compatibility, certification, or execution authority. Private correspondence, screenshots, and unpublished drafts must not be quoted or published.

## Current provenance-date gate

```text
correspondence_date_status = UNVERIFIED
captured_date_range = null
bound_source_capture_count = 7
bounded_library_candidates_hash_checked = 16
exact_hash_matches = 0
previously_recorded_range = RETRACTED_FROM_ASSERTED_PROVENANCE_UNTIL_DIRECTLY_VERIFIED
required_next_transition = recover_exact_bound_source_capture_and_verify_dates
```

The bounded search result is evidence of attempted recovery only. It is not evidence that the original captures are absent, and it cannot substitute later approval/publication correspondence for the original source dates.

## Downstream alignment

```text
StegVerse-Labs/admissibility-wiki -> vocabulary, doctrine, evaluation, receipts, authorization state, provenance state, and proof-path display
StegVerse-Labs/Site -> public mirror/display only when its current handoff permits propagation
GCAT-BCAT-Engine/Publisher -> governed publication transport only when its current handoff permits ingestion
StegVerse-002/stegguardian-wiki -> downstream governance mirror only when its current handoff permits propagation
```

No downstream location becomes an independent editorial or canonical MindForge source.
