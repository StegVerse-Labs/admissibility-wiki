#!/usr/bin/env node
import fs from 'node:fs';

const CANONICAL_WORKFLOW = '.github/workflows/validate-chain-continuation.yml';
const GUARD_DOC = 'docs/governance/publication-chain-guard.md';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(GUARD_DOC)) {
  fail(`missing guard doc: ${GUARD_DOC}`);
}

if (!fs.existsSync(CANONICAL_WORKFLOW)) {
  fail(`missing canonical workflow: ${CANONICAL_WORKFLOW}`);
}

const workflow = fs.readFileSync(CANONICAL_WORKFLOW, 'utf8');
const guardDoc = fs.readFileSync(GUARD_DOC, 'utf8');

if (!workflow.includes('build-pages:')) {
  fail('canonical workflow must include build-pages job');
}

if (!workflow.includes('deploy-pages:')) {
  fail('canonical workflow must include deploy-pages job');
}

if (!workflow.includes('verify-public-pages:')) {
  fail('canonical workflow must include verify-public-pages job');
}

if (!workflow.includes('npm run build')) {
  fail('Pages build job must run npm run build');
}

if (!workflow.includes('actions/deploy-pages@v4')) {
  fail('Pages deploy job must use actions/deploy-pages@v4');
}

if (!workflow.includes("github.event_name == 'workflow_dispatch'")) {
  fail('Pages deploy jobs must support manual workflow_dispatch republish from main');
}

if (!workflow.includes("github.event_name == 'push'")) {
  fail('Pages deploy jobs must support push-triggered publication from main');
}

if (!guardDoc.includes('Pages publication must have a build-only job inside the canonical workflow')) {
  fail('guard doc must state the canonical build-only publication rule');
}

console.log('OK: publication chain guard');
