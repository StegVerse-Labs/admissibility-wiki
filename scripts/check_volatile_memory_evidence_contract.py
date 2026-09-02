#!/usr/bin/env python3
import json, re, sys
from datetime import datetime
from pathlib import Path

HEX64=re.compile(r"^[a-f0-9]{64}$")

def fail(msg):
    raise ValueError(msg)

def parse_time(v):
    try:
        return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception as e:
        fail(f"invalid timestamp: {v}: {e}")

def validate(m):
    required=["schema_version","evidence_id","authorization","target","collector","acquisition","evidence_object","custody","analysis_lineage","authority"]
    for k in required:
        if k not in m: fail(f"missing {k}")
    if m["schema_version"]!="1.0.0": fail("schema_version")
    if len(m["evidence_id"])<8: fail("evidence_id")
    a=m["authorization"]
    if not a.get("authorization_ref") or a.get("scope")!="volatile_memory_acquisition" or not a.get("granted_by"): fail("authorization")
    t=m["target"]
    if not t.get("machine_identity") or not t.get("platform"): fail("target")
    c=m["collector"]
    if not c.get("name") or not c.get("version") or not HEX64.match(c.get("executable_sha256","")) or not isinstance(c.get("parameters"),list): fail("collector")
    ac=m["acquisition"]
    st, et=parse_time(ac.get("started_at","")), parse_time(ac.get("completed_at",""))
    if et < st: fail("completed_at precedes started_at")
    if ac.get("source_memory_bytes",0) < 1 or ac.get("output_bytes",0) < 1 or not ac.get("impact_disclosure"): fail("acquisition")
    eo=m["evidence_object"]
    if not HEX64.match(eo.get("sha256","")): fail("evidence sha256")
    chunks=eo.get("chunks")
    if not isinstance(chunks,list): fail("chunks")
    if eo.get("streamed") and not chunks: fail("streamed acquisition requires chunks")
    if chunks:
        indexes=[]
        for ch in chunks:
            if not isinstance(ch.get("index"),int) or not HEX64.match(ch.get("sha256","")): fail("chunk")
            indexes.append(ch["index"])
        if indexes != list(range(len(indexes))): fail("chunk indexes must be contiguous from zero")
    cu=m["custody"]
    if not cu.get("destination_ref") or not cu.get("receipt_ref"): fail("custody")
    for line in m["analysis_lineage"]:
        if not line.get("tool") or not line.get("version") or not HEX64.match(line.get("tool_sha256","")) or not line.get("finding_ref"): fail("analysis lineage")
        if line.get("source_evidence_id") != m["evidence_id"]: fail("analysis source evidence mismatch")
    au=m["authority"]
    if au.get("effect")!="NONE" or au.get("claims_admissibility") is not False or au.get("claims_court_acceptance") is not False: fail("authority boundary")
    return True

def main(path):
    m=json.loads(Path(path).read_text())
    validate(m)
    print("VOLATILE_MEMORY_EVIDENCE_CONTRACT: PASS")

if __name__=="__main__":
    target=sys.argv[1] if len(sys.argv)>1 else "data/forensics/volatile-memory-reference-manifest.json"
    main(target)
