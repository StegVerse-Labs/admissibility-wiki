---
title: ASRO Provenance and Publication Correction
---

# ASRO Provenance and Publication Correction

## Status

```text
Correction state: IN_PROGRESS_FAIL_CLOSED
Existing public packet: UNILATERAL_STEGVERSE_ANALYSIS
Bilateral Seam Comparison Record: NOT_ISSUED
External ASRO-native execution: NOT_TESTED
Accountable reviewer or issuer: unresolved
Reciprocal execution target: not designated
```

## Source and Derivative Separation

The bounded source example supplied by James Aull / ASRO™ and the public StegVerse metadata artifact occupy distinct provenance levels.

```text
Source example:
- provider: James Aull / ASRO™
- status: bounded, noncanonical, not publicly reproduced
- source-input hash: not recorded
- source linkage: unresolved pending a mutually approved source-input reference or hash

Public metadata artifact:
- creator: StegVerse Labs
- status: transformed or reduced bounded derivative
- canonical status: noncanonical
- purpose: bounded comparison only
- replacement path: static/data/framework-evaluations/asro/stegverse-generated-bounded-metadata-derivative.json
```

The historical path `static/data/framework-evaluations/asro/asro-author-provided-bounded-representative-object.json` is retained as a deprecated alias so the public Git history remains additive and inspectable. It must not be treated as the original ASRO-supplied JSON.

## Publication Classification

The existing ASRO wiki packet is unilateral StegVerse analysis. It is not a jointly issued, bilaterally authorized, independently reviewed, or ASRO-native record.

Nothing in the packet establishes or implies:

```text
partnership
membership
participation
integration
endorsement
certification
joint issuance
adoption
completeness
authority inheritance
execution authority
```

Any future bilateral Seam Comparison Record requires exact-language authorization from both owners and must be labeled bilateral, bounded, owner-authorized, and not independently reviewed unless separate review evidence exists.

## Preserved Boundaries

```text
reviewer_issuer: unresolved
reviewer identity: unset
reviewer authority basis: unset
reviewer authority fields: false
external ASRO-native execution: NOT_TESTED
StegVerse PASS: limited to the bounded StegVerse run
correspondence != truth
correspondence != sufficiency
correspondence != validity
correspondence != admissibility
correspondence != authority inheritance
unsigned receipt != certification
```

## Required Follow-on Corrections

1. Update manifests and tests to reference the StegVerse-generated derivative rather than the deprecated alias.
2. State explicitly that the recorded derivative hash is not a content hash of the original source JSON.
3. Pin the historical public ASRO sources actually observed using repository, commit, path, declared version, artifact hash, and observation date.
4. Correct any `source_version: PRESENT` assertion unless those values are installed.
5. Mark the existing bounded-run receipt provisional or unfinalized while `PENDING_CANONICAL_HASH` remains.
6. Recompute dependent integrity values after the provenance correction is complete.
7. Create a StegVerse owner declaration covering entity form, accountable role, contact point, canonical repository, and website.
8. Create a comparison-scoped contributor protocol and append-only contribution ledger beginning May 6, 2026.

## Authority Boundary

This correction record governs evidence classification and publication posture only. It grants no execution, certification, admissibility, release, partnership, joint ownership, downstream mutation, or reciprocal-testing authority.
