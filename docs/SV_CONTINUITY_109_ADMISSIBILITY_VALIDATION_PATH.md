# Canonical Validation Path

```text
SV-CONTINUITY-109 destination receipt
→ scripts/check_sv_continuity_109_admissibility.py
→ scripts/check_admissibility_automation_handoff.py
→ .github/workflows/validate-chain-continuation.yml
→ merge receipt
→ Continuity issue #3
```

The path is fail-closed. No intermediate artifact grants authority.
