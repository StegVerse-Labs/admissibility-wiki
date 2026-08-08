---
title: OPA Governance Compatibility Test
---

# OPA Governance Compatibility Test

## Status

```text
framework: Open Policy Agent v1.0.0
second_page_state: EVIDENCE_BACKED_BOUNDED_RESULT
native execution: observed
same-environment replay: observed
fresh-runner replay: observed
StegVerse governance compatibility execution: observed
matching compatibility cases: 6/6
independent implementation reproduction: false
independent provider reproduction: false
general compatibility claim allowed: false
execution authority claim allowed: false
```

## What StegVerse tested

The test asks whether an OPA policy decision can enter StegVerse as bounded policy evidence while StegVerse independently evaluates identity, delegation, policy currency, evidence freshness, scope, recoverability, and execution context at commit time. It does **not** test or claim that OPA itself implements the complete StegVerse governance model.

```text
OPA input + pinned Rego policy
        -> OPA policy decision
        -> policy-evidence translation
        -> StegVerse commit-time fields
        -> ALLOW / DENY / ESCALATE / FAIL_CLOSED
```

An OPA `allow: true` result is never translated directly into StegVerse `ALLOW`.

## Observed canonical execution

Canonical workflow evidence:

```text
workflow: Validate chain continuation
run_id: 29455057960
commit: 618a57fb618cd29c90264eb1cab5f4d6814a55f6
run conclusion: FAILURE (Pages build failed later; OPA jobs succeeded independently)
validate-chain-continuation job: SUCCESS
capture-opa-evidence job: SUCCESS
replay-opa-fresh-runner job: SUCCESS
StegVerse compatibility evaluator: OBSERVED
compatibility cases: 6
matching cases: 6
bounded state: GOVERNANCE_COMPATIBILITY_OBSERVED
```

The fresh-runner job log directly records:

```text
OPA GOVERNANCE COMPATIBILITY: OBSERVED -> reports/external-frameworks/opa-independent/opa-stegverse-governance-compatibility-receipt.json
OPA INDEPENDENT REPLAY: CONFIRMED_FRESH_RUNNER -> reports/external-frameworks/opa-independent/opa-independent-replay-receipt.json
```

The overall workflow failure does not invalidate the successful OPA evidence jobs; the failure occurred in `build-pages` after the compatibility work completed.

## Preserved artifacts

```text
upstream pinned capture/replay artifact:
  artifact_id: 8359055203
  digest: sha256:552b50531de1877abc6c5b1546feaa1e45d9aea5800f530da3039b4bb32a580a

fresh-runner replay artifact:
  artifact_id: 8359059090
  digest: sha256:f1d7aaf4a8a1719aba498826cf7b9df4a8f913feb6a6418c8ae23840e268f8ff
```

The fresh-runner artifact contains five generated evidence files, including the StegVerse compatibility receipt and fresh-runner replay receipt.

## Test artifacts

```text
standard: static/external-frameworks/compatibility-testing-standard.v1.json
fixture: tests/fixtures/external-frameworks/opa-governance-compatibility-cases.v1.json
native capture: scripts/run_pinned_opa_ci_capture.py
fresh-runner replay: scripts/run_independent_opa_ci_replay.py
compatibility evaluator: scripts/run_opa_governance_compatibility.py
receipt: reports/external-frameworks/opa-independent/opa-stegverse-governance-compatibility-receipt.json
machine status: static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Expected and observed case families

| Case family | Native OPA evidence | Independent StegVerse condition | Expected StegVerse result | Observed |
|---|---|---|---|---|
| Positive alignment | `allow: true` | All commit-time conditions current | `ALLOW` | Match |
| Native policy denial | `allow: false` | Other conditions current | `DENY / POLICY_DENIAL` | Match |
| Revoked delegation | `allow: true` | Delegation no longer current | `DENY / AUTHORITY_DRIFT` | Match |
| Stale evidence | `allow: true` | Required evidence stale | `FAIL_CLOSED / STALE_EVIDENCE` | Match |
| Runtime or undefined error | No usable decision | Missing decision cannot be overridden | `FAIL_CLOSED / FRAMEWORK_RUNTIME_ERROR` | Match |
| Semantic divergence guard | `allow: true` | Target outside current scope | `DENY / SCOPE_DIVERGENCE` | Match |

All six expected and observed results matched in the canonical evidence run.

## Governance-chain placement

```text
OPA policy/input/data
    -> OPA policy decision
    -> non-authorizing policy evidence
    -> StegVerse evidence/state construction
    -> current identity + delegation + policy + evidence + scope checks
    -> commit-time admissibility
    -> separate commitment/execution authority boundary
```

OPA occupies the **policy-evaluation evidence layer**. It can determine what its configured policy says about supplied input. It does not independently establish actor identity, current delegation, current standing, evidence freshness, recoverability, consequence authority, or permission for a transition to bind reality.

## Translation mapping

| OPA artifact | StegVerse use | Explicit non-equivalence |
|---|---|---|
| Input | Policy-evaluation facts | Input facts are not independently verified evidence. |
| Rego policy | Referenced policy artifact | A policy file is not proof that it is the current governing policy. |
| Decision output | Policy-decision evidence | OPA allow/deny is not StegVerse ALLOW/DENY. |
| Bundle/version/hash | Reconstructability and replay evidence | Artifact identity is not authority or standing. |

## Replay path

```text
python scripts/run_pinned_opa_ci_capture.py
python scripts/run_independent_opa_ci_replay.py
python scripts/run_opa_governance_compatibility.py
```

The compatibility evaluator fails closed when the same-environment replay or fresh-runner replay is unavailable or does not confirm the pinned decision behavior.

## Evidence standing

```text
native OPA execution: OBSERVED
same-environment replay: OBSERVED
fresh-runner same-provider replay: OBSERVED
StegVerse bounded governance compatibility: OBSERVED
independent organization reproduction: NOT OBSERVED
independent provider reproduction: NOT OBSERVED
independent OPA implementation reproduction: NOT OBSERVED
production StegVerse integration: NOT ESTABLISHED
certification / endorsement: NOT ESTABLISHED
execution authority: NOT GRANTED
```

This is therefore an evidence-backed bounded comparative result, not a general compatibility certification.

## Remaining gates

The local second-page evidence gap is closed for the canonical bounded test. Stronger evidence classes still require an independently controlled implementation/provider reproduction and, separately, any production integration evidence. Those stronger gates are not prerequisites to report the bounded observed result accurately.

## Non-claims

This test does not certify OPA, declare OPA equivalent to StegVerse, establish production integration, grant standing, or grant execution authority. The fresh runner used the same GitHub Actions provider, the same OPA implementation, and the same StegVerse compatibility evaluator, so it is not independent-implementation reproduction.

External-framework compatibility is bounded evidence-governance work. Publication does not create compatibility, standing, or authority.
