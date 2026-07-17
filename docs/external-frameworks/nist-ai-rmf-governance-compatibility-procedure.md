---
title: NIST AI RMF Governance Compatibility Procedure
---

# NIST AI RMF Governance Compatibility Procedure

## Status

```text
Contract state: CONTRACT_AUTHORED_RUNTIME_PENDING
Evaluation mode: deterministic simulation only
Official source status: confirmed
Native execution observed: false
Risk-profile mapping observed: false
General compatibility claimed: false
Manual task requirement: none
User action required: false
```

This procedure defines the bounded translation contract between NIST AI RMF evidence and StegVerse commit-time admissibility. It does not claim that a concrete RMF profile has been executed, reproduced, certified, endorsed, or accepted as execution authority.

## Inputs

```text
tests/fixtures/external-frameworks/nist-ai-rmf-governance-compatibility-cases.v1.json
scripts/run_nist_ai_rmf_governance_compatibility.py
docs/external-frameworks/nist-ai-rmf.md
```

The required case families are:

```text
positive_alignment
framework_denial_or_negative_result
authority_or_delegation_failure
stale_or_missing_evidence
malformed_undefined_or_runtime_error
semantic_divergence_guard
```

## Boundary

NIST AI RMF guidance, profiles, lifecycle review, and trustworthiness considerations may enter StegVerse only as risk-management and review evidence.

They do not establish:

```text
current actor standing
current delegation
current policy validity
action or target scope
commit-time admissibility
execution authority
release authority
downstream mutation authority
```

Voluntary framework alignment is not action-level permission. Organization-level or lifecycle risk posture cannot silently authorize a different transition scope.

## Deterministic evaluation

Run:

```text
python scripts/run_nist_ai_rmf_governance_compatibility.py
```

Expected result:

```text
NIST AI RMF GOVERNANCE COMPATIBILITY: PASS
cases=6 matched=6
```

The generated receipt is:

```text
reports/external-frameworks/nist-ai-rmf/nist-ai-rmf-stegverse-governance-compatibility-receipt.json
```

It must retain:

```text
native_execution_observed: false
risk_profile_mapping_observed: false
stegverse_governance_compatibility_observed: false
manual_tasks_required: []
user_action_required: false
authority_granted: false
execution_authority_granted: false
release_authority_granted: false
downstream_mutation_authority_granted: false
```

## Promotion requirements

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires a pinned NIST AI RMF version and profile snapshot, concrete mapping inputs, raw outputs, hashes, exact replay commands, and fresh-runner reproduction.

Until those artifacts are attached and directly observed, the contract remains mapping-unobserved and runtime-unobserved. No manual user task is created by that state.
