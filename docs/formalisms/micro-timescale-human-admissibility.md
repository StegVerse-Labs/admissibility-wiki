# Micro-Timescale Human Admissibility

## Claim

Human conversation can exhibit an admissibility gate at the shortest practical timescale of human-human interaction.

A speaker forms an intended referent, emits a candidate utterance, observes the listener's response, and adjusts the signal until the listener's reconstructed meaning becomes sufficiently aligned with the speaker's intent for consequential response to begin.

The gate does not cross merely because sound was emitted, received, or recognized. It crosses when the available evidence supports an interpretation strongly enough to permit the next interaction state.

## Human Example

A young child repeats one word several times. Each repetition differs slightly in pronunciation. The caregiver's facial expression, gaze, posture, cadence, response delay, and emerging action reveal whether the intended referent has been reconstructed.

The child stops repeating at the moment the caregiver demonstrates understanding.

This is not merely repetition. It is a coupled corrective loop in which:

```text
intent
  -> candidate vocalization
  -> listener reconstruction
  -> listener feedback
  -> speaker-side gate-state estimation
  -> candidate correction
  -> admissibility crossing
  -> consequential response
```

## State Distinctions

The model separates six states:

1. `EMITTED`: a signal exists.
2. `RECEIVED`: the listener detected the signal.
3. `RECOGNIZED`: the listener classified some linguistic or referential structure.
4. `INTERPRETED`: the listener formed a candidate meaning.
5. `ADMISSIBLE`: the candidate meaning has sufficient evidence and standing for response.
6. `COMMITTED`: the listener begins a consequential response based on the admitted interpretation.

These states must not be collapsed.

```text
emitted != received
received != recognized
recognized != interpreted
interpreted != admissible
admissible != committed
```

## Variables

Let:

- \(I\) be the speaker's intended referent or communicative goal.
- \(u_n\) be the candidate utterance at correction step \(n\).
- \(x_n\) be the shared interaction context available at step \(n\).
- \(r_n\) be the listener's reconstructed referent.
- \(f_n\) be the listener feedback observable by the speaker.
- \(q_n\in[0,1]\) be the listener's confidence that \(r_n=I\).
- \(\hat q_n\in[0,1]\) be the speaker's estimate of the listener's reconstruction confidence.
- \(\tau_A\) be the admissibility threshold.
- \(\tau_C\) be the commitment threshold, with \(\tau_C\geq\tau_A\) where consequential action requires stronger confidence.

The listener reconstructs:

$$
r_n = R(u_n,x_n)
$$

and evaluates:

$$
q_n = P(r_n=I\mid u_n,x_n,E_{1:n})
$$

where \(E_{1:n}\) is the accumulated evidence from the interaction so far.

The listener's admissibility decision is:

$$
A_n =
\begin{cases}
1, & q_n\geq\tau_A\\
0, & q_n<\tau_A
\end{cases}
$$

The speaker cannot directly inspect \(q_n\). The speaker infers gate state from feedback:

$$
\hat q_n = S(f_n,x_n,E_{1:n})
$$

The correction rule is:

$$
u_{n+1}=u_n+\Delta(I,u_n,f_n,x_n)
$$

where \(\Delta\) may alter articulation, stress, rhythm, duration, volume, gesture, gaze, or lexical choice.

The loop terminates when:

$$
\hat q_n\geq\tau_A
$$

or, more observably, when the listener begins a response consistent with the intended referent.

## Accumulated-Evidence Gate

The final utterance need not be independently sufficient. Earlier failed attempts may narrow the listener's hypothesis space.

Define the evidence state:

$$
E_n = E_{n-1}\cup\{u_n,f_n,x_n\}
$$

Then admissibility is evaluated over the accumulated state:

$$
A_n = G(u_n,x_n,E_n)
$$

not over the isolated utterance alone:

$$
A_n \neq G(u_n)
$$

This explains why a tenth pronunciation may cross the gate even when it is only slightly different from the ninth. The candidate changed, but so did the evidence state.

## Coupled Gate Dynamics

The process is bidirectional. The listener updates a reconstruction while the speaker updates an estimate of the listener's reconstruction.

$$
r_{n+1}=R(u_{n+1},x_{n+1},E_{n+1})
$$

$$
\hat r_{n+1}=S(f_{n+1},x_{n+1},E_{n+1})
$$

The interaction converges when both sides behave as though:

$$
r_n\approx I
$$

and

