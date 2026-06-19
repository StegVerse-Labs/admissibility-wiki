#!/usr/bin/env node
import fs from 'node:fs';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';
const OUTPUT_DIR = '.sync-output';
const DRIFT_PATH = `${OUTPUT_DIR}/formalism-source-drift-report.md`;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(MANIFEST_PATH)) {
  fail(`missing manifest: ${MANIFEST_PATH}`);
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const driftRecords = [];

for (const source of manifest.sources) {
  const sourceRef = source.current_source_ref || null;
  const publisherRef = source.current_publisher_ref || null;
  const lastSourceRef = source.last_known_source_ref || null;
  const lastPublisherRef = source.last_known_publisher_ref || null;

  const sourceChanged = sourceRef !== null && sourceRef !== lastSourceRef;
  const publisherChanged = publisherRef !== null && publisherRef !== lastPublisherRef;

  if (sourceChanged || publisherChanged) {
    driftRecords.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      wiki_target_path: source.wiki_target_path,
      sourceChanged,
      publisherChanged,
      lastSourceRef,
      sourceRef,
      lastPublisherRef,
      publisherRef
    });
  }
}

const lines = [];
lines.push('# Formalism Source Drift Report');
lines.push('');
lines.push('Authority boundary: Admissible-Existence defines formalisms; Publisher publishes; Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.');
lines.push('');

if (driftRecords.length === 0) {
  lines.push('No source drift detected from manifest-declared current refs.');
} else {
  lines.push(`Detected ${driftRecords.length} source drift record(s).`);
  lines.push('');
  for (const record of driftRecords) {
    lines.push(`## ${record.formalism_term}`);
    lines.push('');
    lines.push(`- Source ID: \`${record.source_id}\``);
    lines.push(`- Canonical source: \`${record.canonical_source_repository}\``);
    lines.push(`- Wiki target: \`${record.wiki_target_path}\``);
    lines.push(`- Source ref changed: \`${record.sourceChanged}\``);
    lines.push(`- Last source ref: \`${record.lastSourceRef || 'none'}\``);
    lines.push(`- Current source ref: \`${record.sourceRef || 'none'}\``);
    lines.push(`- Publisher ref changed: \`${record.publisherChanged}\``);
    lines.push(`- Last publisher ref: \`${record.lastPublisherRef || 'none'}\``);
    lines.push(`- Current publisher ref: \`${record.publisherRef || 'none'}\``);
    lines.push('');
  }
}

fs.writeFileSync(DRIFT_PATH, `${lines.join('\n')}\n`);
console.log(`formalism_source_drift_records=${driftRecords.length}`);
