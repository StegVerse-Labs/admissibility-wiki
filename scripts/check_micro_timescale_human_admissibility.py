from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/formalisms/micro-timescale-human-admissibility.md"
MODEL = ROOT / "static/formalisms/micro-timescale-human-admissibility.v0.1.json"
STATUS = ROOT / "static/status/micro-timescale-human-admissibility-status.json"
PROTOCOL = ROOT / "docs/research/micro-timescale-human-admissibility-observation-protocol.md"
OBSERVATION_SCHEMA = ROOT / "static/schemas/micro-timescale-human-admissibility-observation.schema.json"
EXAMPLE = ROOT / "static/examples/micro-timescale-human-admissibility-observation.example.json"
SIDEBAR = ROOT / "sidebars.js"
CANONICAL_CHECK = ROOT / "scripts/check_admissibility_automation_handoff.py"

required_doc_markers = [
    "Micro-Timescale Human Admissibility",
    "t_A",
    "t_M",
    "emitted != received",
    "admissible != committed",
    "mutually observable",
]
required_protocol_markers = [
    "Observation Protocol",
    "ADMISSIBILITY_CROSSING_CANDIDATE",
    "MUTUALLY_OBSERVABLE_CANDIDATE",
    "A candidate crossing is not accepted merely because repetition stops.",
    "independent",
]
required_event_types = {
    "EPISODE_START",
    "CANDIDATE_SIGNAL",
    "LISTENER_FEEDBACK",
    "SPEAKER_REPAIR_OR_HOLD",
    "ADMISSIBILITY_CROSSING_CANDIDATE",
    "MUTUALLY_OBSERVABLE_CANDIDATE",
    "COMMITMENT_ONSET",
    "EPISODE_END",
}

errors = []

def load_json(path: Path, label: str):
    if not path.exists():
        errors.append(f"missing {label}: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid {label} JSON: {exc}")
        return None

if not DOC.exists():
    errors.append(f"missing doctrine page: {DOC.relative_to(ROOT)}")
else:
    text = DOC.read_text(encoding="utf-8")
    for marker in required_doc_markers:
        if marker not in text:
            errors.append(f"doctrine missing marker: {marker}")

model = load_json(MODEL, "machine-readable model")
if model is not None:
    for key in ("schema_version", "formalism_id", "state_model", "equations", "failure_classes", "research_hypotheses"):
        if key not in model:
            errors.append(f"model missing key: {key}")

status = load_json(STATUS, "publication status")
if status is not None:
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

if not PROTOCOL.exists():
    errors.append(f"missing observation protocol: {PROTOCOL.relative_to(ROOT)}")
else:
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    for marker in required_protocol_markers:
        if marker not in protocol_text:
            errors.append(f"observation protocol missing marker: {marker}")

observation_schema = load_json(OBSERVATION_SCHEMA, "observation schema")
if observation_schema is not None:
    enum_values = set(
        observation_schema.get("properties", {})
        .get("events", {})
        .get("items", {})
        .get("properties", {})
        .get("event_type", {})
        .get("enum", [])
    )
    missing_event_types = sorted(required_event_types - enum_values)
    if missing_event_types:
        errors.append(f"observation schema missing event types: {', '.join(missing_event_types)}")

example = load_json(EXAMPLE, "observation example")
if example is not None:
    if example.get("schema_version") != "0.1.0":
        errors.append("observation example schema_version must equal 0.1.0")
    events = example.get("events")
    if not isinstance(events, list) or len(events) < 2:
        errors.append("observation example must contain at least two events")
    else:
        ids = [event.get("event_id") for event in events]
        sequences = [event.get("sequence") for event in events]
        if len(ids) != len(set(ids)):
            errors.append("observation example event IDs must be unique")
        if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
            errors.append("observation example sequences must be unique and ordered")
        for event in events:
            if event.get("event_type") not in required_event_types:
                errors.append(f"observation example has invalid event type: {event.get('event_type')}")
            if event.get("end_ms", -1) < event.get("start_ms", 0):
                errors.append(f"observation example event ends before it starts: {event.get('event_id')}")
        crossing_id = example.get("candidate_crossing_event_id")
        commitment_id = example.get("commitment_event_id")
        if crossing_id not in ids:
            errors.append("candidate_crossing_event_id must reference an event")
        if commitment_id not in ids:
            errors.append("commitment_event_id must reference an event")
    privacy = example.get("privacy_posture", {})
    if privacy.get("publication_authorized") is not False:
        errors.append("synthetic observation example must not claim publication authority")
    authority = example.get("authority", {})
    for field in (
        "recording_authority_granted",
        "research_authority_granted",
        "publication_authority_granted",
        "execution_authority_granted",
    ):
        if authority.get(field) is not False:
            errors.append(f"observation example {field} must be false")

sidebar_text = SIDEBAR.read_text(encoding="utf-8") if SIDEBAR.exists() else ""
if "formalisms/micro-timescale-human-admissibility" not in sidebar_text:
    errors.append("formalism is not present in sidebars.js")
if "research/micro-timescale-human-admissibility-observation-protocol" not in sidebar_text:
    errors.append("observation protocol is not present in Research navigation")

if not CANONICAL_CHECK.exists() or "MICRO_TIMESCALE_HUMAN_ADMISSIBILITY_CHECK" not in CANONICAL_CHECK.read_text(encoding="utf-8"):
    errors.append("formalism validator is not bound into canonical validation")

if errors:
    print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("MICRO-TIMESCALE HUMAN ADMISSIBILITY: PASS")
