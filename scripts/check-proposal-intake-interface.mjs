#!/usr/bin/env node
import fs from 'node:fs';

const HTML_PATH = 'static/intake/manifest-receipt-intake.html';
const DOC_PATH = 'docs/governance/proposal-intake-interface.md';

const htmlRequired = [
  'Option 1 — Guided Builder',
  'Option 2 — Direct Paste',
  'Shared Manifest/Receipt Preview Window',
  'preview',
  'pasteBox',
  'buildPreview()',
  'usePastedStructure()',
  'preferred_triage',
  'Preview ≠ submission',
  'Not submitted'
];

const docRequired = [
  'Option 1: Guided Builder',
  'Option 2: Direct Paste',
  'Shared Preview Window',
  'ui_scaffold: installed',
  'backend_submission: not_installed',
  'automatic_receipt_issuance: not_installed',
  'automatic_queue_write: not_installed',
  'Preferred triage is not acceptance authority.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function assertFileContains(path, required) {
  if (!fs.existsSync(path)) {
    fail(`missing file: ${path}`);
  }
  const text = fs.readFileSync(path, 'utf8');
  for (const marker of required) {
    if (!text.includes(marker)) {
      fail(`${path} missing marker: ${marker}`);
    }
  }
}

assertFileContains(HTML_PATH, htmlRequired);
assertFileContains(DOC_PATH, docRequired);

console.log(`OK: ${HTML_PATH}`);
console.log(`OK: ${DOC_PATH}`);
console.log('proposal_intake_interface=dual_mode_preview_scaffold');
