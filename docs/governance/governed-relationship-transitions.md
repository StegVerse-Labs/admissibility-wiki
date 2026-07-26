# Governed Relationship Transitions

## Core distinction

A relationship may persist, remain internally coherent, and preserve continuity while no longer being legitimate or admissible.

Giving a relationship identity, provenance, evidence, stewardship, version history, and invariants makes it governable. Those properties do not by themselves establish that continuation remains justified.

StegVerse therefore separates three questions:

```text
Did the relationship persist?
Can its continuity be reconstructed?
May it legitimately continue now?
```

Persistence is not continuity. Continuity is not legitimacy.

## Governed relationships

A governed relationship can be represented as a first-class architectural object with:

- a stable relationship identifier;
- participating entity references;
- constitutional and policy references;
- declared purpose;
- authority and delegation references;
- version lineage;
- evidence and provenance;
- stewardship assignments;
- invariants and boundary conditions;
- runtime bindings;
- suspension, supersession, refusal, and recovery states.

This representation makes the relationship inspectable, versionable, and auditable. It does not make every later continuation admissible.

## The transition requirement

Every consequential continuation or mutation of a governed relationship requires a governed transition determination at the commit-time boundary.

The transition must determine whether:

- the originating and current authorities still have standing;
- the evidence still corresponds to present reality;
- the constitutional purpose remains applicable;
- the relationship has become stale, coercive, obsolete, or purpose-inverting;
- its invariants remain legitimate rather than merely preserved;
- affected entities retain the required consent, delegation, and recoverability;
- the decision can be independently reconstructed;
- continuation is admissible now, not merely explainable from the past.

A prior valid state is evidence. It is not present execution authority.

## Stewardship and legitimacy

Stewardship is not merely the preservation of a relationship or its records. It is the preservation of the conditions through which continuity can remain legitimate as reality changes.

Stewardship still does not confer legitimacy by itself. A steward may faithfully preserve records, enforce inherited constraints, and maintain technical continuity while the relationship has become inadmissible.

The steward's role is therefore bounded by transition governance. Stewardship supplies custody, evidence, review, and remediation capability. The admissibility determination decides whether continuation may be committed.

## Refusal of continuation

A governed architecture must be able to refuse its own continuation.

Refusal is required when continuity would preserve a relationship that is:

- no longer authorized;
- unsupported by current evidence;
- inconsistent with present reality;
- contrary to the purpose it was created to serve;
- unrecoverable as operator or participant authority degrades;
- structurally coherent but constitutionally illegitimate.

This is the point at which governed objects become governed transitions.

## Minimal determination record

A minimal relationship-transition record should contain:

```json
{
  "relationship_id": "rel.example.v1",
  "transition_id": "transition.example.2026-07-26.001",
  "prior_state_ref": "state.example.12",
  "proposed_state_ref": "state.example.13",
  "purpose_ref": "constitution.relationship-purpose.v1",
  "authority_refs": [],
  "delegation_refs": [],
  "evidence_refs": [],
  "invariant_results": [],
  "reality_correspondence": "SUPPORTED | DIVERGED | UNRESOLVED",
  "recoverability": "RECOVERABLE | DEGRADED | UNRECOVERABLE",
  "commit_time_validity": "VALID | INVALID | UNRESOLVED",
  "admissibility_result": "ALLOW | DENY | FAIL_CLOSED",
  "decision_receipt_ref": "receipt.example"
}
```

The record must distinguish evidence of historical persistence from evidence supporting current authority and admissibility.

## Architectural implication

A compiled architectural view can show governed nodes, edges, objects, policies, and runtime bindings. The underlying registry must also preserve the transition records that explain why each relationship was allowed to continue, was modified, was suspended, or was refused.

The resulting architecture is not merely executable and verifiable. It is capable of determining when execution must not preserve the architecture's previous form.

## Comparison boundary

A governed-object architecture asks whether an object or relationship can be compiled, validated, audited, and evidenced.

StegVerse adds the commit-time question:

> Can this relationship legitimately continue under current authority, evidence, purpose, boundary, and reality conditions?

That additional determination separates maintained architecture from admissible transition governance.
