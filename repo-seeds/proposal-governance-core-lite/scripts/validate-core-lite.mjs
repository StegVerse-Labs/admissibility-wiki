#!/usr/bin/env node
import fs from 'node:fs';

const paths = {
  routing: 'schemas/proposal-governance-routing.v1.json',
  decisionSchema: 'schemas/proposal-governance-decision.v1.json',
  postSandboxBundle: 'fixtures/post-sandbox-bundle.example.json',
  decisionRecord: 'fixtures/decision-record.allow-overlap.example.json',
  status: 'status/proposal-governance-core-lite-status.json'
};

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) {
    fail(`missing file: ${path}`);
  }
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

const routing = readJson(paths.routing);
const decisionSchema = readJson(paths.decisionSchema);
const bundle = readJson(paths.postSandboxBundle);
const decision = readJson(paths.decisionRecord);
const status = readJson(paths.status);

for (const cls of ['E', 'G', 'F']) {
  if (!routing.route_classes[cls]) {
    fail(`missing route class: ${cls}`);
  }
}

if (!routing.invariants.includes('Every ingestion/CGE pass emits to master-records.')) {
  fail('missing master-records invariant');
}

for (const result of ['ALLOW', 'ALLOW_AS_OVERLAP', 'DENY', 'DEFER', 'ESCALATE', 'REFUSE', 'SUPERSEDE']) {
  if (!decisionSchema.allowed_decision_results.includes(result)) {
    fail(`missing decision result: ${result}`);
  }
}

if (bundle.proposal_governance_class !== 'G') {
  fail('example post-sandbox bundle must be Class G');
}

if (!Array.isArray(bundle.candidate_paths) || bundle.candidate_paths.length < 3) {
  fail('post-sandbox bundle must preserve multiple candidate paths');
}

if (decision.decision_result !== 'ALLOW_AS_OVERLAP') {
  fail('decision fixture must use ALLOW_AS_OVERLAP');
}

if (decision.public_display_consequence !== 'OVERLAP_MAPPING_DISPLAY') {
  fail('decision fixture must route to overlap display consequence');
}

if (!decision.master_records_copy_refs || decision.master_records_copy_refs.length < 3) {
  fail('decision fixture must preserve master-records copy refs for each phase');
}

if (status.repository_target !== 'StegVerse-Labs/proposal-governance-core-lite') {
  fail('status repository target mismatch');
}

if (status.runtime_status !== 'seed_only_not_deployed') {
  fail('seed must not claim deployed runtime');
}

console.log('OK: proposal-governance-core-lite seed');
console.log('classes=E,G,F');
console.log('runtime_status=seed_only_not_deployed');
