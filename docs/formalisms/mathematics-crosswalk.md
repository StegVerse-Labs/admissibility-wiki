---
title: Mathematics Crosswalk
---

# Mathematics Crosswalk

## Status

Wiki state: intake

Source posture: public-safe crosswalk from published or mirrored GCAT / BCAT equation forms into Transition Table roles

Authority boundary: this page explains mappings. It does not prove the equations, validate parameters, replace source papers, or create commit-time authority.

## Purpose

The Mathematics Crosswalk identifies selected mathematical objects from GCAT / BCAT-related papers and maps them into Transition Table roles.

The crosswalk exists so mathematical terms can be related to state-transition governance without silently turning analogy into equivalence.

## Core Equation Crosswalk

The expressions below are written in MDX-safe plain text so the site renderer does not evaluate mathematical braces as JavaScript.

| Equation or object | Source framing | Transition Table role | Translation record link |
|---|---|---|---|
| state vector x = tuple(g, c, a, t) within unit interval to the fourth power | Four-dimensional governed-autonomy state | Prior state or resulting state | `dtg-physics-state-v0-1`, `dtg-gcat-capacity-margin-v0-1` |
| Lambda of x = K times g^alpha times c^beta times t^gamma | Legitimacy / governance capacity function | Constraint reference | `dtg-gcat-capacity-margin-v0-1` |
| margin m of x = Lambda of x minus a | Admissibility margin | Admissibility question | `dtg-gcat-capacity-margin-v0-1` |
| admissible region A = states where margin is greater than or equal to zero | Admissible region | Boundary condition / admissible state set | `dtg-gcat-capacity-margin-v0-1`, `dtg-bcat-boundary-v0-1` |
| time derivative of x = f of x plus G of x times control u | Control-affine system evolution | Candidate transition / transition dynamics | `dtg-physics-interaction-v0-1` |
| time derivative of margin under x and u is bounded below by negative kappa times margin | Barrier condition preserving admissibility | Constraint reference / policy gate analogue | `dtg-gcat-capacity-margin-v0-1`, `dtg-runtime-fail-closed-v0-1` |
| normalized x = x divided by L1 norm of x, projected into Delta cubed | Normalized simplex projection | State normalization for recoverability review | `dtg-physics-state-v0-1` |
| face distance of normalized x = minimum component of normalized x | Distance to nearest collapse face | Boundary distance / recoverability evidence | `dtg-bcat-boundary-v0-1` |
| Rigel number R_i of normalized x = face distance divided by face distance plus Delta distance plus delta | Rigel number | Recoverability posture | `dtg-bcat-boundary-v0-1` |
| total lag tau = observation lag plus decision lag plus action lag | Total lag | Drift / time validity condition | `dtg-runtime-fail-closed-v0-1` |
| robust recoverability under lag R_rob of tau | Robust recoverability under lag | Commit-time validity input | `dtg-runtime-fail-closed-v0-1` |
| ideal ALLOW predicate for u, x, and tau holds when Phi of x and u is in robust recoverability under tau | Ideal commit admissibility condition | Decision result and commit-time validity | `dtg-runtime-fail-closed-v0-1` |

## Physics Translation Boundary

Some mathematical objects resemble physics language: state, dynamics, interaction, horizon, lag, collapse, and recoverability.

This crosswalk allows those words to be mapped into transition roles only under a non-claim boundary:

```text
A mathematical object may be translated into a Transition Table role.
That translation does not prove the source discipline claim.
That translation does not make governance mathematics identical to physics.
That translation does not create a new physical theory.
```

## First-Pass Interpretation

```text
state equation -> prior/resulting state
capacity equation -> constraint reference
margin equation -> admissibility question
barrier inequality -> policy-gate analogue
simplex distance -> boundary/recoverability evidence
lag equation -> drift/time-validity input
commit predicate -> decision result and commit-time validity
```

## Required Evidence Before Promotion

A crosswalk row should remain `intake` until it has:

1. a source equation or object;
2. a public-safe source reference;
3. a Transition Table role;
4. at least one translation record ID;
5. a non-claim boundary; and
6. a review posture.

## Next Build Target

The next build target is a machine-readable mathematics crosswalk JSON artifact and a validator connecting crosswalk rows to existing translation record IDs.

## Non-Claims

This page does not validate GCAT / BCAT equations, prove physical interpretation, establish source-discipline equivalence, or authorize any transition. It is a public-safe crosswalk for review and later validation.
