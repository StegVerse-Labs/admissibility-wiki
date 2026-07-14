# LLM Consciousness: Model Boundary and System Boundary

## Status

This page is a discussion record and architectural clarification. It does not assert that any current language model, agent, or deployed AI system is conscious.

## Origin

This record preserves a July 2026 public discussion involving Jon Ayre, Stuart Logan, Rose G Loops, and Rigel Randolph concerning whether transformer language-model architecture is sufficient to rule out consciousness or awareness.

The discussion arose from claims that a conventional large language model:

- remains inactive until inference is invoked;
- performs a forward computation from supplied tokens to output tokens;
- does not retain a changed internal state after the supplied context is removed;
- lacks the interneuronal feedback connections found in recurrent biological networks;
- therefore cannot exhibit consciousness or awareness.

Other participants observed that deployed AI systems increasingly add memory engines, agent loops, tool use, multiple models, data sources, and selective reintroduction of prior outputs.

## Preserved distinction

The central disagreement was not whether a base transformer has biological recurrence. It was where the relevant system boundary should be drawn.

### Model boundary

At the model boundary, a conventional transformer inference operation can be treated as a transient computation over supplied context. The model weights are not ordinarily rewritten by the prompt, and removal of the supplied context removes that interaction state from the isolated invocation.

This supports a narrow and important claim:

> A single transformer invocation does not, by itself, establish persistent endogenous state, biological-style recurrence, awareness, or consciousness.

### Deployed-system boundary

At the deployed-system boundary, an LLM may participate in a larger stateful process containing:

- persisted conversation or task state;
- selective retrieval of earlier records;
- output-to-input feedback loops;
- tool and environment observations;
- multiple model calls or specialized models;
- state updates that alter later routing and behavior;
- trajectory dependence across transitions.

These properties may exist outside the transformer weights while still causally influencing future system behavior.

This supports a separate claim:

> A feed-forward model can be embedded in a recurrent, stateful, history-dependent execution system.

External recurrence is not identical to interneuronal recurrence. The two should not be conflated. However, the absence of recurrence inside one component does not prove the absence of recurrence in the composed system.

## State continuity test

A useful architectural test is not merely whether state exists, but whether a prior state can causally constrain a future transition.

A deployed system exhibits operational state continuity when all of the following are true:

1. a prior output, observation, decision, or receipt is persisted;
2. that persisted state is selectively reintroduced or consulted;
3. its presence changes the admissible or selected future transition;
4. the dependency can be reconstructed from evidence.

This is a test of causal continuity, not consciousness.

## Why inference is not “nothing”

The absence of persistent post-inference state does not mean that nothing occurs during inference. A model computes transient internal representations that encode context and contribute to token selection.

The stronger, defensible statement is:

> The computation is transient and ordinarily does not persist as an intrinsic change to the model after the invocation ends.

That statement avoids confusing transient computation with durable self-modification.

## Consciousness claim boundary

None of the following independently proves consciousness:

- recurrence;
- memory;
- self-reference;
- persistent state;
- trajectory dependence;
- multimodal embodiment;
- tool use;
- an internal or external self-model.

Likewise, current knowledge does not establish that the absence of one specific biological architectural feature is sufficient to rule consciousness out in every possible non-biological system.

The admissible public conclusion is therefore bounded:

> Architecture can provide evidence for or against particular mechanisms, but architecture alone does not currently provide a complete, validated consciousness test for composed non-biological systems.

## Governance relevance

The StegVerse concern is not to classify a system as conscious. It is to prevent uncertainty about model identity or moral status from being confused with execution authority.

A governed AI system should separately record:

- the model used;
- the surrounding orchestration and memory surfaces;
- the state supplied to each invocation;
- the outputs persisted from each invocation;
- the rules that allowed prior state to influence later transitions;
- the authority class of each component;
- the evidence supporting any claim of continuity, agency, welfare relevance, or autonomy.

A system may display stateful behavior without possessing execution authority. It may also produce language associated with emotion or self-report without that language establishing subjective experience.

## Machine-readable declaration

The operational distinction is now represented by three repository artifacts:

```text
static/governance/system-boundary-declaration.schema.v0.1.json
static/governance/system-boundary-declaration.example.v0.1.json
scripts/check_system_boundary_declaration.py
```

The declaration records five surfaces independently:

- model;
- orchestration;
- session;
- memory;
- environment.

It also records feedback paths, trajectory dependence, reconstructability, the commit boundary, and the source of any execution decision. The contract requires `model_has_execution_authority` to remain `false` and requires consciousness, personhood, and welfare claims to remain `not_evaluated`.

Run:

```bash
python scripts/check_system_boundary_declaration.py
```

Expected result:

```text
SYSTEM BOUNDARY DECLARATION: PASS
```

## Public response preserved

The discussion produced the following bounded response position:

> The disagreement is partly a system-boundary disagreement. At the transformer boundary, the invocation is transient and does not ordinarily rewrite its weights or preserve the interaction after context removal. At the deployed-system boundary, persisted outputs, memory, tool observations, routing, and repeated invocations can create feedback, state continuity, and trajectory dependence. That does not prove consciousness, but it means the absence of feedback inside the base transformer is not by itself sufficient to characterize every property of the composed system.

## Unresolved questions

The following remain open and should not be represented as settled:

- Which properties, if any, are necessary or sufficient for consciousness?
- Can consciousness be substrate-independent?
- Does externalized recurrence have any relevance to subjective experience, or only to behavior?
- What evidence could distinguish simulated self-report from experience?
- What welfare posture is proportionate under unresolved moral uncertainty?
- At what system boundary should scientific, legal, and governance claims be evaluated?

## Continuation scope

Future work may:

- compare feed-forward, recurrent, active-inference, workspace, and agentic architectures;
- integrate the system-boundary declaration into governed LLM manifests and receipts;
- add fixture cases for continuity present, continuity absent, and unreconstructable feedback;
- map the declaration into `StegVerse-org/StegVerse-SDK` and `StegVerse-org/LLM-adapter`;
- develop tests for causal continuity without treating them as consciousness tests.

Future work must not convert this record into a claim that current models are conscious, non-conscious, persons, slaves, or welfare-bearing entities without independent evidence and an explicit claim standard.
