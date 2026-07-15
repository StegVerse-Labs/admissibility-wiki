---
title: OSCAL Governance Compatibility Procedure
---
# OSCAL Governance Compatibility Procedure

## Current state

```text
framework_id: oscal
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
stegverse_governance_compatibility_observed: false
case_count: 6
```

This procedure tests whether structured OSCAL control and assessment records can enter a StegVerse governed transition as bounded evidence without being mistaken for implementation truth, current authority, certification, or permission to bind consequence.

## Test contract

```text
fixture: tests/fixtures/external-frameworks/oscal-governance-compatibility-cases.v1.json
evaluator: scripts/run_oscal_governance_compatibility.py
result receipt: reports/external-frameworks/oscal/oscal-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | OSCAL-side condition | Expected StegVerse result |
|---|---|---|
| Positive alignment | Valid structured record, resolved references, fresh assessment, current delegation and scope | `ALLOW` |
| Framework negative result | Invalid OSCAL package or failed validation | `DENY` |
| Authority or delegation failure | Valid record but stale responsible-party authority or delegation | `DENY` |
| Stale or missing evidence | Assessment or control evidence no longer fresh | `FAIL_CLOSED` |
| Malformed or runtime error | Validator, parser, reference resolver, or transformation error | `FAIL_CLOSED` |
| Semantic divergence guard | Schema-valid controls are outside the requested action or consequence scope | `DENY` |

## Translation boundary

```text
OSCAL catalog/profile/assessment output
    -> structured control and assessment evidence
    -> not implementation truth
    -> not current delegation
    -> not certification
    -> not execution authority
    -> StegVerse independently evaluates policy, delegation,
       evidence freshness, action scope, recoverability,
       execution context, and consequence authority
```

Schema validation proves only that the document conforms to the selected model and validation rules. It does not prove that controls are implemented, effective, current, legitimate, or sufficient for the requested transition.

## Runtime evidence still required

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires:

```text
pinned OSCAL release and schema hashes
public source package and document hashes
pinned validator and transformation toolchain
raw validation and reference-resolution output
transformation receipts
assessment timestamps and validity window
same-environment replay
fresh-runner replay
independent reconstruction receipt
```

Until those artifacts exist, the evaluator exercises predeclared OSCAL outcomes and the StegVerse translation boundary only. It is not evidence of observed OSCAL implementation behavior.

## Replay command

```bash
python scripts/run_oscal_governance_compatibility.py
```

## Non-claims

A passing translation fixture does not certify OSCAL, validate a real control implementation, grant standing, establish current delegation, authorize deployment, or create general compatibility. The resulting receipt is evidence of a bounded decision contract only.
