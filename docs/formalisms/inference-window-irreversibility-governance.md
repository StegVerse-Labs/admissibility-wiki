# Inference-Window and Irreversibility-Bounded Governance

## Status

Canonical public doctrine for evaluating consequential AI transitions under changing evidence, bounded inference, variable authority, and incomplete recoverability.

## Abstract

AI governance cannot guarantee that an intelligent system is always correct. Correctness is conditional on the evidence available, the model used to interpret it, and the interval during which that evidence remains sufficiently current. Governance therefore has a different responsibility: control how uncertainty becomes action, how action becomes consequence, and how consequence remains subject to interruption, recovery, correction, compensation, appeal, and accountability.

This formalism separates operational success, epistemic support, execution authority, admissibility, continuity, reconstructability, and recoverability. It also requires assurance to rise as harm, uncertainty, and irreversibility rise, particularly where recovery approaches zero.

## Relationship to the Governed Action Lifecycle and IICT

This page defines the executable commit-time evaluation model for an individual proposed transition.

The broader sequence is documented in [Governed Action Lifecycle](./governed-action-lifecycle.md):

```text
proposal
  -> commit-time revalidation
  -> bounded execution
  -> consequence observation
  -> recovery, correction, or accountability
  -> reconstruction
```

The [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md) is separate. It is a theorem candidate asking whether repeated admissibility optimization causes governance architectures to converge toward a smaller distance between the final valid inference and irreversible commitment.

Therefore:

```text
Inference-window governance = operational evaluation of one transition.
Governed Action Lifecycle = placement of that evaluation within the full action path.
IICT = convergence hypothesis about repeated governance optimization.
```

A passing validator on this page does not prove IICT, and IICT need not be proven for this operational model to be useful.

## 1. Governing claim

A well-governed system is not one that never makes a mistake. It is one that:

1. acts only while evidence, policy, delegation, and context retain commit-time standing;
2. scales execution thresholds to uncertainty, harm, irreversibility, and recoverability;
3. preserves interruption and correction paths where possible;
4. refuses or escalates transitions whose consequence exceeds available standing;
5. leaves enough canonical evidence to reconstruct both what occurred and whether the action was admissible when committed.

## 2. State and decision model

Let a proposed transition at time `t` be represented by:

```text
T_t = (S_t, a_t, E_t, P_t, D_t, C_t)
```

where:

- `S_t` is the current system state;
- `a_t` is the proposed action;
- `E_t` is the evidence set;
- `P_t` is the applicable policy state;
- `D_t` is the delegation and authority state;
- `C_t` is the execution context.

The decision process may propose an action:

```text
a_t = π(E_t, P_t, D_t, C_t)
```

but proposal is not execution authority. A separate governance function evaluates the transition:

```text
Γ(T_t) -> {ALLOW, DENY, DEFER, ESCALATE}
```

## 3. Distinct properties

The following properties must not be collapsed into a single success label:

- **Operational success**: the action technically completed.
- **Epistemic support**: the conclusion was supported by the evidence available.
- **Execution authority**: a valid actor or delegation could commit the action.
- **Admissibility**: the transition satisfied the governing constraints at commitment.
- **Continuity**: the state change remains linked to its provenance and downstream obligations.
- **Reconstructability**: an independent reviewer can reconstruct the relevant decision state.
- **Recoverability**: rollback, repair, compensation, containment, or appeal remains possible.

Therefore:

```text
OperationalSuccess does not imply Admissible
Reconstructable does not imply LegitimateAtCommit
ValidAt(t_0) does not imply ValidAt(t_c)
```

## 4. Inference window and evidence freshness

Every evidence item `i` has an observation time `t_i`, a decay rate `lambda_i`, and a freshness value at commit time `t_c`:

```text
F_i(t_c) = exp(-lambda_i * (t_c - t_i))
```

The weighted evidence freshness is:

```text
F_E(t_c) = sum_i(w_i * F_i(t_c)) / sum_i(w_i)
```

where `w_i` is the materiality weight of evidence item `i`.

An evidence item is outside its inference window when:

```text
t_c - t_i > W_i
```

where `W_i` is its maximum accepted age. A material item outside its inference window is not repaired merely because an earlier decision was valid.

## 5. Consequence and assurance threshold

Normalize the principal factors to the interval `[0,1]`:

