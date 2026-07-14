# Commit-Boundary Binding Predicate

## Status

Proposed formalism under active development.

This document defines the minimum conditions under which a proposed state transition may become binding consequence. It separates decision validity, transition admissibility, commit authority, and origin validity so none can silently substitute for another.

## Core distinction

A decision can be valid when evaluated and still fail to produce an admissible transition later.

```text
decision validity != transition validity
approval at t0 != standing at commit tn
execution != admissibility
replayability != authority
```

The governed object at commit is not merely intent. It is the binding of consequence under the live system state.

## Transition model

Let:

- `x_t` be the live system state at commit time;
- `u_t` be the proposed transition;
- `x_t+1 = F(x_t, u_t)` be the resulting state;
- `O_t` be the validated causal origin;
- `A_t` be commit authority re-derived from current state;
- `D_t` be transition admissibility under current state;
- `I_t` be preserved invariants;
- `R_t` be recoverability and viable-option preservation;
- `E_t` be the execution evidence required for independent reconstruction.

A transition may bind only when every predicate holds:

```text
BIND(u_t, x_t) iff
  OriginValid(O_t, x_t)
  and AuthorityValid(A_t, O_t, x_t, u_t)
  and Admissible(D_t, x_t, u_t, x_t+1)
  and InvariantsPreserved(I_t, x_t+1)
  and RecoverabilityPreserved(R_t, x_t+1)
  and EvidenceComplete(E_t)
```

Failure or unresolved standing in any required predicate produces:

```text
FAIL_CLOSED
```

No prior approval, cached role, historical consent, earlier review, or previous successful execution may replace the commit-time result.

## Independent control questions

### Decision validity

Was the proposed action coherent, policy-consistent, or justified when originally evaluated?

Decision validity is evidence. It is not permission to bind consequence later.

### Transition admissibility

Would the proposed mutation preserve a governable state under the conditions that exist at commit?

Admissibility must be redetermined at transition because authority, state, evidence, consent, context, and downstream consequence can drift between approval and execution.

### Commit authority

Does the institution, role, delegation, consent chain, or supervisory structure still have standing to authorize this specific mutation now?

A transition can be technically coherent and still lack the right to exist.

### Origin validity

Who or what actually caused the transition candidate to arrive at the commit boundary, and is that causal source valid for this action under current conditions?

Authority answers who is allowed to act. Origin validation answers who or what actually initiated the transition. They diverge under impersonation, replay, compromised agents, delegated execution, indirect triggering, and transformed inputs.

## Origin validation requirement

Origin validation MUST NOT be reduced to identity lookup or signature presence alone.

A minimum origin record SHOULD establish:

```json
{
  "origin_id": "string",
  "origin_type": "human | agent | service | device | workflow | institution",
  "identity_proof_refs": [],
  "attestation_refs": [],
  "causal_predecessor_refs": [],
  "delegation_refs": [],
  "input_provenance_refs": [],
  "requested_transition_hash": "sha256:...",
  "observed_at_commit": "RFC3339 timestamp",
  "origin_status": "VALID | INVALID | UNRESOLVED"
}
```

The origin proof must bind the actual transition candidate, not merely a session, account, or historically authorized actor.

## Authority re-derivation requirement

Commit authority MUST be recomputed against the live state and requested transition.

```text
AuthorityValid != actor_was_previously_approved
AuthorityValid != role_exists
AuthorityValid != policy_was_satisfied_at_t0
```

Authority evaluation SHOULD include, where applicable:

- current role and institutional standing;
- delegation scope and expiration;
- consent continuity and withdrawal state;
- supervisory availability;
- policy version and jurisdiction;
- execution target and consequence class;
- origin-to-authority binding;
- conflicts, revocation, or stale evidence.

## Admissibility and trajectory viability

Admissibility is not an isolated rule check. The resulting state must remain inside a governable region and preserve the conditions required for later evaluation.

At minimum, a transition must not:

- violate required invariants;
- move the system into an unrecoverable state;
- collapse viable future options below an allowed threshold;
- place the system so near a boundary that ordinary perturbation makes governance unstable;
- destroy the ability to prove authority for subsequent transitions;
- make later reconstruction materially impossible.

