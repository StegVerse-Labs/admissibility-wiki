# Admissibility Wiki

The Admissibility Wiki is the public vocabulary layer for transition governance, commit-time authority, receipt-bound execution, and governed continuity.

This repository is a Docusaurus-ready knowledge base for StegVerse concepts, formal vocabulary, comparison pages, and minimal public proof paths.

## Purpose

This wiki exists to make the StegVerse governance vocabulary visible, stable, linkable, and reviewable without requiring Wikipedia approval first.

It is not a substitute for Wikipedia and does not claim independent notability by itself. It is a public reference layer that can help researchers, developers, reviewers, journalists, and contributors understand the concepts accurately.

## Governed Ecosystem Transition Framing

The current public framing is shifting from external-framework comparison toward a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs.

External frameworks are one input class. The broader path is:

```text
input or request
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

The framing page is:

```text
docs/governance/governed-ecosystem-transitions.md
```

## Core Assumptions

The wiki treats governance as a layered constraint system, not a single approval event.

The current StegVerse interpretation separates:

- human experience before governance;
- inter-entity trust and intuition before boundary formation;
- boundary conditions before execution;
- governance standing at the moment a transition may affect reality;
- continuity records after execution or denial.

This matters because emotional state, intuition, trust, relational coherence, and boundary recoverability can affect whether a proposed transition should ever become admissible.

## Disciplinary Translation Groundwork

The current translation-groundwork section is:

```text
docs/formalisms/disciplinary-translation-groundwork.md
```

The current translation-records reference page is:

```text
docs/formalisms/translation-records.md
```

The current machine-readable translation-record artifact is:

```text
static/translation-records/disciplinary-translation-records.v0.1.json
```

The current validator is:

```text
scripts/check_translation_records.py
```

Run:

```bash
python scripts/check_translation_records.py
```

Expected current state:

```text
TRANSLATION RECORDS: PASS - 6 records validated
```

The validation workflow is displayed here without the leading period:

```text
github/workflows/validate-translation-records.yml
```

The actual repository path begins with a leading period.

The iOS-safe workflow mirror is:

```text
iosnoperiod/github/workflows/validate-translation-records.yml
```

## Triad Governance

Triad governance is the three-part StegVerse governance frame for distinguishing proposal, commitment, and reconstruction.

| Component | Core Question | Function |
| --- | --- | --- |
| Transition Governance | Can this transition be considered? | Determines whether a proposed state change is structurally valid. |
| Admissibility Governance | Can this transition be committed now? | Determines whether execution authority exists at the moment of commitment. |
| Continuity Governance | Can this transition be reconstructed later? | Determines whether the resulting decision path remains replayable, receipt-bound, and independently reviewable. |

The triad keeps these claims separate:

- approval is not continuity;
- execution is not admissibility;
- history is not authority.

A transition may be structurally valid, inadmissible at commit time, and still reconstructable later. A transition may also be admissible at commit time while failing continuity if receipts, manifests, or authority records are insufficient.

## CAT Governance Stack

The CAT stack is currently interpreted as:

| Layer | Working Name | Function |
| --- | --- | --- |
| ECAT | Emotional / Experiential Constraint Analysis | Models intra-entity state: emotion, intuition, perception, affective processing, coherence, and meaning before governance hardens into boundary or authority. |
| ICAT | Interpersonal / Intuitive Constraint Analysis | Models inter-entity state: trust, relationship continuity, shared understanding, social coherence, and intuition formed between entities. |
| BCAT | Boundary Constraint Analysis | Models the boundary conditions under which a transition, entity, claim, or interaction can remain recoverable and non-inverting. |
| GCAT | Governance Constraint Analysis | Models governance standing, admissibility, policy, delegation, authority, and fail-closed execution decisions. |

ECAT and ICAT should not be reduced to evidence and identity labels. Those interpretations may appear in narrower proof-path contexts, but the broader origin of ECAT/ICAT is the human-governance problem: how emotion, intuition, coherence, and relationship dynamics shape the constraints that later become boundary and governance determinations.

In shorthand:

```text
ECAT / ICAT -> BCAT -> GCAT
```

Meaning:

```text
experience and intuition -> boundary formation -> governance admissibility
```

## Existence Interpretation

The expression:

```text
GCAT / BCAT : ECAT / ICAT : %Existence
```

should be read as a governed existence formulation.

`%Existence` is not merely whether something can be observed. It is the degree to which an entity, claim, transition, relationship, or state can be treated as existing under the relevant governance frame.

A strong existence claim requires alignment across:

- ECAT: internal coherence and experiential standing;
- ICAT: relational coherence and inter-entity standing;
- BCAT: boundary recoverability and constraint integrity;
- GCAT: governance admissibility and authority standing.

For commit-time effects, StegVerse should treat missing or failed layers as fail-closed unless a policy explicitly defines a safe partial-standing condition.

## Chain Status Surface

The current chain-status reference is:

```text
docs/CHAIN_STATUS.md
```

The current chain-status handoff is:

```text
docs/CHAIN_STATUS_HANDOFF.md
```

The current chain snapshot and receipt are:

```text
docs/CHAIN_SNAPSHOT_v0_1_0.md
docs/CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json
```

The current automation-state and goal-state records are:

```text
docs/CHAIN_AUTO.json
docs/GOAL_STATE.json
```

The current blocked-destination records are:

```text
docs/CHAIN_STATUS_BLOCKED_DESTINATION.md
docs/CHAIN_STATUS_BLOCKED_DESTINATION.json
docs/CHAIN_STATUS_CONTINUATION.json
docs/CHAIN_STATUS_CONTINUATION.schema.json
```

The current automated validators are:

```text
scripts/check_chain_status_continuation.py
scripts/check_continuation_bundle.py
scripts/check_chain_snapshot.py
scripts/check_chain_snapshot_receipt.py
scripts/check_chain_auto.py
scripts/check_blocked_destination_record.py
scripts/check_goal_state.py
scripts/check_workflow_manifest.py
scripts/check_external_frameworks_index.py
scripts/check_guardian_destination.py
scripts/check_translation_records.py
```

Run:

```bash
python scripts/check_chain_status_continuation.py
python scripts/check_continuation_bundle.py
python scripts/check_chain_snapshot.py
python scripts/check_chain_snapshot_receipt.py
python scripts/check_chain_auto.py
python scripts/check_blocked_destination_record.py
python scripts/check_goal_state.py
python scripts/check_workflow_manifest.py
python scripts/check_external_frameworks_index.py
python scripts/check_guardian_destination.py
python scripts/check_translation_records.py
```

Expected current state:

```text
CHAIN CONTINUATION: PASS
CONTINUATION BUNDLE: PASS
CHAIN SNAPSHOT: PASS
CHAIN SNAPSHOT RECEIPT: PASS
CHAIN AUTO: PASS
BLOCKED DESTINATION RECORD: PASS
GOAL STATE: PASS
WORKFLOW MANIFEST: PASS
EXTERNAL FRAMEWORKS INDEX: PASS
GUARDIAN DESTINATION: BLOCKED
TRANSLATION RECORDS: PASS - 6 records validated
```

The canonical validation workflow is displayed here without the leading dot:

```text
github/workflows/validate-chain-continuation.yml
```

It runs on push, pull request, workflow dispatch, and a daily schedule. The actual repository path begins with a leading dot.

The iOS-safe workflow mirror is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

The mapping is recorded in:

```text
workflow_manifest.json
```

The destination-status report is generated at:

```text
reports/guardian_destination_status.json
```

The blocked destination record exists because no Guardian standing-boundary repository was found under the checked names. This does not change the governance status of the chain. It only prevents future sessions from inventing a destination repo.
