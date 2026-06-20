#!/usr/bin/env node
import fs from 'node:fs';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';
const DRIFT_REPORT_PATH = '.sync-output/formalism-source-drift-report.json';
const OUTPUT_PATH = '.sync-output/formalism-source-sync-issue.md';
const ACTIONABLE_STATES = new Set(['source_changed', 'wiki_update_required']);

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
const driftReport = readJsonIfPresent(DRIFT_REPORT_PATH);
const actionableBySourceId = new Map();

for (const source of manifest.sources.filter((item) => ACTIONABLE_STATES.has(item.sync_state))) {
  actionableBySourceId.set(source.source_id, {
    source,
    reason: `manifest sync_state is ${source.sync_state}`,
    drift: null
  });
}

for (const drift of driftReport?.drift_records || []) {
  const source = manifest.sources.find((item) => item.source_id === drift.source_id);
  if (!source) {
    continue;
  }
  actionableBySourceId.set(source.source_id, {
    source,
    reason: 'fetched or declared source ref drift detected',
    drift
  });
}

const actionable = [...actionableBySourceId.values()];
fs.mkdirSync('.sync-output', { recursive: true });

if (actionable.length === 0) {
  fs.writeFileSync(OUTPUT_PATH, 'NO_SYNC_ISSUE_REQUIRED\n');
  console.log('NO_SYNC_ISSUE_REQUIRED');
  process.exit(0);
}

const lines = [];
lines.push('# Formalism source sync update required');
lines.push('');
lines.push('The formalism source sync workflow detected records that require wiki update review.');
lines.push('');
lines.push('Authority boundary:');
lines.push('');
lines.push('- Admissible-Existence defines formalisms.');
lines.push('- Publisher publishes papers and public exposition.');
lines.push('- Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.');
lines.push('');
lines.push('Actionable records:');
lines.push('');

for (const { source, reason, drift } of actionable) {
  lines.push(`## ${source.formalism_term}`);
  lines.push('');
  lines.push(`- Source ID: \`${source.source_id}\``);
  lines.push(`- Canonical source: \`${source.canonical_source_repository}\``);
  lines.push(`- Source visibility: \`${source.canonical_source_visibility}\``);
  lines.push(`- Publisher artifact: \`${source.publisher_artifact_path || 'none recorded'}\``);
  lines.push(`- Wiki target: \`${source.wiki_target_path}\``);
  lines.push(`- Sync state: \`${source.sync_state}\``);
  lines.push(`- Reason: ${reason}`);
  if (drift) {
    lines.push(`- Last source ref: \`${drift.last_source_ref || 'none'}\``);
    lines.push(`- Current source ref: \`${drift.current_source_ref || 'none'}\``);
    lines.push(`- Last publisher ref: \`${drift.last_publisher_ref || 'none'}\``);
    lines.push(`- Current publisher ref: \`${drift.current_publisher_ref || 'none'}\``);
  }
  lines.push(`- Change rule: ${source.change_detection_rule}`);
  lines.push(`- Wiki update rule: ${source.wiki_update_rule}`);
  lines.push('');
  lines.push('Non-claims:');
  for (const claim of source.non_claims) {
    lines.push(`- ${claim}`);
  }
  lines.push('');
}

lines.push('Next action: create or update public-safe wiki crosswalk content, then record a sync receipt.');
lines.push('');

fs.writeFileSync(OUTPUT_PATH, `${lines.join('\n')}\n`);
console.log(`SYNC_ISSUE_REQUIRED count=${actionable.length}`);
