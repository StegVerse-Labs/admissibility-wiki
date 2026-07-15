# Cedar Policy — StegVerse Governance Compatibility Procedure

## Current state

```text
contract: authored
selected binary build: observed
selected binary execution: not observed
governance translation simulation: authored, not yet workflow-observed
fresh-runner replay: not observed
general compatibility claim: prohibited
```

## Purpose

This procedure tests where a Cedar authorization response can contribute to StegVerse governance and where Cedar and StegVerse intentionally remain separate.

Cedar answers whether a principal is permitted or forbidden to perform an action on a resource in context. StegVerse still determines whether the resulting transition may bind consequence now under current identity, delegation, policy, evidence, scope, recoverability, and execution context.

## Existing evidence

The repository has a pinned Cedar build pipeline for:

```text
repository: https://github.com/cedar-policy/cedar.git
version: 4.11.0
commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
build: cargo build --locked --release -p cedar-policy-cli
```

The build receipt records the resulting binary hash and explicitly states that the binary was not executed. Build provenance is not behavioral evidence or compatibility proof.

## Test contract

Fixture:

```text
tests/fixtures/external-frameworks/cedar-governance-compatibility-cases.v1.json
```

Evaluator:

```text
scripts/run_cedar_governance_compatibility.py
```

Expected receipt:

```text
reports/external-frameworks/cedar/cedar-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | Cedar input posture | Expected StegVerse boundary |
|---|---|---|
| Positive alignment | `permit`, current principal/delegation/policy/entities/evidence/scope/context | `ALLOW` |
| Native denial | `forbid` | `DENY` |
| Authority drift | `permit`, delegation revoked | `DENY` |
| Stale evidence | `permit`, stale entity store or evidence | `FAIL_CLOSED` |
| Framework error | evaluator error or unrecognized response | `FAIL_CLOSED` |
| Semantic divergence | `permit`, resource outside governed scope | `DENY` |

## Current simulation boundary

The authored evaluator currently consumes predeclared Cedar responses. It tests the translation and StegVerse decision contract only.

It does **not** establish:

```text
captured Cedar runtime output
live Cedar-to-StegVerse integration
fresh-runner Cedar replay
independent implementation reproduction
general compatibility
execution authority
```

## Required runtime completion

The contract may advance beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` only after the pinned binary is executed against retained:

```text
schema
policy set
entity store
request vectors
raw authorization responses and errors
runtime configuration
timestamps
binary and input hashes
replay commands
fresh-runner results
```

Captured Cedar outputs must then replace the fixture's predeclared responses before a bounded governance compatibility result can be claimed.

## Authority boundary

Cedar permit or forbid is authorization evidence. It is not StegVerse `ALLOW` or `DENY`, standing, certification, or execution authority. A passing translation simulation does not establish live integration or general compatibility.
