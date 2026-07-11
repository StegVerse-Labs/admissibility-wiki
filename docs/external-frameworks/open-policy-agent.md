---
title: Open Policy Agent
---
# Open Policy Agent

## Evidence posture
`sourced_intake` — canonical official documentation captured; no StegVerse runtime observation is claimed.

## Published scope
Open Policy Agent is a general-purpose policy engine that evaluates structured input against policy and produces policy decisions.

Canonical source: https://www.openpolicyagent.org/docs/latest/

## StegVerse relationship
`adjacent`

OPA can contribute a policy-decision artifact to a governed transition path. That decision is evidence about policy evaluation; it is not execution authority.

```text
OPA input + policy -> policy decision
policy decision -> Commitment Candidate evidence
SPE -> reconstruct current standing
```

## Benchmark relevance
`commitment_boundary`, `authority_boundary`, `unknown_trajectory_boundary`, `interoperability_path`

## Non-claims
OPA inclusion is not certification, equivalence, admissibility proof, or StegVerse standing. A policy allow result does not independently authorize consequence binding.
