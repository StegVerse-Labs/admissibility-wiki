#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/admissibility-wiki-status.json';

const requiredTopLevel = [
  'schema',
  'generated_at',
  'repository',
  'site',
  'status',
  'assessment_goal',
  'activation_target',
  'activation_artifacts',
  'activation_checks',
  'github_io_configuration',
  'proposal_intake',
  'site_bridge',
  'installed_public_pages',
  'installed_governance_records',
  'known_handoff_files',
  'next_safe_build_targets'
];

const requiredBridge = [
  'site_repository',
  'site_bridge_path',
  'site_display_authority',
  'wiki_source_authority',
  'proof_authority'
];

const requiredPublicPages = [
  'landing_page',
  'activation_runbook',
  'proposal_intake_interface',
  'manifest_receipt_submission',
  'terminology_convergence',
  'proposal_lifecycle',
  'decision_record',
  'site_bridge_status',
  'current_task_sync',
  'mirror_handoff'
];

const requiredIntakeFields = [
  'governance_page',
  'manifest_receipt_policy',
  'static_scaffold',
  'validator',
  'guided_builder',
  'direct_paste',
  'shared_preview_window',
  'backend_submission',
  'durable_receipt_issuance',
  'queue_write',
  'automatic_ai_review',
  'automatic_decision_publication',
  'preference_rule'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function requireObject(value, name) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    fail(`${name} must be an object`);
  }
}

function requireArray(value, name) {
  if (!Array.isArray(value)) {
    fail(`${name} must be an array`);
  }
}

if (!fs.existsSync(STATUS_PATH)) {
  fail(`missing status artifact: ${STATUS_PATH}`);
}

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in status)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (status.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (status.site !== 'https://stegverse-labs.github.io/admissibility-wiki/') {
  fail('site must be the GitHub.io project URL');
}

requireObject(status.activation_artifacts, 'activation_artifacts');
requireObject(status.activation_checks, 'activation_checks');
requireObject(status.github_io_configuration, 'github_io_configuration');
requireObject(status.proposal_intake, 'proposal_intake');
requireObject(status.site_bridge, 'site_bridge');
requireObject(status.installed_public_pages, 'installed_public_pages');
requireObject(status.known_handoff_files, 'known_handoff_files');
requireArray(status.installed_governance_records, 'installed_governance_records');
requireArray(status.next_safe_build_targets, 'next_safe_build_targets');

if (status.github_io_configuration.custom_domain !== 'not_configured') {
  fail('custom domain must remain not_configured');
}

if (status.github_io_configuration.baseUrl !== '/admissibility-wiki/') {
  fail('baseUrl must remain /admissibility-wiki/');
}

for (const field of requiredBridge) {
  if (!(field in status.site_bridge)) {
    fail(`missing site_bridge field: ${field}`);
  }
}

if (status.site_bridge.site_display_authority !== 'bridge_display_only') {
  fail('site bridge must remain bridge_display_only');
}

for (const field of requiredPublicPages) {
  if (!(field in status.installed_public_pages)) {
    fail(`missing installed_public_pages field: ${field}`);
  }
}

for (const field of requiredIntakeFields) {
  if (!(field in status.proposal_intake)) {
    fail(`missing proposal_intake field: ${field}`);
  }
}

if (status.proposal_intake.backend_submission !== 'not_installed') {
  fail('proposal_intake.backend_submission must not be claimed active');
}
if (status.proposal_intake.durable_receipt_issuance !== 'not_installed') {
  fail('proposal_intake.durable_receipt_issuance must not be claimed active');
}
if (status.proposal_intake.queue_write !== 'not_installed') {
  fail('proposal_intake.queue_write must not be claimed active');
}

if (status.known_handoff_files.repo_handoff !== 'docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md') {
  fail('canonical repo_handoff must be docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md');
}

if (status.next_safe_build_targets.length === 0) {
  fail('next_safe_build_targets must not be empty');
}

console.log(`OK: ${STATUS_PATH}`);
console.log(`status=${status.status}`);
console.log(`site=${status.site}`);
console.log(`proposal_intake_backend=${status.proposal_intake.backend_submission}`);
console.log(`next_safe_build_targets=${status.next_safe_build_targets.length}`);
