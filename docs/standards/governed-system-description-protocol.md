# Governed System Description Protocol (GSDP)

Status: **Public Draft 0.1**

## 1. Purpose

The Governed System Description Protocol defines a machine-readable declaration for governed AI systems, autonomous systems, agent platforms, orchestration layers, certification systems, and distributed decision infrastructure.

A GSDP declaration makes the system discoverable as an authority-bearing and evidence-producing structure. It does not establish that the declaration is true, complete, independently verified, certified, safe, lawful, interoperable, or authorized to execute.

## 2. Discovery

A conforming publisher SHOULD expose its current declaration at:

```text
/.well-known/governed-system.json
```

The declaration MUST identify its canonical URI, version, effective interval, schema, prior declaration when one exists, and integrity information when available.

## 3. Normative language

The terms MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are normative.

## 4. Core distinctions

A declaration MUST preserve the following distinctions:

```text
capability != authority
identity != standing
approval != current admissibility
implementation != verification
verification != certification
publication != truth
schema conformance != substantive correctness
current state != historical state at time T
interoperability != execution authority
```

## 5. Required top-level fields

A declaration MUST contain:

```text
$schema
gsdp_version
declaration_id
system
operators
components
authority
governance
evidence
status
dependencies
history
claims
explicit_non_claims
```

## 6. System identity

`system` MUST provide a stable identifier, name, description, system class, canonical public URI, and version.

A system identifier MUST NOT be reused for a materially different system without an explicit succession relationship.

## 7. Operators

Each operator MUST identify:

- its stable identifier;
- its relationship to the system;
- the components it operates;
- authority it holds;
- authority it explicitly does not hold;
- the interval during which the declaration says that relationship applies.

Operator control MUST NOT be interpreted as certification, independent verification, or unrestricted execution authority.

## 8. Components

Each component MUST declare:

```text
id
name
class
role
status
operator_refs
capabilities
authority
explicit_non_authority
inputs
outputs
dependencies
interfaces
evidence_refs
```

A capability describes what a component can technically perform. Authority describes what it may legitimately perform under the declared governance conditions. The two MUST remain separate.

## 9. Authority

The declaration MUST expose machine-readable authority classes, delegations, revocation sources, standing requirements, consent conditions, commit authorities, and explicit non-authorities.

Authority declarations SHOULD include:

```text
subject
scope
action classes
resource classes
conditions
effective interval
issuer
revocation source
evidence references
```

No consumer may infer authority from capability, ownership, identity, repository control, network reachability, or prior execution.

## 10. Governance and admissibility

The declaration MUST identify its decision vocabulary and the sources governing transition admissibility.

A GSDP declaration MAY use `ALLOW`, `DENY`, and `DEFER`, but it MUST define the meaning of every decision state it publishes.

Governance declarations SHOULD describe:

```text
policy sources
standing requirements
consent requirements
delegation requirements
commit-time checks
safe states
rollback conditions
refusal behavior
override behavior
dispute routes
```

## 11. Evidence and reconstruction

The declaration MUST identify available evidence types and where verification procedures can be found.

Evidence descriptions SHOULD include:

```text
receipt schemas
provenance records
signatures and hashes
custody references
replay interfaces
reconstruction procedures
retention rules
disclosure rules
```

A declaration MUST NOT claim reconstructability solely because logs or receipts exist. The claimed reconstruction class must identify the required historical declarations, policies, authority records, and evidence boundaries.

## 12. Status and maturity

The declaration MUST separately describe:

```text
declared
implemented
tested
independently verified
certified
operational
authorized
```

Unsupported states MUST be represented as false, unknown, not run, not observed, or another explicitly defined non-positive state.

## 13. Dependencies and external authority

Each dependency MUST state whether it is technical, evidentiary, operational, governance-related, or authority-bearing.

A system MUST NOT inherit authority from a dependency unless the delegation and scope are explicitly declared and independently addressable.

## 14. Historical continuity

A declaration MUST include:

```text
effective_from
effective_until
supersedes
previous_declaration
declaration_hash
evidence_cutoff
```

When no previous declaration exists, that absence MUST be explicit.

Historical declarations SHOULD remain retrievable so an observer can reconstruct the declared system state applicable to an event at time T.

## 15. Claims and explicit non-claims

Every declaration MUST contain both `claims` and `explicit_non_claims`.

Claims SHOULD include evidence references and a status such as:

```text
declared
supported
internally verified
independently verified
disputed
superseded
withdrawn
```

Explicit non-claims prevent a consumer from inferring certification, endorsement, partnership, government recognition, production validation, custody, execution authority, or other standing that has not been established.

## 16. Conformance classes

### GSDP-DISCOVERABLE

Publishes identity, operators, components, interfaces, status, history, claims, and explicit non-claims.

### GSDP-GOVERNED

Adds authority, non-authority, delegation, revocation, consent, standing, policy, and admissibility declarations.

### GSDP-EVIDENCED

Adds evidence schemas, verification methods, receipt locations, integrity records, and custody references.

### GSDP-RECONSTRUCTABLE

Adds historical declarations and the records required to reconstruct the declared commit-time state.

### GSDP-INTEROPERABLE

Adds machine-readable cross-system authority, evidence, and translation relationships with bounded failure behavior.

### GSDP-CERTIFIABLE

Provides a complete assessment profile sufficient for an independent evaluator to determine conformance. Publication of this profile does not itself certify the system.

Higher classes are additive. A publisher MUST NOT claim a higher class while omitting requirements from a lower class.

## 17. Validation

Validation MUST distinguish at least:

```text
JSON syntax
schema structure
reference resolution
internal semantic consistency
authority non-inheritance
historical continuity
evidence availability
independent conformance
```

A schema-valid result MUST NOT be reported as independent conformance.

## 18. StegVerse reference implementation boundary

The StegVerse declaration is the first draft reference fixture. It is a self-description and test artifact. It does not establish external adoption, certification, government recognition, independent verification, or authority over other systems.

## 19. Planned extensions

Future drafts may define:

- signed declarations;
- content-addressed historical chains;
- component-level sub-declarations;
- cross-system translation receipts;
- dispute and correction objects;
- public declaration registries;
- conformance test profiles;
- selective disclosure and redaction profiles.