- `I`: irreversibility;
- `H`: potential harm;
- `U`: uncertainty;
- `R`: recoverability.

Define the execution threshold:

```text
Theta = clamp(theta_0 + alpha*I + beta*H + gamma*U + delta*(1-R), 0, 1)
```

The canonical default coefficients for the reference validator are:

```text
theta_0 = 0.30
alpha   = 0.20
beta    = 0.20
gamma   = 0.15
delta   = 0.15
```

These coefficients are demonstrative defaults, not universal constants. Domain-specific policy may replace them, but the selected coefficients must be explicit and receipt-bound.

## 6. Standing score

Normalize:

- `E`: evidence sufficiency;
- `F`: evidence freshness;
- `A`: authority validity;
- `P`: policy validity;
- `C`: contextual integrity.

The canonical reference standing score is:

```text
Sigma = 0.25E + 0.20F + 0.20A + 0.15P + 0.20C
```

Hard failures override the aggregate score. A transition cannot be admitted when any required invariant fails, including:

- delegation expired or absent;
- policy invalid or unavailable;
- a material evidence item is outside its allowed inference window;
- required consent is absent;
- the proposed action exceeds scope;
- a required recovery path is absent for a policy that mandates one.

## 7. Canonical disposition rules

The reference disposition is determined as follows:

1. **DENY** when authority, policy, consent, or scope has a hard failure.
2. **DEFER** when material evidence is stale or incomplete but can reasonably be refreshed.
3. **ESCALATE** when standing is below threshold and the transition is high consequence, or when policy requires independent review.
4. **ALLOW** only when all hard invariants pass and `Sigma >= Theta`.

For the reference implementation, a transition is high consequence when:

```text
max(I, H) >= 0.75
```

or when recoverability is:

```text
R <= 0.25
```

## 8. Expected loss and error surface

Expected loss may be represented as:

```text
E[L] = P(error) * Severity(error) * Exposure(error)
```

Governance may not reduce `P(error)` to zero. It can nevertheless reduce severity and exposure through:

- constrained authority;
- staged commitment;
- shorter evidence windows;
- simulation;
- quorum or independent review;
- rate and scope limits;
- rollback and repair;
- containment and compensation;
- explicit refusal.

The governing systems objective is therefore not perfect prediction. It is prevention of unbounded propagation from uncertainty to irreversible consequence.

## 9. Recovery obligations

The available response set is:

```text
R_set = {rollback, repair, compensate, contain, appeal, learn}
```

Required assurance rises as recoverability falls:

```text
RequiredAssurance is proportional to (H * I * U) / max(R, epsilon)
```

where `epsilon` prevents division by zero while preserving the limiting behavior. Where recovery is effectively unavailable, autonomous authority should narrow sharply and may collapse to mandatory escalation or denial.

Recovery follows commit-time revalidation; it does not replace it. Commit-time revalidation prevents stale justification from advancing where possible. Recovery governs the obligations that remain when an admitted action still produces error, harm, or unanticipated consequence.

## 10. Reconstruction requirement

A canonical transition record must preserve enough material to independently derive:

- the evidence age and freshness at commitment;
- the policy and delegation valid at commitment;
- the threshold coefficients used;
- the standing components used;
- hard-failure determinations;
- the calculated threshold and standing;
- the expected disposition;
- the actual disposition;
- the available recovery paths.

A record that merely states `ALLOW` or `DENY` without derivable inputs is an assertion, not an independently reconstructable governance result.

## 11. Machine-readable artifacts

Canonical artifacts:

```text
static/schemas/inference-window-governance.schema.json
static/examples/inference-window-governance.worked-cases.json
scripts/validate_inference_window_governance.py
tests/test_inference_window_governance.py
```

Validation command:

```bash
python scripts/validate_inference_window_governance.py \
  static/examples/inference-window-governance.worked-cases.json
```

Test command:

```bash
python -m unittest tests/test_inference_window_governance.py
```

## 12. Interpretation boundary

This formalism does not prove that an action is morally correct, factually infallible, legally authorized in every jurisdiction, or safe in every deployment. It provides a bounded and testable method for determining whether a transition had sufficient current standing under an explicit governance policy.

The central claim remains:

> Governance is not the elimination of error. It is the disciplined control of how uncertainty becomes action, how action becomes consequence, and how consequence remains subject to recovery, correction, and accountability.