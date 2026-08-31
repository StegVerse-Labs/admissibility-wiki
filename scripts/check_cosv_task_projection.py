#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
state=json.loads((ROOT/"data/admissibility-wiki-orchestration-state.json").read_text())
tasks={x["task_id"]:x for x in state["machine_owned_dependency_workloads"]}
row=idx["tasks"][0]
rec=json.loads((ROOT/row["vector_ref"]).read_text())
m=rec["exact_metrics"]
assert idx["profile"]=="task.v1" and idx["width"]==14 and idx["authority_effect"]=="NONE"
assert row["task_id"]=="ADMISSIBILITY-HIL-001"
assert row["binding_mode"]=="EXTERNAL_PROJECTION_READ_ONLY"
assert rec["vector"]==row["vector"]=="60000000107000"
assert m["lifecycle"]=="BLOCKED"
assert m["blocker_count"]==len(tasks["ADMISSIBILITY-HIL-001"]["required_upstream_evidence"])==7
assert m["canonical_owner_installed"] is True
assert m["evidence_complete"] is False
assert m["activated"] is False and m["propagated"] is False
assert rec["authority_effect"]=="NONE"
assert state["authority"]["admissibility"] is False
assert idx["coverage"]["framework_worker_backlog_projected"] is False
assert idx["coverage"]["repository_vector_present_claimed"] is False
print("ADMISSIBILITY_COSV_PROJECTION_PASS blockers=7 repository_vector_present=false")
