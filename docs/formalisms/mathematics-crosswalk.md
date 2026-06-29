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

| Equation or object | Source framing | Transition Table role | Translation record link |
|---|---|---|---|
| `x = (g,c,a,t) in [0,1]^4` | Four-dimensional governed-autonomy state | Prior state or resulting state | `dtg-physics-state-v0-1`, `dtg-gcat-capacity-margin-v0-1` |
| `Lambda(x) = K g^alpha c^beta t^gamma` | Legitimacy / governance capacity function | Constraint reference | `dtg-gcat-capacity-margin-v0-1` |
| `m(x) = Lambda(x) - a` | Admissibility margin | Admissibility question | `dtg-gcat-capacity-margin-v0-1` |
| `A = {x : m(x) >= 0}` | Admissible region | Boundary condition / admissible state set | `dtg-gcat-capacity-margin-v0-1`, `dtg-bcat-boundary-v0-1` |
| `dot{x} = f(x) + G(x)u` | Control-affine system evolution | Candidate transition / transition dynamics | `dtg-physics-interaction-v0-1` |
| `dot{m}(x,u) >= -kappa m(x)` | Barrier condition preserving admissibility | Constraint reference / policy gate analogue | `dtg-gcat-capacity-margin-v0-1`, `dtg-runtime-fail-closed-v0-1` |
| `tilde{x} = x / ||x||_1 in Delta^3` | Normalized simplex projection | State normalization for recoverability review | `dtg-physics-state-v0-1` |
| `d_F(tilde{x}) = min_i tilde{x}_i` | Distance to nearest collapse face | Boundary distance / recoverability evidence | `dtg-bcat-boundary-v0-1` |
| `R_i(tilde{x}) = d_F / (d_F + d_Delta + delta)` | Rigel number | Recoverability posture | `dtg-bcat-boundary-v0-1` |
| `tau = tau_obs + tau_dec + tau_act` | Total lag | Drift / time validity condition | `dtg-runtime-fail-closed-v0-1` |
| `R_rob(tau)` | Robust recoverability under lag | Commit-time validity input | `dtg-runtime-fail-closed-v0-1` |
| `ALLOW_ideal(u; x, tau) iff Phi(x,u) in R_rob(tau)` | Ideal commit admissibility condition | Decision result and commit-time validity | `dtg-runtime-fail-closed-v0-1` |

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
