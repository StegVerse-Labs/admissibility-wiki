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
mapped_partial
replay_required
fixture_ready
```

`mapped_partial` at the dimension level means that a crosswalk exists, but the dimension still lacks the source, replay, or implementation evidence required for a stronger state.

## Current Rollout Table

| Framework | Mapping State | Next Action |
|---|---|---|
| Morrison Runtime | fixture_ready | Attach raw audit payloads and replay table. |
| GLM | fixture_ready | Attach source-versioned GLM declaration examples and replay through Commitment Candidate. |
| EVIDE | fixture_ready | Attach concrete EVIDE evidence package examples and reconstruction receipt. |
| DecisionAssure | fixture_ready | Attach canonical policy/delegation examples and trace hashes. |
| MindForge | fixture_ready | Attach historical review sample and current-standing reconstruction example. |
| ASRO | fixture_ready | Attach concrete ASRO attestation examples and reconstruction receipt. |
| CARE Runtime | fixture_ready | Attach official CARE Runtime source before any public behavior claim. |
| AAR | fixture_ready | Attach concrete AAR operational evidence package and reconstruction receipt. |
| MITRE ATLAS | fixture_ready | Attach source-versioned MITRE ATLAS technique mappings to benchmark cases. |
| OWASP Top 10 for LLM Applications | fixture_ready | Attach source-versioned OWASP risk category mappings to benchmark cases. |
| Agent Governance Playbook | fixture_ready | Attach concrete continuation-state examples and replay through Commitment Candidate. |
| Emergency Stop Convention | fixture_ready | Attach emergency-stop trigger examples and reconstruction receipt. |
| NIST AI RMF | fixture_ready | Attach NIST AI RMF control examples and lifecycle evidence package. |
| ISO/IEC 42001 | fixture_ready | Attach ISO/IEC 42001 control examples and management-record evidence package. |
| EU AI Act | fixture_ready | Attach EU AI Act obligation mapping examples and documentation evidence package. |
| Policy Cards | fixture_ready | Attach source-versioned policy-card examples and replay through unknown/preparation cases. |
| Runtime Governance for AI Agents | fixture_ready | Attach concrete path-policy traces and replay through multi-step cases. |

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
