# Governed LLM Demonstration Verification

## Purpose

This page defines what can be verified across the governed LLM demonstration topology and prevents documentation, fixture, deployment, custody, and execution evidence from being collapsed into one result.

## Verification classes

| Class | Question | Minimum evidence | Current posture |
|---|---|---|---|
| Documentation verification | Are the required pages and navigation references present? | Repository files, sidebar references, successful documentation checker. | `LOCAL_CHECK_AVAILABLE` |
| Fixture execution | Does the pinned fixture produce the expected bounded packet? | Pinned fixture, repository version, command, raw output, expected result. | `REPOSITORY_OWNED` |
| Replay verification | Can stored fixture inputs reproduce the recorded request and response hashes? | Session report, replay command, matching hashes. | `REPOSITORY_OWNED` |
| Reconstruction verification | Can a reviewer determine the prior evidence state and a changed freshness posture? | Evidence pointers, timestamps, policy state, reconstruction report. | `REPOSITORY_OWNED` |
| SDK contract verification | Does the SDK validate, route, bind, and return a receipt handoff without granting authority? | Demo packet, validator output, test results. | `REPOSITORY_OWNED` |
| Public route verification | Are the published wiki routes reachable after deployment? | Workflow-owned route observations and public receipt. | `PENDING_OBSERVATION` |
| Live provider conformance | Does an authorized deployed provider path return conforming governed responses? | Authorized endpoint, pinned configuration, raw response, receipt and conformance report. | `NOT_ESTABLISHED` |
| Master-Records custody | Was the result accepted into authenticated custody and reconstructability verified? | Authenticated custody receipt and reconstructability `PASS`. | `NOT_ESTABLISHED` |
| External execution | Was a consequence-bearing action explicitly authorized and executed? | Commit-time authority decision, executor receipt, result receipt. | `DISABLED_OR_EXTERNAL` |

## Adapter fixture commands

Run in `StegVerse-org/LLM-adapter` against the pinned repository version recorded by the result:

```bash
python scripts/run_end_to_end_demo.py --fixture examples/end_to_end/simple_query.json
python scripts/replay_demo.py --session-report reports/simple_query.session.json
python scripts/reconstruct_demo.py --session-report reports/simple_query.session.json
pytest tests/test_end_to_end_demo.py -v
```

A public result requires the fixture, commit or release identity, configuration, expected result, raw generated reports, timestamps, and hashes. A command list by itself is not a reproduced result.

## SDK commands

Run in `StegVerse-org/StegVerse-SDK` against the pinned repository version recorded by the result:

```bash
python scripts/smoke_governed_llm_sdk.py
python scripts/verify_governed_llm_demo_packet.py
pytest tests/test_governed_llm_demo_packet.py -v
```

SDK validation proves contract handling only. It does not prove provider truth, deployment, authority, execution, persistence, or custody.

## Wiki commands

Run in `StegVerse-Labs/admissibility-wiki`:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run validate
```

These commands establish repository-local documentation and build consistency when they pass. Canonical workflow evidence must be observed separately before a workflow pass is claimed.

## Wider demo-suite verification

The adapter fixture is not the entire demonstration suite. Separate evidence is required for:

```text
Governance Demo Suite
Dynamic Demo / Applicability Suite
Math Solver
Ecosystem Chat
Usage and comparison surfaces
runtime producers
formalism-test fixtures
Master-Records custody
```

Browser-local simulations and displayed examples must be classified as `PUBLIC_SIMULATION` or `PUBLIC_ADAPTER_CONCEPT` unless executable fixtures, expected outcomes, raw outputs, and replay instructions are available from the authority repository.

## Result record

A reusable verification record should contain:

```text
coordinate
repository
commit_or_release
verification_class
input_or_fixture
configuration
expected_result
actual_result
raw_artifact_paths
artifact_hashes
timestamp
operator_or_workflow
reproduced_by
missing_fields
current_posture
non_claims
```

## Boundary

```text
documentation pass != fixture pass
fixture pass != live provider governance
browser simulation != executable proof
replay pass != current authority
reconstruction pass != current authority
SDK validation != execution authority
public reachability != operational standing
receipt handoff != Master-Records custody
custody receipt != execution authority
```
