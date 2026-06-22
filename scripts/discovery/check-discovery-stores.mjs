#!/usr/bin/env node
import fs from 'node:fs';

const files = [
  {
    path: 'static/discovery/discovered-terms.json',
    schema: 'admissibility_wiki_discovered_terms.v0.1',
    recordFieldsKey: 'required_record_fields',
    statusField: 'status',
    allowedKey: 'allowed_statuses'
  },
  {
    path: 'static/discovery/candidate-relationships.json',
    schema: 'admissibility_wiki_candidate_relationships.v0.1',
    recordFieldsKey: 'required_record_fields',
    statusField: 'review_status',
    allowedKey: 'allowed_review_statuses'
  }
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

for (const file of files) {
  if (!fs.existsSync(file.path)) fail(`missing file: ${file.path}`);
  const data = JSON.parse(fs.readFileSync(file.path, 'utf8'));

  if (data.schema !== file.schema) fail(`${file.path} bad schema`);
  if (!data.authority_boundary) fail(`${file.path} missing authority_boundary`);
  if (!Array.isArray(data[file.recordFieldsKey]) || data[file.recordFieldsKey].length === 0) fail(`${file.path} missing required fields`);
  if (!Array.isArray(data.records)) fail(`${file.path} records must be an array`);
  if (!Array.isArray(data.non_claims) || data.non_claims.length === 0) fail(`${file.path} non_claims required`);

  for (const record of data.records) {
    for (const field of data[file.recordFieldsKey]) {
      if (!(field in record)) fail(`${file.path} record missing ${field}`);
    }
    if (!data[file.allowedKey].includes(record[file.statusField])) {
      fail(`${file.path} invalid ${file.statusField}: ${record[file.statusField]}`);
    }
  }
}

console.log(`OK: discovery stores=${files.length}`);
