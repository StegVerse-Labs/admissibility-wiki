# Site Mirror Handoff

## Current source of truth

This file is the documentation mirror handoff source of truth for `StegVerse-Labs/admissibility-wiki/docs/` until superseded.

## Active goal

Goal 5: external framework benchmark mechanism and Morrison Runtime boundary observation.

Goal 4 documented the bounded LLM free-tier trust chain across LLM-adapter, Site, and SDK. Goal 5 adds a reusable benchmark surface for comparing external framework boundaries under evidence-governed, non-certifying terms.

## Current proof path

```text
external framework material
-> benchmark case definition
-> exact input capture
-> observed result capture
-> parser and evaluated-step check
-> boundary-class assignment
-> StegVerse expected posture
-> interoperability opportunity
-> compatibility report
-> commitment-candidate path
-> SPE standing reconstruction
-> public observatory page
```

## Goal 5 benchmark chain

```text
StegVerse-Labs/admissibility-wiki
  -> docs/external-frameworks/runtime-governance-benchmark-suite.md
  -> static/external-frameworks/runtime-governance-benchmark-suite.v0.1.json
  -> scripts/check_runtime_governance_benchmark_suite.py
  -> docs/external-frameworks/morrison-runtime-boundary-observation.md
  -> docs/external-frameworks/reports/morrison-runtime.compatibility.json
  -> scripts/check_external_framework_reports.py
  -> docs/external-frameworks/index.md
  -> sidebars.js
```

## Installed files

```text
docs/external-frameworks/runtime-governance-benchmark-suite.md
static/external-frameworks/runtime-governance-benchmark-suite.v0.1.json
scripts/check_runtime_governance_benchmark_suite.py
docs/external-frameworks/morrison-runtime-boundary-observation.md
docs/external-frameworks/reports/morrison-runtime.compatibility.json update
scripts/check_external_framework_reports.py update
docs/external-frameworks/index.md update
sidebars.js update
docs/SITE_MIRROR_HANDOFF.md update
```

## Local verification

```bash
python scripts/check_runtime_governance_benchmark_suite.py
python scripts/check_external_framework_reports.py
python scripts/check_external_frameworks_index.py
npm run build
```

## Deployment verification

```text
Pending next canonical workflow run.
```

## Remaining hardening

```text
Attach raw audit payloads for Morrison observed cases.
Add replay table for repeated Morrison runs and trajectory hashes.
Route benchmark observations into Commitment Candidate fixtures.
Add framework-specific benchmark mapping pages for the remaining external frameworks.
Prepare release/tag candidate after build and artifact review.
```

## Boundary

External framework benchmark publication is not certification, endorsement, provider governance, execution authority, commit-time standing, replay authority, reconstruction authority, or upgrade-based admissibility.

Benchmark results identify observed boundaries, interoperability requirements, missing evidence, and improvement opportunities. They do not declare external frameworks invalid.

## Next mirror input

Only mirror benchmark results after exact input, output, timestamp, source URL or commit, parser status, evaluated steps, trajectory hash or trace ID, screenshot or raw audit payload, and StegVerse expected posture are captured.
