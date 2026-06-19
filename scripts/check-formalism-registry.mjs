#!/usr/bin/env node
import fs from 'node:fs';

const REGISTRY_PATH = 'static/formalisms/formalism-registry.v0.1.json';

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

const allowedStates = new Set(['intake', 'mirrored', 'crosswalked', 'validated', 'superseded']);

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(REGISTRY_PATH)) {
  fail(`missing registry: ${REGISTRY_PATH}`);
}

const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));

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
}

console.log(`OK: ${REGISTRY_PATH}`);
console.log(`formalism_records=${registry.records.length}`);
