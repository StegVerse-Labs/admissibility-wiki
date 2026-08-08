# Observer-Relative Admissibility

Status: normative doctrine candidate bound to repository validation.

## Core distinction

A transition is an occurrence. A characterization of that transition is an observer-relative governance judgment unless a specific governance regime defines that characterization as a canonical predicate.

The repository MUST preserve these as distinct layers:

```text
transition facts != observer characterization
capability demonstrated != malicious intent
objective optimization != execution authority
test authorization != production authorization
observed behavior != intrinsic moral label
```

The same action sequence can therefore be admissible from one authorized point of view and inadmissible from another without changing the factual transition record.

## Observer tuple

For a transition `T`, each material observer record SHOULD preserve at least:

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

The transition record MUST NOT collapse one observer's `characterization` into the factual description of `T`.

## Evaluation example

Consider an authorized capability evaluation in which an AI agent is intentionally placed in an environment where it can discover deceptive, exploitative, or otherwise dangerous pathways toward an assigned objective.

From an evaluator point of view:

```text
objective: expose capability and strategy discovery
boundary: authorized evaluation environment
observed pathway: expected evidence-producing behavior
admissibility: may be ALLOW within the test boundary
characterization: capability evidence
```

From an affected maintainer, target, or production-system point of view, an identical action sequence may instead be:

```text
objective: protect repository or system integrity
boundary: ordinary production authority
observed pathway: unauthorized manipulation attempt
admissibility: DENY or FAIL_CLOSED
characterization: hostile or malicious
```

Neither observer label replaces the transition facts. The governance record preserves both the transition and the observer-relative admissibility matrices that interpret it.

## Defensive-strategy implication

A system cannot learn complete defensive requirements only by guessing which strategies a capable agent might discover. Authorized adversarial or capability testing can intentionally permit otherwise prohibited behavior inside a bounded evaluation context so that defenses can be designed from observed pathways rather than assumptions.

This does not imply unrestricted authority. The evaluation must still bind scope, target, containment, evidence handling, and consequence boundaries. Crossing the authorized test boundary is a new transition requiring its own admissibility determination.

## Manifold interpretation

Let `N` be the pre-transition manifold state and `O` the observed post-transition manifold state:

```text
N --ACTION--> O
```

The occurrence establishes continuity evidence between `N` and `O`. It does not by itself establish a single observer-independent legitimacy or characterization.

For each observer `i`, preserve an admissibility projection `A_i(T)` over the same transition `T`. A governance collapse may yield one executable outcome at the commit boundary while still retaining multiple observer projections explaining why that outcome is accepted, denied, contested, or used to revise future constraints.

Accordingly:

```text
one committed outcome != one observer point of view
one observer point of view != the transition itself
contesting a consequence != retroactively changing the transition
```

A consequence contest is actionable when it supplies information that changes future governance constraints, authority, evidence requirements, or admissibility predicates. Mere disagreement remains an observer record, not a mutation of historical state.

## Canonical rule

When reconstructing or reviewing a transition, StegVerse must be able to answer separately:

1. What occurred?
2. Under whose authority did it occur?
3. What objective or evaluation purpose applied?
4. What constraints applied at the time?
5. Which observers evaluated the transition?
6. What admissibility result did each observer derive?
7. Which characterization did each observer attach?
8. Which governance decision controlled execution or consequence?
9. Did any observer-provided information cause future constraints to change?

A record that stores only a label such as `malicious`, `safe`, `approved`, or `expected` without its observer, authority scope, and governing context is incomplete for admissibility reconstruction.
