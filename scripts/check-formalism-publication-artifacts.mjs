#!/usr/bin/env node
import fs from 'node:fs';

const INVENTORIES = [
  'static/formalisms/gcat-bcat-publication-artifacts.v0.1.json'
];

const GOVERNED_ACTION_LIFECYCLE = 'docs/formalisms/governed-action-lifecycle.md';

const requiredTopLevel = [
  'schema',
  'formalism_id',
  'canonical_name',
  'canonical_source_repository',
  'publication_family',
  'publication_family_url',
  'authority_boundary',
  'artifact_status',
  'artifacts',
  'candidate_slots',
  'open_questions',
  'non_claims'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

for (const path of INVENTORIES) {
  if (!fs.existsSync(path)) fail(`missing inventory: ${path}`);
  const inventory = JSON.parse(fs.readFileSync(path, 'utf8'));

  for (const field of requiredTopLevel) {
    if (!(field in inventory)) fail(`${path} missing field: ${field}`);
  }

  if (inventory.schema !== 'admissibility_wiki_formalism_publication_artifact_inventory.v0.1') {
    fail(`${path} has unexpected schema`);
  }

  if (!inventory.canonical_source_repository.startsWith('Admissible-Existence/')) {
    fail(`${path} canonical source must be Admissible-Existence`);
  }

  if (!inventory.authority_boundary.includes('Admissible-Existence defines the formalism')) {
    fail(`${path} must preserve AE source authority`);
  }

  if (!Array.isArray(inventory.artifacts)) fail(`${path} artifacts must be array`);
  if (!Array.isArray(inventory.open_questions) || inventory.open_questions.length === 0) fail(`${path} open_questions required`);
  if (!Array.isArray(inventory.non_claims) || inventory.non_claims.length === 0) fail(`${path} non_claims required`);

  const candidateSlots = inventory.candidate_slots;
  for (const slot of ['mathematical_candidates', 'proof_candidates', 'validation_candidates']) {
    if (!Array.isArray(candidateSlots?.[slot])) fail(`${path} missing candidate slot: ${slot}`);
  }
}

if (!fs.existsSync(GOVERNED_ACTION_LIFECYCLE)) {
  fail(`missing formalism page: ${GOVERNED_ACTION_LIFECYCLE}`);
}

const lifecycle = fs.readFileSync(GOVERNED_ACTION_LIFECYCLE, 'utf8');
const forbiddenMdxMathMarkers = [
  /^\s*\\\[\s*$/m,
  /^\s*\\\]\s*$/m,
  /\\not\\Rightarrow/,
  /\\Gamma\s*\(/,
  /\\mathcal\s*\{R\}/
];

for (const pattern of forbiddenMdxMathMarkers) {
  if (pattern.test(lifecycle)) {
    fail(`${GOVERNED_ACTION_LIFECYCLE} reintroduced MDX-sensitive display math: ${pattern}`);
  }
}

const requiredLifecycleStatements = [
  'ValidAt(t_0) does not imply ValidAt(t_c)',
  'Gamma(T_t_c) -> {ALLOW, DENY, DEFER, ESCALATE}',
  'OperationalSuccess does not imply Admissible',
  'R = {rollback, repair, compensate, contain, appeal, learn}',
  'Reconstructable does not imply LegitimateAtCommit'
];

for (const statement of requiredLifecycleStatements) {
  if (!lifecycle.includes(statement)) {
    fail(`${GOVERNED_ACTION_LIFECYCLE} missing static-render-safe lifecycle statement: ${statement}`);
  }
}

console.log(
  `OK: formalism publication artifact inventories=${INVENTORIES.length}; governed lifecycle MDX safety=PASS`
);