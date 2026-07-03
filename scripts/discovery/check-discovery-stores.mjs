#!/usr/bin/env node
import fs from 'node:fs';

const stores = [
  ['static/discovery/discovered-terms.json', 'admissibility_wiki_discovered_terms.v0.1', 'required_record_fields', 'status', 'allowed_statuses'],
  ['static/discovery/candidate-relationships.json', 'admissibility_wiki_candidate_relationships.v0.1', 'required_record_fields', 'review_status', 'allowed_review_statuses'],
  ['static/discovery/relationship-decisions.json', 'admissibility_wiki_relationship_decisions.v0.1', 'required_record_fields', 'decision', 'allowed_decisions']
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing file: ${path}`);
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function requireText(path, marker) {
  const text = fs.readFileSync(path, 'utf8');
  if (!text.includes(marker)) fail(`${path} missing ${marker}`);
}

for (const [path, schema, fieldsKey, statusField, allowedKey] of stores) {
  const data = readJson(path);
  if (data.schema !== schema) fail(`${path} bad schema`);
  if (data.repository !== 'StegVerse-Labs/admissibility-wiki') fail(`${path} bad repository`);
  if (!data.authority_boundary) fail(`${path} missing boundary`);
  if (!Array.isArray(data[fieldsKey]) || data[fieldsKey].length === 0) fail(`${path} missing field list`);
  if (!Array.isArray(data[allowedKey]) || data[allowedKey].length === 0) fail(`${path} missing allowed values`);
  if (!Array.isArray(data.records)) fail(`${path} records must be an array`);
  if (!Array.isArray(data.non_claims) || data.non_claims.length === 0) fail(`${path} missing non_claims`);

  for (const record of data.records) {
    for (const field of data[fieldsKey]) {
      if (!(field in record)) fail(`${path} record missing ${field}`);
    }
    if (!data[allowedKey].includes(record[statusField])) fail(`${path} invalid ${statusField}`);
  }
}

requireText('docs/index.md', '[Discovery Index](./discovery/index.md)');
requireText('docs/discovery/index.md', 'static/discovery/discovered-terms.json');
requireText('docs/discovery/index.md', 'static/discovery/candidate-relationships.json');
requireText('docs/discovery/index.md', 'static/discovery/relationship-decisions.json');

console.log(`OK: discovery stores=${stores.length}; checked-in stores validated without registry parity drift`);
