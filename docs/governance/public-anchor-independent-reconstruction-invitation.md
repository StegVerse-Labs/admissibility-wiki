---
title: Public-Anchor Independent Reconstruction Invitation
sidebar_label: Independent Reconstruction Invitation
---

# Public-Anchor Independent Reconstruction Invitation

## Invitation state

```text
Invitation id: public-anchor-independent-reconstruction-invitation-2026-08-02
Repository: StegVerse-Labs/admissibility-wiki
Target manifest: static/data/governed-framework-reviews/public-anchor-reconstruction-manifest.v1.json
Target manifest id: public-anchor-three-docket-freeze-2026-07-27
State: OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED
Independent reconstruction: NOT_RUN
Neutral reviewer standing: NOT_ESTABLISHED
Certification authority: false
Execution authority: false
Custody authority: false
```

This invitation requests an accountable reconstruction of the frozen three-docket public-anchor package. It does not appoint a reviewer, confer standing, certify the package, or authorize execution.

## Required submission

A reconstruction submission must use:

```text
static/schemas/framework-reconstruction-submission.schema.json
```

The submission must identify the reviewer, evidence inspected, frozen commit, manifest id, reconstruction method, points of agreement, points of divergence, unresolved uncertainty, conflicts of interest, and the reviewer's claimed authority boundary.

## Acceptance boundary

A submission may enter the governed review process only when it is attributable, schema-valid, bound to the frozen target, and explicit about reviewer standing. Acceptance as evidence does not automatically alter any docket's standing.

```text
submission accepted != determination adopted
reviewer identity != neutral reviewer standing
schema validity != substantive correctness
reconstruction agreement != certification
reconstruction divergence != source invalidation
publication != execution authority
```

## Machine-observable release condition

The invitation remains open until a committed reconstruction submission exists and the canonical validator records all of the following:

```text
submission_state: ACCEPTED_FOR_REVIEW
reviewer_identity: ESTABLISHED
reviewer_conflicts: DISCLOSED
reviewer_standing: ESTABLISHED or PUBLICLY_UNRESOLVED
frozen_manifest_binding: PASS
schema_validation: PASS
independent_reconstruction_status: RUN_RECORDED
```

Until then, the correct state is `OPEN_NO_ACCOUNTABLE_REVIEWER_ASSIGNED` and `NOT_RUN`.
