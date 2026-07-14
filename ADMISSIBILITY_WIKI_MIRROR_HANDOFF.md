# Admissibility Wiki Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `StegVerse-Labs/admissibility-wiki` until superseded.

## Active goal

Complete governed public documentation activation through the single canonical validation workflow while preserving proof, execution, deployment, custody, and cross-repository authority boundaries.

## Current repository state

```text
Canonical workflow: .github/workflows/validate-chain-continuation.yml
Public site: https://stegverse-labs.github.io/admissibility-wiki/
Local documentation surfaces: installed
Canonical workflow verification: pending successor evidence
Docusaurus build verification: pending successor evidence
Public route verification: pending successor evidence
Cross-repository mutation authority: not granted
Release/tag authority: not granted by this handoff
```

## Installed governed return-path and runtime-governance surfaces

```text
docs/governance/portable-governed-return-path.md
static/governance/portable-governed-return-path.v0.1.json

docs/external-frameworks/morrison-runtime.md
docs/external-frameworks/reports/morrison-runtime.compatibility.json

docs/formalisms/denial-reachability-at-commit.md
static/formalisms/denial-reachability-at-commit.v0.1.json
scripts/check_denial_reachability_at_commit.py

docs/governance/admissible-automated-transitions.md
static/governance/admissible-automated-transitions.v0.1.json
receipts/admissible-automated-transitions-observatory-receipt.json
```

## Optimization target binding at commit

Installed and validation-bound:

```text
docs/formalisms/optimization-target-binding-at-commit.md
static/formalisms/optimization-target-binding-at-commit.v0.1.json
scripts/check_optimization_target_binding_at_commit.py
static/status/optimization-target-binding-at-commit-status.json
static/status/optimization-target-binding-publication-verification.json
scripts/check_optimization_target_binding_publication.py
sidebars.js
scripts/check_admissibility_automation_handoff.py
```

Durable rule:

```text
A consequence-binding transition MUST NOT be authorized unless its optimization target is explicit before execution, bound to the current transition and current state, derived from current policy and delegation, protected by valid mutation provenance, evaluated with current evidence and authority, and still subject to an enforceable DENY or FAIL_CLOSED result before the actuator boundary.
```

Current publication state:

```text
IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_AND_PUBLIC_ROUTE_VERIFICATION
```

The publication-status artifact intentionally records workflow, build, public-route, and proof-receipt evidence as false until observed. Local installation must not be represented as deployment, public verification, or executable proof.

## Authority boundaries

```text
admissibility-wiki owns public vocabulary, governance explanation, status, and proof-path documentation
Data-Continuation/formalism-tests owns executable fixtures, expected outcomes, and proof receipts
Site is a downstream mirror/display surface only
Publisher is a downstream publication/indexing surface only
StegGuardian interpretation is deferred until proof fixtures exist
StegGuardian implementation mutation is not authorized
Morrison ALLOW is not StegVerse execution authority
Morrison BLOCK is evidence, not final StegVerse standing
Public visibility is not admissibility
Validation success is not deployment, release, custody, or cross-repository authority
```

## Verification target

```text
1. Run python scripts/check_full_validation_chain.py.
2. Confirm scripts/check_optimization_target_binding_at_commit.py passes.
3. Confirm scripts/check_optimization_target_binding_publication.py passes.
4. Confirm scripts/check_admissibility_automation_handoff.py passes with both checks.
5. Repair only exact deterministic failures without removing checks.
6. Run npm validation and Docusaurus build after the Python scan is green.
7. Verify public routes for the doctrine, formalism JSON, and publication-status artifact.
8. Update evidence booleans only from observed records.
```

Expected public routes:

```text
https://stegverse-labs.github.io/admissibility-wiki/docs/formalisms/optimization-target-binding-at-commit
https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json
https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json
```

## Remaining files or modules and destinations

### `Data-Continuation/formalism-tests`

```text
Add explicit-target, stale-binding, unauthorized-mutation, objective-policy-divergence, and denial-unreachable fixtures.
Add expected outcomes proving FAIL_CLOSED for any false or unreconstructable required predicate.
Emit proof receipts consumable by admissibility-wiki without transferring proof authority.
```

### `StegVerse-Labs/admissibility-wiki`

```text
Run the complete validation scan.
Capture canonical workflow and build evidence.
Verify public routes.
Converge the formalism index and formalism registry if canonical validators require registration.
Attach prompt-by-prompt Morrison artifacts when source evidence becomes available.
```

### `StegVerse-Labs/Site`

```text
Do not mirror or index until wiki validation and public routes are verified.
Check docs/SITE_MIRROR_HANDOFF.md immediately before any mutation.
```

### `GCAT-BCAT-Engine/Publisher`

```text
Do not publish or index until wiki evidence and proof receipts are verified.
Check PUBLISHER_MIRROR_HANDOFF.md immediately before any mutation.
```

### `StegVerse-002/stegguardian-wiki`

```text
Evaluate refusal-capability, target-mutation, and recoverability representation only after executable proof fixtures exist and destination handoff review authorizes work.
```

### `StegVerse-002/StegGuardian`

```text
No implementation mutation is authorized by this handoff.
```

## Release posture

No tag or release is authorized until the canonical workflow, build, and public verification gates pass and repository release criteria are separately confirmed. Any later release must trigger review of `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki` propagation status.

## Next task

```text
Run or observe the successor canonical validation chain.
Repair the next exact deterministic failure without weakening checks.
Verify publication routes after deployment.
Then install executable optimization-target fixtures in Data-Continuation/formalism-tests if that repository is accessible and its current *_MIRROR_HANDOFF.md authorizes the task.
```

## Archive posture

This handoff preserves the active goal, installed surfaces, decisions, blockers, ownership boundaries, remaining work, validation requirements, permitted continuation scope, and downstream restrictions. The complete thread is ready for archiving without needing additional conversation context.