This does not require prediction of the entire future trajectory. It requires that every bound state remain governable for what comes next.

## Binding of consequence

The phrase `binding of consequence` identifies the exact governance event addressed by this formalism.

Before commit, the system may contain proposals, recommendations, approvals, or plans. At commit, a state mutation becomes real and downstream consequence attaches.

```text
proposal -> evaluation -> commitment candidate -> commit predicate -> bound consequence
```

Governance that cannot refuse the transition before consequence attaches is observational or advisory, not execution authority.

## Receipt requirement

Every bound transition SHOULD emit a hash-linked receipt sufficient to reconstruct why the transition was allowed to exist.

Minimum receipt fields:

```json
{
  "transition_id": "string",
  "candidate_hash": "sha256:...",
  "state_before_hash": "sha256:...",
  "state_after_hash": "sha256:...",
  "origin_result": "VALID",
  "origin_evidence_refs": [],
  "authority_result": "VALID",
  "authority_evidence_refs": [],
  "admissibility_result": "ALLOW",
  "invariant_results": [],
  "recoverability_result": "PRESERVED",
  "policy_refs": [],
  "delegation_refs": [],
  "consent_refs": [],
  "evaluated_at": "RFC3339 timestamp",
  "committed_at": "RFC3339 timestamp",
  "previous_receipt_hash": "sha256:...",
  "receipt_hash": "sha256:..."
}
```

A receipt proves only what its evidence and verifier independently establish. Receipt presence alone does not prove valid origin, authority, or admissibility.

## Failure classes

### Cached authority

A prior approval, role, or delegation is treated as sufficient without live re-derivation.

### Origin substitution

The authorized actor is recorded, but the actual causal source of the transition is not proven.

### Replay substitution

A previously valid transition or authorization is replayed under a changed state.

### Decision-to-transition leakage

Decision validity is silently converted into permission to commit.

### Local-validity drift

Each transition appears locally acceptable while the resulting states progressively narrow recoverability or viable future options.

### Evidence without refusal power

The system emits logs or receipts but lacks a reachable pre-consequence point that can return `DENY` or `FAIL_CLOSED`.

## Minimum machine-readable result

```json
{
  "transition_id": "string",
  "origin": "VALID | INVALID | UNRESOLVED",
  "authority": "VALID | INVALID | UNRESOLVED",
  "admissibility": "ALLOW | DENY | FAIL_CLOSED",
  "invariants": "PRESERVED | VIOLATED | UNRESOLVED",
  "recoverability": "PRESERVED | DEGRADED | LOST | UNRESOLVED",
  "evidence": "COMPLETE | INCOMPLETE | UNRESOLVED",
  "binding_result": "BIND | DENY | FAIL_CLOSED",
  "reason_codes": [],
  "receipt_ref": "string"
}
```

`BIND` is permitted only when every required component is affirmatively valid. `UNRESOLVED`, missing evidence, stale evidence, or contradictory evidence must not be converted into approval.

## Interoperability posture

External frameworks may use overlapping language such as commit-boundary control, invariant preservation, viability margins, deterministic reconstruction, or recoverability-aware execution. Similar claims do not establish equivalence.

Comparison requires independently inspectable evidence of:

1. the actual commit boundary;
2. the origin-validation mechanism;
3. authority re-derivation;
4. the admissibility function;
5. invariant and recoverability representation;
6. fail-closed enforcement;
7. receipt generation and independent verification;
8. tested failure cases.

Until that evidence exists, framework overlap should be described as conceptual alignment or claimed architectural similarity, not verified interoperability or implementation equivalence.

## Next implementation task

Add a machine-readable schema, positive and negative fixtures, and a deterministic checker that:

1. validates origin-to-transition binding;
2. re-derives commit authority from current evidence;
3. evaluates admissibility, invariants, and recoverability separately;
4. returns `BIND`, `DENY`, or `FAIL_CLOSED`;
5. emits a replayable receipt;
6. demonstrates that a valid decision can still fail at commit because origin, authority, state, or recoverability changed.
