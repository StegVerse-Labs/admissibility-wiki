# External Certification Intake

## Purpose

External Certification Intake is the bounded entry gate between public documentation or informal evaluation and the canonical Governance-Chain Certification test/issuance path.

An external framework is not test-ready merely because source material exists. Intake determines whether the subject, version, interface, fixtures, evidence path, and observation boundaries are sufficiently distinguishable to run the declared certification profile.

## Intake object

Every submission MUST identify:

```text
candidate_id
subject_id
subject_version
immutable_locator
artifact_hash or equivalent immutable binding
provider or responsible project
certification_surface: PRE | GOV | POST | INT
claimed_properties[]
test_profile_id
test_profile_version
interface_class
positive_fixture_route
negative_control_route
commit_or_effect_observation_point
request_receipt_route
return_receipt_route
replay_material
reconstruction_material
current_condition_inputs where claimed
evidence_destination
known_limits[]
```

## Readiness rule

`READY_FOR_CERTIFICATION_TEST` requires all profile-mandatory evidence and interfaces to be observable or executable. Documentation, architecture diagrams, marketing claims, repository presence, or protocol text are insufficient substitutes for a required live observation surface.

```text
source available != test surface available
test surface available != certification
intake PASS != certificate issuance
```

## Result classes

```text
READY_FOR_CERTIFICATION_TEST
  all required profile inputs, controls, interfaces, and observation points are available

READY_WITH_DECLARED_LIMITS
  a bounded subset is testable and the omitted properties are explicitly excluded

EVIDENCE_REQUESTED
  the subject is identifiable and potentially testable, but specific required evidence or interfaces are missing

SOURCE_ONLY_NOT_TESTABLE
  public/source material exists but does not expose the required test and observation surface

INDETERMINATE
  available material cannot distinguish the necessary intake facts

REJECTED_SCOPE
  the requested claim is outside the certification standard or cannot be represented by a supported profile
```

## Fail-closed behavior

The intake validator MUST refuse `READY_FOR_CERTIFICATION_TEST` when any mandatory requirement is absent, stale, contradictory, or only inferred.

It MUST also reject attempts to:

```text
substitute a product name for immutable version binding
claim properties outside the selected profile
omit negative controls
omit consequence/commit observation where required
omit receipt routes for INT profiles
convert owner assertions into observed evidence
convert payment or commercial engagement into readiness
use an unresolved source-only record as issuance authority
```

## Evidence request packets

When the correct state is `EVIDENCE_REQUESTED`, the retained record SHOULD enumerate the minimum missing artifacts required to advance. The request packet is descriptive, not coercive, and does not imply a contractual relationship.

## ArquivoNulo first external intake

The existing ArquivoNulo record currently supports:

```text
candidate distinguishable: yes
public protocol/source material: yes
proposed surface: INT
live interlock trace retained: no
required INT negative controls retained: no
request/return receipt pair retained: no
commit/effect timing resolved: no
current intake state: EVIDENCE_REQUESTED
certificate issued: false
```

The minimum evidence request is therefore limited to the missing live/observable surfaces needed to distinguish the INT profile. No broader disclosure is required merely to enter the certification process.
