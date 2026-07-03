#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';

const registryPath = 'static/formalisms/formalism-registry.v0.1.json';
const outputPath = 'static/discovery/discovered-terms.json';
const shouldRefresh = process.env.DISCOVERY_REFRESH === '1';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function normalizeTerm(term) {
  return term
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

function makeId(input) {
  return `term_${crypto.createHash('sha256').update(input).digest('hex').slice(0, 16)}`;
}

function extractTitle(markdown, fallback) {
  const match = markdown.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : fallback;
}

function validateExistingStore() {
  if (!fs.existsSync(outputPath)) return false;
  const output = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
  if (output.schema !== 'admissibility_wiki_discovered_terms.v0.1') fail('discovered terms schema mismatch');
  if (output.repository !== 'StegVerse-Labs/admissibility-wiki') fail('discovered terms repository mismatch');
  if (!Array.isArray(output.records)) fail('discovered terms records must be an array');
  for (const record of output.records) {
    for (const field of ['term_id', 'term', 'normalized_term', 'source_origin', 'source_path', 'evidence_ref', 'formalism_id', 'status', 'created_at', 'updated_at']) {
      if (!(field in record)) fail(`discovered term missing field: ${field}`);
    }
  }
  console.log(`OK: preserved ${output.records.length} discovered terms in ${outputPath}`);
  return true;
}

if (!shouldRefresh && validateExistingStore()) {
  process.exit(0);
}

if (!fs.existsSync(registryPath)) fail(`missing registry: ${registryPath}`);

const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const now = new Date(0).toISOString();
const records = [];

for (const formalism of registry.records.filter((record) => record.state === 'mirrored')) {
  if (!formalism.wiki_path || !fs.existsSync(formalism.wiki_path)) {
    fail(`missing wiki page for ${formalism.formalism_id}: ${formalism.wiki_path}`);
  }

  const markdown = fs.readFileSync(formalism.wiki_path, 'utf8');
  const title = extractTitle(markdown, formalism.name);
  const normalized = normalizeTerm(title);
  const idSeed = `${formalism.formalism_id}:${formalism.wiki_path}:${normalized}`;

  records.push({
    term_id: makeId(idSeed),
    term: title,
    normalized_term: normalized,
    source_origin: formalism.source_authority,
    source_path: formalism.wiki_path,
    evidence_ref: `${formalism.wiki_path}#definition`,
    formalism_id: formalism.formalism_id,
    status: 'indexed',
    created_at: now,
    updated_at: now
  });
}

const output = {
  schema: 'admissibility_wiki_discovered_terms.v0.1',
  repository: 'StegVerse-Labs/admissibility-wiki',
  authority_boundary: 'This file stores discovered term records and their formal origins. It does not define terms, assert equivalence, prove claims, validate claims, or replace source authority.',
  required_record_fields: [
    'term_id',
    'term',
    'normalized_term',
    'source_origin',
    'source_path',
    'evidence_ref',
    'formalism_id',
    'status',
    'created_at',
    'updated_at'
  ],
  allowed_statuses: [
    'observed',
    'indexed',
    'superseded',
    'rejected'
  ],
  records,
  non_claims: [
    'A discovered term is not a canonical definition.',
    'A discovered term is not a synonym decision.',
    'A discovered term is not a proof or validation result.',
    'A discovered term must preserve its source origin.'
  ]
};

fs.writeFileSync(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(`OK: wrote ${records.length} discovered terms to ${outputPath}`);
