from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "portable-user-ai-pair-participation.md"
MANIFEST = ROOT / "static" / "governance" / "portable-user-ai-pair-participation.v0.1.json"
RECEIPT = ROOT / "receipts" / "portable-user-ai-pair-participation-receipt.json"
STATUS = ROOT / "static" / "status" / "portable-user-ai-pair-participation-status.json"
SIDEBAR = ROOT / "sidebars.js"
PACKAGE = ROOT / "package.json"

SIDEBAR_ENTRY = "governance/portable-user-ai-pair-participation"
PACKAGE_SCRIPT = "validate:portable-user-ai-pair"


def main() -> int:
    errors: list[str] = []

    for path, label in [
        (PAGE, "page"),
        (MANIFEST, "manifest"),
        (RECEIPT, "receipt"),
        (STATUS, "status"),
        (SIDEBAR, "sidebar"),
        (PACKAGE, "package"),
    ]:
        if not path.exists():
            errors.append(f"missing_{label}")

    if errors:
        print("PORTABLE USER/AI PAIR PARTICIPATION: FAIL - " + ", ".join(errors))
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    for required in [
        "Portable ecosystem node",
        "THREAD_SCOPED_PARTICIPANT",
        "user authority != AI authority",
        "Master-Records boundary",
    ]:
        if required not in page:
            errors.append(f"page_missing:{required}")

    if SIDEBAR_ENTRY not in sidebar:
        errors.append("sidebar_entry")

    scripts = package.get("scripts", {})
    if scripts.get(PACKAGE_SCRIPT) != "python scripts/check_portable_user_ai_pair_participation.py":
        errors.append("package_script")
    if f"npm run {PACKAGE_SCRIPT}" not in scripts.get("validate", ""):
        errors.append("canonical_validation_chain")

    classes = {item.get("origin_class"): item for item in manifest.get("origin_classes", [])}
    portable = classes.get("PORTABLE_USER_AI_PAIR", {})
    scoped = classes.get("THREAD_SCOPED_PARTICIPANT", {})

    if not portable:
        errors.append("portable_origin_class")
    if not scoped:
        errors.append("thread_origin_class")

    boundaries = portable.get("authority_boundaries", {})
    if boundaries.get("user_authority_equals_ai_authority") is not False:
        errors.append("user_ai_authority_boundary")
    if boundaries.get("pair_continuity_implies_unrestricted_delegation") is not False:
        errors.append("delegation_boundary")
    if boundaries.get("ai_assistance_implies_autonomous_consent") is not False:
        errors.append("consent_boundary")

    scoped_boundaries = scoped.get("authority_boundaries", {})
    if scoped_boundaries.get("ecosystem_standing_inferred") is not False:
        errors.append("thread_standing_boundary")

    master = manifest.get("master_records_boundary", {})
    if master.get("becomes_global_user_identity_authority") is not False:
        errors.append("master_records_identity_boundary")
    if master.get("portable_node_retains_private_identifier_mappings") is not True:
        errors.append("portable_private_mapping_boundary")

    if receipt.get("result") not in {
        "DECLARED_AND_INSTALLED",
        "LOCAL_VALIDATION_CHAIN_WIRED",
    }:
        errors.append("receipt_result")

    if status.get("schema") != "admissibility_wiki.portable_user_ai_pair_participation_status.v1":
        errors.append("status_schema")
    if status.get("status") != "LOCAL_VALIDATION_CHAIN_WIRED":
        errors.append("status_value")
    verification = status.get("verification", {})
    for key in [
        "artifacts_installed",
        "sidebar_registered",
        "package_validation_registered",
        "canonical_validation_chain_registered",
    ]:
        if verification.get(key) is not True:
            errors.append(f"status_verification:{key}")

    if errors:
        print("PORTABLE USER/AI PAIR PARTICIPATION: FAIL - " + ", ".join(errors))
        return 1

    print("PORTABLE USER/AI PAIR PARTICIPATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
