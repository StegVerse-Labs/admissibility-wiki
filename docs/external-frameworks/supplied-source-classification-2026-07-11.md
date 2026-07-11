---
title: Supplied External Framework Source Classification — 2026-07-11
---

# Supplied External Framework Source Classification — 2026-07-11

## Purpose

This record classifies the supplied URLs before they are used for framework promotion.

| Supplied source | Classification | Use |
|---|---|---|
| Open Policy Agent documentation | canonical official source | existing sourced-intake record refreshed |
| Cedar Policy project site | canonical official source | existing sourced-intake record refreshed |
| NeuralTrust AI governance guide | secondary commentary | research context only; not a framework promotion source |
| SPIFFE project site | canonical official source | existing sourced-intake record refreshed |
| OpenID Foundation AI-governance tag | official organizational commentary | context for OpenID relevance; OpenID Connect Core remains canonical specification |
| NHIMG OAuth governance FAQ | secondary commentary | context only; RFC 6749 remains canonical specification |
| W3C DID editor draft | official editor draft | sourced intake with explicit draft caution |
| in-toto project site | canonical official source | existing sourced-intake record refreshed |
| SLSA project site | canonical official source | existing sourced-intake record refreshed |
| Sigstore project site | canonical official source | existing sourced-intake record refreshed |
| OpenLineage project site | canonical official source | promoted to sourced intake |
| Wikipedia W3C PROV page | secondary discovery source | replaced by W3C PROV Overview as canonical source |
| Guardrails AI project site | canonical official source | promoted to sourced intake |
| Ollama Llama Guard 3 page | model distribution source | promoted with distribution-source caution |
| NVIDIA NeMo Guardrails documentation | canonical vendor documentation | promoted to sourced intake |

## Newly promoted candidates

```text
OpenID Connect
OAuth 2.0
W3C Decentralized Identifiers
OpenLineage
W3C PROV
Guardrails AI
Llama Guard
NeMo Guardrails
```

## Boundary

```text
source classification != validation
secondary commentary != canonical specification
distribution availability != model-behavior proof
editor draft != final recommendation
source capture != compatibility
```

Observed behavior requires exact version, configuration, input, output, timestamp, and replay or reconstruction evidence.
