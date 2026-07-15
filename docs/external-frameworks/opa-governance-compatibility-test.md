---
title: OPA Governance Compatibility Test
---

# OPA Governance Compatibility Test

## Status

```text
framework: Open Policy Agent v1.0.0
native execution: observed
same-environment replay: observed
fresh-runner replay: observed
governance compatibility contract: authored
governance compatibility execution: pending canonical workflow observation
independent implementation reproduction: false
general compatibility claim allowed: false
execution authority claim allowed: false
```

## Question under test

Can an OPA policy decision be translated into StegVerse as bounded policy evidence while StegVerse independently evaluates identity, delegation, policy currency, evidence freshness, scope, recoverability, and execution context at commit time?

The test does **not** ask whether OPA itself implements the complete StegVerse governance model.

## Compatibility boundary

```text
OPA input + pinned Rego policy
        -> OPA policy decision
        -> policy-evidence translation
        -> StegVerse commit-time fields
        -> ALLOW / DENY / ESCALATE / FAIL_CLOSED
```

An OPA `allow: true` result is not translated directly into StegVerse `ALLOW`.

## Test artifacts

```text
standard:
  static/external-frameworks/compatibility-testing-standard.v1.json

fixture:
  tests/fixtures/external-frameworks/opa-governance-compatibility-cases.v1.json

native capture:
  scripts/run_pinned_opa_ci_capture.py

fresh-runner replay:
  scripts/run_independent_opa_ci_replay.py

compatibility evaluator:
  scripts/run_opa_governance_compatibility.py

expected result receipt:
  reports/external-frameworks/opa-independent/opa-stegverse-governance-compatibility-receipt.json
```

## Case set

| Case | Native OPA evidence | Independent StegVerse condition | Expected result |
|---|---|---|---|
| Positive alignment | `allow: true` | All commit-time conditions current | `ALLOW` |
| Native policy denial | `allow: false` | Other conditions current | `DENY / POLICY_DENIAL` |
| Revoked delegation | `allow: true` | Delegation no longer current | `DENY / AUTHORITY_DRIFT` |
| Stale evidence | `allow: true` | Required evidence stale | `FAIL_CLOSED / STALE_EVIDENCE` |
| Runtime or undefined error | No usable decision | Other conditions do not override missing decision | `FAIL_CLOSED / FRAMEWORK_RUNTIME_ERROR` |
| Semantic divergence guard | `allow: true` | Target outside current scope | `DENY / SCOPE_DIVERGENCE` |

## Translation mapping

| OPA artifact | StegVerse use | Explicit non-equivalence |
|---|---|---|
| Input | Policy-evaluation facts | Input facts are not independently verified evidence. |
| Rego policy | Referenced policy artifact | A policy file is not proof that it is the current governing policy. |
| Decision output | Policy-decision evidence | OPA allow/deny is not StegVerse ALLOW/DENY. |
| Bundle/version/hash | Reconstructability and replay evidence | Artifact identity is not authority or standing. |

## Execution procedure

The canonical sequence is:

```text
python scripts/run_pinned_opa_ci_capture.py
python scripts/run_independent_opa_ci_replay.py
python scripts/run_opa_governance_compatibility.py
```

The compatibility evaluator must reject execution when either the same-environment replay or fresh-runner replay is not confirmed.

For every test case it records:

```text
native OPA decision
translation mapping
StegVerse transition fields
expected StegVerse result
observed StegVerse result
expected failure class
observed failure class
case match
artifact hashes
runtime and workflow identity
limitations
```

## Completion gate

A bounded result may be described as `GOVERNANCE_COMPATIBILITY_OBSERVED` only when:

1. the pinned OPA capture succeeds;
2. same-environment replay matches;
3. fresh-runner replay matches;
4. all six cases execute;
5. all expected and observed StegVerse results match;
6. the machine-readable receipt is uploaded;
7. the authority and general-compatibility non-claims remain present.

This still does not qualify as independent-implementation reproduction because the fresh runner uses the same OPA implementation, repository, workflow provider, and StegVerse compatibility evaluator.

## Current result

```text
CONTRACT_AUTHORED
```

No compatibility result is claimed until the canonical workflow runs the evaluator and produces the receipt.

## Non-claims

This procedure does not certify OPA, declare OPA equivalent to StegVerse, establish production integration, grant standing, or grant execution authority. It tests only the declared translation and commit-time behavior for pinned artifacts and cases.

External-framework compatibility is bounded evidence-governance work. Publication does not create compatibility, standing, or authority.
