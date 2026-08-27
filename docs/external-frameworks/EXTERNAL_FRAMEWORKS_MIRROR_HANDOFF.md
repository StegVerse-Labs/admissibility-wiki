# External Frameworks Mirror Handoff

## Source of truth

This file is the continuation source of truth for the External Frameworks section of `StegVerse-Labs/admissibility-wiki`. Repository-wide authority remains governed by `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`; worker ownership and collision control remain governed by `docs/external-frameworks/worker-task-registry.json` and coordinator issue #66.

## Current goal

```text
goal_id: EXT-FRAMEWORK-SECOND-PAGE-36
goal: make every actual external-framework record function as a first-class, evidence-bounded Wiki surface with public navigation, machine-readable companions, deterministic source validation, built-route proof, deployment evidence, content-aware public-route verification, and framework-specific evaluation completion
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
scripts/check_external_framework_publication_proof_contract.py
scripts/check_goal5_external_frameworks_all.py
.github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
scripts/check_ios_workflow_mirror_status.py
static/status/ios-workflow-mirror-status.json
static/status/ios-workflow-mirror-sync-next.json
workflow_manifest.json
scripts/check_workflow_manifest.py
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
canonical/iOS workflow mirror equality: REQUIRED
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

## Three-stage route proof

`scripts/check_external_framework_public_routes.py` enforces three distinct route transitions rather than collapsing source, build, and deployment into one claim.

### Stage 1 — pre-build source-route contract

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
performs no build or network request
```

The canonical `build-pages` job runs this gate before Node dependency installation and before Docusaurus build. The report is uploaded as `external-framework-source-route-contract`.

### Stage 2 — generated Docusaurus route proof

`python scripts/check_external_framework_public_routes.py --built-site --build-dir build` runs only after the Docusaurus build result has been enforced as successful and before the Pages artifact is uploaded.

For every one of the 36 external frameworks it:

```text
repeats the source-route contract
maps the declared sidebar route to build/external-frameworks/<route>/index.html
requires the generated route file to exist
rejects obvious generated 404 content
requires the source title/H1 in the generated HTML
writes reports/external-frameworks/built-route-verification.json
fails build-pages before Pages artifact upload on any missing or mismatched route
```

The report is uploaded as `external-framework-built-route-verification`.

Installed commits:

```text
6de40057249adf47fcee7922b9442b7677580689  add deterministic source-only route-contract mode
d0a16ee850eb62064acb668261f0eb736db01099  bind source-route contract into canonical build-pages job
a3608961a1f3f16aa8b48b2deef92b218ec04dc5  add generated Docusaurus route-file verification mode
b8961bc6c52c0781c602c51eee73e773fa6bed7b  gate Pages artifact upload on 36/36 built-route verification
```

### Stage 3 — post-deployment public-route proof

