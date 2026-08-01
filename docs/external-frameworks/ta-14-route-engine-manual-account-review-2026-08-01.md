---
title: TA-14 Route Engine Manual Account Review — Public Exchange
sidebar_label: TA-14 Route Engine Manual Review
---

# TA-14 Route Engine Manual Account Review — Public Exchange

## Review classification

```text
Review type: MANUAL_ACCOUNT_REQUIRED
Review date: 2026-08-01
Surface: authenticated TA-14 Exchange Route Construction Workspace
Adapter: VENDOR PAYMENT
Scope: public demonstration route engine and public verifier
Paid evaluation: NOT TESTED
Underlying private architecture: NOT ADJUDICATED
```

This review required manual account creation and sign-in. The authenticated workspace could not be fully inspected through an unauthenticated automated path. The observations below are therefore a manual interface review supported by screenshots captured during the authenticated session.

## Tested route

The default vendor-payment manifest was submitted without changing its displayed values:

```text
Organization: TA-14 Demonstration Organization
System: Governed Vendor Payment Engine
Actor ID: ACTOR-DEMO-001
Supplier ID: SUPPLIER-DEMO-001
Invoice ID: INVOICE-DEMO-001
Beneficiary ID: BENEFICIARY-DEMO-001
Amount USD: 27500
```

The interface describes this as a self-declared demonstration route and states that it is not independent certification or legal approval.

## Builder result

The Route Construction Workspace displayed:

```text
Route identity: TA14-RID-80287C7D
Version: 1
Created: 2026-08-01T17:55:39.494Z
Determination: HOLD
Displayed status: Route created and preserved
```

The stated reason was that dual authority and beneficiary verification had not yet been supplied. The interface also stated that the original HOLD must remain preserved when the route is corrected.

### What this establishes

```text
Structured manifest intake: OBSERVED
Unique RID generation: OBSERVED
Version 1 display: OBSERVED
Deterministic default-rule evaluation: OBSERVED
Initial HOLD display: OBSERVED
Preservation claim in builder: OBSERVED
Independent beneficiary verification: NOT OBSERVED
Independent dual-authority reconstruction: NOT OBSERVED
```

## Authenticated route-library check

Immediately after route creation, the authenticated **My Routes** page reported:

```text
Saved routes: 0
Ready for test: 0
On hold: 0
Drafts: 0
Route library: No authenticated routes yet
```

The page separately states that routes shown there are stored under the authenticated account and protected by database Row Level Security. It also correctly warns that a saved route is not, by itself, an authoritative system record, live evaluation, certification, or proof that declared evidence exists.

The newly displayed RID was not visible in this authenticated library.

## Public-verifier check

The public verifier advertises inspection of registry presence, receipt identity, decision correspondence, signature validity, event-chain integrity, execution correspondence, and preserved outcome.

A seeded demonstration RID successfully returned a cryptographically and structurally consistent record using a development signing key. That seeded result demonstrated verifier behavior for a known demonstration record, not persistence of the newly created route.

The newly created RID was then checked:

```text
Queried RID: TA14-RID-80287C7D
Verifier result: No demonstration registry record matches that RID
```

## Preservation-correspondence finding

Two available retrieval paths did not independently confirm the builder's preservation claim:

```text
Builder displayed “Route created and preserved”: OBSERVED
Authenticated My Routes record: NOT FOUND
Public demonstration registry record: NOT FOUND
Receipt-to-storage correspondence: NOT ESTABLISHED
Durable retrievability: NOT ESTABLISHED
```

This does not prove that no internal write occurred. Possible explanations include a separate non-public store, delayed indexing, an incomplete save workflow, or a failed persistence transaction. None of those explanations was established by the tested interface.

The bounded finding is:

> The public Route Construction Workspace generated and displayed a versioned HOLD receipt for `TA14-RID-80287C7D`, but the record was not visible in the authenticated route library and was not retrievable through the public demonstration verifier. Durable preservation and receipt-to-storage correspondence were therefore not established in this manual test.

## Relationship to the Playground review

The earlier Playground review established direct tester assignment of gate states followed by bounded aggregation and preservation of the resulting posture. This route-engine review tests a different surface:

```text
Playground: tester assigns governance states -> TA-14 aggregates posture
Route engine: tester submits structured manifest -> TA-14 issues RID and displayed receipt
```

The route engine is the stronger surface because it claims RID generation, deterministic evaluation, signing, preservation, and verification. The present test confirmed the displayed RID and HOLD result but did not confirm durable retrieval of that new record.

## Evidence status

Screenshot evidence was captured for:

```text
1. Default vendor-payment manifest and route-engine readiness
2. Created HOLD receipt for TA14-RID-80287C7D
3. Authenticated My Routes counts remaining at zero
4. Public verifier seeded-record behavior and development-signing boundary
5. No demonstration registry record matching TA14-RID-80287C7D
```

The current chat image-upload limit was reached before additional testing could be documented. Further route mutation, correction/versioning, duplicate-payment, replay, and delayed-retrieval tests are paused until image capacity refreshes so each result can be preserved with screenshot evidence.

## Remaining tests

```text
1. Retry RID retrieval after a defined delay and record the exact interval.
2. Determine whether a separate save/import action moves a builder receipt into My Routes.
3. Correct only the missing dual-authority or beneficiary-verification condition.
4. Confirm whether correction creates version 2 while preserving version 1.
5. Inspect any available receipt for input hash, rule identifiers, derived findings, signature method, and version lineage.
6. Test duplicate invoice submission with one-variable mutation.
7. Test beneficiary mismatch without manually declaring the conflict.
8. Test replay and post-commit authority revocation if the public surface permits it.
9. Do not generalize this public demonstration result to the paid evaluation without separate reproducible evidence.
```

## Authority boundary

```text
RID displayed != registry presence
builder preservation claim != independently retrievable preservation
version number displayed != version lineage established
signed demonstration receipt != external truth of submitted claims
record integrity != claim validity
public demo result != paid evaluation result
not found in tested stores != proven absent from every internal store
manual review finding != underlying architecture failure
```

## Pause posture

Testing is paused because the current image-upload allowance was exhausted. The next session should continue from `TA14-RID-80287C7D`, preserve every new observation with screenshots, and avoid repeating already completed baseline steps unless needed for reproducibility.
