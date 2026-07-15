# Governed LLM Demonstration Overview

## Purpose

This page introduces the fixture-first governed LLM demonstrator and places it within the wider StegVerse demonstration topology.

The fixture demonstrator shows how an LLM can participate in a governed transition without becoming execution authority. It uses static examples so the path can be replayed and reconstructed without live provider calls, repository writes, public posting, external memory mutation, or consequence-bearing execution.

## Fixture-first adapter demonstration

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
```

## Wider demonstration coordinates

The adapter fixture is one demonstration coordinate, not the entire public demo suite.

| Coordinate | Role | Current posture |
|---|---|---|
| Governed LLM adapter fixture | Demonstrates provider-output-to-governed-packet handling. | `FIXTURE_ONLY` |
| Governance Demo Suite | Demonstrates governance filtering, transition admissibility, receipt replay, comparison, and fail-closed behavior. | `PUBLIC_SIMULATION` |
| Dynamic Demo / Applicability Suite | Accepts tester packets and returns browser-local governed classifications. | `PUBLIC_SIMULATION` |
| Math Solver | Demonstrates source-to-mapping-to-instruction-to-artifact-to-admissibility flow. | `PUBLIC_ADAPTER_CONCEPT` |
| Ecosystem Chat | Public governed request-response entry surface. | `PREPARED_NOT_DEPLOYED` |
| Usage and comparison surfaces | Display configured trust, usage, and comparison contracts. | `PREPARED_NOT_DEPLOYED` |

These surfaces demonstrate different portions of the governed ecosystem and must not be represented as one completed live service.

## Source and display responsibilities

| Repository | Role |
|---|---|
| `StegVerse-org/LLM-adapter` | Emits fixture-first governed session packets and disabled execution handoffs. |
| `StegVerse-org/StegVerse-SDK` | Validates demo packets, routes intake, binds manifests, and emits receipt handoffs. |
| `StegVerse-Labs/Site` | Hosts public demo, Math Solver, Applicability, Ecosystem Chat, usage, and comparison surfaces. |
| `Data-Continuation/formalism-tests` | Owns executable fixtures, expected outcomes, and proof receipts where installed. |
| `master-records/orchestration` | Future authenticated custody and reconstruction coordinate. |
| `StegVerse-Labs/admissibility-wiki` | Publishes doctrine, topology, evidence posture, and verification boundaries. |

## What can be evaluated

A reviewer can evaluate the fixture-first path only to the extent that the pinned fixtures, scripts, expected outputs, generated reports, and replay or reconstruction commands are available in their authority repositories.

Public screenshots, prose, or displayed classifications alone are not reproduced results.

## Activation boundary

```text
fixture success != live provider governance
browser simulation != proof authority
public display != deployed service
SDK validation != execution authority
receipt handoff != Master-Records custody
replay != current standing
reconstruction != current standing
```

## Related pages

- [Governed LLM Activation Map](./governed-llm-activation-map.md)
- [Governed LLM Demo Verification](./governed-llm-demo-verification.md)
- [Governed LLM Deployment Status](./governed-llm-deployment-status.md)
- [LLM Free Tier Trust Chain](./llm-free-tier-trust-chain.md)
- [Wiki Section Completeness Audit](./wiki-section-completeness-audit.md)

## Non-claims

```text
public_demo_page_claims_live_provider_governance == false
public_demo_page_claims_execution_authority == false
public_demo_page_claims_external_indexing == false
public_demo_page_claims_master_records_custody == false
fixture_demo_is_reproducible_only_from_available_artifacts == true
adapter_and_sdk_remain_source_of_implementation_truth == true
formalism_tests_remains_source_of_executable_proof_truth == true
```