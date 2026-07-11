from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_inference_window_governance import ValidationError, validate_document


FIXTURE = Path("static/examples/inference-window-governance.worked-cases.json")


class InferenceWindowGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_all_canonical_dispositions_validate(self) -> None:
        evaluations = validate_document(copy.deepcopy(self.document))
        dispositions = {item.calculated_disposition for item in evaluations}
        self.assertEqual(dispositions, {"ALLOW", "DENY", "DEFER", "ESCALATE"})

    def test_expired_delegation_cannot_be_relabelled_allow(self) -> None:
        document = copy.deepcopy(self.document)
        case = next(item for item in document["cases"] if item["id"] == "deny.expired-delegation")
        case["expected_disposition"] = "ALLOW"
        with self.assertRaisesRegex(ValidationError, "calculated DENY"):
            validate_document(document)

    def test_stale_material_evidence_forces_defer(self) -> None:
        document = copy.deepcopy(self.document)
        case = next(item for item in document["cases"] if item["id"] == "defer.stale-location-evidence")
        case["expected_disposition"] = "ALLOW"
        with self.assertRaisesRegex(ValidationError, "calculated DEFER"):
            validate_document(document)

    def test_future_evidence_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["cases"][0]["evidence"][0]["observed_at"] = "2026-07-11T20:01:00Z"
        with self.assertRaisesRegex(ValidationError, "observed after commit time"):
            validate_document(document)

    def test_out_of_range_score_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["cases"][0]["consequence"]["harm"] = 1.2
        with self.assertRaisesRegex(ValidationError, "within \[0, 1\]"):
            validate_document(document)

    def test_duplicate_case_id_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["cases"][1]["id"] = document["cases"][0]["id"]
        with self.assertRaisesRegex(ValidationError, "duplicate case id"):
            validate_document(document)


if __name__ == "__main__":
    unittest.main()
