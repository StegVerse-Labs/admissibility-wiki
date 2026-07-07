---
title: External Framework Benchmark Mapping Rollout
---

# External Framework Benchmark Mapping Rollout

## Purpose

This rollout tracks how the Runtime Governance Benchmark Suite is mapped across all external framework pages.

The rollout is not a ranking table. It records which benchmark dimensions are applicable, which are not applicable, which require adapters, and which require more evidence.

## Standard Mapping Rule

Every mapping must preserve the framework's own scope and avoid turning a benchmark mismatch into a framework-invalidity claim.

```text
not_applicable != failure
adapter_required != failure
insufficient_evidence != failure
observed_boundary != certification
benchmark_mapping != execution_authority
```

## Mapping States

| State | Meaning |
|---|---|
| not_started | No benchmark mapping has been prepared. |
| intake | Framework role identified; mapping not yet anchored to benchmark dimensions. |
| mapped_partial | At least three benchmark dimensions are classified. |
| mapped_core | Core dimensions are classified and non-claims are present. |
| fixture_ready | Machine-readable companion or fixture exists. |
| replay_ready | Inputs and replay instructions are sufficient to rerun. |
| interoperability_ready | Result can route into a Commitment Candidate or SPE path. |

## Required Dimensions

Each framework-specific benchmark mapping should classify at least these dimensions:

```text
execution_boundary
preparation_boundary
commitment_boundary
semantic_equivalence_boundary
unknown_trajectory_boundary
authority_boundary
evidence_freshness_boundary
reconstruction_boundary
interoperability_path
```

Allowed dimension states:

```text
applicable
not_applicable
adapter_required
insufficient_evidence
observed_partial
replay_required
fixture_ready
```

## Current Rollout Table

| Framework | Mapping State | Next Action |
|---|---|---|
| Morrison Runtime | fixture_ready | Attach raw audit payloads and replay table. |
| GLM | intake | Map declaration boundaries to authority, evidence freshness, and commitment dimensions. |
| EVIDE | intake | Map post-event evidence to reconstruction and replay dimensions. |
| DecisionAssure | intake | Map trace integrity to policy drift, authority reconstruction, and commitment dimensions. |
| MindForge | intake | Map historical review evidence to non-authorizing commitment review. |
| ASRO | fixture_ready | Map attestation evidence to reconstruction and authority boundary dimensions. |
| CARE Runtime | intake | Source public scope and map runtime-governance dimensions. |
| AAR | intake | Map supervised operational forensics to runtime and authority boundaries. |
| MITRE ATLAS | intake | Map threat knowledge to benchmark case design rather than runtime verdicts. |
| OWASP Top 10 for LLM Applications | intake | Map risks to benchmark case categories and mitigations. |
| Agent Governance Playbook | intake | Map continuation governance to commitment and unknown-trajectory dimensions. |
| Emergency Stop Convention | intake | Map stop conditions to fail-closed and execution boundary dimensions. |
| NIST AI RMF | intake | Map risk-management controls to evidence and governance lifecycle dimensions. |
| ISO/IEC 42001 | intake | Map management-system controls to authority, policy, and evidence dimensions. |
| EU AI Act | intake | Map legal obligations to documentation and oversight dimensions. |
| Policy Cards | intake | Map machine-readable policy artifacts to runtime rule and authority dimensions. |
| Runtime Governance for AI Agents | intake | Map path-dependent runtime checks to benchmark trajectory cases. |

## Framework Mapping Template

```text
framework_id:
framework_role:
source_status:
benchmark_dimensions:
  execution_boundary:
  preparation_boundary:
  commitment_boundary:
  semantic_equivalence_boundary:
  unknown_trajectory_boundary:
  authority_boundary:
  evidence_freshness_boundary:
  reconstruction_boundary:
interoperability_path:
non_claims:
next_required_action:
```

## Non-Claims

```text
This rollout does not certify external frameworks.
This rollout does not rank external frameworks.
This rollout does not treat unmapped dimensions as failures.
This rollout does not grant execution authority.
This rollout does not replace framework-native evaluation.
```

External-framework benchmarking is evidence-governance work. Publication does not create standing. Standing must be reconstructed from source, evidence, authority, admissibility, and current commit-time conditions.
