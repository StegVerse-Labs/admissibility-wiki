# Decision Authority Compatibility Report

## Repository

`StegVerse-Labs/admissibility-wiki`

## Canonical Source

`StegVerse-Labs/repo-standards/schemas/decision-authority.schema.json`

## Observed Public Vocabulary

The README governed ecosystem transition framing currently exposes:

```text
ALLOW
DENY
FAIL-CLOSED
```

## Mapping

| Wiki value | ST-004 authority value |
| --- | --- |
| `ALLOW` | `allowed` |
| `DENY` | `denied` |
| `FAIL-CLOSED` | `fail-closed` |
| `FAIL_CLOSED` | `fail-closed` normalized alias |
| `DEFER` | `requires-human-review` reserved |
| `ADVISORY_ONLY` | `advisory-only` reserved |

## Compatibility Posture

```text
local_decision_vocabulary_detected: true
compatibility_status: MAPPING_INSTALLED
```

## Boundary

Wiki vocabulary is public doctrine and explanatory framing. It is not ST-004 transition authority unless mapped to the canonical authority vocabulary and supported by policy, delegation, evidence, and validation.
