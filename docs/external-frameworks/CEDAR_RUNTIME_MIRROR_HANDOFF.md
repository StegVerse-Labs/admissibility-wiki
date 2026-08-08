# Cedar Runtime Mirror Handoff

## Canonical scope

This is the canonical continuation handoff for the Cedar Policy runtime-observation sub-claim inside the 36-framework evaluation program. It is subordinate to `docs/external-frameworks/EXTERNAL_FRAMEWORK_EVALUATION_WORKERS_MIRROR_HANDOFF.md`, `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`, issue #63, and the repository-wide canonical validation workflow. Where the older Cedar subsection of the worker handoff describes a pre-runtime or hash-only state, this file supersedes that Cedar-only state.

## Active goal and goal ID

```text
goal_id: EXT-FRAMEWORK-CEDAR-RUNTIME-001
originating_session_goal: replace scaffolding/procedure-only Cedar evidence with directly observed bounded native authorization evidence, then feed those observations into the existing StegVerse governance compatibility evaluator without inflating authority claims
repository: StegVerse-Labs/admissibility-wiki
branch: main
canonical_owner: Worker B / issue #63
session_role: transferred to repository-native Worker B continuation after installation of the entities repair and this handoff
```

## Authoritative files and surfaces

```text
docs/external-frameworks/capture/cedar/policy.cedar
docs/external-frameworks/capture/cedar/request-allow.json
docs/external-frameworks/capture/cedar/request-deny.json
docs/external-frameworks/capture/cedar/entities.json
scripts/build_selected_cedar_binary.py
scripts/run_pinned_cedar_ci_capture.py
scripts/capture_cedar_observation.py
scripts/validate_cedar_capture_artifacts.py
scripts/run_cedar_governance_compatibility.py
tests/fixtures/external-frameworks/cedar-governance-compatibility-cases.v1.json
docs/external-frameworks/cedar-governance-compatibility-procedure.md
docs/external-frameworks/cedar-policy.md
docs/external-frameworks/implementation-selection-gates.v0.1.json
reports/external-frameworks/cedar-build/cedar-binary-registry-promotion-receipt.applied-hash-only.json
issue #63
.github/workflows/validate-chain-continuation.yml
```

## Canonical task owner and claims

```text
task_id: EXT-FRAMEWORK-CEDAR-RUNTIME-001
originating_goal: 36 evidence-backed external-framework second-page evaluations
organization/repository: StegVerse-Labs/admissibility-wiki
implementation_claim: CLAIMED_FOR_IMPLEMENTATION by Worker B / issue #63
validation_claim: CLAIMED_FOR_VALIDATION by Worker B plus repository-native canonical workflow
claim_created_at: 2026-08-08T17:37:34Z
claim_release_condition: bounded native Cedar ALLOW/DENY captures are preserved and validated, observed outputs are consumed by the existing six-family StegVerse compatibility path, the Cedar second page reflects the resulting evidence class, and issue #63/handoff release the live implementation claim
collision_boundary: do not modify Worker A/C/D framework sets; do not take MindForge/Morrison/ASRO from issue #50; do not reinterpret Cedar authorization as StegVerse execution authority
next_task_after_release: continue Worker B's remaining agent-control frameworks under issue #63
```

## Completed work and evidence

### OPA predecessor

OPA is complete at bounded observed evidence under Worker B and is not part of this active Cedar claim.

### Cedar pinned implementation and hash-only provenance

```text
implementation: cedar-policy-cli 4.11.0
pinned commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
Cargo.lock SHA-256: 6efd3893a3c32d463748edfbd8361152e26dd17964d61bbe94cc4a390cd887b1
build command: cargo build --locked --release -p cedar-policy-cli
hash-only promotion PR: #70
hash-only promotion merge: 388d9f6dbf73cd35b8b89ebc0195b048940c1758
registry observed-build reference: 2f85096e819a40b90a11d45e971c9bb1f6cc1024aa20f00bfc593893d7a3b6d3
```

The registry hash is an observed build reference, not a reproducible-build invariant. Multiple correctly pinned builds produced different binary hashes, so runtime authorization must bind the exact binary described by the current inspected build receipt.

### Exact-binary binding repair

