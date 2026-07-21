# Discovery-to-Governance Minimum Handoff

## Status

Implemented as a deterministic boundary contract pending canonical workflow and public publication verification.

## Purpose

A discovery system may identify an opportunity, collaborator, resource, or recommended next action without becoming the authority that admits, authorizes, commits, or executes the resulting transition.

The minimum handoff record preserves enough context for a downstream governance layer to independently evaluate the proposed transition while keeping the discovery layer focused on discovery.

## Governing distinction

```text
DISCOVERY RECOMMENDATION != CONSENT
DISCOVERY RECOMMENDATION != AUTHORITY
DISCOVERY RECOMMENDATION != ADMISSIBILITY
DISCOVERY RECOMMENDATION != COMMITMENT
DISCOVERY RECOMMENDATION != EXECUTION
```

A discovery handoff preserves the evidence needed to evaluate a possible transition; it does not authorize, admit, or execute that transition.

## Layer responsibilities

### Discovery layer

The discovery layer may:

- surface a candidate opportunity;
- preserve declared intent separately from inferred context;
- record opportunity provenance and confidence basis;
- identify participants, roles, prerequisites, boundaries, and unresolved assumptions;
- propose a next action;
- identify the consent or authority still required;
- emit a signed or content-addressed handoff record.

It must not silently assert:

- participant consent;
- current identity or standing;
- policy compliance;
- action-level authority;
- transition admissibility;
- commitment validity;
- execution permission;
- correctness or endorsement of the recommendation.

### Governance and commitment layers

Downstream layers independently determine:

- identity and standing;
- live policy and delegation validity;
- participant consent;
- conflicts and constraints;
- current-state compatibility;
- commit-time authority;
- transition admissibility;
- reachable denial before consequence;
- execution receipt and reconstruction posture.

## Minimum handoff predicate

Let `H` be a discovery handoff and `T` the proposed downstream transition.

```text
HANDOFF_READY(H, T) iff
  RecommendationIdentified(H)
  and DeclaredAndInferredContextSeparated(H)
  and ProvenancePresent(H)
  and ConfidenceBasisPresent(H)
  and ParticipantsAndBoundariesPresent(H)
  and PrerequisitesPresent(H)
  and UnresolvedAssumptionsExplicit(H)
  and ProposedActionPresent(H)
  and MissingConsentOrAuthorityExplicit(H)
  and EvidenceReferencesPresent(H)
  and NonAuthorityDeclarationPresent(H)
```

`HANDOFF_READY` means only that the record is sufficient for downstream evaluation. It does not mean `ALLOW`, `ADMIT`, `BIND`, or `EXECUTE`.

## Required record classes

The record contains four classes of information.

### Discovery evidence

- handoff and recommendation identifiers;
- discovery system and version;
- opportunity type and description;
- declared intent;
- inferred context with inference labels;
- opportunity provenance;
- confidence score or qualitative basis;
- evidence references;
- generation timestamp and digest.

### Participant boundary evidence

- participant identifiers or unresolved participant references;
- represented roles;
- prerequisites;
- known exclusions and constraints;
- unresolved assumptions;
- required consent and authority classes.

### Proposed coordination step

- proposed action;
- intended destination layer;
- requested review posture;
- expiration or freshness boundary.

### Explicit non-authority declaration

The handoff must state that it grants none of the following:

```text
CONSENT
STANDING
AUTHORITY
ADMISSIBILITY
COMMITMENT
EXECUTION_PERMISSION
CERTIFICATION
ENDORSEMENT
```

## Deterministic outcomes

```text
HANDOFF_READY
REVIEW_REQUIRED
DENY
FAIL_CLOSED
```

- `HANDOFF_READY`: all minimum evidence is present and all authority-bearing states remain explicitly unresolved or downstream-owned.
- `REVIEW_REQUIRED`: the record is structurally usable but contains declared uncertainty requiring downstream review.
- `DENY`: the handoff falsely asserts consent, authority, admissibility, commitment, or execution permission.
- `FAIL_CLOSED`: required evidence, provenance, freshness, or non-authority declarations are missing or contradictory.

## Reconstruction requirement

A downstream evaluator must be able to reconstruct:

1. why the candidate was surfaced;
2. which context was declared and which was inferred;
3. what evidence and provenance supported the recommendation;
4. what remained unresolved at handoff;
5. which consent, standing, policy, or authority still had to be established;
6. whether the handoff changed before commitment.

## Conectrr architectural observation

The Conectrr exchange motivating this fixture supports `DOCUMENTED_ARCHITECTURAL_ALIGNMENT` with the separation described here: Conectrr remains focused on discovery while preserving sufficient context and explainability for later layers. This observation does not establish implementation equivalence, interoperability, certification, or a production integration.

## Governance principle

```text
Portable context may cross the discovery boundary.
Decision authority does not cross that boundary unless separately and explicitly established.
```
