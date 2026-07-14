# System Boundary Mirror Handoff

## Source of truth

This file is the bounded continuation record for the governed-LLM system-boundary workstream in `StegVerse-Labs/admissibility-wiki`. It is subordinate to `docs/SITE_MIRROR_HANDOFF.md` and must not overwrite Goal 5 ownership.

## Installed doctrine

```text
docs/governance/llm-consciousness-model-system-boundary.md
```

The doctrine distinguishes an isolated transformer invocation from a composed, stateful execution system. It does not classify consciousness, personhood, welfare status, or execution authority.

## Installed machine-readable artifacts

```text
static/governance/system-boundary-declaration.schema.v0.1.json
static/governance/system-boundary-declaration.example.v0.1.json
scripts/check_system_boundary_declaration.py
```

## Current contract

The declaration separates:

```text
model state
orchestration state
session state
durable memory
environment state
continuity and feedback paths
commit-time authority
claim boundaries
```

Required safeguards:

```text
model_has_execution_authority: false
consciousness_claim: not_evaluated
personhood_claim: not_evaluated
welfare_claim: not_evaluated
```

## Validation

Run:

```bash
python scripts/check_system_boundary_declaration.py
```

Expected:

```text
SYSTEM BOUNDARY DECLARATION: PASS
surfaces=5 feedback_paths=3
claims=operational-boundary-only authority=model-nonexecuting
```

## Destination integration

| Destination | Required installation |
| --- | --- |
| `StegVerse-org/StegVerse-SDK` | Shared schema, manifest field, receipt reference, fixture validation. |
| `StegVerse-org/LLM-adapter` | Runtime declaration generation from model, orchestration, memory, environment, and authority configuration. |
| `StegVerse-Labs/Site` | Public explanation and bounded status display after SDK and adapter verification. |
| `GCAT-BCAT-Engine/Publisher` | Publication metadata only after the declaration is represented in a governed bundle. |

## Remaining files and modules

```text
StegVerse-Labs/admissibility-wiki:
- negative fixtures for false continuity, missing authority boundary, and prohibited consciousness claims
- package validation integration

StegVerse-org/StegVerse-SDK:
- system-boundary declaration schema mirror
- governed session manifest binding
- declaration receipt reference
- SDK validator and fixtures

StegVerse-org/LLM-adapter:
- declaration builder
- runtime surface inventory
- feedback-path recorder
- adapter tests

StegVerse-Labs/Site:
- public system-boundary status component
- mirror verification receipt
```

## Next action

Create positive and negative declaration fixtures in `admissibility-wiki`, extend the validator to verify expected failures, then install the validated contract into `StegVerse-org/StegVerse-SDK`. Do not treat recurrence, state continuity, or self-report as a consciousness determination.

## Release posture

```text
structural_contract: installed
negative_fixture_suite: pending
canonical_validation_integration: pending
sdk_integration: pending
adapter_integration: pending
site_mirror: pending
release_readiness: not_ready_for_tag
```
