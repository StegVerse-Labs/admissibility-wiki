# Governed LLM Activation Map

## Status

The governed LLM path now has a public doctrine page, a runtime adapter boundary, and an SDK contract layer.

```text
admissibility-wiki
  -> public doctrine and verification map

LLM-adapter
  -> provider/output/continuity/action/authority/execution boundary

StegVerse-SDK
  -> validation/intake/manifest/receipt handoff boundary
```

## Active Repositories

| Repository | Role | Activation surface |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and Site-facing explanation | `docs/governance/governed-llm-reconstructive-search.md` |
| `StegVerse-org/LLM-adapter` | Runtime governed LLM adapter | `adapter.capabilities.json` |
| `StegVerse-org/StegVerse-SDK` | SDK governed LLM contract layer | `sdk.capabilities.json` |

## Adapter Chain

```text
provider request
  -> provider response
  -> continuity evidence
  -> governed adapter receipt
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
```

## SDK Chain

```text
adapter session packet
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
```

## Verification Commands

Adapter:

```bash
pytest
stegverse-llm-adapter fixtures/governed_response_fixture.json --pretty
python scripts/smoke_governed_session.py
```

SDK:

```bash
pytest tests/test_governed_llm.py
pytest tests/test_governed_llm_session.py
pytest tests/test_governed_llm_session_intake.py
pytest tests/test_governed_llm_manifest.py
pytest tests/test_governed_llm_receipt.py
python scripts/smoke_governed_llm_sdk.py
```

## Boundary

```text
Provider output is not authority.
Adapter governance is not execution.
SDK validation is not authority.
Manifest binding is not persistence by itself.
Receipt handoff is not master-record installation by itself.
Execution handoff is not execution.
```

## Remaining External Work

| External layer | Status | Boundary |
| --- | --- | --- |
| Live provider credentials | Optional | Adapter clients fail closed without explicit keys. |
| Continuity search service | Optional | Service client fails closed without endpoint. |
| Master-record persistence | External | SDK emits receipt handoff only. |
| External executor | External | Adapter emits disabled handoff only. |
| Package release | External | Repo code and docs are present; publishing is separate. |

## Activation Statement

The governed LLM path is now build-visible across public doctrine, runtime adapter boundary, and SDK contract intake.

It is not yet a claim of live deployed provider governance, master-record persistence, or external execution authority.
