---
title: AGCP Registry
description: Evidence-bounded review of the AGCP Registry and its runtime-governance conformance claims.
---

# AGCP Registry

## Review posture

**State:** `SOURCE_CAPTURED_REVIEW_ACTIVE`

This page records an evidence-bounded StegVerse review of the AGCP Registry. It does not grant certification, endorsement, admissibility, execution authority, publication authority, or standing to the Registry or any assessed implementation.

## Source captured

A public LinkedIn post attributed to John M. Willis, captured on 2026-08-02, states that:

- the first member of the AGCP Registry Founders Cohort achieved full conformance;
- the assessed implementation satisfied 100% of the applicable Registry requirements;
- the assessment is deterministic and requirement-by-requirement;
- the Registry intends to publish initial Founders Cohort data by the end of August 2026;
- full conformance is limited to the applicable requirements within the scope of the assessment;
- the Registry is intended to create a transparent, technically defensible, comparable public record.

The source is a public announcement, not the complete specification, assessment record, evidence package, evaluator record, or reproducibility package.

## What the announced result establishes

Only the following bounded claim is currently supported by the captured announcement:

> An unnamed implementation was reported by the Registry operator as satisfying every AGCP Registry requirement considered applicable within the scope of its assessment.

## What the announced result does not yet establish

The captured announcement does not independently establish:

- completeness or adequacy of the AGCP requirements;
- the identity and immutable version of the specification used;
- the complete requirement inventory and applicability decisions;
- evaluator independence or conflict controls;
- public access to the evidence examined;
- independent reproducibility of the assessment;
- reconstruction of the assessed system at time T;
- commit-time validity after policy, model, configuration, delegation, or evidence mutation;
- execution authority, consequence authority, or admissibility;
- continuing conformance after the assessed snapshot;
- a governed dispute, correction, withdrawal, or supersession process.

## StegVerse assessment dimensions

| Dimension | Current result | Reason |
|---|---|---|
| Public specification identity | `UNRESOLVED` | No immutable specification version was captured. |
| Requirement inventory | `PARTIAL_CLAIM_ONLY` | Requirement-by-requirement assessment is asserted, but the inventory is not present. |
| Applicability transparency | `PARTIAL_CLAIM_ONLY` | The result is explicitly scoped to applicable requirements, but exclusions are not listed. |
| Evidence accessibility | `UNRESOLVED` | No evidence package was captured. |
| Deterministic assessment | `ASSERTED_NOT_REPRODUCED` | Determinism is claimed but has not been independently replayed. |
| Evaluator independence | `UNRESOLVED` | Assessor identity, role separation, and conflict controls are absent from the captured source. |
| Reconstruction at time T | `UNRESOLVED` | No immutable system snapshot or reconstruction receipt was captured. |
| Commit-time validity | `UNRESOLVED` | No mutation-aware validity test was captured. |
| Dispute and correction | `UNRESOLVED` | No public procedure was captured. |
| Conformance claim | `BOUNDED_REPORTED_RESULT` | Limited to applicable requirements within the assessment scope. |
| Admissibility | `NOT_ESTABLISHED` | Framework conformance does not itself establish admissibility. |
| Execution authority | `NOT_ESTABLISHED` | No execution-authority evidence was captured. |

## Required evidence for promotion

Promotion beyond `SOURCE_CAPTURED_REVIEW_ACTIVE` requires repository-observed evidence for these records:

1. immutable AGCP specification identifier and digest;
2. complete requirement inventory;
3. applicability and exclusion record;
4. assessment method and deterministic evaluation rules;
5. assessed implementation identity and immutable snapshot;
6. evidence references for each requirement result;
7. assessor identity, delegation, independence, and conflict disclosures;
8. machine-readable assessment result;
9. independent replay or reconstruction result;
10. mutation and commit-time validity behavior;
11. dispute, correction, withdrawal, expiration, and supersession procedures.

## Claim boundary

```text
AGCP full conformance
!= completeness of the AGCP specification
!= independent reconstruction
!= commit-time validity
!= admissibility
!= execution authority
!= consequence authority
```

## Repository-owned continuation

The active task and completion criteria are maintained in:

- `docs/external-frameworks/AGCP_REGISTRY_MIRROR_HANDOFF.md`
- `static/external-frameworks/agcp-registry-assessment.v0.1.json`
- `scripts/check_agcp_registry_assessment.py`

No user-operated or external task is required. The canonical repository workflow owns repeated validation after these files are bound into the aggregate validation path.