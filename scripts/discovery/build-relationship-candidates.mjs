#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';

const termsPath = 'static/discovery/discovered-terms.json';
const outputPath = 'static/discovery/candidate-relationships.json';

const KEY_GROUPS = [
  ['transition', 'runtime', 'learning'],
  ['continuity', 'handoff', 'data', 'decision', 'state'],
  ['boundary', 'governance', 'admissibility'],
  ['validation', 'testing', 'factory', 'engine']
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function makeId(input) {
  return `candidate_${crypto.createHash('sha256').update(input).digest('hex').slice(0, 16)}`;
}

function tokens(term) {
  return new Set(term.normalized_term.split('_').filter(Boolean));
}

function sharedTokenCount(a, b) {
  const at = tokens(a);
  const bt = tokens(b);
  let count = 0;
  for (const token of at) if (bt.has(token)) count += 1;
  return count;
}

function groupOverlap(a, b) {
  const at = tokens(a);
  const bt = tokens(b);
  return KEY_GROUPS.some((group) => group.some((token) => at.has(token)) && group.some((token) => bt.has(token)));
}

function classify(a, b) {
  const shared = sharedTokenCount(a, b);
  if (shared >= 2) return 'near_equivalent_candidate';
  if (groupOverlap(a, b)) return 'adjacent_candidate';
  return null;
}

if (!fs.existsSync(termsPath)) fail(`missing discovered terms: ${termsPath}`);
const terms = JSON.parse(fs.readFileSync(termsPath, 'utf8'));

if (!Array.isArray(terms.records)) fail('discovered terms records must be an array');

const records = [];
const now = new Date(0).toISOString();

for (let i = 0; i < terms.records.length; i += 1) {
  for (let j = i + 1; j < terms.records.length; j += 1) {
    const a = terms.records[i];
    const b = terms.records[j];
    const relationship = classify(a, b);
    if (!relationship) continue;

    const shared = sharedTokenCount(a, b);
    const confidence = relationship === 'near_equivalent_candidate'
      ? Math.min(0.75, 0.45 + shared * 0.1)
      : 0.35;

    records.push({
      candidate_id: makeId(`${a.term_id}:${b.term_id}:${relationship}`),
      term_a: a.term,
      term_b: b.term,
      relationship_type: relationship,
      confidence,
      source_origin_a: a.source_origin,
      source_origin_b: b.source_origin,
      evidence_a: a.evidence_ref,
      evidence_b: b.evidence_ref,
      review_status: 'review_required',
      review_notes: 'Deterministically generated candidate. No equivalence, synonymy, dependency, consequence, or conflict is accepted until review.',
      created_at: now,
      updated_at: now
    });
  }
}

records.sort((a, b) => a.candidate_id.localeCompare(b.candidate_id));

const output = {
  schema: 'admissibility_wiki_candidate_relationships.v0.1',
  repository: 'StegVerse-Labs/admissibility-wiki',
  authority_boundary: 'This file stores candidate relationships for review. It does not assert accepted synonymy, equivalence, dependency, consequence, or conflict until reviewed and promoted through a governed decision path.',
  required_record_fields: [
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
  ],
  allowed_relationship_types: [
    'equivalent_candidate',
    'near_equivalent_candidate',
    'parent_candidate',
    'child_candidate',
    'prerequisite_candidate',
    'consequence_candidate',
    'conflict_candidate',
    'adjacent_candidate',
    'unresolved_candidate'
  ],
  allowed_review_statuses: [
    'review_required',
    'accepted',
    'reclassified',
    'rejected',
    'deferred',
    'superseded'
  ],
  records,
  non_claims: [
    'A candidate relationship is not a final relationship claim.',
    'A candidate relationship is not an equivalence decision.',
    'A confidence score is not proof.',
    'A source origin link is not endorsement.'
  ]
};

fs.writeFileSync(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(`OK: wrote ${records.length} candidate relationships to ${outputPath}`);
