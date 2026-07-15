#!/usr/bin/env node
import fs from 'node:fs';

const REGISTRY_PATH = 'static/formalisms/formalism-registry.v0.1.json';
const RECONCILIATION_PATH = 'static/formalisms/formalism-registry-reconciliation.v1.json';
const CLASSIFICATION_PATH = 'static/formalisms/formalism-record-classification.v1.json';

const requiredRecordFields = [
  'formalism_id', 'name', 'state', 'source_authority', 'wiki_path', 'purpose',
  'transition_relationship', 'evidence_posture', 'validation_posture', 'non_claims'
];
const requiredClassificationFields = [
  'formalism_id', 'artifact_class', 'mirror_posture', 'proof_posture',
  'validation_posture', 'publication_posture'
];
const allowedStates = new Set(['intake', 'mirrored', 'crosswalked', 'validated', 'superseded']);
const allowedPublicationPostures = new Set(['COMPLETE_WITH_EXTERNAL_GATES', 'PARTIAL']);

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

for (const path of [REGISTRY_PATH, RECONCILIATION_PATH, CLASSIFICATION_PATH]) {
  if (!fs.existsSync(path)) fail(`missing formalism artifact: ${path}`);
}

const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
const reconciliation = JSON.parse(fs.readFileSync(RECONCILIATION_PATH, 'utf8'));
const classification = JSON.parse(fs.readFileSync(CLASSIFICATION_PATH, 'utf8'));

if (registry.schema !== 'admissibility_wiki_formalism_registry.v0.1') fail('unexpected registry schema');
if (registry.repository !== 'StegVerse-Labs/admissibility-wiki') fail('unexpected registry repository');
if (!registry.authority_boundary.includes('does not create source authority')) fail('registry authority boundary is incomplete');
if (!Array.isArray(registry.records) || registry.records.length < 5) fail('registry must contain records');

const baseById = new Map();
for (const record of registry.records) {
  for (const field of requiredRecordFields) {
    if (!(field in record)) fail(`record ${record.formalism_id || '<unknown>'} missing field: ${field}`);
  }
  if (baseById.has(record.formalism_id)) fail(`duplicate formalism_id: ${record.formalism_id}`);
  if (!allowedStates.has(record.state)) fail(`invalid base state for ${record.formalism_id}: ${record.state}`);
  if (!Array.isArray(record.non_claims) || record.non_claims.length === 0) fail(`record ${record.formalism_id} must include non_claims`);
  if (!fs.existsSync(record.wiki_path)) fail(`missing wiki page for ${record.formalism_id}: ${record.wiki_path}`);
  baseById.set(record.formalism_id, {...record});
}

if (reconciliation.schema !== 'admissibility_wiki_formalism_registry_reconciliation.v1') fail('unexpected reconciliation schema');
if (reconciliation.repository !== registry.repository) fail('reconciliation repository mismatch');
if (reconciliation.base_registry !== REGISTRY_PATH) fail('reconciliation base registry mismatch');
if (!Array.isArray(reconciliation.overrides)) fail('reconciliation overrides must be an array');

const effectiveById = new Map([...baseById.entries()].map(([id, record]) => [id, {...record}]));
const overrideIds = new Set();
for (const override of reconciliation.overrides) {
  const id = override.formalism_id;
  if (!baseById.has(id)) fail(`override references unknown formalism: ${id}`);
  if (overrideIds.has(id)) fail(`duplicate override: ${id}`);
  overrideIds.add(id);
  if (!allowedStates.has(override.effective_state)) fail(`invalid effective state for ${id}: ${override.effective_state}`);
  if (!fs.existsSync(override.page_path)) fail(`override page missing for ${id}: ${override.page_path}`);
  if (!override.authority_boundary?.includes('does not')) fail(`override authority boundary missing for ${id}`);
  const record = effectiveById.get(id);
  record.state = override.effective_state;
  record.purpose = override.effective_purpose;
  record.transition_relationship = override.effective_transition_relationship;
  record.evidence_posture = override.effective_evidence_posture;
  record.validation_posture = override.effective_validation_posture;
}

