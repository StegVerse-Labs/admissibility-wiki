# Translation Records Workflow Manifest

This is an iOS-safe mirror of `docs/TRANSLATION_RECORDS_WORKFLOW_MANIFEST.md`.

## Canonical Paths

```text
docs/formalisms/disciplinary-translation-groundwork.md
docs/formalisms/translation-records.md
static/translation-records/disciplinary-translation-records.v0.1.json
scripts/check_translation_records.py
docs/TRANSLATION_RECORDS_STATUS.md
github/workflows/validate-translation-records.yml
```

The workflow path above is displayed without its leading period for iOS compatibility. The actual repository path begins with a leading period.

## iOS-Safe Mirrors

```text
iosnoperiod/docs/TRANSLATION_RECORDS_STATUS.md
iosnoperiod/github/workflows/validate-translation-records.yml
```

## Validation Command

```bash
python scripts/check_translation_records.py
```

Expected output:

```text
TRANSLATION RECORDS: PASS - 6 records validated
```

## Authority Boundary

Translation records are interoperability artifacts, not proof authority or commit-time authority.
