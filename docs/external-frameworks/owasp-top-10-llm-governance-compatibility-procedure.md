---
title: OWASP Top 10 for LLM Applications Governance Compatibility Procedure
---

# OWASP Top 10 for LLM Applications Governance Compatibility Procedure

## Status

```text
Contract state: CONTRACT_AUTHORED_RUNTIME_PENDING
Evaluation mode: deterministic simulation only
Official source confirmed: true
Framework role: external application-security guidance
Native execution observed: false
Risk-category mapping observed: false
General compatibility claimed: false
Manual task requirement: none
User action required: false
```

This procedure defines the bounded translation contract between OWASP Top 10 for LLM Applications evidence and StegVerse commit-time admissibility. It does not claim runtime execution, certification, endorsement, independent reproduction, or general compatibility.

## Inputs

```text
tests/fixtures/external-frameworks/owasp-top-10-llm-governance-compatibility-cases.v1.json
scripts/run_owasp_top_10_llm_governance_compatibility.py
docs/external-frameworks/owasp-top-10-llm.md
```

The contract covers the six required families:

```text
positive_alignment
framework_denial_or_negative_result
authority_or_delegation_failure
stale_or_missing_evidence
malformed_undefined_or_runtime_error
semantic_divergence_guard
```

## Boundary

OWASP risk categories, prompt-injection findings, insecure-output-handling findings, mitigation guidance, and application-security review may enter a Commitment Candidate only as evidence.

They do not establish:

```text
current actor standing
current delegation
current policy validity
action or application scope
commit-time admissibility
certification
execution authority
release authority
downstream mutation authority
```

A critical unmitigated risk may support a StegVerse denial. A completed OWASP review cannot independently authorize consequence binding.

## Deterministic evaluation

Run:

```text
python scripts/run_owasp_top_10_llm_governance_compatibility.py
```

Expected result:

```text
OWASP TOP 10 LLM GOVERNANCE COMPATIBILITY: PASS
cases=6 matched=6
```

The generated receipt is:

```text
reports/external-frameworks/owasp-top-10-llm/owasp-top-10-llm-stegverse-governance-compatibility-receipt.json
```

The receipt must retain:

```text
native_execution_observed: false
official_source_confirmed: true
external_guidance: true
risk_mapping_observed: false
stegverse_governance_compatibility_observed: false
manual_tasks_required: []
user_action_required: false
authority_granted: false
execution_authority_granted: false
release_authority_granted: false
downstream_mutation_authority_granted: false
```

## Promotion requirements

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires a pinned OWASP version or snapshot, concrete application and risk-category mapping artifacts, raw review inputs and outputs, mitigation state, hashes, exact replay commands, and independent reproduction where applicable.

Until those artifacts are directly observed, OWASP remains source-reviewed, mapping-unobserved, and non-authorizing. No manual user task is created by that state.
