# Governed LLM Activation Map

## Purpose

This page is the public topology of the governed-LLM ecosystem. It identifies every coordinate that accepts, produces, transports, evaluates, proves, records, reconstructs, displays, deploys, or executes a governed LLM transition.

A coordinate is included because it participates in the activation path. Inclusion does not grant authority, prove deployment, or imply that every coordinate is active.

## Coordinate Status Vocabulary

| Status | Meaning |
| --- | --- |
| `PUBLIC` | Publicly visible documentation or interface exists. |
| `FIXTURE_ONLY` | Reproducible local fixture path exists; no live external call is implied. |
| `PREPARED_NOT_DEPLOYED` | Implementation or client contract exists without verified live deployment. |
| `VALIDATION_PENDING` | Required repository-owned validation evidence has not yet been observed. |
| `EXTERNAL` | Coordinate is outside the repository and requires separately authorized evidence. |
| `BLOCKED` | One or more activation prerequisites are missing. |
| `VERIFIED` | Required evidence for the bounded claim has been observed and recorded. |

## Complete Activation Topology

```text
User entry surfaces
  ├─ Ecosystem Chat
  ├─ Math Solver
  ├─ Governance Demo Suite
  └─ Applicability / tester interface

Governed request production
  ├─ Site request envelope
  └─ core-node-runtime-demo or another authorized producer

Runtime governance
  └─ LLM-adapter

Contract and intake
  └─ StegVerse-SDK

Formalism and admissibility authority
  ├─ Data-Continuation/formalism-tests
  ├─ Transition Table proof surfaces
  ├─ RTG candidate formalism
  └─ STCM conservation formalism

Custody and reconstruction
  └─ Master-Records / orchestration

Public doctrine and verification
  ├─ admissibility-wiki
  └─ StegVerse-Labs/Site

External activation
  ├─ provider credentials
  ├─ same-origin gateway
  ├─ live deployment
  └─ explicitly authorized executor
```

## Coordinate Registry

| Coordinate | Repository or surface | Role | Current bounded posture |
| --- | --- | --- | --- |
| Public doctrine | `StegVerse-Labs/admissibility-wiki` | Vocabulary, topology, evidence rules, public verification guidance | `PUBLIC` |
| Ecosystem Chat | `StegVerse-Labs/Site/ecosystem-chat.html` | Primary governed request-response interface | `PREPARED_NOT_DEPLOYED` |
| Usage and role | `StegVerse-Labs/Site/ecosystem-usage.html` | Usage-session and participant-role display | `PREPARED_NOT_DEPLOYED` |
| Comparison | `StegVerse-Labs/Site/ecosystem-comparison.html` | Bounded provider and route comparison | `PREPARED_NOT_DEPLOYED` |
| Operational projection | `StegVerse-Labs/Site/governed-transitions.html` | Transition-state projection | `PUBLIC` |
| Math Solver | `StegVerse-Labs/Site/math-solver/` | Sources, mappings, generated instruction packets, artifact returns, and admissibility results | `PUBLIC`, concept/fixture posture |
| Governance Demo Suite | `StegVerse-Labs/Site/tests/` | Governance filter, LLM comparison, transition admissibility, receipt replay, and fail-closed demonstrations | `PUBLIC`, simulation posture |
| Dynamic demo | `StegVerse-Labs/Site/demo.html` | Browser-local dynamic admissibility classification | `PUBLIC`, simulation posture |
| Applicability suite | `StegVerse-Labs/Site/applicability/` | Discipline registry, tester guide, matrices, packets, and examples | `PUBLIC` |
| Runtime adapter | `StegVerse-org/LLM-adapter` | Provider/output/continuity/action/authority/execution boundary | `FIXTURE_ONLY`; live activation external |
| SDK contract layer | `StegVerse-org/StegVerse-SDK` | Validation, intake, manifest binding, metadata ingestion, and receipt handoff | `FIXTURE_ONLY` / repository contract active |
| Runtime producer | `StegVerse-org/core-node-runtime-demo` or authorized successor | Emits governed runtime requests and usage events | `EXTERNAL`, activation evidence required |
| Formalism tests | `Data-Continuation/formalism-tests` | Executable fixtures, expected outcomes, and proof receipts | `EXTERNAL` authority source |
| Transition Table | formalism-test authority plus public mirrors | Standing, decision classes, consequence tiers, and proof posture | `PUBLIC` mirror; authority remains external |
| RTG | formalism candidate | Relative-transition geometry | Draft/candidate; not proof authority |
| STCM | formalism candidate | State-transition conservation | Research/candidate; not proof authority |
| Custody | `master-records/orchestration` | Authenticated receipt custody and reconstructability evidence | `EXTERNAL`, required before `RECORDED` |
| Same-origin gateway | authorized deployment topology | Authenticated transport between Site and runtime destination | `BLOCKED` until deployment evidence |
| Provider credentials | provider-owned configuration | Live provider access | Optional and `EXTERNAL` |
| Executor | separately authorized executor | Consequence binding | Disabled or absent unless explicit authority exists |

