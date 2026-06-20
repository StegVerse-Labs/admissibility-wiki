#!/usr/bin/env node
import fs from 'node:fs';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';
const FETCHED_REFS_PATH = '.sync-output/public-formalism-source-refs.json';
const DECISION_RECORD_REF = process.env.SYNC_DECISION_RECORD_REF || null;
const REVIEW_STATUS = process.env.SYNC_REVIEW_STATUS || 'accepted';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing file: ${path}`);
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

if (REVIEW_STATUS !== 'accepted') {
  fail('baseline refresh requires SYNC_REVIEW_STATUS=accepted');
}

if (!DECISION_RECORD_REF) {
  fail('baseline refresh requires SYNC_DECISION_RECORD_REF');
}

const manifest = readJson(MANIFEST_PATH);
const fetchedRefs = readJson(FETCHED_REFS_PATH);
const fetchedBySourceId = new Map();

for (const record of fetchedRefs.records || []) {
  fetchedBySourceId.set(record.source_id, record);
}

let updateCount = 0;

manifest.last_baseline_refresh = {
  refreshed_at: new Date().toISOString(),
  decision_record_ref: DECISION_RECORD_REF,
  review_status: REVIEW_STATUS,
  non_claims: [
    'Baseline refresh records accepted wiki sync state only.',
    'Baseline refresh does not define or validate a formalism.',
    'Admissible-Existence remains the canonical formalism source.'
  ]
};

for (const source of manifest.sources) {
  const fetched = fetchedBySourceId.get(source.source_id);
  if (!fetched || fetched.fetch_status !== 'ok' || !fetched.current_source_ref) {
    continue;
  }

  if (source.last_known_source_ref !== fetched.current_source_ref) {
    source.last_known_source_ref = fetched.current_source_ref;
    source.sync_state = 'wiki_update_applied';
    source.last_sync_decision_record_ref = DECISION_RECORD_REF;
    source.last_sync_refreshed_at = manifest.last_baseline_refresh.refreshed_at;
    updateCount += 1;
  }
}

fs.writeFileSync(MANIFEST_PATH, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`formalism_sync_baseline_updates=${updateCount}`);
