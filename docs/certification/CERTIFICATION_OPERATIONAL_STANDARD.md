# Governance-Chain Certification Operational Standard

## Claim discipline

A StegVerse certification claim MUST identify the exact certified component, implementation/version, surface (`PRE`, `GOV`, `POST`, or `INT`), profile version, certified properties, evidence packet, issue time, freshness boundary, and current lifecycle state.

Permitted public language is property-scoped, for example:

> Certified under StegVerse Governance-Chain Profile GOV v0.1 for `FAIL_CLOSED` and `ADMISSIBILITY_COMMIT_BOUND`, based on evidence packet `<id>`, current through `<timestamp>`.

Forbidden or misleading shorthand includes `StegVerse approved`, `safe`, `trusted`, `compliant`, `governance certified`, or any badge that omits the tested property scope and current-state locator.

Payment buys access to testing, evidence generation, examination, and related services. Payment does not buy a disposition. Customer identity, commercial value, or evaluator reputation MUST NOT be decision inputs.

## Lifecycle

Certificates are never timeless. `CURRENT` means only that the tested implementation/profile/evidence remain inside their declared freshness window and no revocation condition is known.

`CURRENT -> EXPIRED` when `fresh_until` passes without renewal.

`CURRENT -> SUSPENDED` when material evidence is disputed or a potentially material implementation/environment change is unresolved.

`CURRENT -> REVOKED` when verification fails, evidence is invalidated, the claim is materially misrepresented, or the tested authority basis is withdrawn.

`CURRENT -> SUPERSEDED` when a later certificate replaces the same scoped claim.

Renewal requires re-evaluation. Prior evidence may be reused only when its continued applicability is independently established.

## Existing Fin-Co precedent mapping

The Fin-Co certification model establishes useful generic invariants:

- implementation claims alone are insufficient;
- certification requires a named suite and retained report;
- pass/fail counts and expected-outcome coverage are explicit;
- `ALLOW`, `DENY`, and `FAIL_CLOSED` behavior are all exercised;
- authority basis and receipt basis are required;
- failure behavior must be as deterministic as allow behavior.

Governance-Chain Certification generalizes those rules beyond finance and beyond governance engines to PRE/GOV/POST/INT components.

## SDK evidence adapter

The StegVerse SDK is the preferred evaluator-facing execution surface when a candidate can be expressed through published SDK capabilities. The adapter maps SDK evidence as follows:

```text
SDK evaluation declaration -> certification candidate test intent metadata
submitted manifest hash -> candidate/input binding
StegGate disposition -> GOV observation
manifested route receipts -> transition evidence
Master Records exact-run custody -> CUSTODY_DURABLE evidence
replay result -> REPLAY_STABLE evidence
reconstruction result -> RECONSTRUCTABLE evidence
result binding hash -> candidate-to-result binding
```

An SDK `ALLOW` does not itself produce a certification. Certification requires the complete profile, required negative controls, evidence sufficiency, lifecycle metadata, and certificate validator to pass.

## Interlock certification

For `INT`, certification evaluates the boundary between two independently authoritative systems. It does not make StegVerse the external system's runtime authority and does not make the external system a StegVerse authority.

Minimum interlock evidence MUST establish source identity, destination identity, the exact translation profile, authority effect, admitted capability, request receipt, return receipt, and negative controls for authority injection and semantic expansion.

## Badge contract

Any machine or visual badge MUST resolve to a machine-readable current certificate. If that locator cannot be resolved or the certificate is not `CURRENT`, the badge MUST NOT represent an active certification.

The badge is a pointer to evidence-backed scope, never a substitute for it.
