#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "scripts/adapt_judgment_architecture_commitment_to_binding.py"
CASES_PATH = ROOT / "tests/fixtures/judgment-architecture-binding-adapter-cases.json"
STATUS_PATH = ROOT / "static/status/judgment-architecture-binding-adapter-status.json"


def load_adapter():
    spec = importlib.util.spec_from_file_location("judgment_architecture_binding_adapter", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load adapter module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    for path in [ADAPTER_PATH, CASES_PATH]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("JUDGMENT ARCHITECTURE BINDING ADAPTER: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    adapter = load_adapter()
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    boundary = payload.get("authority_boundary", {})
    for key in [
        "adapter_is_execution_authority",
        "commitment_record_is_binding_evidence",
        "human_commitment_is_admissibility",
        "fixture_result_is_runtime_authorization",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"authority boundary must be false: {key}")

    results: list[dict[str, Any]] = []
    for case in payload.get("cases", []):
        case_id = case.get("case_id")
        expected = case.get("expected_binding_result")
        adapted = adapter.adapt(case.get("input", {}))
        actual = adapted.get("binding_result")
        reasons = adapted.get("reason_codes", [])
        expected_reason = case.get("expected_reason")
        passed = actual == expected and (expected_reason is None or expected_reason in reasons)
        if not passed:
            failures.append(
                f"{case_id}: expected {expected}"
                + (f" with {expected_reason}" if expected_reason else "")
                + f", got {actual} reasons={reasons}"
            )

        commitment = case.get("input", {}).get("commitment_record", {})
        live_evidence = case.get("input", {}).get("live_evidence", {})
        if adapted.get("candidate_hash") != adapter.canonical_hash(commitment):
            failures.append(f"{case_id}: candidate hash not derived from commitment record")
        if adapted.get("state_before_hash") != adapter.canonical_hash(live_evidence.get("state_before", {"missing": True})):
            failures.append(f"{case_id}: state-before hash mismatch")
        if adapted.get("state_after_hash") != adapter.canonical_hash(live_evidence.get("state_after", {"missing": True})):
            failures.append(f"{case_id}: state-after hash mismatch")
        if actual != "BIND" and adapted.get("committed_at") is not None:
            failures.append(f"{case_id}: non-BIND result must not carry committed_at")
        if actual == "BIND" and not adapted.get("committed_at"):
            failures.append(f"{case_id}: BIND result must carry committed_at")
        if not isinstance(adapted.get("receipt_hash"), str) or not adapted["receipt_hash"].startswith("sha256:"):
            failures.append(f"{case_id}: receipt hash missing")

        results.append({
            "case_id": case_id,
            "expected_binding_result": expected,
            "actual_binding_result": actual,
            "reason_codes": reasons,
            "candidate_hash": adapted.get("candidate_hash"),
            "state_before_hash": adapted.get("state_before_hash"),
            "state_after_hash": adapted.get("state_after_hash"),
            "receipt_hash": adapted.get("receipt_hash"),
            "passed": passed,
        })

    status = {
        "artifact_type": "judgment_architecture_binding_adapter_status",
        "schema_version": "0.1",
        "overall_status": "FAIL" if failures else "PASS",
        "adapter_state": "DETERMINISTIC_NON_AUTHORIZING_ADAPTER_INSTALLED",
        "mapping_state": "fixture_ready",
        "runtime_observation_state": "DETERMINISTIC_LOCAL_ADAPTER_ONLY",
        "results": results,
        "authority_boundary": {
            "adapter_is_execution_authority": False,
            "adapter_bind_result_is_runtime_authorization": False,
            "commitment_record_is_current_standing_proof": False,
            "human_commitment_is_admissibility": False,
            "interoperability_is_verified": False,
        },
        "next_required_action": "observe canonical workflow execution, bind generated receipt to workflow evidence, then add stable public source citations before replay-ready consideration",
    }
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    print("JUDGMENT ARCHITECTURE BINDING ADAPTER:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
