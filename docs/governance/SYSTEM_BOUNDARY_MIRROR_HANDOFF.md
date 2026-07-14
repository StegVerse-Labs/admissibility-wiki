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
static/governance/fixtures/system-boundary-declaration-cases.v0.1.json
scripts/check_system_boundary_declaration.py
scripts/check_governed_llm_pages.py
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
python scripts/check_governed_llm_pages.py
```

Expected:

```text
SYSTEM BOUNDARY DECLARATION: PASS
surfaces=5 feedback_paths=3
fixtures_passed=1 expected_failures=3
claims=operational-boundary-only authority=model-nonexecuting
GOVERNED LLM PAGES: PASS - docs, contracts, fixtures, and references present
```

Fixture coverage:

```text
valid composed system: PASS
false continuity without feedback paths: expected FAIL
missing commit boundary: expected FAIL
prohibited consciousness claim: expected FAIL
```

The governed-LLM pages checker is already invoked by the repository's canonical `npm run validate` chain, so no additional workflow was added.

## SDK integration installed

Destination:

```text
StegVerse-org/StegVerse-SDK
```

Installed SDK files:

```text
schemas/system-boundary-declaration.schema.v0.1.json
stegverse/system_boundary.py
tests/test_system_boundary.py
docs/SYSTEM_BOUNDARY_INGESTION.md
sdk.capabilities.json
SDK_MIRROR_HANDOFF.md
```

Installed bindings:

```text
manifest field: system_boundary_declaration
receipt reference field: system_boundary_declaration_ref
SDK status: accepted_for_non_authorizing_sdk_ingestion
```

SDK validation rejects false continuity, model authority escalation, missing commit boundaries, prohibited consciousness claims, and unexpected top-level fields.

## Destination integration

| Destination | State | Required continuation |
| --- | --- | --- |
| `StegVerse-org/StegVerse-SDK` | Structurally installed; workflow evidence pending. | Verify `pytest tests/test_system_boundary.py` through the existing SDK workflow and retain the receipt. |
| `StegVerse-org/LLM-adapter` | Pending. | Generate declarations from runtime model, orchestration, memory, environment, feedback, and authority configuration. |
| `StegVerse-Labs/Site` | Pending. | Display bounded system-boundary status after SDK and adapter verification. |
| `GCAT-BCAT-Engine/Publisher` | Pending. | Publish metadata only after the declaration is represented in a governed bundle. |

## Remaining files and modules

```text
StegVerse-Labs/admissibility-wiki:
- successful canonical validation receipt

StegVerse-org/StegVerse-SDK:
- successful sdk-demo-test receipt covering tests/test_system_boundary.py
- governed session manifest implementation binding, if not already accepted generically
- receipt serialization implementation for system_boundary_declaration_ref

StegVerse-org/LLM-adapter:
- *_MIRROR_HANDOFF.md review or creation before mutation
- declaration builder
- runtime surface inventory
- feedback-path recorder
- declaration identifier persistence
- adapter tests

StegVerse-Labs/Site:
- public system-boundary status component
- mirror verification receipt
```

## Next action

Check the authoritative `*_MIRROR_HANDOFF.md` in `StegVerse-org/LLM-adapter`, then implement a deterministic declaration builder that inventories configured runtime surfaces and emits evidence-backed feedback paths. Do not infer continuity from natural-language self-report, and do not treat recurrence, state continuity, or self-report as a consciousness determination.

## Release posture

```text
structural_contract: installed
negative_fixture_suite: installed
canonical_validation_integration: installed_execution_pending
sdk_integration: installed_validation_pending
adapter_integration: pending
site_mirror: pending
release_readiness: not_ready_for_tag
```

## Archive readiness

This handoff contains the complete current admissibility-wiki and SDK system-boundary integration state. Earlier thread context is not required for continuation.
