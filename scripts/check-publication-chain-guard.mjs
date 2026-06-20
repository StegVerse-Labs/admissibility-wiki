#!/usr/bin/env node
import fs from 'node:fs';

const BUILD_ONLY_WORKFLOW = '.github/workflows/pages-build-only.yml';
const GUARD_DOC = 'docs/governance/publication-chain-guard.md';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(GUARD_DOC)) {
  fail(`missing guard doc: ${GUARD_DOC}`);
}

if (!fs.existsSync(BUILD_ONLY_WORKFLOW)) {
  fail(`missing build-only Pages workflow: ${BUILD_ONLY_WORKFLOW}`);
}

const workflow = fs.readFileSync(BUILD_ONLY_WORKFLOW, 'utf8');
const guardDoc = fs.readFileSync(GUARD_DOC, 'utf8');

if (!workflow.includes('npm run build')) {
  fail('build-only workflow must run npm run build');
}

if (workflow.includes('npm run validate')) {
  fail('build-only workflow must not run npm run validate');
}

if (!workflow.includes('actions/deploy-pages@v4')) {
  fail('build-only workflow must use actions/deploy-pages@v4');
}

if (!guardDoc.includes('Pages publication must have a build-only path')) {
  fail('guard doc must state the build-only publication rule');
}

console.log('OK: publication chain guard');
