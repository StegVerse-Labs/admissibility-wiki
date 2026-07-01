# Governed LLM and Reconstructive Search

## Status

Public doctrine draft. This page describes the StegVerse-governed LLM model and the reconstructive search layer needed to support replay, reconstruction, freshness review, and storage minimization.

## Purpose

A StegVerse-governed LLM is not an execution authority. It is a reasoning participant inside a governed transition path.

The model may draft, explain, compare, classify, and propose. It may not independently authorize memory mutation, publication, repository mutation, external communication, private-data reuse, or consequence-bearing execution.

## Core Claim

```text
A governed LLM should not merely answer from memory.
It should answer from an admissible evidence state and emit a reconstructable receipt.
```

## System Shape

```text
user query
  -> ingestion
  -> query classification
  -> allowed source map
  -> reconstructive search / governed retrieval
  -> evidence packet
  -> candidate model response
  -> output admissibility check
  -> response receipt
  -> reconstruction record
  -> user
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

| Repository | Responsibility |
| --- | --- |
| `StegVerse-Labs/admissibility-wiki` | Public doctrine and explanatory pages. |
| `StegVerse-org/StegVerse-SDK` | Shared packet, receipt, evidence, and reconstruction contracts. |
| `StegVerse-org/LLM-adapter` | Runtime adapter that converts model output into governed response artifacts. |

## Minimum Public Proof Path

A minimum public proof path should show:

1. a user query enters the LLM adapter;
2. the adapter classifies the query and allowed sources;
3. the SDK creates a governed query packet;
4. the adapter receives candidate output from a model or fixture;
5. the SDK creates a governed response receipt;
6. the reconstruction summary proves the response path;
7. high-consequence output is quarantined until commit-time authority is established.

## Non-Claims

This page does not claim that any external LLM provider has adopted StegVerse governance.

This page does not claim that a model output is true merely because it has a receipt.

This page does not claim that historical reconstruction creates current authority.

## Working Definition

```text
A StegVerse-governed LLM is an LLM adapter path that turns user requests and model outputs into admissible, bounded, receipt-backed, reconstructable transitions.
```
