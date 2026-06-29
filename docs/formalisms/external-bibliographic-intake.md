---
title: External Bibliographic Intake
---

# External Bibliographic Intake

## Status

Record set: `static/translation-records/external-bibliographic-intake.v0.1.json`

Record state: intake

Authority boundary: bibliographic intake records identify source references for translation review. They do not validate source claims, prove equivalence, create citation sufficiency, or create commit-time authority.

## Purpose

External Bibliographic Intake provides the missing source-confirmation layer for external translation records.

A translation record may describe how an external paper or framework maps into the Transition Table. A bibliographic intake record describes whether the source itself has enough confirmed reference information to support review.

## Current Bibliographic Intake Records

| Bibliographic ID | Source ID | Source title | Evidence posture | Review posture |
|---|---|---|---|---|
| `bib-lai-operational-architecture-v0-1` | `external-physics-lai-operational-architecture-v0-1` | `pending_source_confirmed_title` | partial | proposed |

## Required Fields

```text
bibliographic_id
source_id
source_title
creator_or_author_posture
publication_or_source_posture
source_locator
access_posture
evidence_posture
review_posture
linked_external_record_ids
non_claims
```

## Promotion Rule

A bibliographic intake record may move from `proposed` to `mapped` only when it has:

1. source-confirmed title;
2. source-confirmed author or creator posture;
3. stable locator such as URL, DOI, arXiv ID, repository path, or citation record;
4. access posture showing whether the source is public, private, excerpted, or unavailable;
5. linked external translation records;
6. evidence posture that is not merely `partial`; and
7. explicit non-claims.

## Relationship to External Physics Records

External physics records map source terms into transition roles. Bibliographic intake records determine whether the external source reference itself is confirmed enough to support stronger review.

```text
external source claim
-> bibliographic intake
-> external translation record
-> translation record IDs
-> mathematics crosswalk rows
-> Transition Table role
```

## Non-Claims

A bibliographic intake record is not peer review, source validation, citation sufficiency, formal equivalence, proof authority, or commit-time authority.
