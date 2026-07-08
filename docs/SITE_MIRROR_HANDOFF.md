# Site Mirror Handoff

## Current source of truth

This file is the documentation mirror handoff source of truth for `StegVerse-Labs/admissibility-wiki/docs/` until superseded.

## Active goal

Goal 5: external framework benchmark mechanism, Morrison Runtime boundary observation, cross-framework benchmark mapping rollout, and fixture hardening.

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
-> compatibility report
-> observation fixture
-> commitment-candidate fixture
-> benchmark mapping companion
-> benchmark fixture
-> SPE standing reconstruction
-> public observatory page
```

## Goal 5 benchmark chain

```text
StegVerse-Labs/admissibility-wiki
  -> docs/external-frameworks/runtime-governance-benchmark-suite.md
  -> static/external-frameworks/runtime-governance-benchmark-suite.v0.1.json
  -> docs/external-frameworks/benchmark-mapping-rollout.md
  -> docs/external-frameworks/benchmark-mapping-rollout.json
  -> docs/external-frameworks/benchmark-mappings/*.mapping.json
  -> docs/external-frameworks/fixtures/*-benchmark-fixture.v0.1.json
  -> docs/external-frameworks/fixtures/morrison-runtime-benchmark-observations.v0.1.json
  -> scripts/check_external_framework_benchmark_mappings.py
  -> scripts/check_external_framework_benchmark_fixtures.py
  -> scripts/check_runtime_governance_benchmark_suite.py
  -> docs/external-frameworks/morrison-runtime-boundary-observation.md
  -> docs/external-frameworks/reports/morrison-runtime.compatibility.json
  -> docs/external-frameworks/morrison-runtime-commitment-candidate.json
  -> scripts/check_morrison_runtime_benchmark_fixtures.py
  -> scripts/check_external_framework_reports.py
  -> docs/external-frameworks/index.md
  -> sidebars.js
```

## Installed mapping companions

```text
morrison-runtime
asro
glm
evide
decisionassure
mindforge
care-runtime
aar
mitre-atlas
owasp-top-10-llm
agent-governance-playbook
killswitch-md
nist-ai-rmf
iso-iec-42001
eu-ai-act
policy-cards
runtime-governance-policies-on-paths
```

## Installed fixture artifacts

```text
morrison-runtime-benchmark-observations.v0.1.json
glm-benchmark-fixture.v0.1.json
evide-benchmark-fixture.v0.1.json
decisionassure-benchmark-fixture.v0.1.json
mindforge-benchmark-fixture.v0.1.json
asro-benchmark-fixture.v0.1.json
policy-cards-benchmark-fixture.v0.1.json
runtime-governance-policies-on-paths-benchmark-fixture.v0.1.json
killswitch-md-benchmark-fixture.v0.1.json
care-runtime-benchmark-fixture.v0.1.json
aar-benchmark-fixture.v0.1.json
mitre-atlas-benchmark-fixture.v0.1.json
owasp-top-10-llm-benchmark-fixture.v0.1.json
agent-governance-playbook-benchmark-fixture.v0.1.json
nist-ai-rmf-benchmark-fixture.v0.1.json
iso-iec-42001-benchmark-fixture.v0.1.json
eu-ai-act-benchmark-fixture.v0.1.json
```

## Installed files

```text
docs/external-frameworks/runtime-governance-benchmark-suite.md
static/external-frameworks/runtime-governance-benchmark-suite.v0.1.json
docs/external-frameworks/benchmark-mapping-rollout.md
docs/external-frameworks/benchmark-mapping-rollout.json
docs/external-frameworks/benchmark-mappings/*.mapping.json
docs/external-frameworks/fixtures/*-benchmark-fixture.v0.1.json
scripts/check_external_framework_benchmark_mappings.py
scripts/check_external_framework_benchmark_fixtures.py
scripts/check_runtime_governance_benchmark_suite.py
docs/external-frameworks/morrison-runtime-boundary-observation.md
docs/external-frameworks/reports/morrison-runtime.compatibility.json update
docs/external-frameworks/fixtures/morrison-runtime-benchmark-observations.v0.1.json
docs/external-frameworks/morrison-runtime-commitment-candidate.json
scripts/check_morrison_runtime_benchmark_fixtures.py
scripts/check_external_framework_reports.py update
docs/external-frameworks/index.md update
sidebars.js update
docs/SITE_MIRROR_HANDOFF.md update
```

## Local verification

```bash
python scripts/check_runtime_governance_benchmark_suite.py
python scripts/check_morrison_runtime_benchmark_fixtures.py
python scripts/check_external_framework_reports.py
python scripts/check_external_framework_benchmark_mappings.py
python scripts/check_external_framework_benchmark_fixtures.py
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
Run replay captures for repeated Morrison inputs and trajectory hashes.
Attach concrete source-versioned examples to fixture artifacts.
Decide whether Admissible Existence Seed Cycle needs a benchmark mapping or should remain a mirror-only page.
Prepare release/tag candidate after build and artifact review.
```

## Boundary

External framework benchmark publication is not certification, endorsement, provider governance, execution authority, commit-time standing, replay authority, reconstruction authority, or upgrade-based admissibility.

Benchmark results identify observed boundaries, interoperability requirements, missing evidence, and improvement opportunities. They do not declare external frameworks invalid.

## Next mirror input

Only mirror benchmark results after exact input, output, timestamp, source URL or commit, parser status, evaluated steps, trajectory hash or trace ID, screenshot or raw audit payload, and StegVerse expected posture are captured.
