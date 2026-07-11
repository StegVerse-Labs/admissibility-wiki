---
title: Observed Evidence Capture Status
---

# Observed Evidence Capture Status

## Current coverage

```text
promoted frameworks: 18
source records: 18 of 18
individual pages: 18 of 18
benchmark mappings: 18 of 18
non-authorizing fixtures: 18 of 18
priority capture queue: 7 of 7
executable capture harnesses: 7 of 7
captured external outputs: 0 of 18
independently replayed outputs: 0 of 18
```

## Priority capture harnesses

| Framework | Harness posture | Runtime posture | Evidence state |
|---|---|---|---|
| Open Policy Agent | dedicated deterministic harness | pinned OPA executable required | awaiting_capture |
| Cedar Policy | dedicated implementation-neutral harness | exact Cedar implementation required | awaiting_capture |
| Model Context Protocol | reusable command harness + manifest | exact client/server and transport required | awaiting_capture |
| Agent2Agent Protocol | reusable command harness + manifest | exact agent implementation required | awaiting_capture |
| Guardrails AI | reusable command harness + manifest | exact package, validator, and model context required | awaiting_capture |
| Llama Guard | reusable command harness + manifest | exact model digest and runtime required | awaiting_capture |
| NeMo Guardrails | reusable command harness + manifest | exact package, rails configuration, and model context required | awaiting_capture |

## Evidence progression

```text
fixture_ready
-> awaiting_capture
-> captured_unverified
-> observed_partial
-> replay_ready
-> replay_confirmed
-> interoperability_candidate
```

No framework has advanced beyond `awaiting_capture` on this surface. Harness installation is structural readiness, not observed behavior.

## Boundary

```text
capture harness != external execution
captured output != compatibility
single run != replayability
matching replay != execution authority
policy decision != current delegation
classifier result != admissibility
protocol response != standing
```

The exact version, timestamp, execution environment, input, output, policy or configuration, authority context, freshness context, hashes, limitations, and replay instructions must be retained before any state advancement.
