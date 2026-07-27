#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "static/data/governed-framework-reviews/wiki-public-anchor.reconstruction-manifest.v1.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require_file(relative_path: str) -> Path:
    path = ROOT / relative_path
    if not path.exists() or not path.is_file():
        fail(f"declared reconstruction artifact missing: {relative_path}")
    return path


manifest = load_json(MANIFEST)

required_top_level = {
    "schema_version",
    "manifest_id",
    "repository",
    "goal_id",
    "frozen_from_commit",
    "state",
    "authority_boundary",
    "doctrine",
    "dockets",
    "schemas",
    "examples",
    "validators",
    "status_artifact",
    "routes",
    "reconstruction_requirements",
    "custody",
    "next_required_artifacts",
}
missing = sorted(required_top_level - manifest.keys())
if missing:
    fail(f"manifest missing fields: {', '.join(missing)}")

if manifest["schema_version"] != "1.0.0":
    fail("unexpected schema_version")
if manifest["repository"] != "StegVerse-Labs/admissibility-wiki":
    fail("unexpected repository")
if len(manifest["frozen_from_commit"]) != 40:
    fail("frozen_from_commit must be a full commit SHA")

boundary = manifest["authority_boundary"]
for key in (
    "publication_is_truth",
    "manifest_is_certification",
    "manifest_is_execution_authority",
    "repository_ownership_is_reviewer_standing",
    "internal_validation_is_independent_reconstruction",
):
    if boundary.get(key) is not False:
        fail(f"authority boundary must remain false: {key}")

for collection_name in ("doctrine", "schemas", "examples", "validators"):
    values = manifest.get(collection_name)
    if not isinstance(values, list) or not values:
        fail(f"{collection_name} must be a non-empty list")
    for relative_path in values:
        require_file(relative_path)

require_file(manifest["status_artifact"])

dockets = manifest["dockets"]
if not isinstance(dockets, list) or len(dockets) != 3:
    fail("manifest must freeze exactly three activation dockets")

review_ids = set()
expected_standing = {
    "review-ta14-reference-docket-2026-07-27": "PUBLICLY_UNRESOLVED",
    "review-asro-reference-docket-2026-07-27": "PROVISIONAL",
    "review-stegverse-public-anchor-self-2026-07-27": "PROVISIONAL",
}
for docket in dockets:
    for field in ("review_id", "page", "record", "standing"):
        if not docket.get(field):
            fail(f"docket missing {field}")
    if docket["review_id"] in review_ids:
        fail(f"duplicate review_id: {docket['review_id']}")
    review_ids.add(docket["review_id"])
    require_file(docket["page"])
    record_path = require_file(docket["record"])
    load_json(record_path)
    if expected_standing.get(docket["review_id"]) != docket["standing"]:
        fail(f"standing drift for {docket['review_id']}")

if set(expected_standing) != review_ids:
    fail("activation docket set drift")

routes = manifest["routes"]
if not isinstance(routes, list) or len(routes) != 4 or len(set(routes)) != 4:
    fail("routes must contain four unique canonical routes")
if not all(isinstance(route, str) and route.startswith("/docs/") for route in routes):
    fail("all routes must be canonical /docs/ routes")

requirements = manifest["reconstruction_requirements"]
for key in (
    "all_declared_files_present",
    "records_parse_as_json",
    "review_ids_unique",
    "standing_preserved",
    "authority_boundaries_fail_closed",
    "independent_reviewer_required_for_independent_reconstruction",
):
    if requirements.get(key) is not True:
        fail(f"reconstruction requirement must remain true: {key}")
if requirements.get("route_reachability_proves_truth") is not False:
    fail("route reachability must not be treated as truth")

custody = manifest["custody"]
if custody.get("publisher_receipt") != "NOT_AUTHORIZED":
    fail("Publisher custody must remain NOT_AUTHORIZED")
if custody.get("master_records_hash_receipt") != "NOT_AUTHORIZED":
    fail("Master Records custody must remain NOT_AUTHORIZED")
if custody.get("signature_status") != "NOT_BOUND":
    fail("signature status must remain NOT_BOUND")

print(f"OK: {MANIFEST.relative_to(ROOT)}")
print("activation_dockets=3")
print("canonical_routes=4")
print("authority_boundary=FAIL_CLOSED")
print("independent_reconstruction=NOT_CLAIMED")
