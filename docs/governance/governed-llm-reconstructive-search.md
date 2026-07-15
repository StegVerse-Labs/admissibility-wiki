# Governed LLM and Reconstructive Search

## Status

```text
page_posture: PUBLIC_DOCTRINE_WITH_FIXTURE_IMPLEMENTATION_REFERENCES
live_continuity_search_service: NOT_VERIFIED
live_provider_governance: NOT_CLAIMED
master_records_custody: EXTERNAL_NOT_ESTABLISHED_BY_THIS_PAGE
execution_authority: NOT_GRANTED
```

This page describes the governed LLM model, the reconstructive-search requirements needed for replay and reconstruction, and the ecosystem coordinates that produce, validate, display, preserve, and potentially execute governed results.

## Purpose

A StegVerse-governed LLM is a reasoning participant inside a governed transition path. It may draft, explain, compare, classify, retrieve, summarize, and propose. It may not independently authorize memory mutation, publication, repository mutation, external communication, private-data reuse, custody, or consequence-bearing execution.

## Core claim

```text
A governed LLM should not merely answer from model memory or present-day search.
It should identify an admissible evidence state, preserve source and policy context,
and emit a receipt that supports later reconstruction without converting history into current authority.
```

## Complete coordinate map

| Coordinate | Role | Current posture |
| --- | --- | --- |
| Ecosystem Chat | User-facing governed request and response surface | `PREPARED_NOT_DEPLOYED` for live same-origin usage path |
| Math Solver | Governed source, mapping, instruction and result pathway | `PUBLIC_CONCEPT_AND_FIXTURE_PATH` |
| Governance Demo Suite and Applicability | Browser-local and fixture testing surfaces | `FIXTURE_OR_BROWSER_ONLY` |
| `StegVerse-org/LLM-adapter` | Provider, output, continuity, action, commitment and disabled-execution boundary | `IMPLEMENTED_FIXTURE_FIRST` |
| `StegVerse-org/StegVerse-SDK` | Packet validation, intake, manifest binding and receipt handoff | `IMPLEMENTED_CONTRACT_LAYER` |
| Runtime producers | Core-node or micro-node governed request production | `DEMO_OR_FIXTURE_COORDINATES` |
| `Data-Continuation/formalism-tests` | Executable fixtures, expected outcomes and proof receipts | `EXTERNAL_PROOF_AUTHORITY` |
| `master-records/orchestration` | Authenticated custody and reconstruction evidence | `EXTERNAL_GATE` |
| Same-origin gateway, provider, search service and executor | Live network and consequence-bearing coordinates | `EXTERNAL_OR_BLOCKED_UNTIL_AUTHORIZED` |
| Admissibility Wiki and Site | Public explanation, topology and bounded display | `PUBLIC_DOCUMENTATION` |

## Runtime shape

```text
user or system request
  -> entry surface
  -> provider request envelope
  -> provider or fixture response
  -> source pointers and continuity evidence
  -> freshness, supersession and conflict classification
  -> governed session packet
  -> informational response or action route
  -> non-authorizing commitment request
  -> authority decision
  -> disabled execution handoff by default
  -> SDK validation, intake and manifest binding
  -> receipt handoff
  -> optional authenticated custody and reconstruction
```

No later stage may be inferred merely because an earlier stage exists.

## Why reconstructive search is needed

Ordinary search asks:

```text
What sources match this query now?
```

Reconstructive search asks:

```text
What admissible evidence state existed at the earlier decision time?
Which sources, policies, delegations and model versions were used?
What has changed, expired, conflicted, been revoked, or been superseded?
Can the prior result be reconstructed without treating it as current authority?
```

This supports questions about prior conversations or decisions without requiring every component to retain duplicate full transcripts. It does not eliminate the need for authorized payload custody where policy, consent, quarantine, litigation hold, explicit distribution, or Master-Records rules require it.

## Storage-minimizing reconstruction record

A bounded record may preserve:

```text
transition_id
query_hash
origin and entry surface
retrieval source pointers
source and evidence hashes
source timestamps and freshness state
policy and delegation references and hashes
model, provider and version reference
runtime configuration or fixture identity
candidate output hash
admissibility or authority decision
execution posture and result, if any
receipt and STRP references
custody pointer and reconstruction posture
```

Full payload retention should be governed separately. Hashes and pointers support integrity and location; they do not prove that a payload remains available or admissible.

## Replay, reconstruction, custody and reuse

| Term | Required distinction |
| --- | --- |
| Replay | Re-run a query or process and compare behavior. It may produce a different answer. |
| Reconstruction | Establish what happened then, which evidence and rules applied, and why the bounded result occurred. |
| Custody | Prove that required records were authentically installed and retained by the responsible layer. |
| Current reuse | Re-evaluate whether historical material may be used now under current policy, consent, freshness and authority. |

```text
Replayable != reconstructable.
Reconstructable != retained in authenticated custody.
Retained history != currently admissible evidence.
```

## Evidence-state vocabulary

A retrieved or reconstructed item should distinguish at least:

```text
CURRENT
STALE
SUPERSEDED
REVOKED
CONFLICTED
QUARANTINED
MISSING
SOURCE_BLOCKED
DENIED
```

The classification must identify who or what produced it, which rule set was applied, and whether it is an observation, fixture result, or authenticated status.

## Consequence boundary

Low-risk, read-only explanation may use a bounded informational path. Consequence-bearing actions require current commit-time standing:

```text
publish
commit or merge
send or post
execute a tool or external request
mutate memory or KnowledgeVault state
change repository or infrastructure state
create a public association
change user-impacting state
install or delete a master record
```

A prior answer, receipt, review, approval, or reconstruction does not authorize these actions.

## Public proof path

A minimum evaluable proof should show:

1. the request and entry surface;
2. allowed source scope and retrieval posture;
3. provider or fixture identity and version;
4. source pointers, hashes and freshness state;
5. the governed session packet;
6. separation of informational output from proposed action;
7. a commitment request for consequence-bearing action;
8. the authority decision and validity window;
9. an explicitly disabled execution handoff unless separately authorized;
10. SDK validation, intake, manifest and receipt handling;
11. replay and reconstruction artifacts;
12. custody status stated separately from receipt emission.

## Verification ownership

Adapter and SDK commands are repository-local implementation checks. The wiki's canonical workflow validates documentation references and public routes. Neither creates cross-repository current-main proof by itself.

```text
StegVerse-org/LLM-adapter
  -> adapter tests, demo replay and reconstruction

StegVerse-org/StegVerse-SDK
  -> packet, intake, manifest and receipt tests

StegVerse-Labs/admissibility-wiki
  -> documentation, navigation and bounded deployment-route checks
```

## Non-claims

```text
No external provider is claimed to have adopted StegVerse governance.
A receipt does not prove the truth of model output.
A query or source hash does not prove payload availability.
Historical reconstruction does not create current standing.
Adapter governance does not execute side effects.
SDK validation and manifest binding do not create authority or Master-Records custody.
A public page or reachable route does not prove live provider, search, gateway or executor activation.
```

## Working definition

```text
A StegVerse-governed LLM is a bounded reasoning and retrieval path that turns requests and candidate outputs into evidence-aware, receipt-backed and reconstructable transition records while preserving explicit separation among information, proposal, commitment, authority, execution, custody and current reuse.
```