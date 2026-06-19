#!/usr/bin/env node
import fs from 'node:fs';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';

const requiredTopLevel = [
  'schema',
  'repository',
  'purpose',
  'authority_boundary',
  'sync_states',
  'required_source_fields',
  'sources',
  'next_action'
];

const requiredSourceFields = [
  'source_id',
  'formalism_term',
  'canonical_source_repository',
  'canonical_source_visibility',
  'publisher_artifact_path',
  'wiki_target_path',
  'sync_state',
  'last_known_source_ref',
  'last_known_publisher_ref',
  'change_detection_rule',
  'wiki_update_rule',
  'non_claims'
];

const allowedStates = new Set([
  'watching',
  'source_available',
  'source_changed',
  'wiki_update_required',
  'wiki_update_proposed',
  'wiki_update_applied',
  'blocked_private_source',
  'blocked_missing_source',
  'superseded'
]);

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(MANIFEST_PATH)) {
  fail(`missing manifest: ${MANIFEST_PATH}`);
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in manifest)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (manifest.schema !== 'admissibility_wiki_formalism_source_sync.v0.1') {
  fail('unexpected manifest schema');
}

if (manifest.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (!manifest.authority_boundary.includes('Admissible-Existence defines formalisms')) {
  fail('authority boundary must identify Admissible-Existence as formalism source');
}

if (!manifest.authority_boundary.includes('The Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships')) {
  fail('authority boundary must limit wiki role to convergence functions');
}

for (const field of requiredSourceFields) {
  if (!manifest.required_source_fields.includes(field)) {
    fail(`required_source_fields missing ${field}`);
  }
}

if (!Array.isArray(manifest.sources) || manifest.sources.length < 1) {
  fail('manifest must include at least one source');
}

const ids = new Set();
for (const source of manifest.sources) {
  for (const field of requiredSourceFields) {
    if (!(field in source)) {
      fail(`source ${source.source_id || '<unknown>'} missing field: ${field}`);
    }
  }

  if (ids.has(source.source_id)) {
    fail(`duplicate source_id: ${source.source_id}`);
  }
  ids.add(source.source_id);

  if (!allowedStates.has(source.sync_state)) {
    fail(`invalid sync_state for ${source.source_id}: ${source.sync_state}`);
  }

  if (!source.canonical_source_repository.startsWith('Admissible-Existence/')) {
    fail(`canonical source must be in Admissible-Existence: ${source.source_id}`);
  }

  if (!source.wiki_target_path.startsWith('docs/')) {
    fail(`wiki target must be a docs page: ${source.source_id}`);
  }

  if (!Array.isArray(source.non_claims) || source.non_claims.length === 0) {
    fail(`source ${source.source_id} must include non_claims`);
  }
}

console.log(`OK: ${MANIFEST_PATH}`);
console.log(`formalism_sources=${manifest.sources.length}`);
