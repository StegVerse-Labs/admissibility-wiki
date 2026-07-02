# Governed LLM Demonstration Overview

This page introduces the fixture‑based **governed large language model (LLM) demonstrator**.  The demonstrator shows how an LLM can participate in a **governed transition** without ever holding execution authority.  It runs entirely on static examples so that it can be replayed and reconstructed without writing to user memory, modifying repositories, or making outbound network calls.  It is an educational artifact rather than a production service.

## Purpose

The governed LLM demonstrator helps readers understand how the StegVerse ecosystem layers governance around a language model.  It illustrates the path from a user query to a response that includes:

* **Provider request and response envelopes** – the LLM adapter turns the user’s query into a hashable request object and receives a candidate response from a fixture or API provider.
* **Evidence and receipts** – every piece of external data used during reasoning is fingerprinted and bound to a receipt so the transition can be reconstructed later.
* **Governed session packet** – the adapter classifies the query, decides whether it is admissible, and emits a structured session object rather than a free‑form answer.
* **SDK intake and manifest** – the StegVerse SDK validates the session packet, produces an intake classification, binds a manifest, and issues a receipt ready for later replay.

By following this flow, the demonstrator highlights how StegVerse separates **reasoning** (what the model does) from **authority** (who can commit changes).  The model cannot mutate memory, commit to a repository, or take irreversible actions; it can only propose candidates.

## What the Demo Includes

The demonstrator ships with a set of JSON fixtures and scripts in the `stegverse_demo` folder of the **LLM adapter** repository:

* `examples/simple_query.json` – asks a basic informational question (“What is the capital of France?”) and produces an allowed response.
* `examples/action_commit_candidate.json` – simulates a query that would produce a commit candidate (e.g. drafting a repository change).  The adapter routes it to a non‑executing action candidate, and the SDK marks it as quarantined.
* `examples/stale_evidence_query.json` – simulates a replay where evidence has become stale.  The adapter identifies stale evidence and marks the session as quarantined.

The adapter’s scripts (`run_end_to_end_demo.py`, `replay_demo.py`, and `reconstruct_demo.py`) drive these fixtures through the governed path.  They produce session packets, manifests, and receipts in a `reports/` directory.

## Running the Demonstration

1. **Clone the repositories** – you will need the `LLM‑adapter`, `StegVerse‑SDK` and `admissibility‑wiki` repositories on your machine.  The demo does not require any network keys.
2. **Execute a demo** – run `python3 stegverse_demo/scripts/run_end_to_end_demo.py --fixture stegverse_demo/examples/simple_query.json` from the root of the `LLM‑adapter` repository.  This will generate a governed session packet and corresponding SDK artifacts.
3. **Inspect the output** – the script writes a JSON report in `stegverse_demo/reports/`.  You can open the report to see the query, request hash, provider response, evidence pointers, session classification, manifest, and receipt.
4. **Replay the session** – run `python3 stegverse_demo/scripts/replay_demo.py --session-report <path>` with the report from the previous step.  This recomputes the request hash and provider response from the stored query and checks that they match.
5. **Reconstruct stale evidence** – run `python3 stegverse_demo/scripts/reconstruct_demo.py --session-report <path>`.  This simulates evidence expiry and shows how the classification changes when sources are stale.

For full details on verifying the demonstrator and checking the public documentation, see the companion page **Governed LLM Demonstration Verification**.

## Important Limitations and Invariants

* **Fixture‑only** – the demonstrator never calls live web search, memory, or repository APIs.  All provider responses are defined in static fixtures to keep the demo deterministic.
* **No memory writes** – running the scripts does not persist any information beyond the generated reports.  Nothing is stored in user memory or written to a repository.
* **No execution authority** – commit, publish, or send actions are never executed.  Even when the adapter produces an action candidate, it is quarantined by default.
* **Not an external API** – this demo is not a hosted service.  It must be run locally and should not be treated as an authoritative or production environment.

By adhering to these invariants, the governed LLM demonstrator illustrates the governance model safely and reproducibly.
