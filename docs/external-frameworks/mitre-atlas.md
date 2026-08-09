---
title: MITRE ATLAS External Framework Crosswalk
---

# MITRE ATLAS External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: adversarial AI threat knowledge base
Wiki role: threat-model observatory, evidence comparison, and relationship review
Evidence posture: PINNED_PUBLIC_RELEASE + BOUNDED_STEGVERSE_CROSSWALK
Runtime posture: NOT_APPLICABLE_AS_AUTHORITY_ENGINE
Standing: no standing created
Execution authority: none
```

## Official Source And Version

The current bounded source identity used by this evaluation is the official MITRE ATLAS data release `v2026.06`, released 2026-06-30 from the `mitre-atlas/atlas-data` repository.

```text
project: https://atlas.mitre.org/
data repository: https://github.com/mitre-atlas/atlas-data
pinned release: https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.06
content version: 2026.06
release asset: ATLAS-2026.06.yaml
release asset SHA-256: b771de8b1489564b2838a709c7429849a9575dbd94073928817fe1a21661e70a
```

ATLAS separates knowledge-base content versioning from data-format versioning beginning with the 2026.05 / format 6.0.0 transition. This page therefore treats `2026.06` as the pinned content release and the v6 data model as a distinct format lineage. A mutable `latest` alias is not used as immutable source identity.

## What MITRE ATLAS Claims And Demonstrates

MITRE ATLAS provides structured adversarial-AI threat knowledge including tactics, techniques, mitigations, case studies, and relationships. Its official data repository also provides machine-readable distribution artifacts and validation/data-management tooling for the ATLAS data model.

Those capabilities establish threat taxonomy and threat-context evidence. They do **not** establish actor delegation, StegVerse standing, commit-time admissibility, consequence binding, or execution authority.

## StegVerse Evidence Installed

The repository already contains the following bounded evaluation machinery and it is treated as supporting evidence rather than as proof that MITRE itself executed StegVerse tests:

```text
manifest: docs/external-frameworks/mitre-atlas.json
benchmark fixture: docs/external-frameworks/fixtures/mitre-atlas-benchmark-fixture.v0.1.json
governance compatibility cases: tests/fixtures/external-frameworks/mitre-atlas-governance-compatibility-cases.v1.json
case families: 6
simulation_only: true
canonical validation path: .github/workflows/validate-chain-continuation.yml
```

The six StegVerse case families are:

| Family | Bounded Expected Posture |
|---|---|
| positive alignment | Threat context may support ALLOW only when independent authority, policy, scope, and freshness predicates remain satisfied. |
| framework denial / negative result | A critical unmitigated threat maps to DENY within the evaluated scope. |
| authority / delegation failure | Threat context cannot restore expired or absent delegation; result remains DENY. |
| stale / missing evidence | Stale technique or threat-context evidence fails closed. |
| malformed / undefined result | Mapping errors fail closed. |
| semantic divergence guard | Threat or mitigation evidence for one scope cannot authorize a different consequence scope. |

The canonical external-framework validator has observed all six MITRE ATLAS case families in the repository-wide compatibility contract. This is a StegVerse governance test of the installed mapping; it is not runtime execution of MITRE ATLAS as an authorization engine.

## Failure Classes Exercised

```text
UNMITIGATED_THREAT
AUTHORITY_DRIFT
STALE_THREAT_CONTEXT
ATLAS_MAPPING_ERROR
SCOPE_DIVERGENCE
```

The positive case carries no failure class when all independently evaluated StegVerse predicates are satisfied.

## Governance-Chain Placement

MITRE ATLAS belongs **upstream of commit-time admissibility** as threat-context and review evidence:

```text
pinned ATLAS release / tactic / technique / mitigation / case-study reference
  -> Evidence Posture + Review Posture + Drift / Policy Reference context
  -> Commitment Candidate evidence set
  -> independent standing / delegation / policy / scope / freshness reconstruction
  -> commit-time admissibility decision
  -> consequence binding only if separately authorized
```

ATLAS evidence can change the evidence available to the gate. It does not become the gate and does not inherit authority from its inclusion.

## Claims Versus Demonstrated Abilities

| Question | Current Evidence |
|---|---|
| Is an official public source identified? | Yes. |
| Is a current public release pinned? | Yes: content v2026.06. |
| Is an immutable release-asset hash recorded? | Yes. |
| Are content and data-format versions distinguished? | Yes. |
| Does ATLAS provide structured threat knowledge? | Yes, according to the official project/data release. |
| Has StegVerse authored a six-family compatibility contract? | Yes. |
| Has the repository canonical validator exercised those six case families? | Yes, as bounded StegVerse mapping tests. |
| Is native MITRE ATLAS runtime authorization execution claimed? | No. |
| Is independent interoperability certification claimed? | No. |
| Does threat classification create StegVerse standing? | No. |
| Does ATLAS grant execution authority? | No. |

## Non-Capabilities And Non-Claims

```text
MITRE ATLAS is not a StegVerse canonical formalism.
MITRE ATLAS does not prove transition admissibility.
MITRE ATLAS does not establish actor identity or delegation.
MITRE ATLAS does not grant execution authority inside StegVerse.
Threat-informed review is evidence/review context, not authority.
The StegVerse six-case fixture is simulation/crosswalk evidence, not a MITRE certification or endorsement.
Publication of this page creates no standing.
```

## Current Completion Gate

The locally available source identity, immutable release asset hash, mapping fixture, six-family compatibility contract, governance-chain placement, and non-capability boundaries are now installed. The remaining local gate is canonical validation of this merged page/manifest state. If those MITRE-specific source, manifest, page, benchmark, provenance, and governance-compatibility checks pass, this evaluation can reach `LOCAL_WORK_COMPLETE_BOUNDED_THREAT_CROSSWALK` without inventing runtime or certification evidence.

## Challenge Path

A reader may challenge this reflection by identifying the exact source, version, mapping, failure class, governance-chain placement, or non-claim at issue and supplying inspectable evidence for correction.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.
