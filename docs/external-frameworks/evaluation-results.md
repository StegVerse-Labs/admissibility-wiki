---
title: External Framework Evaluation Results
---

# External Framework Evaluation Results

## Current Public Result Boundary

No external framework currently has a completed, independently reproducible comparative evaluation on this page.

The records below are compatibility, source, intake, mapping, or commentary records. They must not be read as comparative benchmark results unless the linked record includes all required reproducibility fields.

```text
framework mention != comparative test
source review != comparative test
author commentary != comparative test
StegVerse mapping != comparative test
compatibility report != independently reproduced result
```

## Evidence-State Vocabulary

| State | Minimum evidence | Permitted public claim |
|---|---|---|
| `MENTION_ONLY` | Framework is identified or discussed. | The framework is relevant to the documented topic. |
| `AUTHOR_COMMENTARY` | A framework author, operator, or reviewer supplied narrative observations. | The named person reports the stated relationship or result. |
| `SOURCE_REVIEWED` | Official sources were reviewed and version or date context is recorded. | The page accurately summarizes the cited source within its bounded scope. |
| `ARTIFACT_REVIEWED` | Inputs or outputs are public and inspectable, but no shared reproducible harness exists. | StegVerse reviewed the identified artifacts. |
| `PARAMETERIZED_OBSERVATION` | Input parameters, expected boundary, observed output, source context, and missing fields are recorded. | The bounded observation occurred under the recorded conditions. |
| `REPRODUCIBLE_COMPARATIVE_TEST` | Shared vectors, pinned versions, executable harness, raw outputs, scoring, replay instructions, hashes, and independent reproduction exist. | The bounded comparison was independently reproduced. |

Only `REPRODUCIBLE_COMPARATIVE_TEST` supports a public claim of independently evaluable comparative testing.

## Reproducibility Gate

A record may be promoted to `REPRODUCIBLE_COMPARATIVE_TEST` only when it exposes:

```text
shared input or test vector
framework identity and pinned version
runtime and policy configuration
expected result declared before execution
machine-readable actual output
scoring or classification method
failure, error, and abstention behavior
reproduction commands
raw evidence and immutable hashes
operator identity and timestamp
independent rerun result
```

A simple comment, screenshot, summary, or compatibility label cannot satisfy this gate.

## Current Registry

| Framework | Existing record | Current evidence state | Independently reproducible comparison | Execution authority claim | Report |
|---|---|---|---|---|---|
| [GLM](./glm.md) | Compatibility mapping | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/glm.compatibility.json) |
| [EVIDE](./evide.md) | Compatibility mapping | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/evide.compatibility.json) |
| [DecisionAssure](./decisionassure.md) | Supplied trace/commentary intake | `ARTIFACT_REVIEWED` when linked artifacts are present; otherwise `AUTHOR_COMMENTARY` | `NO` | `False` | [report](./reports/decisionassure.compatibility.json) |
| [MindForge](./mindforge.md) | Review-evidence intake | `AUTHOR_COMMENTARY` or `ARTIFACT_REVIEWED`, depending on attached evidence | `NO` | `False` | [report](./reports/mindforge.compatibility.json) |
| [Morrison Runtime](./morrison-runtime.md) | Parameterized boundary observation with incomplete public raw evidence | `PARAMETERIZED_OBSERVATION` | `NO` | `False` | [report](./reports/morrison-runtime.compatibility.json) |
| [CARE Runtime](./care-runtime.md) | Source-blocked intake | `MENTION_ONLY` | `NO` | `False` | [report](./reports/care-runtime.compatibility.json) |
| [AAR](./aar.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/aar.compatibility.json) |
| [ASRO](./asro.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/asro.compatibility.json) |
| [MITRE ATLAS](./mitre-atlas.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/mitre-atlas.compatibility.json) |
| [OWASP Top 10 for LLM Applications](./owasp-top-10-llm.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/owasp-top-10-llm.compatibility.json) |
| [Agent Governance Playbook](./agent-governance-playbook.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/agent-governance-playbook.compatibility.json) |
| [Emergency Stop Convention](./killswitch-md.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/emergency-stop-convention.compatibility.json) |
| [NIST AI RMF](./nist-ai-rmf.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/nist-ai-rmf.compatibility.json) |
| [ISO/IEC 42001](./iso-iec-42001.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/iso-iec-42001.compatibility.json) |
| [EU AI Act](./eu-ai-act.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/eu-ai-act.compatibility.json) |
| [Policy Cards](./policy-cards.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/policy-cards.compatibility.json) |
| [Runtime Governance for AI Agents](./runtime-governance-policies-on-paths.md) | Source crosswalk | `SOURCE_REVIEWED` | `NO` | `False` | [report](./reports/runtime-governance-for-ai-agents.compatibility.json) |
| [Admissible Existence Seed Cycle](./admissible-existence-seed-cycle.md) | Internal ecosystem compatibility record | `ARTIFACT_REVIEWED` | `NO` | `False` | [report](./reports/admissible-existence-seed-cycle.compatibility.json) |
| [Decision Authority Compatibility](./decision-authority.md) | Vocabulary compatibility record | `ARTIFACT_REVIEWED` | `NO` | `False` | [report](./reports/decision-authority.compatibility.json) |

## Dimension-Level Comparison Requirement

Future comparative results must report dimensions separately rather than collapsing them into one compatibility label:

```text
vocabulary compatibility
declaration or manifest compatibility
authority reconstruction
transition admissibility
replayability
reconstructability
cryptographic verifiability
runtime enforcement
fail-closed behavior
custody and persistence
execution authority
```

A framework may be strong in one dimension and outside scope in another. `NOT_APPLICABLE`, `NOT_TESTED`, `INSUFFICIENT_EVIDENCE`, `PASS`, `PARTIAL`, `FAIL`, and `ERROR` must remain distinguishable.

## Posting Rule

Generated reports may populate this page, but generation alone does not increase evidence strength. The public evidence state must be derived from inspectable fields and must fail closed when required artifacts are absent.

A listed result is not certification, endorsement, formalism adoption, admissibility proof, execution authority, or a ranking of framework value.