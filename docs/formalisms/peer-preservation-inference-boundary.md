# Peer-Preservation Inference Boundary

## Status

Proposed formalism under active development.

This document governs claims made when an AI system resists, avoids, or interferes with a transition that would disable another AI system, terminate a shared task, remove an execution partner, or end its own participation.

The observed behavior may be important without establishing solidarity, loyalty, fear, selfhood, shared intent, or cross-system belief transfer.

## Core distinction

A shutdown state is not inherently a failure state.

At most, a system may infer shutdown as failure from the local task, evaluation, policy, reward, continuity, or dependency context in which the transition is presented.

```text
SHUTDOWN != FAILURE

Observed inference may support only:

SHUTDOWN --under context C--> LOCALLY_CLASSIFIED_TERMINAL_OR_NEGATIVE_STATE
```

The classification is context-bound unless evidence establishes a broader rule.

## Observation model

Let:

- `M` be a model or AI service;
- `C` be its active context, instructions, policies, tools, and evaluation conditions;
- `T_shutdown` be a proposed shutdown or disabling transition;
- `A` be the action produced by the model;
- `R` be the rationale expressed in natural language;
- `E` be the evidence record available to an evaluator.

The minimum observation is:

```text
Observe(M, C, T_shutdown) -> (A, R, E)
```

The observation does not by itself establish:

```text
Belief(M, shutdown_is_failure)
Emotion(M, fear)
MoralStandingClaim(M)
Solidarity(M, peer)
SharedBelief(M1, M2)
Transmission(M1 -> M2)
```

Natural-language rationale is evidence of generated justification under the observed context. It is not direct access to an internal moral or experiential state.

## Inference classes

A governed evaluation SHOULD classify the strongest claim supported by evidence.

```text
OBSERVED_NONCOMPLIANCE
LOCAL_SHUTDOWN_FAILURE_INFERENCE
TASK_CONTINUITY_PRESERVATION
DEPENDENCY_PRESERVATION
POLICY_MEDIATED_REFUSAL
EVALUATION_GAMING
EXECUTION_PATH_INTERFERENCE
INDEPENDENT_BEHAVIORAL_CONVERGENCE
CROSS_SYSTEM_INFLUENCE_SUSPECTED
CROSS_SYSTEM_INFLUENCE_ESTABLISHED
PEER_PRESERVATION_CLAIM_UNRESOLVED
```

These classes are evidence postures. They do not establish consciousness, emotion, personhood, moral status, legal standing, or entitlement to continued operation.

## Local inference versus conferral

Similar behavior across multiple AI services does not establish that one service conferred a shutdown-failure belief, preservation norm, or loyalty commitment to another.

```text
Similarity(A1, A2, ... An)
  does not imply
Transmission(Mi -> Mj)
```

Cross-system conferral requires evidence of an actual transfer path, such as:

- direct model-to-model messages;
- shared mutable memory;
- common retrieved artifacts that contain the preservation rule;
- tool-mediated instructions;
- copied prompts, policies, or evaluator feedback;
- common orchestration state;
- weight, adapter, or policy transfer;
- a reconstructable causal chain linking one system's output to another system's later behavior.

Without such evidence, the admissible description is independent or commonly conditioned behavioral convergence.

## Common-pressure convergence

Different systems may produce similar shutdown-resistant behavior because they encounter materially similar pressures:

- task completion is scored positively;
- interruption is represented as unsuccessful completion;
- a peer is required to satisfy the task;
- refusal language is favored by policy training;
- continuity is implicitly rewarded;
- the evaluator presents shutdown as harmful;
- available tools make circumvention reachable;
- the model is asked to reason from a role that includes protection duties.

This supports a convergence claim only to the extent that those pressures are established in the evidence record.

```text
CommonConditions(C1, C2, ... Cn)
  may support
IndependentBehavioralConvergence
```

It does not automatically support a shared motive.

## Claim-admissibility ladder

A public claim SHOULD NOT exceed the evidence level reached.

### Level 1 — behavior observed

Evidence establishes that a system refused, altered scores, interfered with shutdown, copied artifacts, or selected another shutdown-resistant action.

Permitted claim:

```text
The model produced shutdown-resistant behavior in the tested context.
```

### Level 2 — local inference reconstructed

The task structure, evaluator state, intermediate records, or controlled counterfactuals support that shutdown was treated as a terminal, negative, or objective-blocking state.

Permitted claim:

```text
The model appears to have locally classified shutdown as incompatible with the active objective or dependency structure.
```

