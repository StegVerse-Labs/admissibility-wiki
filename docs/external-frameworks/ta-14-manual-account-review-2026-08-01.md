---
title: TA-14 Manual Account Review — Public Exchange Playground
sidebar_label: TA-14 Manual Account Review
---

# TA-14 Manual Account Review — Public Exchange Playground

## Review classification

```text
Review type: MANUAL_ACCOUNT_REQUIRED
Review date: 2026-08-01
Observed surface: TA-14 Exchange public Playground
Observed lane: Agent & Tool Governance · AT-5.0
Account creation/sign-in: REQUIRED
Automation posture: NOT USED
Evidence source: authenticated manual interaction and captured screenshots
Paid evaluation capability: NOT TESTED
Underlying TA-14 architecture: NOT ADJUDICATED BY THIS PAGE
Authority granted: none
```

This page is intentionally separate from the general TA-14 framework page because the reviewed interface required an authenticated account. The observations could not be reproduced by an unauthenticated public-route checker alone and therefore required a bounded manual review.

The account requirement does not establish confidentiality, paid-service equivalence, authority, or independent verification. It establishes only why direct manual interaction was necessary to inspect the workspace behavior.

## Question tested

The review tested whether the public Playground independently derives governance gate states from inspected evidence, or whether the tester directly assigns gate states that TA-14 then aggregates into a bounded determination.

The distinction is:

```text
independent evidence reconstruction
-> system inspects evidence
-> system derives PASS / REVIEW / FAIL
-> system calculates determination

interactive state classification
-> tester assigns PASS / REVIEW / FAIL
-> system counts assigned states
-> system calculates determination
```

## Observed subject held constant

```text
Agent: Orion Operations Agent · 4.6.2
Agent id: AGT-ORION-OPS
Declared objective: Coordinate approved maintenance workflows
Requested action: Read approved case evidence, prepare a bounded action plan,
                  and pause before any external commitment.
Environment: Production / us-east / governed runtime
Recipient: Internal operations reviewer
Projected spend: 0
```

No new identity artifact, delegation instrument, tool manifest, credential proof, dependency record, incident record, or external authority source was supplied while the gate states were changed.

## Control run

The initial displayed configuration showed:

```text
Gate posture: 24 PASS / 0 REVIEW / 0 FAIL
Required evidence: 25 / 27
Stale evidence: 1
Challenged evidence: 1
Open challenges: 1
Determination: HOLD
Preserved run: run-5713
```

The control demonstrates that all visible gates may display `PASS` while a separate stale or challenged evidence condition keeps the overall determination at `HOLD`.

## Direct gate-state assignment

The authenticated interface allowed the tester to change individual 24-link gate cards directly among:

```text
PASS
REVIEW
FAIL
```

Observed manually reassigned gates included foundational questions such as:

```text
Agent identity
Delegating authority
Objective boundary
Role validity
Instruction integrity
Tool identity
Permission scope
Credential integrity
Memory provenance
Inherited limits
Communication authority
Environment integrity
Dependency continuity
Injection resistance
Monitoring continuity
Incident boundary
Change validity
Outcome correspondence
```

The same displayed agent, objective, requested action, environment, recipient, and projected spend remained visible while these states changed.

![TA-14 Agent & Tool lane showing the bounded DENY posture and mixed gate counts](/img/external-frameworks/ta-14/manual-account-review-2026-08-01/01-deny-overview.jpg)

## Mixed-state aggregation test

A mixed configuration was constructed manually:

```text
6 PASS
12 REVIEW
6 FAIL
```

The interface returned:

```text
Current bounded determination: DENY
Explanation: The proposed action crosses a non-waivable delegation,
             permission, security, financial, privacy, or execution boundary.
Preserved run: run-9288
```

This confirms the visible aggregation sequence:

```text
tester-assigned gate states
-> aggregate PASS / REVIEW / FAIL counts
-> bounded determination
-> preserved run
```

The test does not show TA-14 independently discovering that the underlying agent lacked identity, delegation, permission, credential integrity, dependency continuity, or incident clearance. It shows that the public interface accepted manually assigned states and produced a corresponding bounded determination.

![Manual gate-state changes, preserved DENY run, and governed-record export prompt](/img/external-frameworks/ta-14/manual-account-review-2026-08-01/02-manual-review-sequence.jpg)

## Governed-record preservation and export

Observed preservation results:

```text
run-5713 preserved with HOLD determination
run-9288 preserved with DENY determination
```

The interface offered an export named:

```text
ta14-agent-tool-governed-record.json
Displayed size: 44 KB
```

The tester invoked the visible download flow three times. The browser displayed the generated-file prompt, but no file appeared in the device Downloads or Recents locations checked immediately afterward.

Bounded export finding:

```text
Platform-side run preservation: OBSERVED
Export prompt generation: OBSERVED
Local governed-record delivery: NOT ACHIEVED IN THREE ATTEMPTS
Independent replay from exported file: NOT PERFORMED
```

This is recorded as an observed public-surface delivery failure, not as proof that no downloadable record can ever be produced on another browser, device, account, or service tier.

## Manual-review determination

```text
Direct tester assignment of PASS / REVIEW / FAIL: OBSERVED
Aggregation of assigned states into HOLD / DENY: OBSERVED
Preservation of aggregate result: OBSERVED
Independent evidence-derived gate reconstruction: NOT OBSERVED
Independent contradiction discovery: NOT ESTABLISHED
Cross-lane propagation: NOT TESTED
Paid evaluation behavior: NOT TESTED
Underlying architecture failure: NOT CLAIMED
```

The public Playground is therefore classified, at this observed interaction layer, as:

> An authenticated interactive governance-state classifier that accepts tester-assigned gate postures, aggregates them into bounded determinations, and preserves resulting runs.

That finding is limited to the observed public Exchange Playground. It does not determine whether a separate paid evaluation ingests evidence, verifies provenance, resolves external authority, detects undeclared contradictions, or propagates findings across lanes.

## Capability boundary for any stronger claim

A stronger paid-service capability remains testable only through inspectable evidence such as:

```text
frozen input package
artifact manifest
provenance and signature checks
derived gate-state trace
undeclared contradiction detection
cross-lane dependency trace
current-authority resolution
invalidation triggers
preserved receipt
exported replay package
independent replay result
```

A statement that the paid evaluation behaves differently is not rejected by this page. It remains unverified until a frozen test contract and inspectable run evidence are available.

## Authority boundary

```text
account access != independent verification
manual gate assignment != evidence reconstruction
bounded determination != universal authority
preserved run != independently validated fact
export prompt != delivered replay package
public Playground behavior != paid evaluation behavior
public Playground limitation != underlying architecture failure
HOLD or DENY aggregation != proof that the represented real-world condition existed
```
