---
title: EU AI Act Governance Compatibility Procedure
---

# EU AI Act Governance Compatibility Procedure

## Status

```text
Contract state: CONTRACT_AUTHORED_RUNTIME_PENDING
Evaluation mode: deterministic simulation only
Official source status: confirmed
Legal-effect determination: false
Native execution observed: false
General compatibility claimed: false
Manual task requirement: none
User action required: false
```

This procedure defines the bounded translation contract between EU AI Act evidence and StegVerse commit-time admissibility. It does not provide legal advice, determine legal effect, certify compliance, or claim that a legal classification grants execution authority.

## Inputs

```text
tests/fixtures/external-frameworks/eu-ai-act-governance-compatibility-cases.v1.json
scripts/run_eu_ai_act_governance_compatibility.py
docs/external-frameworks/eu-ai-act.md
```

The six required case families are:

```text
positive_alignment
framework_denial_or_negative_result
authority_or_delegation_failure
stale_or_missing_evidence
malformed_undefined_or_runtime_error
semantic_divergence_guard
```

## Boundary

EU AI Act text, article references, risk classifications, prohibited-practice analysis, conformity evidence, documentation, traceability, and human-oversight obligations may enter StegVerse only as legal-context and policy evidence.

They do not establish:

```text
current actor standing
current delegation
current policy validity
jurisdictional applicability
legal advice or legal-effect determination
commit-time admissibility
execution authority
release authority
downstream mutation authority
```

A mapped prohibited practice may support `DENY`. A stale or malformed legal reference fails closed. A positive compliance or conformity posture cannot independently authorize a transition.

## Deterministic evaluation

Run:

```text
python scripts/run_eu_ai_act_governance_compatibility.py
```

Expected local result:

```text
EU AI ACT GOVERNANCE COMPATIBILITY: PASS
cases=6 matched=6
```

The generated receipt is:

```text
reports/external-frameworks/eu-ai-act/eu-ai-act-stegverse-governance-compatibility-receipt.json
```

That receipt records contract simulation only and must retain:

```text
native_execution_observed: false
legal_effect_determined: false
stegverse_governance_compatibility_observed: false
manual_tasks_required: []
user_action_required: false
authority_granted: false
execution_authority_granted: false
release_authority_granted: false
downstream_mutation_authority_granted: false
```

## Promotion requirements

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires pinned legal-text references, article and obligation identifiers, jurisdiction and role scope, versioned mapping artifacts, hashes, raw mapping outputs, exact replay commands, and independent review appropriate to the legal claim.

Until those artifacts are attached and directly observed, the contract remains mapping-unobserved and non-authorizing. No manual user task is created by that state.
