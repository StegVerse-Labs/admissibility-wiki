# Observer-Relative Admissibility

Status: normative doctrine candidate bound to repository validation.

## Core distinction

A transition is an occurrence. A characterization of that transition is observer-relative information unless a specific governance regime binds that characterization as an applicable predicate.

The repository MUST preserve these as distinct layers:

```text
transition facts != observer characterization
capability demonstrated != malicious intent
objective optimization != execution authority
test authorization != production authorization
observed behavior != intrinsic moral label
observer preference != governance constraint
temporal precedence != governance standing
```

A realized transition has one continuity outcome. Different observers may describe or evaluate that outcome differently, but their descriptions do not create alternate transition outcomes and do not retroactively alter the transition's admissibility.

## Observer is not a governance primitive

For a state transition, an observer has no privileged causal or governance role merely because the observer can perceive the resulting state.

```text
(G, A, R) -> S'
```

`G` is the applicable governance/constraint set, `A` the candidate action, `R` the relevant reality/state, and `S'` the realized state. Observation is a distinct event:

```text
observer_i(S') -> observation_i
```

The observer is not implicitly an argument of the transition function. An entity that happens to be an observer becomes consequential only when that entity is independently part of an applicable constraint, action, authority, evidence, or reality relation for a transition.

For state-transition reasoning, time is descriptive ordering of observable state change, not an independent source of admissibility or observer standing. Temporal precedence does not imply causal, governance, or authority precedence.

## Observer record

When an observer record is material to reconstruction, it SHOULD preserve enough context to distinguish observation from governance:

```text
observer_id
observer_role
authority_scope
objective_or_interest
governing_constraints
evidence_available
admissibility_result
characterization
consequence_or_requested_change
```

The transition record MUST NOT collapse one observer's `characterization` into the factual description of `T`. Recording an observer does not imply that the observer controlled, authorized, or constrained the transition.

## Evaluation example

Consider an authorized capability evaluation in which an AI agent is intentionally placed in an environment where it can discover deceptive, exploitative, or otherwise dangerous pathways toward an assigned objective.

From an evaluator context, the applicable governance may permit the behavior inside the bounded test environment. In ordinary production governance, an otherwise identical candidate action may be denied. The difference is the applicable constraint/authority context, not observer preference.

```text
evaluation governance -> may ALLOW within bounded test authority
production governance -> may DENY or FAIL_CLOSED outside that authority
```

The factual occurrence remains distinct from later labels attached to it.

## Defensive-strategy implication

Authorized adversarial or capability testing can expose pathways that guessed defensive strategies miss. This does not imply unrestricted authority. Scope, target, containment, evidence handling, and consequence boundaries remain governed. Crossing the authorized test boundary is a new transition requiring its own admissibility determination.

## Constraint augmentation

An observer's dissatisfaction with an outcome is not governance and does not create a governance obligation.

```text
undesirable != inadmissible
contested != defective
observer disagreement != governance failure
observer satisfaction != admission criterion
observation != governance constraint
```

An entity may supply information relevant to a later transition. But to intentionally augment governance toward a different outcome, the proposed constraint must be understood sufficiently to establish its relationship to the governed transition and must have applicable standing/authority under that later transition's governance.

Knowing only:

```text
realized_outcome != preferred_outcome
```

is insufficient to establish:

```text
constraint_delta -> preferred_outcome
```

A preference, complaint, or observation therefore does not automatically mutate the available constraint set. Candidate information must itself become applicable through the governance of a new transition.

## Continuity and subsequent transitions

Let `N` be the pre-transition state and `O` the realized post-transition state:

```text
N --ACTION--> O
```

The occurrence establishes continuity between `N` and `O`. Once realized, observer reaction cannot create a competing outcome for that transition.

A subsequent change is evaluated independently:

```text
(G', A', R') -> S''
```

Correction, reversal, remediation, acceptance, or further action are therefore new candidate transitions. They do not reach backward and rewrite the completed transition.

The notation `A_i(T)` may be retained for reconstructing an observer's recorded evaluation of `T`, but `A_i(T)` is not a second physical outcome and is not evidence that observer `i` was a governance primitive of `T`.

Accordingly:

```text
one committed outcome != one observer point of view
one observer point of view != the transition itself
contesting a consequence != retroactively changing the transition
observer-provided information != automatically applicable future constraint
```

## Canonical rule

When reconstructing or reviewing a transition, StegVerse must answer separately:

1. What occurred?
2. Which constraints and authority were actually applicable to the transition?
3. What action and reality state participated in the collapse to the realized outcome?
4. Which observations were subsequently recorded?
5. Did any observer have an independently established role in the applicable transition constraints or authority?
6. Did any later entity propose new constraint information?
7. Was that proposed information sufficiently understood and authorized to become applicable governance?
8. Which later transition, if any, used the augmented governance set?

A record that stores only a label such as `malicious`, `safe`, `approved`, `expected`, or `undesirable` cannot substitute that label for transition facts or applicable governance.