const effectiveCounts = {intake: 0, mirrored: 0, crosswalked: 0, validated: 0, superseded: 0};
for (const record of effectiveById.values()) effectiveCounts[record.state] += 1;
const reconciliationCounts = reconciliation.counts || {};
if (reconciliationCounts.base_records !== registry.records.length) fail('reconciliation base_records count is stale');
if (reconciliationCounts.overrides !== reconciliation.overrides.length) fail('reconciliation override count is stale');
if (reconciliationCounts.effective_intake !== effectiveCounts.intake) fail('effective intake count is stale');
if (reconciliationCounts.effective_mirrored !== effectiveCounts.mirrored) fail('effective mirrored count is stale');
if (reconciliationCounts.effective_crosswalked !== effectiveCounts.crosswalked) fail('effective crosswalked count is stale');

if (classification.schema !== 'admissibility_wiki_formalism_record_classification.v1') fail('unexpected classification schema');
if (classification.repository !== registry.repository) fail('classification repository mismatch');
if (classification.registry !== REGISTRY_PATH) fail('classification registry reference mismatch');
if (classification.registry_reconciliation !== RECONCILIATION_PATH) fail('classification reconciliation reference mismatch');
if (!classification.authority_boundary.includes('does not create source authority')) fail('classification authority boundary is incomplete');
if (!Array.isArray(classification.entries) || classification.entries.length !== registry.records.length) fail('classification coverage mismatch');

const allowedArtifactClasses = new Set(classification.allowed_artifact_classes || []);
const classificationIds = new Set();
let theoremCount = 0;
let infrastructureCount = 0;
for (const entry of classification.entries) {
  for (const field of requiredClassificationFields) {
    if (!(field in entry)) fail(`classification ${entry.formalism_id || '<unknown>'} missing field: ${field}`);
  }
  if (!effectiveById.has(entry.formalism_id)) fail(`classification references unknown formalism: ${entry.formalism_id}`);
  if (classificationIds.has(entry.formalism_id)) fail(`duplicate classification: ${entry.formalism_id}`);
  classificationIds.add(entry.formalism_id);
  if (!allowedArtifactClasses.has(entry.artifact_class)) fail(`invalid artifact class for ${entry.formalism_id}`);
  if (!allowedPublicationPostures.has(entry.publication_posture)) fail(`invalid publication posture for ${entry.formalism_id}`);
  if (!entry.proof_posture || !entry.validation_posture || !entry.mirror_posture) fail(`empty classification posture for ${entry.formalism_id}`);
  if (entry.artifact_class === 'theorem_candidate') {
    theoremCount += 1;
    if (!entry.proof_posture.includes('UNPROVEN')) fail(`theorem candidate must remain unproven: ${entry.formalism_id}`);
  }
  if (['executable_engine', 'validation_infrastructure'].includes(entry.artifact_class)) infrastructureCount += 1;
  const effective = effectiveById.get(entry.formalism_id);
  if (effective.state === 'intake' && entry.publication_posture !== 'PARTIAL') fail(`effective intake must remain PARTIAL: ${entry.formalism_id}`);
}

const counts = classification.counts || {};
if (counts.records !== registry.records.length) fail('classification record count is stale');
if (counts.effective_mirrored !== effectiveCounts.mirrored) fail('classification effective_mirrored count is stale');
if (counts.effective_crosswalked !== effectiveCounts.crosswalked) fail('classification effective_crosswalked count is stale');
if (counts.effective_intake !== effectiveCounts.intake) fail('classification effective_intake count is stale');
if (counts.theorem_candidates !== theoremCount) fail('classification theorem count is stale');
if (counts.executable_or_validation_infrastructure !== infrastructureCount) fail('classification infrastructure count is stale');

console.log(`OK: ${REGISTRY_PATH}`);
console.log(`formalism_records=${registry.records.length}`);
console.log(`formalism_classified=${classification.entries.length}`);
console.log(`effective_mirrored=${effectiveCounts.mirrored}`);
console.log(`effective_crosswalked=${effectiveCounts.crosswalked}`);
console.log(`effective_intake=${effectiveCounts.intake}`);
console.log(`theorem_candidates=${theoremCount}`);