```text
PR: #72
merge commit: f4611c465a08d4bb5723177662414346f13d8c5f
main run: 31277526767
Cedar job: 93153673495
artifact: 9027488042
```

Run `31277526767` successfully built the pinned Cedar CLI and bound runtime execution to the exact binary described by that build receipt. The build receipt recorded:

```text
build result: BUILT_HASHED_UNEXECUTED
build exit code: 0
observed binary SHA-256: 42bda9fdc5d94e7fdadb35ffd9c2b0cbedf0135621c683dfacdb7d94f5a78472
registry reference matched current binary: false
binary_hash_reproducibility_claimed: false
execution_binding: exact_same_binary_as_inspected_build_receipt
```

The native authorization attempt then failed closed before a decision because Cedar CLI required an entity-store argument:

```text
error: the following required arguments were not provided:
  --entities <FILE>
```

The failure is retained in artifact `9027488042`, including `capture/cedar-allow-capture.json` and `capture/cedar-pinned-ci-capture-summary.json`.

### Entity-store repair

```text
PR: #73
merge commit: e3332a199f7f85758aa166f5cf93b108d5ccc7a7
fixture: docs/external-frameworks/capture/cedar/entities.json
fixture value: []
runner: scripts/run_pinned_cedar_ci_capture.py
```

The empty entity store is intentional: the retained fixture policy compares literal entity UIDs and does not consume entity attributes or parent relationships. The runner now:

```text
requires the entity fixture to exist
requires valid JSON-array syntax
passes --entities <fixture> to cedar authorize
binds entities_path and entities_sha256 into the capture summary
preserves exact-binary receipt binding
preserves repository-local-only execution boundaries
```

Canonical Cedar upstream evidence confirms Cedar CLI entity stores are JSON arrays; no special authority or external dependency is created by this fixture.

## Current machine-owned state

The first main workflow triggered directly by PR #73 was run `31281020432`; it was superseded/cancelled by a later main commit from another nonconflicting workstream before the Cedar job executed. This is not a Cedar validation failure.

Current main head observed after that supersession:

```text
main head: b3f6b3fd01ea074ee29e88bd17c463b8676833de
current canonical run: 31281075331
run number: 4009
state at last observation: PENDING
jobs materialized at last observation: none
```

The current run is repository-native and machine-owned. No duplicate Cedar workflow or manual alternative execution path is authorized while the canonical workflow owns the same run lane.

## Exact next executable actions

```text
1. Observe the latest non-superseded canonical main run that contains merge e3332a199f7f85758aa166f5cf93b108d5ccc7a7.
2. Inspect job `build-selected-cedar-binary` when materialized.
3. If the job fails, inspect its log and `cedar-selected-binary-build` artifact and repair the exact preserved failure under issue #63.
4. If the job succeeds, inspect:
   - cedar-allow-capture.json
   - cedar-deny-capture.json
   - cedar-pinned-ci-capture-summary.json
   - Cedar capture validator output.
5. Confirm the observed native decision semantics rather than inferring them from process exit alone.
6. Bind the observed outputs into the existing `scripts/run_cedar_governance_compatibility.py` six-family evaluator; do not create a duplicate compatibility system.
7. Execute and preserve `reports/external-frameworks/cedar/cedar-stegverse-governance-compatibility-receipt.json`.
8. Update `docs/external-frameworks/cedar-policy.md` from simulation-only/runtime-pending to the strongest evidence class actually supported.
9. Update issue #63 and this handoff, then release or retain the Cedar claim according to observed evidence.
```

## Blockers and machine-observable release conditions

Current blocker classification:

```text
state: MACHINE_OWNED_PENDING_CANONICAL_EXECUTION
owner: StegVerse-Labs/admissibility-wiki canonical workflow + Worker B issue #63
release condition: latest non-superseded main workflow containing PR #73 reaches a terminal Cedar build/capture result
observer: GitHub Actions workflow `.github/workflows/validate-chain-continuation.yml`
evidence surface: workflow job logs plus `cedar-selected-binary-build` artifact
```

If GitHub supersedes a run because a newer main commit arrives, continuation follows the newest descendant run containing PR #73. A superseded run is not interpreted as success or failure of the Cedar repair.

## Validation commands and evidence hierarchy

