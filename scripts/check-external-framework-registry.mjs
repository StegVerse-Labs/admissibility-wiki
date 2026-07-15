#!/usr/bin/env node
import fs from 'node:fs';

const STATIC_REGISTRY_PATH = 'static/external-frameworks/external-framework-registry.v0.1.json';
const DOCS_REGISTRY_PATH = 'docs/external-frameworks/index.json';
const ASSOCIATIONS_PATH = 'static/external-frameworks/sidebar-page-associations.v1.json';
const SIDEBARS_PATH = 'sidebars.js';

const requiredTopLevel = [
  'schema',
  'repository',
  'authority_boundary',
  'allowed_relationships',
  'required_record_fields',
  'records',
  'next_action'
];
const requiredRecordFields = [
  'framework_id',
  'name',
  'status',
  'external_role',
  'wiki_path',
  'primary_relationship',
  'crosswalk_targets',
  'non_claims'
];
const allowedPresenceStates = new Set(['present', 'missing_explicit']);

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing JSON artifact: ${path}`);
  try {
    return JSON.parse(fs.readFileSync(path, 'utf8'));
  } catch (error) {
    fail(`invalid JSON in ${path}: ${error.message}`);
  }
}

function extractExternalFrameworkSidebarRoutes() {
  if (!fs.existsSync(SIDEBARS_PATH)) fail(`missing sidebar file: ${SIDEBARS_PATH}`);
  const text = fs.readFileSync(SIDEBARS_PATH, 'utf8');
  const categoryStart = text.indexOf("label: 'External Frameworks'");
  if (categoryStart < 0) fail('External Frameworks sidebar category not found');
  const nextCategory = text.indexOf("label: 'Research'", categoryStart);
  if (nextCategory < 0) fail('could not determine end of External Frameworks sidebar category');
  const block = text.slice(categoryStart, nextCategory);
  return [...block.matchAll(/'((?:external-frameworks)\/[^']+)'/g)].map(match => match[1]);
}

const registry = readJson(STATIC_REGISTRY_PATH);
for (const field of requiredTopLevel) {
  if (!(field in registry)) fail(`missing top-level field in static registry: ${field}`);
}
if (registry.schema !== 'admissibility_wiki_external_framework_registry.v0.1') fail('unexpected static registry schema');
if (registry.repository !== 'StegVerse-Labs/admissibility-wiki') fail('unexpected static registry repository');
if (!registry.authority_boundary.includes('They do not become canonical Admissible-Existence formalism sources')) {
  fail('authority boundary must preserve AE canonical-source separation');
}

const allowedRelationships = new Set(registry.allowed_relationships);
const staticRegistryIds = new Set();
for (const record of registry.records) {
  for (const field of requiredRecordFields) {
    if (!(field in record)) fail(`static registry record ${record.framework_id || '<unknown>'} missing field: ${field}`);
  }
  if (staticRegistryIds.has(record.framework_id)) fail(`duplicate static framework_id: ${record.framework_id}`);
  staticRegistryIds.add(record.framework_id);
  if (!record.wiki_path.startsWith('docs/')) fail(`wiki_path must be under docs/: ${record.framework_id}`);
  if (!allowedRelationships.has(record.primary_relationship)) fail(`invalid primary relationship: ${record.framework_id}`);
  if (!Array.isArray(record.crosswalk_targets) || record.crosswalk_targets.length === 0) fail(`crosswalk_targets required: ${record.framework_id}`);
  if (!Array.isArray(record.non_claims) || record.non_claims.length === 0) fail(`non_claims required: ${record.framework_id}`);
}

const docsRegistry = readJson(DOCS_REGISTRY_PATH);
if (!Array.isArray(docsRegistry.entries)) fail('docs registry entries must be an array');
const docsRegistryIds = new Set();
for (const record of docsRegistry.entries) {
  if (!record.framework_id) fail('docs registry record missing framework_id');
  if (docsRegistryIds.has(record.framework_id)) fail(`duplicate docs framework_id: ${record.framework_id}`);
  docsRegistryIds.add(record.framework_id);
}

const associations = readJson(ASSOCIATIONS_PATH);
if (associations.schema !== 'external_framework_sidebar_associations.v1') fail('unexpected sidebar association schema');
if (associations.repository !== 'StegVerse-Labs/admissibility-wiki') fail('unexpected sidebar association repository');
if (!Array.isArray(associations.entries)) fail('sidebar association entries must be an array');

const sidebarRoutes = extractExternalFrameworkSidebarRoutes();
const associatedRoutes = associations.entries.map(entry => entry.sidebar_route);
if (sidebarRoutes.length !== associatedRoutes.length) {
  fail(`sidebar/association count mismatch: sidebar=${sidebarRoutes.length}, associations=${associatedRoutes.length}`);
}
for (let index = 0; index < sidebarRoutes.length; index += 1) {
  if (sidebarRoutes[index] !== associatedRoutes[index]) {
    fail(`sidebar association drift at index ${index}: sidebar=${sidebarRoutes[index]}, association=${associatedRoutes[index]}`);
  }
}

const routeIds = new Set();
const frameworkIds = new Set();
let supportPages = 0;
let frameworkPages = 0;
for (const entry of associations.entries) {
  if (!entry.sidebar_route || !entry.page_path || !entry.page_type) fail('association entry missing sidebar_route, page_path, or page_type');
  if (routeIds.has(entry.sidebar_route)) fail(`duplicate sidebar association: ${entry.sidebar_route}`);
  routeIds.add(entry.sidebar_route);
  if (!fs.existsSync(entry.page_path)) fail(`associated page missing: ${entry.page_path}`);
  if (entry.page_type === 'support') {
    supportPages += 1;
    if (!entry.association_id) fail(`support page missing association_id: ${entry.sidebar_route}`);
    continue;
  }
  if (entry.page_type !== 'framework') fail(`unsupported page_type for ${entry.sidebar_route}: ${entry.page_type}`);
  frameworkPages += 1;
  if (!entry.framework_id) fail(`framework page missing framework_id: ${entry.sidebar_route}`);
  if (frameworkIds.has(entry.framework_id)) fail(`duplicate associated framework_id: ${entry.framework_id}`);
  frameworkIds.add(entry.framework_id);

  if (!allowedPresenceStates.has(entry.docs_registry_state)) fail(`invalid docs_registry_state for ${entry.framework_id}`);
  const docsPresent = docsRegistryIds.has(entry.framework_id);
  if ((entry.docs_registry_state === 'present') !== docsPresent) {
    fail(`docs registry state mismatch for ${entry.framework_id}: declared=${entry.docs_registry_state}, actual=${docsPresent ? 'present' : 'missing'}`);
  }

  if (!allowedPresenceStates.has(entry.static_registry_state)) fail(`invalid static_registry_state for ${entry.framework_id}`);
  const staticPresent = entry.static_registry_id ? staticRegistryIds.has(entry.static_registry_id) : false;
  if ((entry.static_registry_state === 'present') !== staticPresent) {
    fail(`static registry state mismatch for ${entry.framework_id}: declared=${entry.static_registry_state}, actual=${staticPresent ? 'present' : 'missing'}`);
  }
  if (entry.static_registry_state === 'present' && !entry.static_registry_id) {
    fail(`static registry presence requires static_registry_id: ${entry.framework_id}`);
  }
  if (entry.static_registry_state === 'missing_explicit' && entry.static_registry_id && staticRegistryIds.has(entry.static_registry_id)) {
    fail(`static registry entry exists but is declared missing: ${entry.framework_id}`);
  }
}

const expectedCounts = associations.counts || {};
if (expectedCounts.sidebar_entries !== associations.entries.length) fail('association sidebar_entries count is stale');
if (expectedCounts.support_pages !== supportPages) fail('association support_pages count is stale');
if (expectedCounts.framework_pages !== frameworkPages) fail('association framework_pages count is stale');

console.log(`OK: ${STATIC_REGISTRY_PATH}`);
console.log(`OK: ${ASSOCIATIONS_PATH}`);
console.log(`external_framework_static_registry_records=${registry.records.length}`);
console.log(`external_framework_docs_registry_records=${docsRegistry.entries.length}`);
console.log(`external_framework_sidebar_entries=${sidebarRoutes.length}`);
console.log(`external_framework_sidebar_framework_pages=${frameworkPages}`);
console.log(`external_framework_sidebar_support_pages=${supportPages}`);
console.log('silent_sidebar_add_remove_change_guard=ENFORCED');