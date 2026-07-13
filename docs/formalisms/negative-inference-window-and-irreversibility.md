# Negative Inference Windows and Practical Irreversibility

## Canonical source

```text
source_repository: Admissible-Existence/IW
source_commit: 87fd24ea829b413373ea42381dd0b08d45b79239
canonical_markdown: docs/irreversibility.md
publication_pdf: docs/irreversibility.pdf
authority: false
```

This page is an admissibility reference to the IW formalism. It does not supersede the canonical source or create an independent execution rule.

## Negative inference window

A negative inference window is the interval in which a system can still observe and infer an approaching irreversible boundary, but the remaining time may already be insufficient to authorize and complete an effective intervention.

```text
W^- = [t_d, t_c]
```

where `t_d` is the time a material deviation becomes detectable and `t_c` is the latest safe decision point.

## Conservative latest safe decision

```text
t_i^- = expected_irreversibility - confidence_multiplier × uncertainty
L_total = sense + transmit + infer + authorize + actuate + stabilize
t_c = t_i^- - L_total
```

Uncertainty contracts the safe execution window. It must not expand standing near commitment.

## Admissibility warrants

A consequence-bearing transition requires all of the following:

```text
physical warrant
governance warrant
recoverability warrant
observability warrant
```

A recovery path contributes to admissibility only when it is:

```text
physically available
AND authorized
AND evidentially supported
AND current
AND executable within the remaining recovery time
```

## Decision posture

```text
ALLOW: all warrants and recovery margins hold
WARN: intervention remains possible but margins are degrading
STOP: practical recovery is no longer available
FAIL_CLOSED: required evidence or warrant is absent, malformed, stale, or inconsistent
```

## Canonical references

- `https://github.com/Admissible-Existence/IW/blob/main/docs/irreversibility.md`
- `https://github.com/Admissible-Existence/IW/blob/main/docs/irreversibility.pdf`

## Boundary

```text
Reference != certification
Inference != authorization
Physical possibility != governance standing
Publication != destination completion
```

The admissibility-wiki preserves source attribution and the `authority: false` boundary.
