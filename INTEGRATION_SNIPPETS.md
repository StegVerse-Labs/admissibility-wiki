# admissibility-wiki Integration Snippets

## sidebars.js

Add these two entries near the existing governed LLM pages in the Governance section:

```js
'governance/governed-llm-demo-overview',
'governance/governed-llm-demo-verification',
```

Recommended cluster:

```js
'governance/governed-llm-reconstructive-search',
'governance/governed-llm-activation-map',
'governance/governed-llm-demo-overview',
'governance/governed-llm-demo-verification',
'governance/governed-llm-site-verification',
'governance/governed-llm-deployment-status',
'governance/governed-llm-archive-handoff',
```

## README.md

Add this near the existing governed LLM section:

```md
The governed LLM end-to-end demonstrator pages are:

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/GOVERNED_LLM_SITE_NEXT_STAGES_README.md
```

Run:

```bash
python scripts/check_governed_llm_demo_docs.py
```

Expected current state:

```text
GOVERNED LLM DEMO DOCS: PASS - demo pages and navigation references present
```
```

## governed-llm-activation-map.md

Add this section:

```md
## End-to-End Demonstrator

The governed LLM path now includes a fixture-first end-to-end demonstrator.

```text
fixture query
  -> LLM-adapter governed session packet
  -> SDK demo packet verification
  -> Site demo overview
  -> Site demo verification
```

Implementation surfaces:

```text
StegVerse-org/LLM-adapter/docs/END_TO_END_DEMO.md
StegVerse-org/LLM-adapter/examples/end_to_end/
StegVerse-org/StegVerse-SDK/examples/governed_llm_demo/
StegVerse-Labs/admissibility-wiki/docs/governance/governed-llm-demo-overview.md
StegVerse-Labs/admissibility-wiki/docs/governance/governed-llm-demo-verification.md
```

The demonstrator remains fixture-first and does not prove live provider governance, execution authority, master-record persistence, external indexing, or production deployment.
```

## governed-llm-archive-handoff.md

Add these completed surfaces after installation:

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/GOVERNED_LLM_SITE_NEXT_STAGES_README.md
scripts/check_governed_llm_demo_docs.py
sidebars.js
README.md
```

Archive-ready condition:

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## governed-llm-deployment-status.md / deployment checker

Add the public route paths:

```text
/governance/governed-llm-demo-overview
/governance/governed-llm-demo-verification
```
