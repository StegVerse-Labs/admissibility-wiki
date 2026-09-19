# Evidence-Based Reputation Model

## Purpose

This model describes how StegVerse may preserve and classify recurring interaction patterns without turning observation into accusation.

The model has three distinct layers:

1. **Raw evidence** — complete source material, timestamps, source identity, provenance, and the exact statements or actions observed.
2. **Governed classification** — a reproducible description of which predefined interaction-state transitions are supported by the preserved evidence.
3. **Public reputation signal** — an aggregate, evidence-linked summary that reflects documented conduct without asserting criminal intent, hidden motive, institutional endorsement, or other unsupported conclusions.

The reputation signal is downstream of evidence. It is never a substitute for the evidence.

## Evidence classes

Every retained assertion must be classified as one of:

- `OBSERVED_FACT` — directly visible in preserved source material.
- `PARTICIPANT_REPORT` — reported by a participant but not independently preserved in the current evidence set.
- `GOVERNED_INFERENCE` — a reproducible inference from one or more observed facts under a declared rule.
- `DISPUTED` — challenged by a participant or by contrary preserved evidence.
- `UNRESOLVED` — insufficient evidence to classify further.

A public-facing claim must identify which class it belongs to.

## Interaction transition model

The initial pattern model contains eight possible states:

1. `CONTACT` — an interaction begins.
2. `CREDIBILITY_ESTABLISHMENT` — credentials, frameworks, affiliation, experience, or authority-relevant representations are introduced.
3. `COLLABORATIVE_EXCHANGE` — substantive reciprocal discussion or work occurs.
4. `CONTRIBUTION_ACCUMULATION` — one or both parties add material ideas, analysis, artifacts, or effort.
5. `ASYMMETRY_INTRODUCED` — one party begins treating the exchange as materially asymmetric.
6. `VALUE_OR_OWNERSHIP_REFRAMING` — prior collaborative contribution is reframed as individually owned, separately valuable, compensable, or otherwise entitled.
7. `COMPENSATION_REQUEST` — compensation, payment, commercial consideration, or equivalent benefit is requested.
8. `POST_REJECTION_RESPONSE` — conduct after the request is accepted, rejected, challenged, or left unresolved.

A case need not contain every state. Missing states remain `NOT_ESTABLISHED`; they are not inferred merely because later states exist.

## Pattern classification

A governed classifier may report that an interaction is consistent with a recurring sequence only when each counted state is linked to preserved evidence.

Example bounded output:

`6 of 8 declared interaction states are supported by preserved evidence in this record.`

It must not silently convert that statement into:

- proof of fraudulent intent;
- proof of extortion;
- proof of a deliberate scheme;
- proof of predatory conduct;
- a legal adjudication;
- a diagnosis of motive;
- an institutional judgment about the person.

Those conclusions require their own evidence and, where applicable, appropriate legal or institutional authority.

## Cross-interaction aggregation

Multiple records may be aggregated only when:

- each record preserves its own provenance;
- the same versioned state model is applied;
- state determinations remain independently inspectable;
- the denominator is explicit;
- contradictory cases are retained rather than discarded;
- participant identity matching is evidence-backed;
- absence of evidence is not converted into negative evidence.

The aggregate may describe recurrence, for example:

`The same value-reframing -> compensation-request transition was observed in 4 of 6 preserved interactions evaluated under model v0.1.`

It must not state that recurrence proves common coordination, shared intent, or criminal purpose without independent evidence for that proposition.

## Reputation signal

A reputation signal is an evidence index, not a verdict.

A bounded public projection should include:

- number of preserved interactions;
- number evaluated under the current model;
- supported state counts per interaction;
- recurring transitions;
- unresolved or disputed points;
- links to the underlying evidence where publication is authorized;
- model version and evaluation timestamp;
- correction/rebuttal history.

No score should conceal the underlying evidence or imply precision that the records do not support.

## Corrections and rebuttal

Every public record must be correctable without erasing history.

A correction should:

1. preserve the superseded classification;
2. identify the new evidence;
3. state which determination changed;
4. retain the prior record as historical;
5. issue a new versioned classification.

A subject or participant response is evidence and should be preserved as such. A rebuttal does not automatically invalidate the earlier record, and the earlier record does not automatically invalidate the rebuttal.

## Publication boundary

Private conversation material is not automatically public evidence.

A record may exist in a non-public or evidence-pending state until publication authority, consent, lawful basis, redaction, or other applicable release conditions are satisfied.

The model separates:

`evidence retained != evidence published`

`classification produced != accusation made`

`recurring pattern != proven intent`

`reputation signal != adjudication`

`public availability != independent validation`

## Initial bounded case

The first bounded intake created with this model is:

`data/evidence-based-reputation/linkedin-interaction-2026-09-19.json`

It records only what is currently preserved or reported from the September 19, 2026 LinkedIn-related discussion and explicitly leaves unsupported stages unresolved.
