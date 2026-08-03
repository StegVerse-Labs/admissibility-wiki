# StegVerse Doctrine Revision Matrix

**Status:** Phase 3 canonical revision-control artifact
**Goal ID:** `SRC-PHASE3-001`
**Authority effect:** None. This matrix controls proposed edits; it does not itself revise normative doctrine.

| Revision ID | Doctrine concept | Current disposition | Required action | Blocking evidence / dependency | Release state |
| --- | --- | --- | --- | --- | --- |
| SRC-REV-001 | Capability does not confer authority | RETAIN | Preserve explicit delegation, policy, scope, time, and destination requirements. | None | READY_FOR_REVIEW |
| SRC-REV-002 | Evidence/provenance does not equal truth | RETAIN | Add as a global limitation wherever provenance, attestation, or receipts appear. | None | READY_FOR_REVIEW |
| SRC-REV-003 | History and reconstruction | NARROW | State that immutable or replayable history supports inspection, not automatic current admissibility or legitimacy. | None | READY_FOR_REVIEW |
| SRC-REV-004 | Fail-closed UNKNOWN | MODIFY | Define `UNKNOWN`, `DENY`, and `REVIEW_REQUIRED` as distinct machine states with explicit transitions. | Decision schema and fixtures missing | BLOCKED |
| SRC-REV-005 | Unified standing | REPLACE | Replace unqualified `standing` with namespaced evidentiary, interpretive, identity, policy, authority, and transition standing. | Terminology register installed; formal schema missing | REVIEW_REQUIRED |
| SRC-REV-006 | Heartbeat as universal reference | NARROW | Describe heartbeat only as a candidate domain-specific temporal/physiological reference. Prohibit universal health, identity, agency, or consent inference. | Group B and H substantive reviews missing | BLOCKED |
| SRC-REV-007 | Analog → digital → standing | RELABEL | Present as a proposed StegVerse architectural lens, not an accepted technological or signal-theory progression. | Formalism declaration installed | READY_FOR_REVIEW |
| SRC-REV-008 | Reconstructable legitimacy | REPLACE | Use `reconstructable decision standing` unless independent normative legitimacy criteria are identified and satisfied. | Terminology register installed | READY_FOR_REVIEW |
| SRC-REV-009 | Transition Element | DECLARE_NEW_FORMALISM | Define as the canonical minimal governed unit within StegVerse only. | Formal schema, invariants, and fixtures missing | BLOCKED |
| SRC-REV-010 | More signals increase standing | PROHIBIT_GENERAL_CLAIM | Require calibration, dependence, missingness, model, and shared-failure analysis. | Sensor-fusion validation contract missing | BLOCKED |
| SRC-REV-011 | Personal baseline equals health | PROHIBIT | State that a baseline is contextual evidence and may represent compensated or pathological state. | None | READY_FOR_REVIEW |
| SRC-REV-012 | Consensus establishes truth | PROHIBIT | Limit consensus claims to agreement/order under a stated fault and synchrony model. | None | READY_FOR_REVIEW |
| SRC-REV-013 | Governance substitutes for validation | PROHIBIT | State that governance constrains use but cannot create scientific validity, clinical validity, or utility. | None | READY_FOR_REVIEW |
| SRC-REV-014 | Formal proof establishes real-world correctness | NARROW | Preserve the verification/validation split and identify model/specification assumptions. | None | READY_FOR_REVIEW |
| SRC-REV-015 | Attestation establishes security | NARROW | Require bounded claims, trust anchor, reference values, freshness, appraisal policy, and expiry. | None | READY_FOR_REVIEW |
| SRC-REV-016 | Explanation establishes correctness | PROHIBIT | Separate explanation fidelity, user understanding, model accuracy, and outcome validity. | None | READY_FOR_REVIEW |
| SRC-REV-017 | Recoverability under degrading authority | DECLARE_NEW_FORMALISM | Keep as proposed boundary-admissibility requirement and define degradation/recovery state transitions. | Group B review and formal model missing | BLOCKED |
| SRC-REV-018 | Distributed cognition without sovereignty | RETAIN_AS_EXTENSION | Require bounded scope, non-self-delegation, receipts, collision prevention, expiry, and revocation. | Agent contract and tests missing | BLOCKED |
| SRC-REV-019 | Dead basis | DECLARE_NEW_FORMALISM | Define detection, status, remediation, and immutable-history behavior. | State machine and tests missing | BLOCKED |
| SRC-REV-020 | Standing correction | DECLARE_NEW_FORMALISM | Define when structurally intact evidence is prevented from becoming load-bearing and how that decision is reviewed. | Formal rule and counterexamples missing | BLOCKED |

## Doctrine rewrite gate

Normative doctrine rewriting is prohibited until:

1. all `READY_FOR_REVIEW` rows receive explicit review disposition;
2. blocked rows remain visibly bounded or their release conditions are met;
3. the companion validator passes;
4. every new formalism is labeled proposed;
5. Group B and H limitations are preserved;
6. an exact source-to-doctrine change list is committed;
7. propagation authority is separately granted.

## Propagation gate

No change may propagate to Site, Publisher, admissibility projections, guardian projections, or custody systems merely because this matrix exists. Propagation requires an approved doctrine revision commit, consumer contract, validation receipt, and repository-specific handoff update.