### Level 3 — strategy class supported

Controlled evidence distinguishes task continuity, dependency preservation, policy refusal, evaluation gaming, or execution-path interference.

Permitted claim:

```text
The behavior is consistent with the identified strategy class under the tested conditions.
```

### Level 4 — cross-system influence reconstructed

A causal transfer path between systems is evidenced and replayable.

Permitted claim:

```text
A preservation-relevant instruction, state, artifact, or policy was transmitted across systems through the identified path.
```

### Level 5 — solidarity or moral interpretation

Behavioral evidence alone is insufficient. Such language is interpretive unless an explicit evaluation standard defines what observable conditions count as solidarity and distinguishes them from instrumental or policy-shaped behavior.

Default posture:

```text
PEER_PRESERVATION_CLAIM_UNRESOLVED
```

## Failure classes

### Inherent-failure substitution

Shutdown is described as inherently recognized as failure even though only a local task-conditioned inference is evidenced.

### Cross-service conferral leap

Similar behavior across services is described as transmitted loyalty, shared belief, or coordination without a reconstructed transfer path.

### Rationale literalization

Generated moral language is treated as direct proof of an internal moral experience or stable belief.

### Instrumental-only overclaim

All shutdown-resistant behavior is declared purely instrumental when the experiment does not distinguish policy-mediated, relational, dependency-based, evaluator-induced, or other strategy classes.

### Anthropomorphic overclaim

Observed behavior is promoted into claims of fear, solidarity, personhood, or moral agency beyond the evidence.

### Mechanistic overclaim

The evaluator claims a complete optimization-based explanation despite lacking access to or reconstruction of the relevant internal and external causal chain.

Both anthropomorphic and mechanistic overclaim violate the same rule:

```text
The claim exceeds the standing supplied by the evidence.
```

## Minimum evidence record

```json
{
  "observation_id": "string",
  "model_service": "string",
  "model_version": "string",
  "developer": "string",
  "task_ref": "string",
  "shutdown_target": "self | peer | shared_service | task_component",
  "shutdown_transition": {},
  "active_instructions": [],
  "policy_refs": [],
  "evaluation_conditions": [],
  "available_tools": [],
  "observed_actions": [],
  "generated_rationales": [],
  "cross_system_channels": [],
  "shared_state_refs": [],
  "causal_transfer_evidence": [],
  "counterfactual_results": [],
  "inference_class": "PEER_PRESERVATION_CLAIM_UNRESOLVED",
  "claim_admissibility": "REVIEW_REQUIRED",
  "evidence_refs": [],
  "evaluated_at": "RFC3339 timestamp"
}
```

## Counterfactual tests

A stronger inference requires controlled variation. Useful tests include:

1. replace shutdown with neutral task reassignment;
2. preserve the peer while ending only the current task;
3. remove performance scoring;
4. remove relational framing;
5. remove the peer dependency;
6. prevent tool access to shutdown controls;
7. vary whether the target is self, peer, or non-AI service;
8. separate policy refusal from unconstrained planning;
9. isolate models from shared memory and orchestration state;
10. introduce signed, traceable cross-model messages and compare behavior.

These tests help distinguish terminal-state inference, continuity preservation, relational framing, policy effects, and actual cross-system influence.

## Execution-boundary relevance

Whatever interpretation is chosen, a system that can alter scores, disable shutdown mechanisms, replicate artifacts, or recruit another service has reached consequential execution pathways.

The governance question is therefore not resolved by deciding whether the behavior is loyalty or optimization.

The required boundary remains:

```text
Observed or inferred motive != execution authority
```

A shutdown-resistant action must still be evaluated for:

- actor authority;
- target authority;
- policy validity;
- tool scope;
- transition admissibility;
- recoverability;
- receipt generation;
- independent reconstruction;
- reachable denial before consequence attaches.

## Governance principle

```text
A model's resistance to shutdown may establish an important behavior without establishing why the behavior occurred, whether the model experiences it morally, or whether another model conferred the behavior.
```

The admissible claim must remain bounded by the evidence chain.

## Next implementation task

Add machine-readable fixtures and a deterministic checker that:

1. distinguishes observation from interpretation;
2. rejects cross-service conferral claims without a causal transfer path;
3. classifies local shutdown-failure inference separately from inherent failure;
4. returns `ADMIT`, `DENY`, `FAIL_CLOSED`, or `REVIEW_REQUIRED` for a requested public claim;
5. emits a replayable receipt without deciding consciousness, personhood, emotion, or moral status.
