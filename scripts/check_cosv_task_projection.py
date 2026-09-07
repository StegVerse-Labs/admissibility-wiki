#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
idx = json.loads((ROOT / "data/cosv/task-vector-index.json").read_text())
state = json.loads((ROOT / "data/admissibility-wiki-orchestration-state.json").read_text())
registry = json.loads((ROOT / "static/status/wiki-public-anchor-internal-task-registry.json").read_text())

rows = {row["task_id"]: row for row in idx["tasks"]}
machine_tasks = {x["task_id"]: x for x in state["machine_owned_dependency_workloads"]}
registry_tasks = {x["task_id"]: x for x in registry["tasks"]}

assert idx["profile"] == "task.v1" and idx["width"] == 14 and idx["authority_effect"] == "NONE"

hil = rows["ADMISSIBILITY-HIL-001"]
hil_rec = json.loads((ROOT / hil["vector_ref"]).read_text())
hil_m = hil_rec["exact_metrics"]
assert hil["binding_mode"] == "EXTERNAL_PROJECTION_READ_ONLY"
assert hil_rec["vector"] == hil["vector"] == "60000000107000"
assert hil_m["lifecycle"] == "BLOCKED"
assert hil_m["blocker_count"] == len(machine_tasks["ADMISSIBILITY-HIL-001"]["required_upstream_evidence"]) == 7
assert hil_m["canonical_owner_installed"] is True
assert hil_m["evidence_complete"] is False
assert hil_m["activated"] is False and hil_m["propagated"] is False
assert hil_rec["authority_effect"] == "NONE"

pa = rows["PA-INT-009"]
pa_rec = json.loads((ROOT / pa["vector_ref"]).read_text())
pa_m = pa_rec["exact_metrics"]
pa_task = registry_tasks["PA-INT-009"]
assert pa["binding_mode"] == "CANONICAL_INTERNAL_TASK_POINTER"
assert pa_rec["identity"] == "StegVerse-Labs/admissibility-wiki:task:PA-INT-009"
assert pa_rec["vector"] == pa["vector"] == pa_task["cosv_task_vector"] == "50000000100000"
assert pa_task["cosv_profile"] == pa_rec["profile"] == "task.v1"
assert pa_task["cosv_task_vector_ref"] == pa["vector_ref"] == "data/cosv/task-vectors/PA-INT-009.json"
assert pa_task["state"] == "ACTIVE_INTERNAL"
assert pa_m["lifecycle"] == "MACHINE_OWNED"
assert pa_m["archive_ready"] is False
assert pa_m["unassigned_work"] == 0
assert pa_m["canonical_owner_installed"] is True
assert pa_m["thread_required"] is False
assert pa_m["blocker_count"] == 0
assert pa_m["evidence_complete"] is False
assert pa_m["activated"] is False and pa_m["propagated"] is False
assert pa_rec["authority_effect"] == "NONE"

assert state["authority"]["admissibility"] is False
assert idx["coverage"]["machine_owned_dependency_gap"] == 0
assert idx["coverage"]["public_anchor_internal_executor_tasks_projected"] == 1
assert idx["coverage"]["public_anchor_internal_executor_gap"] == 0
assert idx["coverage"]["framework_worker_backlog_projected"] is False
assert idx["coverage"]["repository_vector_present_claimed"] is False

print("ADMISSIBILITY_COSV_PROJECTION_PASS hil=60000000107000 pa_int_009=50000000100000 repository_vector_present=false")
