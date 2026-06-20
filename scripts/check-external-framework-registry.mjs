#!/usr/bin/env node
import fs from 'node:fs';

const REGISTRY_PATH = 'static/external-frameworks/external-framework-registry.v0.1.json';
const requiredTopLevel = [
  'schema',
  'repository',
  'authority_boundary',
  'allowed_relationships',
  'required_record_fields',
  'records',
  'next_action'
];
const requiredRecordFields = [
  'framework_id',
  'name',
  'status',
  'external_role',
  'wiki_path',
  'primary_relationship',
  'crosswalk_targets',
  'non_claims'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(REGISTRY_PATH)) fail(`missing registry: ${REGISTRY_PATH}`);
const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in registry)) fail(`missing top-level field: ${field}`);
}

if (registry.schema !== 'admissibility_wiki_external_framework_registry.v0.1') fail('unexpected registry schema');
if (registry.repository !== 'StegVerse-Labs/admissibility-wiki') fail('unexpected repository');
if (!registry.authority_boundary.includes('They do not become canonical Admissible-Existence formalism sources')) {
  fail('authority boundary must preserve AE canonical-source separation');
}

const allowedRelationships = new Set(registry.allowed_relationships);
const ids = new Set();

for (const record of registry.records) {
  for (const field of requiredRecordFields) {
    if (!(field in record)) fail(`record ${record.framework_id || '<unknown>'} missing field: ${field}`);
  }
  if (ids.has(record.framework_id)) fail(`duplicate framework_id: ${record.framework_id}`);
  ids.add(record.framework_id);
  if (!record.wiki_path.startsWith('docs/')) fail(`wiki_path must be under docs/: ${record.framework_id}`);
  if (!allowedRelationships.has(record.primary_relationship)) fail(`invalid primary relationship: ${record.framework_id}`);
  if (!Array.isArray(record.crosswalk_targets) || record.crosswalk_targets.length === 0) fail(`crosswalk_targets required: ${record.framework_id}`);
  if (!Array.isArray(record.non_claims) || record.non_claims.length === 0) fail(`non_claims required: ${record.framework_id}`);
}

console.log(`OK: ${REGISTRY_PATH}`);
console.log(`external_framework_records=${registry.records.length}`);
