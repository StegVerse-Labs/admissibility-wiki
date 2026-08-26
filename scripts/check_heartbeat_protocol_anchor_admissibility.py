#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'data'/'heartbeat-protocol-anchor-admissibility.json'
def main():
 d=json.loads(STATE.read_text())
 expected={'state':'COMPLETE_SOURCE_AUDIT','anchor_epoch':32,'anchor_time_utc':'2026-08-23T19:00:00.000Z','period_ms':10,'reference_rate_hz':100,'progression_dependency':'OSCILLATOR_ONLY','continuous_reference_stream':True,'new_reference_every_10ms':True,'continuous_process_required':False,'resident_sampler_required_for_progression':False,'observation_is_causal':False,'live_009_state':'COMPLETED','live_009_transition':'INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED','heartbeat_existence_is_admissibility':False,'heartbeat_freshness_is_authorization':False,'workflow_tick_is_protocol_epoch':False,'heartbeat_grants_execution_authority':False,'heartbeat_grants_publication_authority':False,'authority_effect':'NONE','credential_authority':'TV/TVC','repository_release_posture_changed':False}
 bad=[k for k,v in expected.items() if d.get(k)!=v]
 if bad:
  print('ADMISSIBILITY_HB32_FAIL:'+','.join(bad)); return 1
 print('ADMISSIBILITY_HB32_PASS continuous_10ms=true heartbeat_is_authority_neutral=true'); return 0
if __name__=='__main__': raise SystemExit(main())
