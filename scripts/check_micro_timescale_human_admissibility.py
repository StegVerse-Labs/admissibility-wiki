from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/formalisms/micro-timescale-human-admissibility.md"
MODEL = ROOT / "static/formalisms/micro-timescale-human-admissibility.v0.1.json"
SIDEBAR = ROOT / "sidebars.js"

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

if not SIDEBAR.exists() or "formalisms/micro-timescale-human-admissibility" not in SIDEBAR.read_text(encoding="utf-8"):
    errors.append("formalism is not present in sidebars.js")

if errors:
    print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: PASS")
