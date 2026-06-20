#!/usr/bin/env node
import fs from 'node:fs';

const TEMPLATE_PATH = process.env.SYNC_RECEIPT_TEMPLATE || '.sync-output/formalism-source-sync-receipt-template.json';
const REVIEW_STATUS = process.env.SYNC_REVIEW_STATUS || 'accepted';
const DECISION_RECORD_REF = process.env.SYNC_DECISION_RECORD_REF || null;
const NEW_WIKI_REF = process.env.SYNC_NEW_WIKI_REF || null;
const PRIOR_WIKI_REF = process.env.SYNC_PRIOR_WIKI_REF || null;
const OUTPUT_DIR = 'static/sync/receipts';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(TEMPLATE_PATH)) {
  fail(`missing receipt template: ${TEMPLATE_PATH}`);
}

const template = JSON.parse(fs.readFileSync(TEMPLATE_PATH, 'utf8'));

if (!Array.isArray(template.records)) {
  fail('receipt template must include records array');
}

if (template.records.length === 0) {
  console.log('NO_FINAL_RECEIPT_REQUIRED');
  process.exit(0);
}

if (REVIEW_STATUS !== 'accepted') {
  fail('final receipt can only be produced when SYNC_REVIEW_STATUS=accepted');
}

if (!DECISION_RECORD_REF) {
  fail('SYNC_DECISION_RECORD_REF is required');
}

if (!NEW_WIKI_REF) {
  fail('SYNC_NEW_WIKI_REF is required');
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const now = new Date().toISOString();
const safeDate = now.slice(0, 10).replaceAll('-', '');
const finalized = {
  schema: 'admissibility_wiki_formalism_source_sync_receipt.v0.1',
  finalized_at: now,
  authority_boundary: template.authority_boundary,
  review_status: REVIEW_STATUS,
  decision_record_ref: DECISION_RECORD_REF,
  records: template.records.map((record, index) => ({
    ...record,
    receipt_id: `formalism-sync.${safeDate}.${index + 1}.${record.source_id}`,
    prior_wiki_ref: PRIOR_WIKI_REF,
    new_wiki_ref: NEW_WIKI_REF,
    sync_outcome: 'wiki_update_applied',
    review_status: REVIEW_STATUS,
    decision_record_ref: DECISION_RECORD_REF,
    non_claims: [
      'This receipt records a public-safe wiki synchronization.',
      'This receipt does not define, prove, or validate the formalism.',
      'Admissible-Existence remains the canonical formalism source.'
    ]
  }))
};

const path = `${OUTPUT_DIR}/formalism-source-sync-${safeDate}.json`;
fs.writeFileSync(path, `${JSON.stringify(finalized, null, 2)}\n`);
console.log(`FINAL_SYNC_RECEIPT=${path}`);
