# Micro-Timescale Human Admissibility Observation Protocol

## Purpose

This protocol turns the Micro-Timescale Human Admissibility formalism into an empirically testable observation method without treating one family interaction as universal proof.

The unit of analysis is one unresolved communicative episode that begins with a candidate signal and ends in convergence, abandonment, substitution, or an unresolved stop.

## Required Capture

A research-grade observation should preserve synchronized:

- audio;
- video of speaker and listener;
- interaction context;
- candidate utterance boundaries;
- listener feedback boundaries;
- consequential response onset;
- coder uncertainty and disagreement.

Private family recordings must not be published or ingested without informed authorization. A derived observation record should minimize identity and biometric exposure.

## Event Sequence

Each episode is represented as an ordered event stream:

```text
EPISODE_START
  -> CANDIDATE_SIGNAL
  -> LISTENER_FEEDBACK
  -> SPEAKER_REPAIR_OR_HOLD
  -> ...
  -> ADMISSIBILITY_CROSSING_CANDIDATE
  -> COMMITMENT_ONSET
  -> EPISODE_END
```

A candidate crossing is not accepted merely because repetition stops. Termination may also result from fatigue, distraction, coercion, abandonment, or context loss.

## Coding Fields

For each candidate step \(n\), record:

- `candidate_id`;
- start and end time;
- acoustic or lexical change from \(u_{n-1}\);
- gaze, gesture, stress, rhythm, duration, and volume changes;
- listener gaze, posture, facial, prosodic, verbal, and action feedback;
- shared-context changes;
- candidate referent set;
- coder estimate of listener reconstruction state;
- coder estimate of speaker-side gate-state detection;
- whether consequential action began;
- confidence and uncertainty.

## State Labels

Permitted interaction states are:

```text
EMITTED
RECEIVED
RECOGNIZED
INTERPRETED
ADMISSIBLE_CANDIDATE
MUTUALLY_OBSERVABLE_CANDIDATE
COMMITTED
ABANDONED
UNRESOLVED
```

`ADMISSIBLE_CANDIDATE` and `MUTUALLY_OBSERVABLE_CANDIDATE` are observational labels, not direct access to either participant's internal state.

## Timing Measures

Let candidate onset times be \(t_1,\ldots,t_N\). Define:

\[
\Delta t_n=t_{n+1}-t_n
\]

Let \(t_F^{(n)}\) be the first observable listener feedback after candidate \(n\). The feedback latency is:

\[
L_F^{(n)}=t_F^{(n)}-t_n
\]

Let \(t_R^{(n+1)}\) be the onset of the next repair. The repair latency is:

\[
L_R^{(n)}=t_R^{(n+1)}-t_F^{(n)}
\]

Let \(t_A^*\) be the first independently coded admissibility-crossing candidate, \(t_M^*\) the first mutually observable candidate, and \(t_C^*\) consequential response onset.

The observed intervals are:

\[
D_{A\rightarrow M}=t_M^*-t_A^*
\]

and:

\[
D_{M\rightarrow C}=t_C^*-t_M^*
\]

These are observational estimates of the formal variables, not measurements of neural decision time.

## Acoustic Change

Successive candidates should be compared using predeclared features such as:

- segment duration;
- syllable duration;
- fundamental-frequency contour;
- intensity;
- pause placement;
- vowel-formant estimates where appropriate;
- consonant-release timing;
- lexical substitution;
- gesture or gaze supplementation.

The protocol does not presume that the final candidate is acoustically closest to an adult target. Convergence may result from accumulated context rather than pronunciation improvement alone.

## Competing Explanations

Coders must test at least these alternatives:

1. attention acquisition rather than meaning repair;
2. generic repetition or play;
3. caregiver guessing without sufficient understanding;
4. speaker stopping from fatigue or distraction;
5. correct understanding occurring before the visible response;
6. response beginning before sufficient reconstruction;
7. contextual accumulation without meaningful signal correction.

## Independent Coding

At least two coders should independently mark candidate boundaries, feedback events, crossing candidates, commitment onset, and failure class.

Report agreement separately for:

- temporal boundaries;
- state labels;
- referent reconstruction;
- crossing identification;
- failure classification.

Disagreement must remain visible. Consensus coding may be added, but it must not replace the independent records.

## Minimum Hypothesis Tests

### H1 — Incremental correction

Compare observed successive-candidate changes against within-episode permutation or matched repetition baselines.

### H2 — Feedback-sensitive termination

Model termination probability using referent-consistent action, generic acknowledgment, and no-response feedback classes.

### H3 — Evidence accumulation

Compare listener reconstruction from the final candidate alone against reconstruction with the preceding candidate sequence.

### H4 — Mutual observability

Compare termination prediction from verbal acknowledgment alone against combined visual, prosodic, and action feedback.

### H5 — Timescale compression

Compare overt repair count, latency, and repair modality across developmental or proficiency groups without assuming one fixed developmental trajectory.

## Privacy and Governance Boundary

This protocol does not authorize recording, publication, biometric analysis, child research, or dataset distribution. Applicable consent, parental permission, participant assent, institutional review, privacy, retention, and jurisdictional requirements remain separate admissibility gates.

Observation is not consent. De-identification is not automatically anonymity. Research usefulness is not publication authority.

## Output

A conforming study should publish, where authorized:

- a protocol version;
- a machine-readable event schema;
- de-identified derived records;
- coding guidance;
- inter-coder agreement;
- exclusions and uncertainty;
- analysis code;
- non-claim boundaries.

The protocol supports empirical challenge and refinement of the formalism. It does not presume confirmation.
