# Discovery-Governance Activation Evidence Contract Addendum

## Authority and scope

This addendum extends `docs/DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md` without replacing it. Repository authority remains governed by `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`.

## Installed contract validation

The run-bound activation evidence layer is statically and canonically validated by:

```text
scripts/check_discovery_governance_activation_evidence_contract.py
commit 584ccbd2849200c86ac4df956c0a91219041e8fa
```

It is now also executed against deterministic complete and fail-closed evidence sets by:

```text
scripts/check_discovery_governance_activation_evidence_runtime.py
commit b5c15296aa30ddf77b7919e7c29b0505377a866a
```

Canonical integration:

```text
scripts/check_admissibility_automation_handoff.py
contract integration commit d0b94fc66c5eb5f038f709b72fef9a76b4aa6d07
runtime integration commit 36ae276aad984f7b288a7ba11c798fb46d5270b2
```

Status advancement:

```text
static/status/discovery-governance-handoff-status.json
runtime-validation commit 54035ab6b0d92d73532671d596a0a24f2b45a5b0
```

## Contract enforced

Canonical validation fails if any of the following drift or disappear:

```text
activation evidence writer
activation evidence receipt schema
ACTIVATION_EVIDENCE_COMPLETE / ACTIVATION_EVIDENCE_FAIL_CLOSED states
canonical dependency assertion
proof/publication/public-activation receipt paths
workflow closure-integrity execution
workflow activation-evidence generation
final artifact custody
required receipt fields
explicit completion criteria
all false authority constants
runtime complete-case behavior
runtime failed-route fail-closed behavior
```

The contract validator requires exact paths for:

```text
reports/discovery-governance-handoff-proof-receipt.json
reports/discovery-governance-publication-receipt.json
reports/public-activation-receipt.json
```

## Runtime cases

The runtime validator snapshots any pre-existing report files, executes the evidence writer, validates the output, and restores the original files before exiting.

Complete case:

```text
all four deterministic outcomes preserved
all five routes reachable with HTTP 200
publication state complete
Pages deployment observed
standalone and embedded receipts equal
run identity equal
all completion criteria true
expected state: ACTIVATION_EVIDENCE_COMPLETE
expected goal_completion_observed: true
```

Fail-closed case:

```text
one required public route unreachable with HTTP 503
publication state fail-closed
Pages deployment not observed
public activation publication_complete false
expected state: ACTIVATION_EVIDENCE_FAIL_CLOSED
expected goal_completion_observed: false
```

The runtime validator also confirms that authority-bearing fields remain false in the successful evidence receipt.

## Preserved boundary

A passing source-side runtime test proves that deterministic fixtures produce the intended complete and fail-closed receipt behavior. It does not prove that a GitHub Actions run passed, that Pages deployed, that live public routes are reachable, or that activation evidence is complete for a real run.

It grants no consent, standing, authority, admissibility, commitment, execution permission, certification, endorsement, interoperability standing, release authority, or downstream mutation authority.

## Current state

```text
SOURCE_COMPLETE_WITH_CANONICAL_RUNTIME_VALIDATION_PENDING_WORKFLOW_OBSERVATION
```

## Remaining work

Destination: `StegVerse-Labs/admissibility-wiki`

```text
1. Observe a canonical workflow run containing commit 54035ab6b0d92d73532671d596a0a24f2b45a5b0 or a successor.
2. Inspect and repair only evidence-grounded validation or Docusaurus build failures.
3. Confirm both activation-evidence contract and runtime validators pass inside canonical validation.
4. Retrieve the proof and public-activation artifacts.
5. Confirm all five live routes and ACTIVATION_EVIDENCE_COMPLETE.
6. Record run id, attempt, commit, artifact ids, route statuses, and receipt digests in the authoritative handoff.
```

No downstream repository mutation is authorized by this addendum.
