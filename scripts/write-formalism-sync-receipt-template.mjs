#!/usr/bin/env node
import fs from 'node:fs';

const DRIFT_REPORT_PATH = '.sync-output/formalism-source-drift-report.json';
const OUTPUT_DIR = '.sync-output';
const RECEIPT_PATH = `${OUTPUT_DIR}/formalism-source-sync-receipt-template.json`;

function readJsonIfPresent(path) {
  if (!fs.existsSync(path)) return null;
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const driftReport = readJsonIfPresent(DRIFT_REPORT_PATH);
const driftRecords = driftReport?.drift_records || [];

const receipt = {
  schema: 'admissibility_wiki_formalism_source_sync_receipt_template.v0.1',
  receipt_status: driftRecords.length > 0 ? 'sync_review_required' : 'no_sync_review_required',
  authority_boundary: 'Admissible-Existence defines formalisms. Publisher publishes. Admissibility Wiki mirrors and crosswalks public-safe relationships.',
  required_receipt_fields: [
    'receipt_id',
    'source_id',
    'formalism_term',
    'canonical_source_repository',
    'prior_source_ref',
    'new_source_ref',
    'publisher_artifact_ref',
    'wiki_target_path',
    'prior_wiki_ref',
    'new_wiki_ref',
    'sync_outcome',
    'review_status',
    'decision_record_ref',
    'non_claims'
  ],
  records: driftRecords.map((record) => ({
    receipt_id: `pending.${record.source_id}`,
    source_id: record.source_id,
    formalism_term: record.formalism_term,
    canonical_source_repository: record.canonical_source_repository,
    prior_source_ref: record.last_source_ref,
    new_source_ref: record.current_source_ref,
    publisher_artifact_ref: record.current_publisher_ref,
    wiki_target_path: record.wiki_target_path,
    prior_wiki_ref: null,
    new_wiki_ref: null,
    sync_outcome: 'pending_review',
    review_status: 'not_yet_reviewed',
    decision_record_ref: null,
    non_claims: [
      'This template does not define the formalism.',
      'This template does not prove or validate the formalism.',
      'A final receipt requires public-safe wiki review.'
    ]
  }))
};

fs.writeFileSync(RECEIPT_PATH, `${JSON.stringify(receipt, null, 2)}\n`);
console.log(`formalism_sync_receipt_template_records=${receipt.records.length}`);
