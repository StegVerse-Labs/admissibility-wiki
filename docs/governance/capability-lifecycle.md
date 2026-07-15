# Capability Lifecycle

## Purpose

This page defines the shared lifecycle used to distinguish documentation, implementation, validation, release, deployment, operation, custody, and retirement.

A capability is not operational merely because a page, script, workflow, fixture, endpoint, or status artifact exists. Each state requires evidence appropriate to that state, and advancement must be monotonic only when the required evidence is present.

## Lifecycle states

| State | Meaning | Required evidence |
|---|---|---|
| `PROPOSED` | Scope and intended boundary are documented. | Proposal, owner, exclusions, intended evidence path. |
| `SCAFFOLDED` | Structure or placeholder files exist. | Paths and ownership, with explicit missing implementation fields. |
| `IMPLEMENTED` | Source or configuration exists. | Repository identity, commit or release, source files, implementation record. |
| `FIXTURE_VALIDATED` | Deterministic local fixtures pass. | Pinned fixtures, expected outcomes, raw outputs, validator result. |
| `INTERNALLY_VALIDATED` | Canonical repository automation validates the implementation. | Observed workflow result, commit binding, generated receipts or reports. |
| `RELEASE_AUTHORIZED` | A governed release decision has been recorded. | Release authority record, scope, version, current standing. |
| `RELEASED` | A release or tag exists under valid authority. | Tag or release identity and release receipt. |
| `DEPLOYED` | The released capability is present at an authorized deployment coordinate. | Deployment identity, environment, endpoint or artifact, deployment receipt. |
| `PUBLICLY_VERIFIED` | Deployed public surfaces were observed after deployment. | Route observations bound to deployed version and timestamp. |
| `CONFORMANCE_VERIFIED` | The deployed interface satisfies the relevant contract. | Request and response fixtures, raw payloads, expected result, conformance report. |
| `CUSTODY_RECORDED` | Authenticated record custody and reconstructability are proven. | Custody receipt, master hash or pointer, reconstructability `PASS`. |
| `OPERATIONAL` | The capability may participate in governed transitions within its authorized scope. | Current standing, deployment, conformance, policy, delegation, receipts, required custody. |
| `SUSPENDED` | Operational use is temporarily blocked. | Suspension reason, authority record, affected scope, recovery conditions. |
| `REVOKED` | Prior standing or authority has been withdrawn. | Revocation record, effective time, affected versions and transitions. |
| `DEPRECATED` | New use is discouraged or prohibited in favor of a successor. | Deprecation record, replacement path, migration or shutdown boundary. |
| `RETIRED` | The capability is no longer valid for new governed transitions. | Retirement record, custody and archival disposition, terminal boundary. |

## Transition rules

```text
page presence cannot advance a capability beyond SCAFFOLDED
source presence cannot advance beyond IMPLEMENTED
fixture success cannot advance beyond FIXTURE_VALIDATED
expected workflow output cannot advance to INTERNALLY_VALIDATED
release intent cannot advance to RELEASE_AUTHORIZED
route reachability cannot establish RELEASED or OPERATIONAL
public verification cannot establish conformance
conformance cannot establish custody
custody cannot create execution authority
OPERATIONAL requires current standing and may later become SUSPENDED or REVOKED
```

## Evidence identity

Every lifecycle claim should identify:

```text
capability_id
owner_repository
coordinate
version_or_commit
current_state
prior_state
state_change_time
state_change_authority
evidence_refs
evidence_hashes
external_gates
blocked_by
scope
non_claims
next_evaluation
```

## Multi-coordinate capabilities

A capability spanning several repositories must not use one aggregate state when the coordinates differ. For example:

```text
wiki documentation: DEPLOYED or PUBLICLY_VERIFIED
adapter source: IMPLEMENTED or INTERNALLY_VALIDATED
Site client: PREPARED_NOT_DEPLOYED
provider gateway: NOT_DEPLOYED
Master-Records custody: NOT_ESTABLISHED
external executor: DISABLED_OR_EXTERNAL
```

The public summary must expose the weakest consequence-bearing coordinate rather than promoting the entire capability to the strongest documentation state.

## Machine-readable companion

A lifecycle registry or status artifact should expose the fields above and preserve missing evidence explicitly. Unknown or unavailable evidence must produce a fail-closed posture rather than defaulting to complete.

## Boundary

```text
classification != authority
validation != release
release != deployment
deployment != public verification
public verification != conformance
conformance != custody
custody != execution authority
operational standing is scoped, current, and revocable
```

## Current status

```text
CAPABILITY_LIFECYCLE_MODEL_DOCUMENTED
OPERATIONAL_ADVANCEMENT_REQUIRES_EVIDENCE
```
