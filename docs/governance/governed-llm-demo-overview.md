# Governed LLM Demonstration Overview

This page introduces the fixture-first governed large language model demonstrator.

The demonstrator shows how an LLM can participate in a governed transition without becoming execution authority. It runs from static examples so that the path can be replayed and reconstructed without live provider calls, repository writes, public posting, or external memory mutation.

## Demonstration path

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
-> SDK manifest binding
-> SDK receipt handoff
```

## Source repositories

| Repository | Role |
| --- | --- |
| `StegVerse-org/LLM-adapter` | Emits the fixture-first governed session packet. |
| `StegVerse-org/StegVerse-SDK` | Validates the demo packet and receipt handoff. |
| `StegVerse-Labs/admissibility-wiki` | Publishes the public explanation and verification path. |

## Non-claims

```text
public_demo_page_claims_live_provider_governance == false
public_demo_page_claims_execution_authority == false
public_demo_page_claims_external_indexing == false
demo_is_fixture_first == true
adapter_and_sdk_remain_source_of_implementation_truth == true
```
