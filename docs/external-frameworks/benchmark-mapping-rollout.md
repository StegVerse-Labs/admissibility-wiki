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
| GLM | mapped_partial | Add GLM benchmark fixture for declaration freshness and semantic-equivalence boundary handling. |
| EVIDE | mapped_partial | Add EVIDE evidence fixture for replay and reconstruction dimensions. |
| DecisionAssure | mapped_partial | Add DecisionAssure canonical-policy fixture and map policy drift cases to benchmark dimensions. |
| MindForge | mapped_partial | Add MindForge historical-review fixture showing non-authorizing evidence routed through SPE. |
| ASRO | fixture_ready | Add ASRO observation fixture and replay/reconstruction status record. |
| CARE Runtime | mapped_partial | Identify official CARE Runtime source and create first sourced benchmark fixture. |
| AAR | mapped_partial | Add AAR evidence fixture for operational preparation and execution boundary records. |
| MITRE ATLAS | mapped_partial | Add MITRE ATLAS case-design fixture for adversarial trajectory benchmark categories. |
| OWASP Top 10 for LLM Applications | mapped_partial | Add OWASP risk-category fixture mapped to runtime benchmark cases. |
| Agent Governance Playbook | mapped_partial | Add continuation-state fixture for preparation and unknown-trajectory benchmark cases. |
| Emergency Stop Convention | mapped_partial | Add emergency-stop fixture for execution and unknown-trajectory benchmark cases. |
| NIST AI RMF | mapped_partial | Add NIST AI RMF control-mapping fixture for evidence freshness and lifecycle review. |
| ISO/IEC 42001 | mapped_partial | Add ISO/IEC 42001 management-control fixture for authority and policy dimensions. |
| EU AI Act | mapped_partial | Add EU AI Act obligation-mapping fixture for documentation and oversight dimensions. |
| Policy Cards | mapped_partial | Add policy-card fixture for unknown trajectory and preparation boundary cases. |
| Runtime Governance for AI Agents | mapped_partial | Add path-governance fixture for multi-step and unknown-trajectory benchmark cases. |

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
