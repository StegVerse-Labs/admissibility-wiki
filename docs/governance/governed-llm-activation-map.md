# Governed LLM Activation Map

## Status

The governed LLM path now has a public doctrine page, a runtime adapter boundary, an SDK contract layer, and a fixture-first end-to-end demonstrator path.

```text
admissibility-wiki
  -> public doctrine, verification map, demo overview, and demo verification

LLM-adapter
  -> provider/output/continuity/action/authority/execution boundary
  -> fixture-first end-to-end demo files

StegVerse-SDK
  -> validation/intake/manifest/receipt handoff boundary
  -> demo packet verification
```

## Active Repositories

| Repository | Role | Activation surface |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and Site-facing explanation | `docs/governance/governed-llm-demo-overview.md` |
| `StegVerse-org/LLM-adapter` | Runtime governed LLM adapter | `examples/end_to_end/simple_query.json` and `scripts/run_end_to_end_demo.py` |
| `StegVerse-org/StegVerse-SDK` | SDK governed LLM contract layer | `examples/governed_llm_demo/session_packet.simple_query.json` and `scripts/verify_governed_llm_demo_packet.py` |

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
  -> demo report artifacts
  -> replay verification
  -> reconstruction verification
  -> SDK demo packet verification
  -> Site demo overview and verification pages
```

## Adapter Demo Files

```text
examples/end_to_end/simple_query.json
examples/end_to_end/action_commit_candidate.json
examples/end_to_end/stale_evidence_query.json
scripts/run_end_to_end_demo.py
scripts/replay_demo.py
scripts/reconstruct_demo.py
docs/END_TO_END_DEMO.md
tests/test_end_to_end_demo.py
```

## SDK Demo Packet Files

```text
examples/governed_llm_demo/session_packet.simple_query.json
examples/governed_llm_demo/README.md
scripts/verify_governed_llm_demo_packet.py
tests/test_governed_llm_demo_packet.py
```

## Site Demo Overview Files

```text
docs/SITE_MIRROR_HANDOFF.md
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
scripts/check_governed_llm_demo_docs.py
sidebars.js
README.md
```

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
python scripts/run_end_to_end_demo.py --fixture examples/end_to_end/simple_query.json
python scripts/replay_demo.py --session-report reports/simple_query.session.json
python scripts/reconstruct_demo.py --session-report reports/simple_query.session.json
pytest tests/test_end_to_end_demo.py -v
pytest tests/ -v
```

SDK:

```bash
python scripts/smoke_governed_llm_sdk.py
python scripts/verify_governed_llm_demo_packet.py
pytest tests/test_governed_llm_demo_packet.py -v
pytest tests/test_governed_llm_session.py tests/test_governed_llm_session_intake.py tests/test_governed_llm_manifest.py tests/test_governed_llm_receipt.py -v
```

Site:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Boundary

```text
Provider output is not authority.
Adapter governance is not execution.
SDK validation is not authority.
Manifest binding is not persistence by itself.
Receipt handoff is not master-record installation by itself.
Execution handoff is not execution.
The demonstrator is fixture-first.
The demonstrator does not prove live provider governance.
The demonstrator does not prove external execution authority.
```

## Remaining External Work

| External layer | Status | Boundary |
| --- | --- | --- |
| Live provider credentials | Optional | Adapter clients fail closed without explicit keys. |
| Continuity search service | Optional | Service client fails closed without endpoint. |
| Master-record persistence | External | SDK emits receipt handoff only. |
| External executor | External | Adapter emits disabled handoff only. |
| Package release | External | Repo code and docs are present; publishing is separate. |
| GitHub Pages deployment | External | Local repo completion and public route reachability are checked separately. |

## Activation Statement

The governed LLM path is now build-visible across public doctrine, runtime adapter boundary, SDK contract intake, fixture-first demo artifacts, replay verification, reconstruction verification, and public demo documentation.

It is not yet a claim of live deployed provider governance, master-record persistence, external indexing, or external execution authority.
