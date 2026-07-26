from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/formalisms/micro-timescale-human-admissibility.md"
MODEL = ROOT / "static/formalisms/micro-timescale-human-admissibility.v0.1.json"
STATUS = ROOT / "static/status/micro-timescale-human-admissibility-status.json"
SIDEBAR = ROOT / "sidebars.js"
CANONICAL_CHECK = ROOT / "scripts/check_admissibility_automation_handoff.py"

required_doc_markers = [
    "Micro-Timescale Human Admissibility",
    "t_A",
    "t_M",
    "Emission is not reception",
    "Admissibility is not commitment",
    "mutually observable",
]

errors = []

if not DOC.exists():
    errors.append(f"missing doctrine page: {DOC.relative_to(ROOT)}")
else:
    text = DOC.read_text(encoding="utf-8")
    for marker in required_doc_markers:
        if marker not in text:
            errors.append(f"doctrine missing marker: {marker}")

if not MODEL.exists():
    errors.append(f"missing machine-readable model: {MODEL.relative_to(ROOT)}")
else:
    try:
        model = json.loads(MODEL.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid model JSON: {exc}")
    else:
        for key in ("schema_version", "formalism_id", "state_model", "equations", "failure_classes", "research_hypotheses"):
            if key not in model:
                errors.append(f"model missing key: {key}")

if not STATUS.exists():
    errors.append(f"missing publication status: {STATUS.relative_to(ROOT)}")
else:
    try:
        status = json.loads(STATUS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid status JSON: {exc}")
    else:
        expected = {
            "formalism_id": "micro-timescale-human-admissibility",
            "linkedin_link_status": "WAIT_FOR_PUBLIC_ROUTE_OBSERVATION",
            "authority_posture": "EXPLANATORY_MODEL_NO_EXECUTION_AUTHORITY",
        }
        for key, value in expected.items():
            if status.get(key) != value:
                errors.append(f"status {key} must equal {value}")
        if not status.get("public_route", "").startswith("https://stegverse-labs.github.io/admissibility-wiki/"):
            errors.append("status public_route is missing or outside the public wiki origin")

if not SIDEBAR.exists() or "formalisms/micro-timescale-human-admissibility" not in SIDEBAR.read_text(encoding="utf-8"):
    errors.append("formalism is not present in sidebars.js")

if not CANONICAL_CHECK.exists() or "MICRO_TIMESCALE_HUMAN_ADMISSIBILITY_CHECK" not in CANONICAL_CHECK.read_text(encoding="utf-8"):
    errors.append("formalism validator is not bound into canonical validation")

if errors:
    print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: PASS")