```text
python scripts/check_cedar_observation_capture_harness.py
python scripts/check_external_framework_implementation_selection_gates.py
python scripts/check_cedar_implementation_selection_evidence.py
python scripts/check_cedar_selected_binary_build_harness.py
python scripts/check_cedar_binary_promotion_automation.py
python scripts/check_cedar_binary_registry_promotion_receipts.py
python scripts/check_cedar_binary_hash_registry_application.py
python scripts/check_cedar_binary_provenance_reconciliation.py
python scripts/validate_cedar_capture_artifacts.py
python scripts/run_cedar_governance_compatibility.py
```

Validation levels must remain distinct:

```text
file present != valid fixture
valid fixture != native execution
native execution != semantic compatibility
compatibility evidence != certification
Cedar permit/forbid != StegVerse execution authority
workflow success != repository release
publication != standing
```

## Automation

Existing repository-native automation is the continuation path. It has:

```text
owner repository: StegVerse-Labs/admissibility-wiki
trigger: main/PR canonical workflow execution
inputs: pinned Cedar source commit, Cargo.lock, repository fixtures, governed registry/authority references
outputs: build receipt, capture artifacts, validation artifacts
state persistence: GitHub Actions artifacts + issue #63 + mirror handoffs
failure posture: fail closed
collision behavior: canonical workflow concurrency may supersede older runs; newest descendant run is authoritative
```

No second workflow is authorized for this sub-claim.

## Cross-repository dependencies and propagation

No Cedar runtime completion is currently claimed to require mutation of Site, Publisher, StegGuardian, or master-records. The canonical evidence owner is `StegVerse-Labs/admissibility-wiki`. If the completed Cedar comparison becomes a consumed downstream governance contract, propagation must first inspect the destination repository's current mirror handoff and install only the required consumer contract/evidence reference.

Potential destinations to inspect only after a concrete downstream contract exists:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
master-records owner identified by live contracts
```

Propagation is not claimed complete merely because the wiki publishes the evaluation.

## Session consolidation and merge record

```text
MERGED INTO: StegVerse-Labs/admissibility-wiki/docs/external-frameworks/CEDAR_RUNTIME_MIRROR_HANDOFF.md + issue #63
transferred:
  - exact-binary binding requirement
  - observed non-reproducible binary-hash distinction
  - run 31277526767 failure evidence and artifact 9027488042
  - Cedar CLI --entities failure diagnosis
  - PR #73 entity-store repair
  - canonical machine-owned continuation rule
  - exact compatibility next actions
already complete:
  - pinned source/build provenance
  - hash-only registry transition
  - exact-binary runtime binding repair
  - entity-store fixture and runner installation
remaining:
  - terminal canonical native ALLOW/DENY capture observation
  - semantic inspection of native outputs
  - observed-output integration into existing six-family StegVerse compatibility evaluator
  - Cedar second-page evidence-class promotion
continuation_owner: Worker B / issue #63 + repository-native canonical workflow
session-specific undocumented requirements remaining: none
```

This chat session does not need to remain open merely to poll the workflow. The repository, issue, and this handoff contain the current evidence, exact owner, blocker, release condition, collision rules, and next actions.

## Current completion metrics

Denominator for the Cedar runtime sub-claim, not the full 36-framework program:

```text
required task transitions: 8
completed task transitions: 5
required developed/runtime-control surfaces: 8
fully developed surfaces: 8
scaffolding or stubs: 0
missing required files: 0
required validation/observation gates: 4
validated/observed gates complete: 2
required integration gates: 2
integration gates complete: 1
goal activation: 5/8 transitions complete
session consolidation: 1/1
```

Repository-wide 36-framework accounting remains governed by the worker handoff and coordinator issue #66. Do not convert these Cedar-subclaim metrics into a claim that the overall 36-framework goal is complete.

## Archive conditions for this originating session

The originating session may close when:

```text
all unique Cedar implementation knowledge is durable: satisfied
exact current evidence and failure is durable: satisfied
owner is named: satisfied
next executable actions are named: satisfied
machine-observable release condition exists: satisfied
collision/supersession behavior is defined: satisfied
no unique chat-only implementation or validation responsibility remains: satisfied
```

Closing the session does not mark Cedar complete. It transfers continuation to the canonical repository-native workstream.
