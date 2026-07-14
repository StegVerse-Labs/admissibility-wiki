# AI-Led Radiology Mirror Handoff

This file is the durable activation handoff for the AI-led radiology execution-boundary work in `StegVerse-Labs/admissibility-wiki`.

The overall repository source of truth remains `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`. This file narrows the current activation state so future sessions and canonical automation do not require prior chat context.

## Goal

```text
Goal id: ai-led-radiology-execution-boundary
Issue: StegVerse-Labs/admissibility-wiki#15
Objective: publish and automatically validate a non-certifying execution-boundary formalism distinguishing assistive AI, AI-first mandatory human review, and prohibited autonomous negative clearance.
```

## Installed artifacts

```text
docs/formalisms/ai-led-radiology-execution-boundary.md
static/schemas/ai-led-radiology-execution-case.schema.json
tests/fixtures/ai-led-radiology-execution-cases.json
scripts/check_ai_led_radiology_execution.py
scripts/check_ai_led_radiology_publication.py
scripts/check_ai_led_radiology_handoff_sync.py
static/status/ai-led-radiology-execution-status.json
reports/ai-led-radiology-execution-receipt.json (generated automatically)
reports/public-activation-receipt.json (generated and uploaded automatically)
scripts/write-public-activation-receipt.mjs
scripts/check-public-activation-receipt-writer.mjs
sidebars.js
docs/formalisms/index.md
scripts/check_admissibility_automation_handoff.py
```

## Decision coverage

```text
ADMIT_ASSISTIVE_USE
ADMIT_AI_FIRST_WITH_MANDATORY_HUMAN_REVIEW
REVIEW_REQUIRED
DENY_AUTONOMOUS_CLEARANCE
FAIL_CLOSED
```

## Automation ownership

```text
Canonical workflow: .github/workflows/validate-chain-continuation.yml
Canonical validation seam: npm run validate:admissibility-automation-handoff
Execution validator: scripts/check_ai_led_radiology_execution.py
Publication validator: scripts/check_ai_led_radiology_publication.py
Handoff sync validator: scripts/check_ai_led_radiology_handoff_sync.py
Public activation receipt writer: scripts/write-public-activation-receipt.mjs
Receipt-writer validator: scripts/check-public-activation-receipt-writer.mjs
Execution receipt generation: automatic
Live publication evidence capture: automatic
Public activation receipt upload: automatic through the existing verify-public-pages job
Public navigation: installed
Manual task requirement: NONE
User manual action required: false
Additional active workflow created: false
```

## Run-bound live evidence

The existing public activation receipt writer now performs retrying live checks for:

```text
ai_led_radiology_formalism_reachable
ai_led_radiology_schema_reachable
ai_led_radiology_status_reachable
```

Each successful workflow receipt binds the checked URL, HTTP status, response size, attempt count, commit, workflow run ID, and run attempt. Local validation uses deterministic mock mode and does not require network access.

## Public endpoints

```text
https://stegverse-labs.github.io/admissibility-wiki/formalisms/ai-led-radiology-execution-boundary
https://stegverse-labs.github.io/admissibility-wiki/schemas/ai-led-radiology-execution-case.schema.json
https://stegverse-labs.github.io/admissibility-wiki/status/ai-led-radiology-execution-status.json
```

## Authority boundary

This activation does not certify clinical performance, authorize medical practice, endorse a hospital or vendor, establish regulatory compliance, or claim that any referenced institution has deployed autonomous radiology. It defines a governance distinction between assistive use and transfer of diagnostic execution authority.

## Remaining automation-owned observation

```text
- canonical workflow records and uploads the next passing run-bound public activation receipt
- future handoff reconciliation may record the observed workflow identifiers
```

This observation does not create a user task. Canonical automation and future handoff reconciliation own it.

## Continuation rule

Continue from this file together with `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` and `static/status/ai-led-radiology-execution-status.json`. No prior conversation is required.

The complete thread is ready for archiving without any additional part of the thread being needed to continue.
