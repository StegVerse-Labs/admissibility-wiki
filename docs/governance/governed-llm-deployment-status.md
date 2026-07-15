# Governed LLM Deployment Status

## Purpose

This page distinguishes repository-local documentation validation, GitHub Pages reachability, Site application deployment, destination adapter deployment, authenticated custody, and execution authority.

These states are separate and must not be collapsed into one deployment claim.

## Current status

```text
wiki_documentation: PRESENT
wiki_local_validation: REPOSITORY_OWNED
wiki_public_route_verification: PENDING_OBSERVATION
site_contract_status: PREPARED_NOT_DEPLOYED
site_live_transport_enabled: false
adapter_authorized_same_origin_deployment: NOT_OBSERVED
master_records_custody: NOT_OBSERVED
reconstructability_pass: NOT_OBSERVED
external_execution_authority: NOT_GRANTED
release_or_tag_authority: NOT_GRANTED
```

## Validation layers

| Layer | What it establishes | What it does not establish |
|---|---|---|
| Repository-local checks | Required files, navigation, schemas, and documentation assertions are present. | Public reachability or live service activation. |
| Wiki Pages verification | Expected wiki routes respond after deployment. | Site application deployment, provider calls, custody, or execution authority. |
| Site current-main validation | Site contract and public display pass repository-owned checks. | Authorized same-origin deployment. |
| Adapter current-main validation | Destination source implementation and contracts pass destination-owned tests. | A deployed endpoint or live provider governance. |
| Same-origin conformance | An authorized deployed route returns a conformant response and retrieval receipt. | Master-Records custody or current execution authority. |
| Custody and reconstruction | Authenticated custody and reconstructability PASS are evidenced. | Permission to execute a new consequence-bearing action. |

## Canonical workflow ownership

The single canonical wiki workflow owns local validation, Pages build, Pages deployment, public route verification, and public activation receipt generation:

```text
.github/workflows/validate-chain-continuation.yml
```

No manual route check or workflow rerun is assigned to the user.

## Wiki public routes

The governed LLM deployment checker should cover the complete public documentation set, including:

```text
/governance/governed-ecosystem-index
/governance/governed-ecosystem-transitions
/governance/governed-llm-reconstructive-search
/governance/governed-llm-activation-map
/governance/governed-llm-demo-overview
/governance/governed-llm-demo-verification
/governance/governed-llm-site-verification
/governance/governed-llm-deployment-status
/governance/llm-free-tier-trust-chain
/governance/portable-governed-return-path
/governance/wiki-section-completeness-audit
```

A reachable route is deployment evidence for that documentation page only.

## External activation gates

Live governed LLM activation remains blocked until all relevant evidence is verified:

```text
destination current-main tests
same-origin authenticated deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records custody
reconstructability PASS
explicit action-level execution authority when consequence is requested
```

## Boundary

```text
Local validation != public deployment.
Wiki public reachability != Site application deployment.
Site display != provider call.
Prepared client != deployed endpoint.
Retrieval receipt != Master-Records custody.
Custody evidence != execution authority.
Replayability != current admissibility.
Historical reconstruction != current authority.
Pages deployment != release readiness.
```

## Completion class

```text
COMPLETE_WITH_EXTERNAL_GATES
```

The documentation model is complete enough to distinguish the relevant activation coordinates. Public workflow evidence and all live external gates remain fail-closed until observed.