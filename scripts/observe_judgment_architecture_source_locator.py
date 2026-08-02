#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "static/data/external-frameworks/judgment-architecture-source-locator-candidates.v1.json"
STATUS = ROOT / "static/status/judgment-architecture-source-locator-observation.json"
ACCEPTED = {"creator_publication_page", "publisher_publication_page", "isbn_catalog_record", "doi_or_archival_record", "durable_public_pdf"}


def main() -> int:
    payload = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    candidates = payload.get("candidates", [])
    accepted = []
    review = []
    for item in candidates:
        if item.get("locator_type") in ACCEPTED:
            if item.get("publication_title_present") is True and item.get("stable_page_or_section_anchors_available") is True:
                accepted.append(item.get("candidate_id"))
            else:
                review.append(item.get("candidate_id"))

    if accepted:
        state = "COMPLETE"
        next_task = "Bind accepted locator and citation anchors into the research page, mapping, and source status."
    elif review:
        state = "REVIEW_REQUIRED"
        next_task = "Review candidate publication identity and citation-anchor completeness before binding."
    else:
        state = "BLOCKED"
        next_task = "Wait for a new accepted-type candidate, then rerun this observer."

    result = {
        "schema_version": "judgment-architecture-source-locator-observation.v1",
        "framework": payload.get("framework"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": state,
        "accepted_candidate_ids": accepted,
        "review_required_candidate_ids": review,
        "candidate_count": len(candidates),
        "next_executable_task": next_task,
        "release_condition": payload.get("machine_state", {}).get("release_condition"),
        "duplicate_execution_key": payload.get("machine_state", {}).get("duplicate_execution_key"),
        "authority_boundary": payload.get("authority_boundary", {}),
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"JUDGMENT ARCHITECTURE SOURCE LOCATOR OBSERVER: {state}")
    print(f"observation: {STATUS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
