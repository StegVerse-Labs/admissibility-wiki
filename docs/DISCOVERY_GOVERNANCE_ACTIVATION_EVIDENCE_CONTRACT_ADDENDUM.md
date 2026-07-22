# Discovery-Governance Activation Evidence Contract Addendum

## Authority and scope

This addendum extends `docs/DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md` without replacing it. Repository authority remains governed by `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`.

## Installed contract validation

The run-bound activation evidence layer is now statically and canonically validated by:

```text
scripts/check_discovery_governance_activation_evidence_contract.py
```

Installed commit:

```text
584ccbd2849200c86ac4df956c0a91219041e8fa
```

Canonical integration:

```text
scripts/check_admissibility_automation_handoff.py
commit d0b94fc66c5eb5f038f709b72fef9a76b4aa6d07
```

Status advancement:

```text
static/status/discovery-governance-handoff-status.json
commit bd8f51ac84f77d6b6bad325bc2fd8034513d897a
```

## Contract enforced

Canonical validation now fails if any of the following drift or disappear:

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
all false authority constants
```

The validator also requires the schema to preserve exact paths for:

```text
reports/discovery-governance-handoff-proof-receipt.json
reports/discovery-governance-publication-receipt.json
reports/public-activation-receipt.json
```

## Preserved boundary

A passing contract check proves only that the source-side evidence contract remains installed and internally consistent. It does not prove that a GitHub Actions run passed, that Pages deployed, that public routes are reachable, or that activation evidence is complete.

It grants no consent, standing, authority, admissibility, commitment, execution permission, certification, endorsement, interoperability standing, release authority, or downstream mutation authority.

## Current state

```text
SOURCE_COMPLETE_WITH_CANONICALLY_VALIDATED_RUN_BOUND_ACTIVATION_EVIDENCE_PENDING_WORKFLOW_OBSERVATION
```

## Remaining work

Destination: `StegVerse-Labs/admissibility-wiki`

```text
1. Observe a canonical workflow run containing commit bd8f51ac84f77d6b6bad325bc2fd8034513d897a or a successor.
2. Inspect and repair only evidence-grounded validation or Docusaurus build failures.
3. Confirm the activation-evidence contract validator passes inside canonical validation.
4. Retrieve the proof and public-activation artifacts.
5. Confirm all five routes and ACTIVATION_EVIDENCE_COMPLETE.
6. Record run id, attempt, commit, artifact ids, route statuses, and receipt digests in the authoritative handoff.
```

No downstream repository mutation is authorized by this addendum.
