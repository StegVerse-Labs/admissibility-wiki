---
title: Tier 1 Source Intake Work Packets
---

# Tier 1 Source Intake Work Packets

## Purpose

This page turns the Tier 1 promotion queue into bounded source-capture work packets.

A work packet is not a promotion. It defines what must be collected before a candidate can move from `source_required` to `sourced_intake`.

```text
work packet != sourced intake
work packet != page candidate
work packet != benchmark mapping
work packet != endorsement
work packet != execution authority
```

## Required Capture Fields

Every Tier 1 packet must collect:

```text
canonical_source
source_version_or_date
published_scope
published_non_claims
artifact_type
relationship_class
benchmark_relevance
authority_boundary
evidence_posture
```

## Tier 1 Packets

| Candidate | Family | Capture focus | Target state |
|---|---|---|---|
| Open Policy Agent | policy_as_code | policy decision model, input/output contract, decision authority boundary, runtime integration | sourced_intake |
| Cedar Policy | policy_as_code | authorization model, policy language scope, entity/action semantics, decision boundary | sourced_intake |
| OSCAL | risk_and_assurance | machine-readable controls, assessment artifacts, evidence references, control versioning | sourced_intake |
| SPIFFE/SPIRE | identity_and_authority | workload identity, trust domains, attestation, credential lifecycle | sourced_intake |
| W3C Verifiable Credentials | identity_and_authority | credential model, roles, proof/status, revocation semantics | sourced_intake |
| in-toto | provenance_and_trace | supply-chain layout, link metadata, functionary identity, verification | sourced_intake |
| SLSA | provenance_and_trace | provenance levels, build integrity, source/builder identity, verification | sourced_intake |
| Sigstore | provenance_and_trace | artifact signing, identity binding, transparency log, verification | sourced_intake |
| Model Context Protocol | agent_protocols | tool/resource contracts, client-server roles, capability exposure, authorization | sourced_intake |
| Agent2Agent Protocol | agent_protocols | agent identity, task delegation, artifact exchange, completion/failure semantics | sourced_intake |

## Completion Rule

A packet is complete only when all required capture fields are present and the source is canonical enough to support independent review.

A packet with missing fields remains `source_capture_required`. It must not be copied into the promoted-intake registry.

## Non-Claims

```text
Packet completion does not certify the framework.
Packet completion does not prove compatibility.
Packet completion does not grant authority.
Packet completion does not establish benchmark standing.
Packet completion only permits sourced-intake review.
```

Standing remains a separate commit-time reconstruction question.
