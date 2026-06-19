#!/usr/bin/env node
import fs from 'node:fs';

const QUEUE_PATH = 'static/discovery/term-candidate-queue.v0.1.json';

const requiredTopLevel = [
  'schema',
  'repository',
  'purpose',
  'origin_boundary',
  'allowed_relationships',
  'allowed_origin_types',
  'disallowed_origin_types',
  'required_candidate_fields',
  'candidates',
  'next_action'
];

const requiredCandidateFields = [
  'candidate_id',
  'created_at',
  'search_cycle_id',
  'wiki_term_or_formalism',
  'candidate_term',
  'candidate_relationship',
  'origin_type',
  'origin_title',
  'origin_url',
  'origin_repository',
  'origin_publisher',
  'origin_stability',
  'claim_summary',
  'match_dimensions',
  'mismatch_dimensions',
  'overclaiming_risk',
  'review_status',
  'non_claims'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(QUEUE_PATH)) {
  fail(`missing queue: ${QUEUE_PATH}`);
}

const queue = JSON.parse(fs.readFileSync(QUEUE_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in queue)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (queue.schema !== 'admissibility_wiki_term_candidate_queue.v0.1') {
  fail('unexpected queue schema');
}

if (queue.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (!queue.origin_boundary.includes('Social-media comments may be leads but are not acceptable origins.')) {
  fail('origin boundary must reject social-media comments as origins');
}

for (const field of requiredCandidateFields) {
  if (!queue.required_candidate_fields.includes(field)) {
    fail(`required_candidate_fields missing ${field}`);
  }
}

const allowedOrigins = new Set(queue.allowed_origin_types);
const disallowedOrigins = new Set(queue.disallowed_origin_types);

if (allowedOrigins.has('linkedin_comment') || allowedOrigins.has('social_media_post')) {
  fail('social origins must not be allowed origin types');
}

const ids = new Set();
for (const candidate of queue.candidates) {
  for (const field of requiredCandidateFields) {
    if (!(field in candidate)) {
      fail(`candidate ${candidate.candidate_id || '<unknown>'} missing field: ${field}`);
    }
  }
  if (ids.has(candidate.candidate_id)) {
    fail(`duplicate candidate_id: ${candidate.candidate_id}`);
  }
  ids.add(candidate.candidate_id);
  if (!queue.allowed_relationships.includes(candidate.candidate_relationship)) {
    fail(`candidate ${candidate.candidate_id} has invalid relationship: ${candidate.candidate_relationship}`);
  }
  if (!allowedOrigins.has(candidate.origin_type)) {
    fail(`candidate ${candidate.candidate_id} has invalid origin_type: ${candidate.origin_type}`);
  }
  if (disallowedOrigins.has(candidate.origin_type)) {
    fail(`candidate ${candidate.candidate_id} uses disallowed origin_type: ${candidate.origin_type}`);
  }
  if (!Array.isArray(candidate.non_claims) || candidate.non_claims.length === 0) {
    fail(`candidate ${candidate.candidate_id} must include non_claims`);
  }
}

console.log(`OK: ${QUEUE_PATH}`);
console.log(`candidate_count=${queue.candidates.length}`);
