# Governed LLM Activation Map

## Status

The governed LLM path now has a public doctrine page, a runtime adapter boundary, an SDK contract layer, and a fixture-first end-to-end demonstrator documentation surface.

```text
admissibility-wiki
  -> public doctrine, activation map, demo overview, demo verification, Site verification, archive handoff

LLM-adapter
  -> provider/output/continuity/action/authority/execution boundary and fixture-first demo runtime

StegVerse-SDK
  -> validation/intake/manifest/receipt handoff boundary and demo packet verification
```

## Active Repositories

| Repository | Role | Activation surface |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and Site-facing explanation | `docs/governance/governed-llm-reconstructive-search.md`, `docs/governance/governed-llm-demo-overview.md`, `docs/governance/governed-llm-demo-verification.md` |
| `StegVerse-org/LLM-adapter` | Runtime governed LLM adapter | `adapter.capabilities.json`, `examples/end_to_end/*.json`, `scripts/run_end_to_end_demo.py`, `scripts/replay_demo.py`, `scripts/reconstruct_demo.py` |
| `StegVerse-org/StegVerse-SDK` | SDK governed LLM contract layer | `sdk.capabilities.json`, `scripts/verify_governed_llm_demo_packet.py`, `tests/test_governed_llm_demo_packet.py` |

## End-to-End Demonstrator Status

```text
fixture query
  -> provider request envelope
  -> fixture provider response
  -> continuity evidence pointers
  -> governed session packet
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
  -> public demo overview
  -> public demo verification
```

The Site layer now explains the demonstrator through:

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
scripts/check_governed_llm_demo_docs.py
```

## Adapter Chain

```text
fixture query
  -> provider request
  -> fixture provider response
  -> continuity evidence
  -> governed adapter receipt
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
  -> demo report artifacts
  -> replay verification
  -> reconstruction verification
```

## SDK Chain

```text
adapter session packet
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
  -> demo packet verification
```

## Site Chain

```text
public doctrine
  -> public activation map
  -> public demo overview
  -> public demo verification
  -> local Site verification
  -> deployed route verification
  -> archive handoff
```

## Fixture-First Proof Path

The demonstrator is fixture-first. It does not call live providers by default, does not execute side effects, does not grant authority, and does not persist master records by itself.

The fixture-first path exists so a reviewer can reproduce the documentation and demo behavior without keys, network calls, repository writes, external memory mutation, or provider governance claims.

## Replay and Reconstruction Proof Path

Replay checks whether the stored query and session report can reproduce the request hash and fixture provider response.

Reconstruction checks whether evidence freshness changes the admissibility posture. A stale-evidence reconstruction may quarantine or deny a transition even when the original informational query was allowed.

## Verification Commands

Adapter:

```bash
python scripts/run_end_to_end_demo.py --fixture examples/end_to_end/simple_query.json
python scripts/replay_demo.py --session-report reports/simple_query.session.json
python scripts/reconstruct_demo.py --session-report reports/simple_query.session.json
pytest tests/test_end_to_end_demo.py -v
```

SDK:

```bash
python scripts/smoke_governed_llm_sdk.py
python scripts/verify_governed_llm_demo_packet.py
pytest tests/test_governed_llm_demo_packet.py -v
```

Site:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

Deployment:

```bash
python scripts/check_governed_llm_deployment_status.py
```

## Boundary

```text
Provider output is not authority.
Adapter governance is not execution.
SDK validation is not authority.
Manifest binding is not persistence by itself.
Receipt handoff is not master-record installation by itself.
Execution handoff is not execution.
Fixture success is not live provider governance.
Replayability is not current execution authority.
Historical reconstruction is not current admissibility.
```

## Remaining External Work

| External layer | Status | Boundary |
| --- | --- | --- |
| Live provider credentials | Optional | Adapter clients fail closed without explicit keys. |
| Continuity search service | Optional | Service client fails closed without endpoint. |
| Master-record persistence | External | SDK emits receipt handoff only. |
| External executor | External | Adapter emits disabled handoff only. |
| Package release | External | Repo code and docs are present; publishing is separate. |
| Deployed route confirmation | External to local repo completion | GitHub Pages and caches must be checked separately. |

## Activation Statement

The governed LLM path is now build-visible across public doctrine, runtime adapter boundary, SDK contract intake, and fixture-first public demonstrator documentation.

It is not a claim of live deployed provider governance, master-record persistence, external indexing, or external execution authority.
