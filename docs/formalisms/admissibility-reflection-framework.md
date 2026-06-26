# StegVerse-Labs/admissibility-wiki

## Reflection Metadata

```text
Claim ID: CLM-ARF-0001
Packet ID: ARF-PKT-0001
Evidence grade: PRIMARY
Admissibility result: ALLOW-WITH-LIMITS
Standing: CURRENT
Reflection status: ALLOW-WITH-LIMITS
Source artifacts: 2
Known limits: 1
Last evaluation: 2026-06-24T00:00:00Z
Challenge path: submit a challenge packet against this claim ID
```

## Public Claim

The Admissibility Wiki reflects admissibility determinations. It does not create standing.

## Evidence Summary

| Source ID | Source type | Path or URL | Role | Hash |
| --- | --- | --- | --- | --- |
| SRC-ARF-0001 | canonical-repository | StegVerse-Labs/admissibility-wiki | reflection-target |  |
| SRC-ARF-0002 | governance-formalism | Admissible-Existence/AE/docs/admissibility-reflection-framework.md | reflection-governance |  |

## Evidentiary Grade

```text
Grade: PRIMARY
Confidence: HIGH
```

### Reasoning

- The claim is defined by the governing framework document that specifies how wiki reflection must be bounded.

### Limits

- The grade applies to the governance claim, not to every current or future wiki entry.

## Admissibility Result

```text
Result: ALLOW-WITH-LIMITS
Scope: public-reflection
```

### Reasoning

- The reflected claim is narrow and prevents the wiki from being treated as an authority source.
- The claim preserves the distinction between evidence, standing, admissibility, publication, and reflection.

### Fail-closed Conditions

- The wiki entry asserts authority not present in the packet.
- The evidence source cannot be reconstructed.
- The public claim implies certification or endorsement.

## Standing

```text
Standing: CURRENT
Expires at: None
Review required on change: True
```

### Standing Basis

- reconstructable framework document
- bounded public claim
- explicit prohibited claims

## Prohibited Claims

- The wiki is the authority source.
- Publication proves admissibility.
- External framework reflection is endorsement or certification.
- A reflected claim automatically has current standing.

## Reflection Receipt

```text
Receipt ID: RCP-ARF-0001
Packet hash: TBD
Reflection hash: TBD
Status: EXAMPLE
Created at: 2026-06-24T00:00:00Z
```

## Challenge Path

A reader may challenge this reflection by identifying the claim, challenged field, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.
