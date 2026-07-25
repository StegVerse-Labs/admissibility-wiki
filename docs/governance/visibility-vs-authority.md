# Visibility Versus Authority

Public accessibility and governance authority are independent state dimensions.

A document, manifest, receipt, model, or review record may be publicly visible while remaining non-authoritative. Visibility permits inspection. It does not create publication authority, attribution authority, endorsement, compatibility, interoperability, external-association authority, execution authority, standing, admissibility, or custody.

## Required state separation

A governed artifact must declare at least:

- `visibility_state`
- `process_state`
- `claim_authority`
- `publication_authority`
- `attribution_authority`
- `public_association_authority`
- `endorsement`
- `compatibility`
- `interoperability`

`PUBLICLY_VISIBLE` is descriptive only. It must never be accepted as an `authority_source`.

## Review-only posture

When `process_state` is `REVIEW_ONLY`:

- every authority flag must be `false`;
- endorsement, compatibility, and interoperability must be `NONE`;
- acknowledgement may record receipt, understanding, or feedback;
- acknowledgement must not be interpreted as endorsement, attribution, adoption, association, certification, or authorization.

## Transition to consequential use

A transition from review to adoption or publication requires an explicit authorizer identity, a valid authority reference, complete declaration of every authority dimension, deterministic source binding, and a pre-consequence decision. Missing, malformed, stale, conflicting, or visibility-derived authority fails closed.

## Admissibility rule

An artifact is not admissible for a consequential action merely because it can be found, read, linked, indexed, mirrored, rendered, or reconstructed. The intended action must be supported by the corresponding authority dimension at the time of consequence.

```text
visibility != authority
inspection != adoption
acknowledgement != endorsement
reference != association
publication != attribution
reconstruction != authorization
```

## Ecosystem implementation

The executable chain is distributed across:

- `StegVerse-org/StegVerse-SDK` — declaration, acknowledgement receipts, and authority transitions;
- `GCAT-BCAT-Engine/Publisher` — consequential publication enforcement;
- `StegVerse-Labs/Site` — independent human and machine projection;
- `master-records/orchestration` — custody and replay reconstruction without authority creation.

This wiki records the admissibility doctrine. It does not acquire execution, publication, release, custody, Guardian, or downstream mutation authority by documenting the chain.
