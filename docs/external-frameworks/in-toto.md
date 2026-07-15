---
title: in-toto
---
# in-toto

## Status

```text
Relationship type: external framework crosswalk
Evidence class: SOURCE_REVIEWED
Page completeness: COMPLETE_WITH_EXTERNAL_GATES
Runtime observation: none attached
Independent reproduction: false
Comparative testing claim allowed: false
Execution authority claim allowed: false
Maintenance owner: admissibility-wiki External Frameworks audit
```

## Official Source

- Project source: https://in-toto.io/
- Source posture: official project documentation captured; no pinned implementation run or verification fixture is attached.

## Framework-Native Scope

in-toto is a software supply-chain integrity framework built around layouts and signed link metadata. A layout describes expected steps, authorized functionaries, and inspection rules. Link metadata records what a functionary performed and the materials and products associated with that step.

## Evidence Provenance

| Evidence class | Current evidence | Status | Missing fields |
|---|---|---|---|
| Official framework source | Project documentation | present | pinned snapshot or immutable source hash |
| Official implementation | No versioned implementation package attached | missing | repository commit, package version, binary hash |
| Observed behavior | No StegVerse verification run attached | missing | layout, links, verifier output, timestamp |
| Reproduced behavior | No independent rerun | missing | replay command, environment, independent result |
| StegVerse analysis | Bounded crosswalk | present | common fixture execution |

## Relationship to Admissibility

```text
in-toto asks: Did the recorded supply-chain steps and functionaries conform to the declared layout?
StegVerse Admissibility asks: May this transition bind consequence at commit time under current authority, policy, delegation, evidence, and recoverability conditions?
```

Signed link metadata can strengthen origin, process, and custody evidence. It does not establish that a later actor remains authorized, that the intended action is currently permitted, or that consequence may bind.

## Execution Authority Boundary

```text
verified supply-chain step != current delegation
layout conformance != transition admissibility
signed metadata != execution authority
artifact provenance != permission to use or deploy the artifact
```

## Observation Boundary

```text
Public StegVerse fixture: none
Pinned in-toto implementation: none
Layout and link bundle: none
Verifier raw output: none
Timestamp and environment: none
Independent replay: none
```

No runtime, verifier, interoperability, or comparative result is claimed.

## StegVerse Analysis

| Criterion | Current result |
|---|---|
| Identity | Functionary identity may be represented, but current actor identity must be reconstructed separately. |
| Authority | Layout authorization is scoped to supply-chain steps, not later consequence binding. |
| Policy | Layout rules may become policy evidence; current StegVerse policy remains independently evaluated. |
| Delegation | Historical functionary authorization does not prove current delegation. |
| Evidence | Signed links may strengthen provenance if signatures, keys, and materials remain verifiable. |
| Replayability | Requires pinned implementation, layout, link bundle, keys, and verifier command. |
| Reconstructability | Strong for declared steps when custody and signature evidence remain available. |
| Commit-time validity | Not established by supply-chain verification alone. |
| Failure behavior | Missing links, invalid signatures, or layout mismatch must fail closed. |

## Commit-Time Interoperability Contract

Minimum fields for routing an in-toto result into a Commitment Candidate:

```text
transition_id
artifact_digest
layout_digest
link_metadata_digests
functionary_identities
verification_result
verification_timestamp
verifier_version
policy_reference
delegation_reference
target_action
execution_context
validity_window
recoverability_profile
```

## Failure Classes

| Failure class | Applies | Notes |
|---|---:|---|
| Semantic equivalence divergence | yes | A verified supply-chain claim may be overread as runtime safety or authorization. |
| Authority drift | yes | Historical functionary authority may no longer be current. |
| Stale evidence | yes | Keys, attestations, or dependency state may have changed. |
| Replay divergence | yes | Unpinned verifier or environment can change results. |
| Source-claim mismatch | yes | Layout coverage may be narrower than public wording. |
| Evidence-class confusion | yes | Source review must not be presented as a reproduced verification run. |

## Machine-Readable Companions

- Manifest: `docs/external-frameworks/in-toto.json`
- Compatibility report: `docs/external-frameworks/reports/in-toto.compatibility.json`
- Registry: `docs/external-frameworks/index.json`
- Canonical inventory: `static/external-frameworks/canonical-union-inventory.v1.json`

## Validation Completion Criteria

```text
pin an in-toto implementation and source hash
publish a minimal layout and signed link bundle
capture raw verifier output and timestamp
publish replay commands and expected result
rerun independently
route the result into a Commitment Candidate fixture
preserve non-claim and authority boundaries
```

## Non-Claims

in-toto is not a StegVerse canonical formalism. Verified provenance is not current delegation, transition admissibility, execution authority, certification, or general compatibility. This page does not claim a live integration or reproduced comparison.

## Challenge Path

A challenge must identify the affected claim or field, the layout or source version at issue, supporting evidence, and the requested correction or evidence-class change. Challenges do not themselves create standing.

## Next Safe Build Target

Publish one pinned layout/link verification fixture with raw output, immutable hashes, replay instructions, and an independent rerun before advancing beyond `SOURCE_REVIEWED`.

This page reflects a bounded admissibility packet. Publication does not create standing.