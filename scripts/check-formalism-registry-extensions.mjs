#!/usr/bin/env node
import fs from 'node:fs';

const EXTENSIONS = [
  'static/formalisms/boundary-conditions-registry-extension.v0.1.json'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

for (const path of EXTENSIONS) {
  if (!fs.existsSync(path)) fail(`missing extension: ${path}`);
  const record = JSON.parse(fs.readFileSync(path, 'utf8'));
  for (const field of [
    'schema',
    'formalism_id',
    'name',
    'state',
    'source_authority',
    'source_visibility',
    'wiki_path',
    'purpose',
    'transition_relationship',
    'evidence_posture',
    'validation_posture',
    'non_claims'
  ]) {
    if (!(field in record)) fail(`${path} missing ${field}`);
  }
  if (record.schema !== 'admissibility_wiki_formalism_registry_extension.v0.1') fail(`${path} bad schema`);
  if (!record.source_authority.startsWith('Admissible-Existence/')) fail(`${path} bad source authority`);
  if (!record.wiki_path.startsWith('docs/formalisms/')) fail(`${path} bad wiki path`);
  if (!Array.isArray(record.non_claims) || record.non_claims.length === 0) fail(`${path} non_claims required`);
}

console.log(`OK: formalism registry extensions=${EXTENSIONS.length}`);
