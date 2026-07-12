# Conceptual Inheritance and Provenance Standing

## Status

Proposed formalism under active development.

This document defines conceptual inheritance as a governed transition and separates three properties that are often collapsed:

1. **architectural integrity** — whether an artifact is coherent and internally valid;
2. **provenance continuity** — whether its material conceptual and artifact dependencies remain traceable;
3. **origin-claim standing** — whether available evidence supports a public claim such as independent development, bounded influence, or derivation.

A derived architecture may preserve architectural integrity while losing provenance continuity or standing to assert independent origin.

## Transition model

Let a conceptual-development path be:

```text
SOURCE_CONCEPT
  -> EXPOSURE
  -> INGESTION
  -> TRANSFORMATION
  -> DERIVED_ARTIFACT
  -> PUBLIC_CLAIM
```

For a path `P`, define:

- `S` as the source concept or artifact;
- `E` as evidence of exposure;
- `I` as evidence of ingestion or receipt;
- `T` as the transformation record;
- `D` as the resulting artifact;
- `C` as the public claim made about `D`.

The admissibility of `C` is not implied by the coherence or operational validity of `D`.

Formally:

```text
Integrity(D) does not imply Standing(C)
```

and:

```text
Interoperable(D) does not imply Independent(D)
```

## Inheritance-state classes

A governance interface exchanging concepts, evidence, authority state, decision state, proof artifacts, schemas, or implementation structures SHOULD preserve an inheritance-state classification.

```text
NO_KNOWN_EXPOSURE
INDEPENDENT_PARALLEL_DEVELOPMENT
GENERAL_DOMAIN_INFLUENCE
ACKNOWLEDGED_CONCEPTUAL_INFLUENCE
BOUNDED_INTEROPERABILITY
STRUCTURAL_INHERITANCE
DIRECT_ARTIFACT_TRANSFER
TRANSFORMED_DERIVATION
CO_DEVELOPED
PROVENANCE_UNRESOLVED
PROVENANCE_CONFLICTED
```

These classes describe evidence posture. They do not determine authorship, ownership, infringement, intent, or legal liability.

## Independence-claim admissibility

An assertion of independent origin has standing only when the available evidence does not establish a material dependency incompatible with that assertion.

Let:

- `X` = material exposure established;
- `R` = direct receipt or artifact transfer established;
- `H` = structural inheritance established;
- `A` = attribution or dependency disclosure present;
- `U` = provenance unresolved;
- `C_ind` = claim of independent development.

A minimum fail-closed rule is:

```text
Admit(C_ind) only if:
  not R
  and not H
  and not U
  and no evidence record materially contradicts C_ind
```

Exposure alone does not necessarily defeat independence. However, as exposure becomes more specific, direct, structurally relevant, or artifact-bound, the evidence burden required to sustain an independence claim increases.

```text
Burden(C_ind) increases with Specificity(X), Materiality(X), Directness(R), and StructuralCorrespondence(H)
```

When evidence is insufficient to distinguish independent development from inheritance, the admissible result is not automatic denial of all provenance claims. It is:

```text
PROVENANCE_UNRESOLVED
```

The system must not convert uncertainty into either accusation or certification.

## Integrity versus provenance continuity

An artifact can be:

- operationally valid but provenance-incomplete;
- internally coherent but incorrectly attributed;
- interoperable but structurally inherited;
- independently developed but conceptually convergent;
- derived with adequate attribution;
- derived with unresolved inheritance state.

Therefore, governance evaluation SHOULD return separate determinations:

```json
{
  "architectural_integrity": "PASS | FAIL | UNRESOLVED",
  "provenance_continuity": "PASS | PARTIAL | FAIL | UNRESOLVED",
  "origin_claim_standing": "ADMIT | DENY | FAIL_CLOSED | REVIEW_REQUIRED",
  "inheritance_state": "<class>",
  "evidence_refs": [],
  "attribution_refs": [],
  "contradiction_refs": []
}
```

## Interface requirement

A governed interoperability boundary SHOULD carry inheritance state in addition to evidence, authority, and decision state.

Minimum fields:

```json
{
  "transition_id": "string",
  "source_artifact_refs": [],
  "source_concept_refs": [],
  "exposure_event_refs": [],
  "received_artifact_refs": [],
  "transformation_record_refs": [],
  "inheritance_state": "PROVENANCE_UNRESOLVED",
  "attribution_required": true,
  "attribution_satisfied": false,
  "independence_claim_requested": false,
  "claim_admissibility": "REVIEW_REQUIRED",
  "evaluated_at": "RFC3339 timestamp",
  "policy_ref": "string"
}
```

This information must survive translation across interfaces. Removing or flattening inheritance state during exchange is itself a provenance-affecting transition.

## Failure classes

### Provenance flattening

Distinct source relationships are compressed into a generic description such as collaboration, interoperability, common influence, or convergence, preventing reconstruction of actual dependency.

### Integrity substitution

The coherence or usefulness of the derived artifact is presented as evidence that its origin claim is valid.

### Attribution discontinuity

A source relationship was previously acknowledged but is absent from a later public claim or artifact record.

### Interface laundering

A concept or proof artifact passes through an interoperability boundary and emerges without the inheritance state that accompanied it.

### Independence overclaim

Independent development is asserted while material dependency evidence remains unresolved or contradictory.

### Accusation overclaim

Derivation, copying, or improper appropriation is asserted when the evidence establishes only thematic similarity, public exposure, or domain convergence.

Both independence overclaim and accusation overclaim fail the same governance principle: the claim exceeds the standing provided by the evidence.

## Neutral examples

### Example A — parallel convergence

Two teams publish similar execution-time controls after working from common public standards. No direct artifact transfer or specific exposure is established.

```text
inheritance_state: INDEPENDENT_PARALLEL_DEVELOPMENT
origin_claim_standing: ADMIT
```

### Example B — acknowledged influence

A team receives a published formalism, cites it, and develops a narrower implementation with clear transformation records.

```text
inheritance_state: ACKNOWLEDGED_CONCEPTUAL_INFLUENCE
provenance_continuity: PASS
independence claim: not admissible as stated
bounded derivation claim: admissible
```

### Example C — direct artifact transfer

A team receives proof artifacts and incorporates their structure into a later execution surface. The implementation may be valid, but an unqualified independent-origin claim conflicts with the evidence chain.

```text
inheritance_state: DIRECT_ARTIFACT_TRANSFER or TRANSFORMED_DERIVATION
architectural_integrity: independently evaluated
origin_claim_standing: DENY or REVIEW_REQUIRED
```

### Example D — unresolved public similarity

Two architectures use overlapping terminology, but the record does not establish direct exposure, transfer, or inheritance.

```text
inheritance_state: PROVENANCE_UNRESOLVED
origin_claim_standing: REVIEW_REQUIRED
accusation of derivation: not admissible
certification of independence: not admissible
```

## Governance principle

```text
A transition may preserve the integrity of an artifact while altering the standing of claims made about its origin.
```

Conceptual inheritance is therefore not merely historical context. It is governed state that must remain reconstructable through exposure, ingestion, transformation, publication, and later interoperability.

## Next implementation task

Add machine-readable fixtures and a deterministic checker that:

1. reads an inheritance-state record;
2. evaluates a requested origin claim;
3. returns `ADMIT`, `DENY`, `FAIL_CLOSED`, or `REVIEW_REQUIRED`;
4. emits a replayable receipt without deciding legal ownership or intent.
