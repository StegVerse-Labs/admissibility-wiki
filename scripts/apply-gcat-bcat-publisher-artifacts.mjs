#!/usr/bin/env node
import fs from 'node:fs';

const ENUMERATION_PATH = process.env.GCAT_BCAT_ENUMERATION_PATH || '.sync-output/gcat-bcat-publisher-artifacts.json';
const INVENTORY_PATH = 'static/formalisms/gcat-bcat-publication-artifacts.v0.1.json';
const REVIEW_STATUS = process.env.GCAT_BCAT_ARTIFACT_REVIEW_STATUS || 'accepted';
const DECISION_RECORD_REF = process.env.GCAT_BCAT_ARTIFACT_DECISION_REF || null;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing file: ${path}`);
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

if (REVIEW_STATUS !== 'accepted') {
  fail('artifact inventory application requires GCAT_BCAT_ARTIFACT_REVIEW_STATUS=accepted');
}

if (!DECISION_RECORD_REF) {
  fail('artifact inventory application requires GCAT_BCAT_ARTIFACT_DECISION_REF');
}

const enumeration = readJson(ENUMERATION_PATH);
const inventory = readJson(INVENTORY_PATH);

if (enumeration.status !== 'ok') {
  fail(`enumeration status must be ok, got ${enumeration.status}`);
}

if (!Array.isArray(enumeration.artifacts)) {
  fail('enumeration artifacts must be an array');
}

inventory.artifact_status = enumeration.artifact_count > 0 ? 'file_inventory_applied' : 'directory_empty_or_no_files_detected';
inventory.last_file_inventory_application = {
  applied_at: new Date().toISOString(),
  decision_record_ref: DECISION_RECORD_REF,
  enumeration_schema: enumeration.schema,
  enumeration_status: enumeration.status,
  artifact_count: enumeration.artifact_count,
  non_claims: [
    'Applying enumeration records file-level Publisher artifacts only.',
    'Applying enumeration does not define, prove, or validate the formalism.',
    'Admissible-Existence remains the canonical formalism source.'
  ]
};

inventory.artifacts = enumeration.artifacts.map((artifact) => ({
  name: artifact.name,
  path: artifact.path,
  url: artifact.url,
  sha: artifact.sha,
  size: artifact.size,
  artifact_role: artifact.artifact_role,
  candidate_slots: artifact.candidate_slots
}));

inventory.candidate_slots = {
  mathematical_candidates: inventory.artifacts.filter((artifact) => artifact.candidate_slots.includes('mathematical_candidates')),
  proof_candidates: inventory.artifacts.filter((artifact) => artifact.candidate_slots.includes('proof_candidates')),
  validation_candidates: inventory.artifacts.filter((artifact) => artifact.candidate_slots.includes('validation_candidates'))
};

fs.writeFileSync(INVENTORY_PATH, `${JSON.stringify(inventory, null, 2)}\n`);
console.log(`applied_gcat_bcat_artifacts=${inventory.artifacts.length}`);