The same script without `--source-only` or `--built-site` remains the post-deployment verifier. It:

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
successful Docusaurus build != 36/36 generated route files
36/36 generated route files != Pages artifact preservation
Pages artifact preservation != deployment
deployment != route reachability
route reachability != content fidelity
content fidelity != framework compatibility
```

## Publication proof contract regression guard

The three-stage chain is itself now validated as a Goal-5 contract rather than relying on documentation alone.

`scripts/check_external_framework_publication_proof_contract.py` requires:

```text
36 framework associations
all three route-validator modes and report schemas
source-route validation before Node/build
source-route artifact binding
Docusaurus build before built-route validation
built-route validation before Pages artifact upload
built-route artifact binding
deployment after Pages artifact production
post-deployment public-route verification
public-route artifact binding
canonical/iOS-safe workflow byte equality
iOS workflow mirror status = synchronized
handoff preservation of non-authority and stage-separation markers
```

`check_goal5_external_frameworks_all.py` executes this validator. Therefore removal, reordering, silent weakening, or iOS-mirror loss of the source -> build -> generated-route -> Pages artifact -> deployment -> public-route proof chain is a Goal-5 failure rather than an unobserved documentation regression.

Installed commits:

```text
4906baa3ee8bc3a24d29e8479ce40723ca1bd965  add publication proof contract validator
2503fd6482332636ed211095e76774b0d425b814  bind publication proof contract into Goal-5 aggregate validation
464e33cf79469bd54c738685e552798f66a79410  require synchronized iOS mirror in publication proof contract
```

## iOS-safe workflow mirror synchronization

The iOS-safe workflow mirror was materially stale and did not contain the current External Frameworks source-route or generated-route gates. The repository already contained `static/status/ios-workflow-mirror-sync-next.json`, whose required next state was exact synchronization. That transition is now executed.

Installed synchronization chain:

```text
c9d6beb641a3e86f642cdf989e9953d7db4552bf  replace iOS-safe workflow mirror with the canonical workflow
25b01f1462f8416e8db216e2bbccaf9c9e0f3168  make mirror guard state-aware for synchronized vs controlled-delta states
d99e0bdb4b6f50d8f091df5619e79f837296984a  promote iOS workflow mirror status to synchronized
3a72cace1b2c4193b9f32c099cded7c348b7e2f7  close the previously queued synchronization transition
486c4c120a8a1bce19558f3663d71648cb9f1690  reconcile workflow manifest to synchronized mirror state
b1bf42c9c65e9d0552aeffa9becc34a83fc6f16c  require byte-identical synchronized mirror in workflow-manifest validation
a6bacbf82d1c9d2e7382eb21222d321dc76dc9df  reconcile activation checklist from patched delta to synchronized
20f1402def9695e3eda3855007eb2c161532ed80  retire the stale active patch description into a historical/future-drift record
```

The mirror remains a usability surface, not a second workflow authority. Future canonical workflow drift must either update the mirror byte-identically in the same transition or explicitly demote the mirror state to `patched_delta_recorded` with a complete controlled delta record. Silent drift is fail-closed.

```text
iOS mirror synchronized != canonical workflow executed
mirror equality != deployment
mirror equality != activation evidence
mirror equality != release authority
```

Current hosted result must remain UNOBSERVED until the workflow result for the exact resulting commit is directly inspected. Moving-main substitution is prohibited for evidence claims.

## Worker ownership and framework-specific evaluation

Do not use this cross-cutting navigation/build repair to overwrite worker-owned framework analysis. The current worker registry and issue #66 partition all 36 framework evaluation workloads among issues #62, #63, #64, #65, and #50.

The 36-page navigation denominator and the 36-framework evaluation denominator are separate:

```text
public Wiki source wiring: 36/36
terminal framework-specific evaluation: determined only by issue #66 direct evidence
```

A framework page being visible, authored, manifest-bound, report-bound, built, deployed, route-verified, or portable through the synchronized iOS mirror does not by itself answer the stronger second-page evaluation completion criteria.

Latest direct coordinator evidence still records 7/36 terminally reconciled and 29/36 incomplete. No newer issue-#66 evidence was observed during this transition, so the denominator is not promoted.

## Exact hosted publication proof — run 33011831798

Exact commit `74bf7edffc0b975c70a15b649653c32b26bb1ca1` produced direct hosted evidence for the publication side of this goal:

```text
canonical pre-scan: 11/11 PASS
36/36 source wiring: PASS
source-route contract: 36/36 PASS
Docusaurus build: PASS
36/36 generated-route verification: PASS
Pages artifact upload: PASS
deploy-pages: PASS
36/36 public route/content verification: PASS
framework-specific evidence completion: SEPARATE / NOT PROMOTED
repository-wide canonical validation: 47/56 PASS, 9 FAIL, 0 SKIPPED
repository release authority: NONE
```

Retained route-proof artifacts:

```text
external-framework-source-route-contract: artifact 9622942474; sha256:558d1c4a758210c275f0d3049cc5cf30c9b1336893a3389ef138338c125be7c5
external-framework-built-route-verification: artifact 9622986502; sha256:dca3725bdb1f4700227e7f3aff834aa0eb902df88e9f457771b6f7e49d04c3a7
external-framework-public-route-verification: artifact 9623014776; sha256:720c1bd70b4ae2bd62dac3e52807ba88a643322b67b4ee0592411916cbbb75df
```

Observed-evidence continuation is governed by `observed-evidence-capture-protocol.md` and `observed-evidence-capture-queue.v0.1.json`.

This closes the previously unobserved three-stage route-proof requirement for that exact commit only. It does not establish repository-wide canonical PASS, framework-specific terminal evaluation, certification, release, or activation.

## Required next transitions

1. Observe an exact-head canonical validation/build run containing the current three-stage route-proof chain, Goal-5 regression validator, and synchronized iOS mirror contract.
2. Require the Goal-5 publication-proof-contract check to PASS at that exact head, including canonical/iOS mirror equality.
3. Require `external-framework-source-route-contract` to report 36/36 source-contract-verified routes.
4. Require Docusaurus build success for that same exact head.
5. Require `external-framework-built-route-verification` to report 36/36 generated route files with content fidelity.
6. Require Pages artifact upload and `deploy-pages` success for that same source set.
7. Consume `external-framework-public-route-verification` and require 36/36 reachable and content-verified.
8. Repair any failure at the exact failing transition; do not substitute a moving `main` result.
9. Continue the framework-specific worker program until every one of the 36 framework records reaches its strongest legitimate terminal or explicit evidence-blocked state under issue #66.
10. Obtain repository-wide canonical PASS before any repository release/activation claim.
11. At release readiness only, inspect current destination handoffs before propagation-status verification for `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, and `StegVerse-002/stegguardian-wiki`.

