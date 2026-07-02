# Governed LLM and Reconstructive Search

## Status

Public doctrine and implementation-status page.

This page describes the StegVerse-governed LLM model, the reconstructive search layer needed to support replay and reconstruction, and the current repository split that implements the adapter and SDK contract boundaries.

## Current Build State

```text
StegVerse-org/LLM-adapter
  -> adapter boundary complete

StegVerse-org/StegVerse-SDK
  -> governed LLM contract layer active

StegVerse-Labs/admissibility-wiki
  -> public doctrine and verification map
```

## Purpose

A StegVerse-governed LLM is not an execution authority. It is a reasoning participant inside a governed transition path.

The model may draft, explain, compare, classify, and propose. It may not independently authorize memory mutation, publication, repository mutation, external communication, private-data reuse, or consequence-bearing execution.

## Core Claim

```text
A governed LLM should not merely answer from memory.
It should answer from an admissible evidence state and emit a reconstructable receipt.
```

## Built Runtime Shape

The current adapter-side runtime chain is:

```text
provider request
  -> provider response
  -> continuity evidence
  -> governed adapter receipt
  -> action route
  -> commitment request
  -> authority decision
  -> disabled execution handoff
  -> no side effect by default
```

The current SDK-side contract chain is:

```text
adapter session packet
  -> SDK validation
  -> SDK intake routing
  -> SDK manifest binding
  -> SDK receipt handoff
```

## Why Reconstructive Search Is Needed

Normal search asks:

```text
What documents match this query now?
```

Reconstructive search asks:

```text
What admissible evidence state existed then?
What changed since then?
What evidence supersedes the prior answer?
What can be reconstructed but not reused as current authority?
```

This allows the ecosystem to reconstruct prior discussions without storing every full transcript everywhere.

## Storage-Minimizing Reconstruction

The preferred record stores:

```text
query hash
retrieval source pointers
evidence hashes
source timestamps
policy hash
delegation hash
model/provider/version reference
output hash
admissibility decision
receipt chain
```

It avoids duplicating full payloads unless custody, quarantine, explicit distribution, or master-record policy requires retention.

## Replay Versus Reconstruction

| Term | Meaning |
| --- | --- |
| Replay | Run the same query or process again and compare the result. |
| Reconstruction | Prove what happened then, what evidence was available, what rules applied, and why the response was allowed, denied, or quarantined. |

Replay may not produce identical wording because models, sources, and sampling behavior can change.

Reconstruction should still prove the prior transition path.

## Freshness and Reuse

A prior answer may be historically reconstructable while no longer being currently admissible.

The governed response path must distinguish:

```text
current
stale
superseded
revoked
conflicted
quarantined
denied
```

## Consequence Boundary

Read-only explanation may use a fast path when the evidence state is low risk.

Consequence-bearing action must use a strict path:

```text
publish
commit
send
execute
mutate memory
change repository state
create public association
change user-impacting state
```

These actions require current standing at commit time.

## Repository Responsibilities

| Repository | Responsibility | Current implementation state |
| --- | --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and explanatory pages. | This page plus related governance documentation. |
| `StegVerse-org/StegVerse-SDK` | Shared packet, receipt, evidence, manifest, and handoff contracts. | Governed LLM contract layer active. |
| `StegVerse-org/LLM-adapter` | Runtime adapter that converts model output into governed response artifacts. | Adapter boundary complete. |

## Implementation Artifacts

### LLM Adapter

```text
adapter.capabilities.json
docs/ACTIVATION_STATUS.md
docs/GOVERNED_LLM_RUNTIME.md
scripts/smoke_governed_session.py
```

The adapter proves the full chain through fixture and optional provider boundaries while keeping execution disabled by default.

### SDK

```text
sdk.capabilities.json
docs/GOVERNED_LLM_SDK_ACTIVATION.md
docs/GOVERNED_LLM_SESSION_PACKETS.md
scripts/smoke_governed_llm_sdk.py
```

The SDK validates adapter session packets, routes them, binds manifests, and produces receipt handoffs without granting authority or executing side effects.

## Minimum Public Proof Path

A minimum public proof path should show:

1. a user query enters the LLM adapter;
2. the adapter classifies the query and allowed sources;
3. continuity search supplies evidence pointers;
4. a provider or fixture produces candidate output;
5. the adapter emits a governed session packet;
6. high-consequence output becomes an action route, not an action;
7. the action route becomes a non-authorizing commitment request;
8. authority decision is captured without side effects;
9. execution handoff remains disabled by default;
10. SDK validates the session packet;
11. SDK intake returns route, quarantine, reject, or fail-closed guidance;
12. SDK binds a manifest and receipt handoff for later persistence or review.

## Local Verification Commands

Adapter verification:

```bash
pytest
stegverse-llm-adapter fixtures/governed_response_fixture.json --pretty
python scripts/smoke_governed_session.py
```

SDK verification:

```bash
pytest tests/test_governed_llm.py
pytest tests/test_governed_llm_session.py
pytest tests/test_governed_llm_session_intake.py
pytest tests/test_governed_llm_manifest.py
pytest tests/test_governed_llm_receipt.py
python scripts/smoke_governed_llm_sdk.py
```

## Non-Claims

This page does not claim that any external LLM provider has adopted StegVerse governance.

This page does not claim that a model output is true merely because it has a receipt.

This page does not claim that historical reconstruction creates current authority.

This page does not claim that an adapter receipt grants execution authority.

This page does not claim that SDK manifest binding creates master-record persistence by itself.

## Working Definition

```text
A StegVerse-governed LLM is an LLM adapter path that turns user requests and model outputs into admissible, bounded, receipt-backed, reconstructable transitions while preserving a hard boundary between candidate output, authority, and side-effect execution.
```
