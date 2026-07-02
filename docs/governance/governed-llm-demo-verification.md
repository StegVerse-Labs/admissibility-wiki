# Governed LLM Demonstration Verification

This page describes how to verify the governed LLM demonstrator from the perspective of a StegVerse user.  It walks through running the demo, replaying and reconstructing sessions, and checking that the public documentation and navigation are present.  The verification steps ensure that the demo remains fixture‑based, reproducible, and non‑authoritative.

## Prerequisites

Before starting, ensure you have cloned the following repositories locally:

1. **LLM‑adapter** – contains the demo fixtures and scripts under `stegverse_demo/`.
2. **StegVerse‑SDK** – provides validation functions for governed session packets.
3. **admissibility‑wiki** – hosts the public documentation, including this page.

You should have Python 3.8 or newer installed.  No API keys or network access are required for the demo.

## Verifying the End‑to‑End Flow

1. **Run the demo** – From the root of the `LLM‑adapter` repository, execute:

   ```bash
   python3 stegverse_demo/scripts/run_end_to_end_demo.py --fixture stegverse_demo/examples/simple_query.json
   ```

   This generates a governed session packet and writes a report file to `stegverse_demo/reports/simple_query.session.json`.  The command also prints a summary to the console.

2. **Validate the session packet** – Use the SDK to validate the governed session packet:

   ```bash
   python3 stegverse_demo/scripts/validate_session_packet.py --session-report stegverse_demo/reports/simple_query.session.json
   ```

   This script calls the SDK’s `validate_governed_llm_session_packet` function and prints whether the packet conforms to the contract.

3. **Replay the session** – Check that the session can be reproduced from the report:

   ```bash
   python3 stegverse_demo/scripts/replay_demo.py --session-report stegverse_demo/reports/simple_query.session.json
   ```

   The script recomputes the request hash and provider response from the stored query and confirms they match the report.  A mismatch would indicate the session is not reproducible.

4. **Test stale evidence reconstruction** – Simulate a case where evidence becomes stale:

   ```bash
   python3 stegverse_demo/scripts/reconstruct_demo.py --session-report stegverse_demo/reports/simple_query.session.json
   ```

   The script artificially expires the evidence pointers and reruns the classification.  It should show that the session is now quarantined, demonstrating how governance responds to changing inputs.

5. **Inspect the manifest and receipt** – The demo writes a manifest and receipt file to the `stegverse_demo/reports/` directory.  Open these JSON files to see how the session packet is bound to a manifest and a verifiable receipt.

By completing these steps, you demonstrate that the governed LLM pipeline is reproducible and that stale evidence affects admissibility.

## Verifying the Public Documentation

To ensure that this documentation appears on the public site and remains linked correctly, a simple verification script is provided in the `admissibility‑wiki/scripts` folder.  After cloning the wiki repository, run:

```bash
python3 scripts/check_governed_llm_demo_docs.py
```

The script checks that the following conditions hold:

* The files `docs/governance/governed-llm-demo-overview.md` and `docs/governance/governed-llm-demo-verification.md` exist.
* Each file contains the expected top‑level heading (the first `#` heading matches the filename).
* `sidebars.js` lists both demo docs in the Governance section.
* The wiki `README.md` mentions the governed LLM demonstration and links to this page.

If any of these checks fail, the script exits with a non‑zero status and prints the missing element.  Running this script after updates helps maintain the integrity of the documentation.

## Non‑Claims

Remember that this demonstration **does not** provide any execution authority or live data retrieval.  It is a teaching tool designed to be fully reproducible.  Running it should not modify any external state or memory.  The examples and fixtures are purely illustrative and should not be interpreted as representing real‑world data or current states.
