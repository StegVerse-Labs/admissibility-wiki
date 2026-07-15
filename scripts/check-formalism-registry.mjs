#!/usr/bin/env node
import fs from 'node:fs';

const REGISTRY_PATH = 'static/formalisms/formalism-registry.v0.1.json';
const CLASSIFICATION_PATH = 'static/formalisms/formalism-record-classification.v1.json';

const requiredTopLevel = [
  'schema',
  'repository',
  'authority_boundary',
  'states',
  'required_record_fields',
  'records',
  'next_action'
];

const requiredRecordFields = [
  'formalism_id',
  'name',
  'state',
  'source_authority',
  'wiki_path',
  'purpose',
  'transition_relationship',
  'evidence_posture',
  'validation_posture',
  'non_claims'
];

const requiredClassificationFields = [
  'formalism_id',
  'artifact_class',
  'mirror_posture',
  'proof_posture',
  'validation_posture',
  'publication_posture'
];

const allowedStates = new Set(['intake', 'mirrored', 'crosswalked', 'validated', 'superseded']);
const allowedPublicationPostures = new Set(['COMPLETE_WITH_EXTERNAL_GATES', 'PARTIAL']);

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

for (const path of [REGISTRY_PATH, CLASSIFICATION_PATH]) {
  if (!fs.existsSync(path)) {
    fail(`missing formalism artifact: ${path}`);
  }
}

const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
const classification = JSON.parse(fs.readFileSync(CLASSIFICATION_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in registry)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (registry.schema !== 'admissibility_wiki_formalism_registry.v0.1') {
  fail('unexpected registry schema');
}

if (registry.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (!registry.authority_boundary.includes('does not create source authority')) {
  fail('authority boundary must preserve non-source-authority claim');
}

if (!Array.isArray(registry.records) || registry.records.length < 5) {
  fail('registry must contain at least five formalism records');
}

const ids = new Set();
for (const record of registry.records) {
  for (const field of requiredRecordFields) {
    if (!(field in record)) {
      fail(`record ${record.formalism_id || '<unknown>'} missing field: ${field}`);
    }
  }

  if (ids.has(record.formalism_id)) {
    fail(`duplicate formalism_id: ${record.formalism_id}`);
  }
  ids.add(record.formalism_id);

  if (!allowedStates.has(record.state)) {
    fail(`invalid state for ${record.formalism_id}: ${record.state}`);
  }

  if (!Array.isArray(record.non_claims) || record.non_claims.length === 0) {
    fail(`record ${record.formalism_id} must include non_claims`);
  }

  if (!fs.existsSync(record.wiki_path)) {
    fail(`missing wiki page for ${record.formalism_id}: ${record.wiki_path}`);
  }
}

if (classification.schema !== 'admissibility_wiki_formalism_record_classification.v1') {
  fail('unexpected formalism classification schema');
}
if (classification.repository !== registry.repository) {
  fail('formalism classification repository mismatch');
}
if (classification.registry !== REGISTRY_PATH) {
  fail('formalism classification registry reference mismatch');
}
if (!classification.authority_boundary.includes('does not create source authority')) {
  fail('formalism classification must preserve source-authority boundary');
}
if (!Array.isArray(classification.entries)) {
  fail('formalism classification entries must be an array');
}
if (classification.entries.length !== registry.records.length) {
  fail('formalism classification count must equal registry count');
}

const allowedArtifactClasses = new Set(classification.allowed_artifact_classes || []);
const classificationIds = new Set();
let mirroredCount = 0;
let intakeCount = 0;
let theoremCount = 0;
let infrastructureCount = 0;

for (const entry of classification.entries) {
  for (const field of requiredClassificationFields) {
    if (!(field in entry)) {
      fail(`classification ${entry.formalism_id || '<unknown>'} missing field: ${field}`);
    }
  }
  if (!ids.has(entry.formalism_id)) {
    fail(`classification references unknown formalism: ${entry.formalism_id}`);
  }
  if (classificationIds.has(entry.formalism_id)) {
    fail(`duplicate classification formalism_id: ${entry.formalism_id}`);
  }
  classificationIds.add(entry.formalism_id);
  if (!allowedArtifactClasses.has(entry.artifact_class)) {
    fail(`invalid artifact_class for ${entry.formalism_id}: ${entry.artifact_class}`);
  }
  if (!allowedPublicationPostures.has(entry.publication_posture)) {
    fail(`invalid publication_posture for ${entry.formalism_id}: ${entry.publication_posture}`);
  }
  if (!entry.proof_posture || !entry.validation_posture || !entry.mirror_posture) {
    fail(`classification postures must be non-empty: ${entry.formalism_id}`);
  }

  const record = registry.records.find(item => item.formalism_id === entry.formalism_id);
  if (record.state === 'mirrored') mirroredCount += 1;
  if (record.state === 'intake') intakeCount += 1;
  if (entry.artifact_class === 'theorem_candidate') theoremCount += 1;
  if (['executable_engine', 'validation_infrastructure'].includes(entry.artifact_class)) infrastructureCount += 1;

  if (entry.artifact_class === 'theorem_candidate' && !entry.proof_posture.includes('UNPROVEN')) {
    fail(`theorem candidate must remain explicitly unproven: ${entry.formalism_id}`);
  }
  if (record.state === 'intake' && entry.publication_posture !== 'PARTIAL') {
    fail(`intake record must remain PARTIAL: ${entry.formalism_id}`);
  }
}

for (const id of ids) {
  if (!classificationIds.has(id)) {
    fail(`registry record missing classification: ${id}`);
  }
}

const counts = classification.counts || {};
if (counts.records !== registry.records.length) fail('classification records count is stale');
if (counts.mirrored !== mirroredCount) fail('classification mirrored count is stale');
if (counts.intake !== intakeCount) fail('classification intake count is stale');
if (counts.theorem_candidates !== theoremCount) fail('classification theorem count is stale');
if (counts.executable_or_validation_infrastructure !== infrastructureCount) fail('classification infrastructure count is stale');

console.log(`OK: ${REGISTRY_PATH}`);
console.log(`formalism_records=${registry.records.length}`);
console.log(`formalism_classified=${classification.entries.length}`);
console.log(`formalism_intake=${intakeCount}`);
console.log(`theorem_candidates=${theoremCount}`);
