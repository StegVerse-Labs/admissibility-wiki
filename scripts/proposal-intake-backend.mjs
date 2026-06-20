#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const inputPath = process.argv[2];

const OUT_ROOT = 'static/governance/intake';
const CANDIDATE_DIR = `${OUT_ROOT}/candidates`;
const RECEIPT_DIR = `${OUT_ROOT}/receipts`;
const QUEUE_DIR = `${OUT_ROOT}/queue`;
const INDEX_PATH = `${OUT_ROOT}/queue/index.json`;

const REQUIRED_MANIFEST_FIELDS = [
  'schema',
  'proposal_id',
  'submitted_at',
  'submitter_class',
  'target',
  'proposal',
  'transition_origin_claim',
  'relationship_claims',
  'evidence_refs',
  'non_claims',
  'receipt_request'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function stableJson(value) {
  return JSON.stringify(value, Object.keys(value).sort(), 2);
}

function hash(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function readJson(filePath) {
  if (!filePath) {
    fail('usage: node scripts/proposal-intake-backend.mjs <submission.json>');
  }
  if (!fs.existsSync(filePath)) {
    fail(`missing input file: ${filePath}`);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function requireObject(value, name) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    fail(`${name} must be an object`);
  }
}

function validateManifest(manifest) {
  requireObject(manifest, 'manifest');
  for (const field of REQUIRED_MANIFEST_FIELDS) {
    if (!(field in manifest)) {
      fail(`manifest missing field: ${field}`);
    }
  }
  if (manifest.schema !== 'admissibility_wiki_submission_manifest.v1') {
    fail('manifest schema must be admissibility_wiki_submission_manifest.v1');
  }
  requireObject(manifest.target, 'manifest.target');
  requireObject(manifest.proposal, 'manifest.proposal');
  requireObject(manifest.transition_origin_claim, 'manifest.transition_origin_claim');
  if (!Array.isArray(manifest.relationship_claims)) {
    fail('manifest.relationship_claims must be an array');
  }
  if (!Array.isArray(manifest.evidence_refs)) {
    fail('manifest.evidence_refs must be an array');
  }
  if (!Array.isArray(manifest.non_claims)) {
    fail('manifest.non_claims must be an array');
  }
}

function loadQueueIndex() {
  if (!fs.existsSync(INDEX_PATH)) {
    return {
      schema: 'admissibility_wiki_proposal_queue_index.v1',
      generated_at: new Date().toISOString(),
      queue_status: 'open',
      items: []
    };
  }
  return JSON.parse(fs.readFileSync(INDEX_PATH, 'utf8'));
}

function writeJson(filePath, value) {
  if (fs.existsSync(filePath)) {
    fail(`refusing to overwrite durable artifact: ${filePath}`);
  }
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

const receivedAt = new Date().toISOString();
const rawText = fs.readFileSync(inputPath, 'utf8');
const submission = readJson(inputPath);
const manifest = submission.manifest ?? submission;

validateManifest(manifest);

ensureDir(CANDIDATE_DIR);
ensureDir(RECEIPT_DIR);
ensureDir(QUEUE_DIR);

const rawHash = hash(rawText);
const normalizedManifest = JSON.parse(JSON.stringify(manifest));
const manifestHash = hash(JSON.stringify(normalizedManifest));
const shortHash = manifestHash.slice(0, 12);
const proposalId = manifest.proposal_id === 'pending' ? `proposal.${shortHash}` : manifest.proposal_id;
const receiptId = `receipt.${shortHash}`;
const queueId = `queue.${shortHash}`;

const candidate = {
  schema: 'admissibility_wiki_candidate_submission.v1',
  proposal_id: proposalId,
  received_at: receivedAt,
  manifest: normalizedManifest,
  hashes: {
    raw_submission_sha256: rawHash,
    normalized_manifest_sha256: manifestHash
  },
  posture: {
    incoming_governed_data: true,
    not_effect_capable_by_default: true,
    not_accepted_by_receipt: true,
    requires_review_before_standing: true
  }
};

const receiptIssuedAt = new Date().toISOString();
const receipt = {
  schema: 'admissibility_wiki_submission_receipt.v1',
  receipt_id: receiptId,
  proposal_id: proposalId,
  received_at: receivedAt,
  receipt_issued_at: receiptIssuedAt,
  submission_lane: 'lane_1_manifest_receipt',
  preference_posture: 'preferred_triage',
  validation_posture: 'valid_manifest',
  candidate_ref: `../candidates/${proposalId}.json`,
  queue_ref: `../queue/${queueId}.json`,
  hashes: {
    raw_submission_sha256: rawHash,
    normalized_manifest_sha256: manifestHash
  },
  tasks: [
    { task: 'receive_request', started_at: receivedAt, completed_at: receivedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'parse_manifest', started_at: receivedAt, completed_at: receivedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'validate_manifest_schema', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'classify_submission_lane', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'assign_preference_posture', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'compute_submission_hashes', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'write_candidate_record', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'write_queue_record', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' },
    { task: 'issue_submission_receipt', started_at: receivedAt, completed_at: receiptIssuedAt, status: 'completed', timing_posture: 'recorded' }
  ],
  non_claims: [
    'Receipt does not accept the proposal.',
    'Receipt does not prove the submitted claim.',
    'Receipt does not create equivalent-term standing.',
    'Queue placement does not create decision authority.'
  ]
};

const receiptHash = hash(JSON.stringify(receipt));
receipt.hashes.receipt_sha256 = receiptHash;

const queueRecord = {
  schema: 'admissibility_wiki_proposal_queue_record.v1',
  queue_id: queueId,
  proposal_id: proposalId,
  receipt_id: receiptId,
  queued_at: receiptIssuedAt,
  status: 'queued_for_review',
  review_route: 'admissibility_wiki_ai_entity',
  target: manifest.target,
  proposal: manifest.proposal,
  transition_origin_claim: manifest.transition_origin_claim,
  candidate_ref: `../candidates/${proposalId}.json`,
  receipt_ref: `../receipts/${receiptId}.json`,
  hashes: {
    normalized_manifest_sha256: manifestHash,
    receipt_sha256: receiptHash
  },
  non_claims: [
    'Queue placement does not accept the proposal.',
    'Queue placement does not prove the submitted claim.',
    'Queue placement does not create decision authority.'
  ]
};

writeJson(`${CANDIDATE_DIR}/${proposalId}.json`, candidate);
writeJson(`${RECEIPT_DIR}/${receiptId}.json`, receipt);
writeJson(`${QUEUE_DIR}/${queueId}.json`, queueRecord);

const index = loadQueueIndex();
index.generated_at = receiptIssuedAt;
index.items.push({
  queue_id: queueId,
  proposal_id: proposalId,
  receipt_id: receiptId,
  status: 'queued_for_review',
  target_path: manifest.target.path,
  queued_at: receiptIssuedAt,
  queue_ref: `${queueId}.json`
});
fs.writeFileSync(INDEX_PATH, `${JSON.stringify(index, null, 2)}\n`);

console.log(JSON.stringify({
  proposal_id: proposalId,
  receipt_id: receiptId,
  queue_id: queueId,
  candidate_path: path.join(CANDIDATE_DIR, `${proposalId}.json`),
  receipt_path: path.join(RECEIPT_DIR, `${receiptId}.json`),
  queue_path: path.join(QUEUE_DIR, `${queueId}.json`),
  index_path: INDEX_PATH,
  status: 'queued_for_review'
}, null, 2));
