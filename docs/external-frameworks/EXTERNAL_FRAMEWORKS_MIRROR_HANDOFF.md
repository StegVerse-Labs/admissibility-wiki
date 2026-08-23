# External Frameworks Mirror Handoff

## Source of truth

This file is the continuation source of truth for the External Frameworks section of `StegVerse-Labs/admissibility-wiki`. Repository-wide authority remains governed by `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`; worker ownership and collision control remain governed by `docs/external-frameworks/worker-task-registry.json` and coordinator issue #66.

## Current goal

```text
goal_id: EXT-FRAMEWORK-SECOND-PAGE-36
goal: make every actual external-framework record function as a first-class, evidence-bounded Wiki surface with public navigation, machine-readable companions, deterministic source validation, canonical build/deploy evidence, content-aware public-route verification, and framework-specific evaluation completion
actual external-framework denominator: 36
internal ecosystem records in the same canonical registry: 2
public sidebar source wiring: 36/36
internal records intentionally excluded from external-framework sidebar: 2/2
framework-evaluation terminal denominator: preserve coordinator issue #66 until newer direct evidence changes it
release authority: none
execution authority: none
cross-repository mutation authority: none
```

## Public Wiki navigation repair

The prior registry state contained 36 actual external frameworks but only 26 public-sidebar framework pages. Ten real framework pages were direct-path-only. That split is removed.

The ten newly public-sidebar-bound framework records are:

```text
aar
mitre-atlas
owasp-top-10-llm
agent-governance-playbook
emergency-stop-convention -> page slug killswitch-md
nist-ai-rmf
iso-iec-42001
eu-ai-act
policy-cards
runtime-governance-for-ai-agents -> page slug runtime-governance-policies-on-paths
```

The following internal ecosystem records remain outside the external-framework sidebar by design:

```text
admissible-existence-seed-cycle
decision-authority
```

This is record-type separation, not concealment or evidence promotion.

## Installed cross-cutting surfaces

```text
sidebars.js
static/external-frameworks/sidebar-page-associations.v1.json
static/external-frameworks/sidebar-framework-artifact-bindings.v1.json
static/external-frameworks/registry-navigation-dispositions.v1.json
static/external-frameworks/canonical-union-inventory.v1.json
static/external-frameworks/all-navigated-framework-page-completeness.v1.json
static/external-frameworks/full-registry-public-navigation-remediation.v1.json
scripts/check-external-framework-registry.mjs
scripts/check_external_frameworks_index.py
scripts/check_all_navigated_external_framework_page_completeness.py
scripts/check_external_framework_public_routes.py
.github/workflows/validate-chain-continuation.yml
```

Current structural target:

```text
canonical registry records: 38
actual external frameworks: 36
internal records: 2
public-sidebar external frameworks: 36
non-public actual external frameworks: 0
sidebar support pages: 33
sidebar total entries: 69
framework manifest bindings: 36/36
framework compatibility-report bindings: 36/36
navigated authored-page completeness: 36/36 COMPLETE_WITH_EXTERNAL_GATES
```

All 36 sidebar framework records have an existing manifest and compatibility report bound through `sidebar-framework-artifact-bindings.v1.json`. The compatibility reports remain evidence artifacts; their existence is not certification or terminal framework evaluation.

## Fail-closed navigation invariants

`check-external-framework-registry.mjs` enforces exact sidebar/association ordering, page existence, registry-state declarations, manifest/report bindings, and the rule that a registry record is exactly one of sidebar-bound or explicitly dispositioned.

`check_external_frameworks_index.py` additionally requires:

```text
sidebar framework IDs == canonical-union actual external-framework IDs
canonical union public_sidebar IDs == all actual external-framework IDs
non-public actual external-framework IDs == empty set
public_sidebar count == external-framework count
non_public_explicit count == 0
internal records must not appear as framework sidebar items
every public framework association must be linked from the External Frameworks index
```

This prevents a future actual external framework from silently becoming direct-path-only while still appearing complete in the canonical registry.

## Authored-page completeness boundary

The four completeness cohorts cover all 36 actual external-framework pages:

```text
policy_identity_provenance_supply_chain: 13
priority_agent_protocol_guardrail: 5
legacy_priority_runtime_and_intake: 8
previously_direct_path_only_external_frameworks: 10
total: 36
```

`COMPLETE_WITH_EXTERNAL_GATES` means the Wiki page has the required authored semantic surface. It does not establish source sufficiency, observed runtime behavior, independent reproduction, compatibility, certification, standing, admissibility, release authority, or execution authority.

## Two-stage route proof

`scripts/check_external_framework_public_routes.py` now has two fail-closed modes.

### Pre-build source-route contract

`python scripts/check_external_framework_public_routes.py --source-only`:

