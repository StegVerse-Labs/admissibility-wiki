#!/usr/bin/env node
import fs from 'node:fs';

const outputPath = 'static/discovery/candidate-relationships.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(outputPath)) {
  fail(`missing candidate relationships: ${outputPath}`);
}

const output = JSON.parse(fs.readFileSync(outputPath, 'utf8'));

if (output.schema !== 'admissibility_wiki_candidate_relationships.v0.1') {
  fail('candidate relationships schema mismatch');
}
if (output.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('candidate relationships repository mismatch');
}
if (!Array.isArray(output.records)) {
  fail('candidate relationships records must be an array');
}

for (const record of output.records) {
  for (const field of [
    'candidate_id',
    'term_a',
    'term_b',
    'relationship_type',
    'confidence',
    'source_origin_a',
    'source_origin_b',
    'evidence_a',
    'evidence_b',
    'review_status',
    'review_notes',
    'created_at',
    'updated_at'
  ]) {
    if (!(field in record)) {
      fail(`candidate relationship missing field: ${field}`);
    }
  }
}

console.log(`OK: preserved ${output.records.length} candidate relationships in ${outputPath}`);