$$
\hat r_n\approx r_n
$$

The second condition matters. Communication has not socially completed until the speaker has evidence that the listener understood.

## Continuous-Time Form

At conversational scale, evaluation is better represented as continuous or quasi-continuous rather than as a slow sequence of explicit decisions.

Let \(q(t)\) be listener reconstruction confidence and \(\hat q(t)\) the speaker's estimate of that confidence.

The admissibility crossing time is:

$$
t_A=\inf\{t:q(t)\geq\tau_A\}
$$

The mutually observable crossing time is:

$$
t_M=\inf\{t:q(t)\geq\tau_A\land\hat q(t)\geq\tau_A\}
$$

The consequential commitment time is:

$$
t_C=\inf\{t\geq t_M:q(t)\geq\tau_C\land a(t)\neq 0\}
$$

where \(a(t)\) is listener action based on the admitted interpretation.

The central timing claim is not that every human gate has one fixed duration. It is that this loop can operate at the shortest practical timescale available to human perception, vocal production, social prediction, and motor response: often within fractions of a second for each update and within a few seconds for the full repair sequence.

## Admissibility at the Consequence Boundary

The gate must be located where interpretation begins to produce consequence.

A listener may entertain several candidate meanings without admitting any of them for action. Therefore:

$$
\text{candidate interpretation}\neq\text{admitted interpretation}
$$

and:

$$
\text{high plausibility}\neq\text{response authority}
$$

The gate crossing is visible when the interaction changes from search or repair into referent-consistent response.

## Relationship to Commit-Time Admissibility

This human process is a minimal natural example of commit-time admissibility reconstruction.

```text
candidate signal
  -> contextual reconstruction
  -> evidence accumulation
  -> current-state evaluation
  -> threshold crossing
  -> response commitment
  -> observable receipt
```

The decisive question is not whether an earlier utterance was once plausible. It is whether the current candidate, current context, accumulated evidence, and current interaction state jointly support commitment now.

## Receipt

The listener's changed body language, cadence, gaze, or action functions as a receipt observable by the speaker.

The receipt is not a formal signed artifact, but it serves the same functional role inside the interaction:

```text
receipt of hearing != receipt of understanding
receipt of understanding != proof of objective truth
receipt of admissibility != unrestricted authority
```

## Failure Modes

The model predicts several failure classes:

- `FALSE_POSITIVE_ADMISSION`: the listener acts on the wrong referent.
- `FALSE_NEGATIVE_REPAIR`: the listener understood, but the speaker fails to detect it and continues repair.
- `PREMATURE_COMMITMENT`: action begins before confidence or context is sufficient.
- `STALLED_REPAIR`: repeated candidates fail to add useful evidence.
- `CONTEXT_COLLAPSE`: the participants do not share enough state to converge.
- `FEEDBACK_OPACITY`: the speaker cannot reliably observe the listener's gate state.
- `PURPOSE_INVERSION`: the repair mechanism becomes so rigid that it obstructs successful communication.

## StegVerse Interpretation

This model provides a human-scale grounding for StegVerse admissibility doctrine:

> A transition is not admissible merely because a signal exists, reaches a receiver, or can be interpreted. It becomes admissible when the current candidate and accumulated evidence establish sufficient standing at the boundary where consequence may begin.

It also grounds four broader principles:

1. Admissibility is state-dependent.
2. Evidence may accumulate across failed candidates.
3. Gate state must be observable enough to support repair.
4. Commitment must remain distinct from recognition and interpretation.

## Research Hypotheses

### H1 — Incremental correction
Successive child utterances in unresolved interactions will show non-random acoustic variation correlated with caregiver feedback.

### H2 — Feedback-sensitive termination
Repetition will terminate more strongly after referent-consistent caregiver action than after generic acknowledgment.

### H3 — Evidence accumulation
Listener accuracy will depend on the sequence of prior attempts, not only on the final utterance.

### H4 — Mutual observability
Speaker termination will be better predicted by visible and prosodic evidence of listener understanding than by the listener's verbal acknowledgment alone.

### H5 — Timescale compression
With development, the same repair loop will persist but move from overt repetition toward faster lexical substitution, prosodic adjustment, and internal prediction.

## Public Boundary

This formalism is a conceptual and mathematical model. It does not claim that a single observed interaction proves a universal neurocognitive mechanism. Empirical validation requires synchronized audio, video, contextual annotation, acoustic analysis, and independently coded listener-response states.
