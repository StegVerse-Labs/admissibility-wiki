#!/usr/bin/env node
import fs from 'node:fs';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';
const FETCHED_REFS_PATH = '.sync-output/public-formalism-source-refs.json';
const OUTPUT_DIR = '.sync-output';
const DRIFT_PATH = `${OUTPUT_DIR}/formalism-source-drift-report.md`;
const DRIFT_JSON_PATH = `${OUTPUT_DIR}/formalism-source-drift-report.json`;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJsonIfPresent(path) {
  if (!fs.existsSync(path)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

if (!fs.existsSync(MANIFEST_PATH)) {
  fail(`missing manifest: ${MANIFEST_PATH}`);
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
const fetchedRefs = readJsonIfPresent(FETCHED_REFS_PATH);
const fetchedRefBySourceId = new Map();

if (fetchedRefs?.records) {
  for (const record of fetchedRefs.records) {
    fetchedRefBySourceId.set(record.source_id, record);
  }
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const driftRecords = [];

for (const source of manifest.sources) {
  const fetched = fetchedRefBySourceId.get(source.source_id);
  const sourceRef = fetched?.current_source_ref || source.current_source_ref || null;
  const publisherRef = source.current_publisher_ref || null;
  const lastSourceRef = source.last_known_source_ref || null;
  const lastPublisherRef = source.last_known_publisher_ref || null;
  const fetchStatus = fetched?.fetch_status || 'not_fetched';

  const sourceChanged = sourceRef !== null && sourceRef !== lastSourceRef;
  const publisherChanged = publisherRef !== null && publisherRef !== lastPublisherRef;

  if (sourceChanged || publisherChanged) {
    driftRecords.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      canonical_source_visibility: source.canonical_source_visibility,
      wiki_target_path: source.wiki_target_path,
      fetch_status: fetchStatus,
      source_changed: sourceChanged,
      publisher_changed: publisherChanged,
      last_source_ref: lastSourceRef,
      current_source_ref: sourceRef,
      last_publisher_ref: lastPublisherRef,
      current_publisher_ref: publisherRef,
      recommended_sync_state: 'wiki_update_required'
    });
  }
}

const report = {
  schema: 'admissibility_wiki_formalism_source_drift_report.v0.1',
  authority_boundary: manifest.authority_boundary,
  drift_count: driftRecords.length,
  drift_records: driftRecords
};
fs.writeFileSync(DRIFT_JSON_PATH, `${JSON.stringify(report, null, 2)}\n`);

const lines = [];
lines.push('# Formalism Source Drift Report');
lines.push('');
lines.push('Authority boundary: Admissible-Existence defines formalisms; Publisher publishes; Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.');
lines.push('');

if (driftRecords.length === 0) {
  lines.push('No source drift detected from fetched public refs or manifest-declared current refs.');
} else {
  lines.push(`Detected ${driftRecords.length} source drift record(s).`);
  lines.push('');
  for (const record of driftRecords) {
    lines.push(`## ${record.formalism_term}`);
    lines.push('');
    lines.push(`- Source ID: \`${record.source_id}\``);
    lines.push(`- Canonical source: \`${record.canonical_source_repository}\``);
    lines.push(`- Source visibility: \`${record.canonical_source_visibility}\``);
    lines.push(`- Wiki target: \`${record.wiki_target_path}\``);
    lines.push(`- Fetch status: \`${record.fetch_status}\``);
    lines.push(`- Source ref changed: \`${record.source_changed}\``);
    lines.push(`- Last source ref: \`${record.last_source_ref || 'none'}\``);
    lines.push(`- Current source ref: \`${record.current_source_ref || 'none'}\``);
    lines.push(`- Publisher ref changed: \`${record.publisher_changed}\``);
    lines.push(`- Last publisher ref: \`${record.last_publisher_ref || 'none'}\``);
    lines.push(`- Current publisher ref: \`${record.current_publisher_ref || 'none'}\``);
    lines.push(`- Recommended sync state: \`${record.recommended_sync_state}\``);
    lines.push('');
  }
}

fs.writeFileSync(DRIFT_PATH, `${lines.join('\n')}\n`);
console.log(`formalism_source_drift_records=${driftRecords.length}`);
