# Standing Research Companion — Volume III
## Comparative Terminology

**Status:** Phase 3 canonical terminology register
**Goal ID:** `SRC-PHASE3-001`

This register prevents cross-field terms from being treated as interchangeable merely because they share a word.

| Canonical StegVerse term | Field-specific meanings that must remain distinct | Required doctrine usage |
| --- | --- | --- |
| `signal.observable` | Measured waveform, symbol stream, image, event, or sensor output. | Never equate the observable with interpretation, health, truth, intent, or authority. |
| `signal.estimate` | Statistical inference about an unknown state or parameter. | Carry uncertainty, model assumptions, and validation scope. |
| `evidence.statistical` | Likelihood, posterior, confidence interval, detection statistic, or estimate. | Does not imply forensic admissibility or provenance integrity. |
| `evidence.custodial` | Preserved artifact with chain of custody and handling history. | Does not imply scientific truth or correct interpretation. |
| `provenance` | Origin, transformation, agent, and activity history. | Must not be described as proof of truth, authenticity, or authorization by itself. |
| `attestation` | Bounded signed claim about a measured entity or system state. | Require claim scope, freshness, appraisal policy, and trust anchor. Never use as a synonym for authorization. |
| `identity.proofing` | Establishing an identity claim. | Keep separate from authentication, federation, delegation, and authority. |
| `identity.authentication` | Demonstrating control of an authenticator. | Does not establish role, legal identity, delegation, or current permission. |
| `authority` | Current power to permit, deny, or commit a transition. | Must be derived from explicit policy, delegation, scope, time, and destination. |
| `standing.evidentiary` | Whether evidence is sufficient and admissible for a specified claim. | Namespaced; never collapse into a single standing score. |
| `standing.interpretive` | Whether an interpretation is justified by validated models and context. | Distinct from evidentiary presence and execution authority. |
| `standing.identity` | Whether identity assurance is sufficient for the action. | Distinct from authentication success. |
| `standing.policy` | Whether the applicable policy is current, applicable, and satisfied. | Must identify policy version and effective interval. |
| `standing.authority` | Whether an actor has current delegated authority. | Must identify issuer, scope, expiry, and revocation state. |
| `standing.transition` | Composite StegVerse determination for a proposed transition. | A proposed StegVerse formalism; its component standings remain inspectable. |
| `admissibility` | Whether a transition may be committed now under current evidence, policy, and authority. | Not a synonym for validity, approval, execution, consensus, or continuity. |
| `continuity` | Preservation of reconstructable linkage across states, decisions, and receipts. | Does not prove legitimacy or current admissibility. |
| `reconstructability` | Ability to reproduce and inspect the evidence and decision path. | Prefer `reconstructable decision standing`; do not claim substantive legitimacy automatically. |
| `consensus.agreement` | Agreement among distributed participants under a stated fault model. | Never equate with truth, ethics, scientific validity, or authority. |
| `state.estimation` | Latent state inferred from observations. | Distinct from database state, logical state, and physiological state. |
| `state.distributed` | Replicated or partitioned machine state. | Must specify consistency semantics and failure assumptions. |
| `state.physiological` | Context-bounded biological condition or operating regime. | Must not be treated as one universal health variable. |
| `stability.control` | Bounded response or convergence under a defined model. | Distinct from health, resilience, social stability, and legitimacy. |
| `health` | Clinical and biological concept requiring context, validation, and intended use. | No universal signal-derived health claim without domain validation. |
| `baseline.personal` | Individual reference distribution or history. | Contextual evidence only; not proof of health or normality. |
| `explanation.fidelity` | Accuracy with which an explanation reflects a model's behavior. | Distinct from model correctness, outcome validity, and user understanding. |
| `verification` | Conformance to specification or declared requirements. | Always paired with separate validation of the specification and context. |
| `validation` | Evidence that the measured or specified construct is appropriate for intended use. | Must state context, population, environment, and decision consequences. |

## Prohibited unqualified terms

The following words must be namespaced or explicitly defined when used in doctrine: `standing`, `state`, `consistency`, `safety`, `trust`, `evidence`, `model`, `accuracy`, `temporal`, `control`, `stability`, `identity`, and `attestation`.

## Adoption rule

A doctrine term may be introduced only when its definition states:

1. its namespace and field provenance;
2. what it does not establish;
3. its validation method;
4. its authority effect, if any;
5. whether it is established, demonstrated, emerging, or a proposed StegVerse formalism.