```text
requires exactly 36 framework associations
requires unique framework_id values
requires unique sidebar routes
requires unique framework page paths
requires every page under docs/external-frameworks/
requires every source page to exist
requires an extractable frontmatter title or H1 for every page
writes reports/external-frameworks/source-route-contract.json
performs no network request
```

The canonical `build-pages` job runs this gate before Node dependency installation and before Docusaurus build. A source-wiring or content-marker defect therefore fails the Pages build lane before deployment. The report is uploaded as `external-framework-source-route-contract`.

Installed commits:

```text
6de40057249adf47fcee7922b9442b7677580689  add deterministic source-only route-contract mode
d0a16ee850eb62064acb668261f0eb736db01099  bind source-route contract into canonical build-pages job
```

### Post-deployment public-route proof

The same script without `--source-only` remains a post-deployment verifier. It:

```text
repeats the source-route contract
requests each deployed public route
requires HTTP 200
rejects obvious rendered 404 content
requires normalized source heading/title in rendered HTML
writes reports/external-frameworks/public-route-verification.json
fails if any framework route is missing or content-mismatched
```

The canonical Pages workflow runs this verifier only after successful deployment and uploads the resulting report as `external-framework-public-route-verification`.

```text
source wiring != source-route contract PASS
source-route contract PASS != successful Docusaurus build
successful build != deployment
deployment != route reachability
route reachability != content fidelity
content fidelity != framework compatibility
```

Current hosted result must remain UNOBSERVED until the workflow result for the exact resulting commit is directly inspected. The currently installed source/build transition ends at `d0a16ee850eb62064acb668261f0eb736db01099`, subject to later nonconflicting main commits; moving-main substitution is prohibited for evidence claims.

## Worker ownership and framework-specific evaluation

Do not use this cross-cutting navigation repair to overwrite worker-owned framework analysis. The current worker registry and issue #66 partition all 36 framework evaluation workloads among issues #62, #63, #64, #65, and #50.

The 36-page navigation denominator and the 36-framework evaluation denominator are separate:

```text
public Wiki source wiring: 36/36
terminal framework-specific evaluation: determined only by issue #66 direct evidence
```

A framework page being visible, authored, manifest-bound, report-bound, built, deployed, and route-verified does not by itself answer the stronger second-page evaluation completion criteria.

## Required next transitions

1. Observe an exact-head canonical validation/build run containing commits `6de4005...` and `d0a16ee...` plus any later nonconflicting main commits.
2. Require the `external-framework-source-route-contract` artifact to report 36/36 source-contract-verified routes.
3. Repair any structural or validation failures directly observed at that exact commit; do not substitute a moving `main`.
4. Require `build-pages` to succeed for the exact validated source set.
5. Require `deploy-pages` to succeed for that same source set.
6. Consume `external-framework-public-route-verification` and require 36/36 reachable and content-verified.
7. Continue the framework-specific worker program until every one of the 36 framework records reaches its strongest legitimate terminal or explicit evidence-blocked state under issue #66.
8. Obtain repository-wide canonical PASS before any repository release/activation claim.
9. At release readiness only, inspect current destination handoffs before propagation-status verification for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, and `StegVerse-002/stegguardian-wiki`.

## Remaining modules and destinations

### `StegVerse-Labs/admissibility-wiki`

- exact-head canonical validation evidence;
- 36/36 source-route contract artifact;
- exact-head Pages build and deploy evidence;
- 36/36 content-aware public-route verification artifact;
- completion or explicit evidence-blocked resolution for all 36 framework-specific worker evaluations;
- repository-wide canonical PASS;
- release/activation evidence only after the preceding gates.

### Downstream at release readiness only

- `StegVerse-Labs/Site`
- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-002/stegguardian-wiki`

No downstream mutation is authorized by this handoff.

## Authority boundary

```text
registry inclusion != certification
sidebar visibility != compatibility
manifest presence != source sufficiency
compatibility report presence != terminal evaluation
page completeness != independent reproduction
source-route contract PASS != deployment
workflow pass != runtime authority
build success != deployment
route verification != release
public rendering != endorsement
ALLOW != execution
```

## Archive posture

```text
archive_state: NOT_READY
source_navigation_goal: 36_OF_36_INSTALLED_WITH_PREBUILD_AND_POSTDEPLOY_GATES_PENDING_HOSTED_PROOF
framework_evaluation_goal: NONTERMINAL_UNTIL_ISSUE_66_DIRECT_EVIDENCE_CLOSES_36_OF_36
repository_release: NOT_AUTHORIZED
repository_activation: NOT_COMPLETE
```

Keep this workstream open until exact-head validation, source-route proof, build, deployment, all-route runtime proof, framework-specific evaluation completion, repository-wide PASS, and any required release/propagation/activation evidence are directly established.