## Remaining modules and destinations

### `StegVerse-Labs/admissibility-wiki`

- exact-head canonical validation evidence;
- Goal-5 publication-proof-contract PASS;
- canonical/iOS workflow mirror equality validation;
- 36/36 source-route contract artifact;
- exact-head Docusaurus build evidence;
- 36/36 generated built-route verification artifact;
- exact-head Pages artifact and deployment evidence;
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
source-route contract PASS != build success
build success != generated-route verification
generated-route verification != deployment
publication-proof-contract PASS != deployment
iOS mirror equality != workflow execution
workflow pass != runtime authority
route verification != release
public rendering != endorsement
ALLOW != execution
```

## Archive posture

```text
archive_state: NOT_READY
source_navigation_goal: 36_OF_36_INSTALLED_WITH_SOURCE_BUILD_POSTDEPLOY_AND_IOS_MIRROR_GATES_PENDING_HOSTED_PROOF
framework_evaluation_goal: NONTERMINAL_UNTIL_ISSUE_66_DIRECT_EVIDENCE_CLOSES_36_OF_36
repository_release: NOT_AUTHORIZED
repository_activation: NOT_COMPLETE
```

Keep this workstream open until exact-head validation, publication-proof-contract validation, synchronized mirror validation, source-route proof, build, generated-route proof, Pages artifact/deployment, all-route runtime proof, framework-specific evaluation completion, repository-wide PASS, and any required release/propagation/activation evidence are directly established.


## 2026-08-26 archive-continuity reconciliation

Latest directly observed publication/runtime proof is run `33033268340`: source-route 36/36 PASS, generated built-route/content 36/36 PASS, Pages build/deploy PASS, and deployed public-route/content 36/36 PASS. These publication proofs do not promote framework-specific evaluation.

Framework-specific terminal evaluation remains `7_OF_36` last directly observed; `29` remain incomplete. Worker/collision ownership remains authoritative in `EXTERNAL_FRAMEWORK_EVALUATION_WORKERS_MIRROR_HANDOFF.md`, `worker-task-registry.json`, issues #62-#65, and issue #50. Do not absorb worker-owned framework pages without explicit ownership transition.

Release remains prohibited until framework evaluations are terminal or legitimately evidence-blocked, repository-wide canonical validation passes for the exact candidate, and release/propagation/activation evidence exists. Session dependency for continuation is false once this handoff and the global Projects coordination documents are updated.


## 2026-08-27 exact repository-wide canonical PASS — run 33118691192

Exact `main` head `925b4f7a1346ce3f9516224daabe9d2467be2c6d` produced the first directly observed repository-wide canonical PASS after the TA-14 path repairs and Generated StegPay merge reconciliation.

```text
run: 33118691192
head: 925b4f7a1346ce3f9516224daabe9d2467be2c6d
canonical pre-scan: 11/11 PASS
full canonical validation: 56/56 PASS
failed: 0
skipped: 0
Goal 5 aggregate: PASS
publication-proof contract: PASS
framework associations: 36/36
source-route contract: PASS
Docusaurus build: PASS
built-route verification: PASS
Pages artifact: PASS
deploy-pages: PASS
public-route/content verification: PASS
Discovery Governance activation closure: PASS
Discovery Governance activation evidence: ACTIVATION_EVIDENCE_COMPLETE
```

Artifacts include:
- full validation report `9665746417`, digest `sha256:ec266fce6e7e19b4e662179d8bba63fbaf27e0cbd439ad648db233373e4515df`;
- source-route contract `9665757372`, digest `sha256:d96143aa6de56d0375bc5380aaa4826cf0be49e97c589e19f0385e5f20c2936a`;
- built-route verification `9665806310`, digest `sha256:d024e7ffbfc795a8f5a4f3b249eaf5c08589b8d2fa7f75fa601bf91fa959d19e`;
- public-route verification `9665839609`, digest `sha256:3de0ea31ad15898311c3c97531c7574d3b2b02d49b302ae6909cdaf532c6e268`;
- public activation receipt `9665838987`, digest `sha256:e06ecb95a9f08b001b7625d0897385ef4260465be4244a87cc3c340b066c6a51`.

This closes the External Framework publication/exact-canonical-proof gate for that exact head. It does **not** promote framework-specific terminal evaluation: issue #66 remains the denominator authority, with the last directly observed state still `7/36` terminal and `29` incomplete. Release remains unauthorized until all framework evaluations are terminal or legitimately evidence-blocked and the exact release candidate satisfies the separate release/propagation contract.

No worker-owned framework evaluation file is absorbed by this transition.
