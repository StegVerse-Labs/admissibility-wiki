#!/usr/bin/env node
import fs from 'node:fs';

const registryPath = 'static/formalisms/formalism-registry.v0.1.json';

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
  },
  {
    path: 'static/discovery/relationship-decisions.json',
    schema: 'admissibility_wiki_relationship_decisions.v0.1',
    recordFieldsKey: 'required_record_fields',
    statusField: 'decision',
    allowedKey: 'allowed_decisions',
    relationshipTypeKey: 'allowed_relationship_types'
  }
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing file: ${path}`);
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function validateStore(file, data) {
  if (data.schema !== file.schema) fail(`${file.path} bad schema`);
  if (!data.authority_boundary) fail(`${file.path} missing authority_boundary`);
  if (!Array.isArray(data[file.recordFieldsKey]) || data[file.recordFieldsKey].length === 0) fail(`${file.path} missing required fields`);
  if (!Array.isArray(data.records)) fail(`${file.path} records must be an array`);
  if (!Array.isArray(data.non_claims) || data.non_claims.length === 0) fail(`${file.path} non_claims required`);
  if (!Array.isArray(data[file.allowedKey]) || data[file.allowedKey].length === 0) fail(`${file.path} missing allowed status values`);

  for (const record of data.records) {
    for (const field of data[file.recordFieldsKey]) {
      if (!(field in record)) fail(`${file.path} record missing ${field}`);
    }
    if (!data[file.allowedKey].includes(record[file.statusField])) {
      fail(`${file.path} invalid ${file.statusField}: ${record[file.statusField]}`);
    }
    if (file.relationshipTypeKey && !data[file.relationshipTypeKey].includes(record.relationship_type)) {
      fail(`${file.path} invalid relationship_type: ${record.relationship_type}`);
    }
    if (file.relationshipTypeKey) {
      for (const field of ['source_origin_a', 'source_origin_b', 'evidence_a', 'evidence_b', 'decision_basis']) {
        if (!record[field]) fail(`${file.path} decision record missing ${field}`);
      }
    }
  }
}

function validateGeneratedCoverage(stores) {
  const registry = readJson(registryPath);
  const mirrored = registry.records.filter((record) => record.state === 'mirrored');
  const terms = stores.get('static/discovery/discovered-terms.json').records;
  const candidates = stores.get('static/discovery/candidate-relationships.json').records;

  for (const formalism of mirrored) {
    const matchingTerms = terms.filter((term) => term.formalism_id === formalism.formalism_id);
    if (matchingTerms.length !== 1) fail(`expected exactly one discovered term for ${formalism.formalism_id}`);

    const term = matchingTerms[0];
    if (term.term !== formalism.name) fail(`term name mismatch for ${formalism.formalism_id}`);
    if (term.source_origin !== formalism.source_authority) fail(`source origin mismatch for ${formalism.formalism_id}`);
    if (term.source_path !== formalism.wiki_path) fail(`source path mismatch for ${formalism.formalism_id}`);
    if (term.evidence_ref !== `${formalism.wiki_path}#definition`) fail(`evidence ref mismatch for ${formalism.formalism_id}`);
    if (term.status !== 'indexed') fail(`term is not indexed for ${formalism.formalism_id}`);
  }

  for (const candidate of candidates) {
    if (candidate.review_status !== 'review_required') fail(`candidate is not review_required: ${candidate.candidate_id}`);
    if (!candidate.source_origin_a || !candidate.source_origin_b) fail(`candidate missing source origin: ${candidate.candidate_id}`);
    if (!candidate.evidence_a || !candidate.evidence_b) fail(`candidate missing evidence: ${candidate.candidate_id}`);
    if (!candidate.review_notes.includes('No equivalence')) fail(`candidate missing non-promotion note: ${candidate.candidate_id}`);
  }
}

const stores = new Map();

for (const file of files) {
  const data = readJson(file.path);
  validateStore(file, data);
  stores.set(file.path, data);
}

validateGeneratedCoverage(stores);

console.log(`OK: discovery stores=${files.length}; generated coverage checked`);
