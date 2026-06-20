#!/usr/bin/env node
import fs from 'node:fs';

const DOC_PATH = 'docs/governance/proposal-governance-classes.md';
const ROUTING_PATH = 'static/governance/proposal-routing/proposal-governance-classes.v1.json';
const FIXTURE_PATH = 'fixtures/intake/submission.valid.example.json';

const docMarkers = [
  'CLASS_E_EDITORIAL',
  'CLASS_G_GOVERNANCE',
  'CLASS_F_FORMALISM',
  'proposal_governance_class',
  'Every ingestion/CGE pass -> master-records',
  'Public display is a consequence path, not a submission path.',
  'StegVerse-Labs/proposal-governance-core-lite'
];

const invariantMarkers = [
  'Every ingestion/CGE pass routes to master-records.',
  'Public display is consequence path only.',
  'Receipt issuance is not proposal acceptance.',
  'Queue placement is not decision authority.',
  'LLM recommendation is not decision authority.',
  'Decision record is required before public display standing.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function requireFile(path) {
  if (!fs.existsSync(path)) {
    fail(`missing file: ${path}`);
  }
}

requireFile(DOC_PATH);
requireFile(ROUTING_PATH);
requireFile(FIXTURE_PATH);

const docText = fs.readFileSync(DOC_PATH, 'utf8');
for (const marker of docMarkers) {
  if (!docText.includes(marker)) {
    fail(`docs missing marker: ${marker}`);
  }
}

const routing = JSON.parse(fs.readFileSync(ROUTING_PATH, 'utf8'));
if (routing.schema !== 'admissibility_wiki_proposal_governance_classes.v1') {
  fail('routing schema mismatch');
}
for (const cls of ['E', 'G', 'F']) {
  if (!routing.classes?.[cls]) {
    fail(`missing class: ${cls}`);
  }
}
if (routing.classes.E.sandbox_required !== false) {
  fail('Class E must not require sandbox by default');
}
if (routing.classes.G.sandbox_required !== true) {
  fail('Class G must require sandbox');
}
if (routing.classes.F.sandbox_required !== true) {
  fail('Class F must require sandbox');
}
for (const invariant of invariantMarkers) {
  if (!routing.global_invariants.includes(invariant)) {
    fail(`missing invariant: ${invariant}`);
  }
}
if (routing.core_lite_target.organization !== 'StegVerse-Labs') {
  fail('core_lite_target.organization must be StegVerse-Labs');
}
if (routing.core_lite_target.repository_candidate !== 'proposal-governance-core-lite') {
  fail('repository_candidate must be proposal-governance-core-lite');
}

const fixture = JSON.parse(fs.readFileSync(FIXTURE_PATH, 'utf8'));
const manifest = fixture.manifest;
if (!['E', 'G', 'F'].includes(manifest.proposal_governance_class)) {
  fail('fixture manifest must include proposal_governance_class E|G|F');
}
if (!manifest.class_assignment || manifest.class_assignment.assigned_at !== 'intake') {
  fail('fixture must include intake class_assignment');
}
if (manifest.proposal.class === 'overlap_claim' && manifest.proposal_governance_class !== 'G') {
  fail('overlap_claim fixture must be Class G');
}

console.log(`OK: ${DOC_PATH}`);
console.log(`OK: ${ROUTING_PATH}`);
console.log(`fixture_class=${manifest.proposal_governance_class}`);
console.log('proposal_governance_classes=installed');