## Entry-Surface Detail

### Math Solver

The Math Solver coordinate includes more than a landing page. Its activation surface includes:

```text
source and paper registry
  -> source-to-instruction mapping
  -> generated instruction packet
  -> generated or returned artifact
  -> admissibility result
  -> receipt or evidence handoff
```

A generated solver artifact is not automatically correct, admissible, authoritative, or executable.

### Governance Demo Suite

The demo suite includes separate bounded demonstrations for:

```text
governance filtering
LLM governance comparison
transition admissibility
receipt replay
fail-closed behavior
```

Browser simulation is not proof authority and is not a live runtime deployment.

### Applicability and Dynamic Tester

The applicability coordinate contains discipline-facing registries, test matrices, packet templates, and examples. Dynamic browser classification demonstrates packet shape and governance vocabulary; it does not replace executable formalism tests.

## Runtime and SDK Chain

```text
entry-surface request
  -> provider request envelope
  -> fixture or live provider response
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

The reproducible default remains fixture-first. Fixture success does not establish live provider governance.

## Formalism, Proof, and Standing Chain

```text
proposed transition
  -> formalism fixture or declared test vector
  -> expected outcome
  -> executable evaluation
  -> proof receipt
  -> Transition Table standing
  -> current commit-time validity check
```

Public mirrors may explain or display this chain. They do not become the formalism or proof authority.

## Custody and Reconstruction Chain

```text
runtime or denial receipt
  -> authenticated custody submission
  -> master-record pointer and digest
  -> reconstruction inputs
  -> reconstructability evaluation
  -> bounded RECORDED claim
```

Receipt creation is not custody. `RECORDED` requires authenticated custody evidence and reconstructability evidence.

## Deployment and Execution Chain

```text
prepared Site client
  -> authorized same-origin gateway
  -> validated runtime destination
  -> conforming live response
  -> retrieval and usage receipts
  -> authenticated custody
  -> current admissibility
  -> separately authorized execution
```

Prepared source code is not deployment. Deployment is not authority. Execution remains a distinct, explicitly authorized boundary.

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

Wiki:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
python scripts/check_governed_llm_deployment_status.py
```

Site validation and deployment evidence remain owned by the Site and destination repositories.

## Activation Gates

Full live activation remains blocked until the bounded path has all applicable evidence:

```text
destination current-main validation
same-origin authenticated deployment
sample response conformance
retrieval and usage receipts
no browser secret surface
Site current-main validation
formalism or policy standing where required
Master-Records custody
reconstructability PASS
explicit execution authority for any consequence-binding action
```

## Boundary

```text
Provider output is not authority.
Adapter governance is not execution.
SDK validation is not authority.
Manifest binding is not persistence.
Receipt handoff is not custody.
Fixture success is not live provider governance.
Browser simulation is not proof authority.
Public display is not deployment.
Deployment is not admissibility.
Replayability is not current execution authority.
Historical reconstruction is not current admissibility.
Execution handoff is not execution.
```

## Activation Statement

The governed-LLM ecosystem is build-visible across public doctrine, user-entry surfaces, fixture-first runtime governance, SDK intake, formalism and proof coordinates, custody requirements, and deployment boundaries.

The complete topology is visible; complete live activation is not claimed. Provider access, authorized deployment, authenticated custody, reconstructability, and any consequence-binding execution remain separately evidenced and governed.