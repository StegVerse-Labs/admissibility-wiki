# Pages Public Endpoint Verification Handoff

## Installed transition

```text
PAGES_ARTIFACT_PRESERVED
-> observed Pages deployment
-> public endpoint verification receipt
-> separate release and destination-propagation review
```

## Installed files

```text
static/schemas/pages-public-endpoint-verification-receipt.schema.json
tests/fixtures/pages-public-endpoint-verification-receipt.fail-closed.json
scripts/check_pages_public_endpoint_verification_receipt.py
```

## Verification boundary

A receipt may advance to `PUBLIC_ENDPOINTS_VERIFIED` only when it binds:

```text
source deployment-observation receipt SHA-256
deployment run and job IDs
HTTPS deployment URL
verification run, job, and attempt IDs
verification evidence reference
all required endpoint HTTP 200 observations
content SHA-256 for every required endpoint
endpoint-specific evidence references
```

The minimum required endpoint set includes:

```text
/admissibility-wiki/
/admissibility-wiki/status/admissibility-wiki-status.json
/admissibility-wiki/status/ios-workflow-mirror-status.json
/admissibility-wiki/formalisms/inference-window-irreversibility-governance
```

A root-page response alone is insufficient. HTTP status without content hashing and evidence references is also insufficient.

## States

```text
FAIL_CLOSED
PUBLIC_ENDPOINTS_VERIFIED
```

The installed fixture remains `FAIL_CLOSED`; it carries no observed verification run or endpoint results.

## Authority boundary

Every receipt preserves:

```text
release_authorized: false
downstream_propagation_authorized: false
```

Therefore:

```text
deployment observation != public endpoint verification
public endpoint verification != release authority
public endpoint verification != destination propagation authority
route reachability != semantic correctness
same-provider verification != independent-provider verification
```

## Next transition

Inspect an actual successful `verify-public-pages` job and bind the exact run, job, URL, route responses, content hashes, and evidence references. Only then may the receipt state become `PUBLIC_ENDPOINTS_VERIFIED`. Release and destination propagation still require separate governed review.
